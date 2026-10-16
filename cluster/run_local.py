"""
Rerun the timing experiment of Figures 9-12 on this machine, in parallel and resumably.

    python cluster/run_local.py --dry-run        list the jobs and estimate the running time
    python cluster/run_local.py                  the core set (about 5 hours on an M2 Pro)
    python cluster/run_local.py --set extra      no pruning at 4 rectangles, Section 4 at 5

A job is one (M, N, seed, pruning variant) of the cluster runs in results/cluster_timings
(or of EXTRA_CONFIGS, which the cluster never ran), run as `run_example.py --pruning VARIANT --verbose`.  Its log goes to
OUT/logs/VARIANT/M_N_seed.txt, in the format cluster/parse_logs.py reads, and the output of
/usr/bin/time -l (peak memory) to the .err file next to it.  The jobs run on a snapshot of
Code/ at the current commit (OUT/src), so editing the code during a run does not affect it.

Jobs start longest first, while at most --workers run and their estimated memory stays
below --mem-gb.  The pipeline keeps every line in memory (about 450 bytes each), so the
estimates come from the line counts in OUT/expected_lines.csv.  A restart skips finished
jobs and reruns interrupted ones; Ctrl-C or `kill $(cat OUT/runner.pid)` stops the run and
its jobs.  When all jobs have finished, OUT/timings.csv is written, then
cluster/summarize_local.py is run if present, then OUT/DONE is created.

Section 4 pruning at 6 rectangles and no pruning at 5 or 6 need 26-180 GB and are not offered.
"""
import argparse
import csv
import datetime
import glob
import heapq
import os
import re
import signal
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_OUT = os.path.join(REPO, "results", "laptop_timings")
CLUSTER_CSVS = ["dardel_experiment_results.csv", "dardel_experiment_results_six.csv", "six_results_3_Nov.csv",
                "dardel_experiment_results_six_seed2.csv"]
PRUNE_NAMES = {"none": "NO PRUNING WHATSOEVER", "section4": "ONLY OLD PRUNING", "all": "ALL (including NEW) PRUNING"}
DONE_MARKER = "lines evaluated:"   # the last line run_example.py prints

# (variant, totals of rectangles) per set
SETS = {
    "core": [("all", {2, 3, 4, 5, 6}), ("section4", {2, 3, 4}), ("none", {2, 3})],
    "extra": [("none", {4}), ("section4", {5})],
}
# seconds per line evaluated, by total number of rectangles, measured with 3-5 jobs in parallel
SEC_PER_LINE = {2: 90e-6, 3: 43e-6, 4: 29e-6, 5: 31e-6, 6: 36e-6}
BYTES_PER_LINE = 450
# the current code evaluates 0.16-0.50x the lines of the cluster runs (6 rectangles, all pruning);
# a job missing from expected_lines.csv is budgeted at the top of that range
LINES_PER_CLUSTER_LINE = 0.5
BASE_GB = 0.15
# configurations the cluster never ran, with the lines budgeted for each if expected_lines.csv
# lacks them: six_results_3_Nov.csv has seeds 3-7 of every 6-rectangle split except seed 3 of 3+3
# (budget: the largest 3+3 job)
EXTRA_CONFIGS = {(3, 3, 3): 35_000_000}


def log(out, msg):
    line = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    print(line, flush=True)
    with open(os.path.join(out, "progress.log"), "a") as f:
        f.write(line + "\n")


def cluster_lines():
    """Lines evaluated by each cluster run, keyed (M, N, seed, variant)."""
    variant_of = {name: variant for variant, name in PRUNE_NAMES.items()}
    lines = {}
    for name in CLUSTER_CSVS:
        for r in csv.DictReader(open(os.path.join(REPO, "results", "cluster_timings", name))):
            lines[(int(r["M"]), int(r["N"]), int(r["seed"]), variant_of[r["prune"]])] = int(r["exact_lines_counted"])
    return lines


def expected_lines(out):
    path = os.path.join(out, "expected_lines.csv")
    return {(int(r["M"]), int(r["N"]), int(r["seed"]), r["variant"]): int(r["lines"])
            for r in csv.DictReader(open(path))}


class Job:
    def __init__(self, M, N, seed, variant, lines, out):
        self.M, self.N, self.seed, self.variant, self.lines = M, N, seed, variant, lines
        self.log = os.path.join(out, "logs", variant, f"{M}_{N}_{seed}.txt")
        self.err = self.log[:-4] + ".err"
        self.seconds = 3 + lines * SEC_PER_LINE[M + N]
        self.gb = BASE_GB + 1.1 * BYTES_PER_LINE * lines / 1e9

    def name(self):
        return f"{self.variant} {self.M}+{self.N} seed {self.seed}"

    def finished(self):
        return os.path.exists(self.log) and DONE_MARKER in open(self.log).read()


def make_jobs(sets, out):
    lines, cluster = expected_lines(out), cluster_lines()
    jobs = []
    for M, N, seed in sorted({key[:3] for key in cluster} | set(EXTRA_CONFIGS)):
        for s in sets:
            for variant, totals in SETS[s]:
                if M + N in totals:
                    key = (M, N, seed, variant)
                    if key in lines:
                        n = lines[key]
                    elif key in cluster:
                        n = round(LINES_PER_CLUSTER_LINE * cluster[key])
                    else:
                        n = EXTRA_CONFIGS[(M, N, seed)]
                    jobs.append(Job(M, N, seed, variant, n, out))
    return sorted(jobs, key=lambda j: -j.seconds)


def fits(job, running, workers, mem_gb):
    used = sum(j.gb for j in running)
    return len(running) < workers and (used + job.gb <= mem_gb or not running)


def simulate(jobs, workers, mem_gb):
    """Estimated wall-clock hours of the greedy schedule used by run()."""
    t, pending, running = 0.0, list(jobs), []   # running: heap of (end time, index, job)
    while pending or running:
        started = True
        while started:
            started = False
            for i, job in enumerate(pending):
                if fits(job, [r[2] for r in running], workers, mem_gb):
                    heapq.heappush(running, (t + job.seconds * 1.15, id(job), job))
                    pending.pop(i)
                    started = True
                    break
        t = heapq.heappop(running)[0]
    return t / 3600


def snapshot_code(out):
    src = os.path.join(out, "src")
    commit = subprocess.run(["git", "-C", REPO, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    if not os.path.isdir(src):
        os.makedirs(src)
        archive = subprocess.run(["git", "-C", REPO, "archive", "HEAD", "Code", "cluster"], capture_output=True, check=True).stdout
        subprocess.run(["tar", "-x", "-C", src], input=archive, check=True)
        with open(os.path.join(src, "COMMIT"), "w") as f:
            f.write(commit + "\n")
    return src, open(os.path.join(src, "COMMIT")).read().strip()


def write_run_info(out, args, commit, jobs):
    python = os.path.join(REPO, "venv", "bin", "python")
    versions = subprocess.run([python, "-c", "import sys, gudhi, numpy; print(sys.version.split()[0], gudhi.__version__, numpy.__version__)"],
                              capture_output=True, text=True).stdout.split()
    chip = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip()
    with open(os.path.join(out, "run_info.txt"), "a") as f:
        f.write(f"started {datetime.datetime.now():%Y-%m-%d %H:%M}  set {'+'.join(args.set)}  code {commit}  "
                f"{chip}  workers {args.workers}  memory cap {args.mem_gb} GB  "
                f"python {versions[0] if versions else '?'} gudhi {versions[1] if len(versions) > 1 else '?'}  "
                f"jobs {len(jobs)}\n")


def write_timings(out):
    """One CSV row per finished job: the cluster columns plus approximations, grid time and memory."""
    sys.path.insert(0, os.path.join(REPO, "cluster"))
    from parse_logs import COLUMNS, parse_log
    extra = {
        "crit_point_dist": r"Maximum distance for lines through critical points:\s*([\d.]+)",
        "grid_dist": r"Maximum distance computed for grid of lines:\s*([\d.]+)",
        "time_grid": r"Time elapsed \(theta b grid\):\s*([\d.]+)",
        "n_critvals": r"NUMBER OF CRITVALS:\s*(\d+)",
        "exact_dist": r"exact matching distance, pruning = \S+\s*:\s*([\d.]+)",
    }
    fields = ["variant"] + COLUMNS + list(extra) + ["peak_rss_gb", "wall_s"]
    rows = []
    for variant in PRUNE_NAMES:
        for path in sorted(glob.glob(os.path.join(out, "logs", variant, "*.txt"))):
            text = open(path).read()
            if DONE_MARKER not in text:
                continue
            row = parse_log(path)[0]
            row["variant"] = variant
            for key, pattern in extra.items():
                m = re.search(pattern, text)
                row[key] = m.group(1) if m else ""
            err = open(path[:-4] + ".err").read() if os.path.exists(path[:-4] + ".err") else ""
            m = re.search(r"(\d+)\s+maximum resident set size", err)
            row["peak_rss_gb"] = f"{int(m.group(1)) / 1e9:.3f}" if m else ""
            m = re.search(r"([\d.]+) real", err)
            row["wall_s"] = m.group(1) if m else ""
            rows.append(row)
    rows.sort(key=lambda r: (int(r["M"]) + int(r["N"]), int(r["M"]), int(r["seed"]), list(PRUNE_NAMES).index(r["variant"])))
    with open(os.path.join(out, "timings.csv"), "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def run(args, jobs):
    out = args.out
    src, commit = snapshot_code(out)
    write_run_info(out, args, commit, jobs)
    with open(os.path.join(out, "runner.pid"), "w") as f:
        f.write(f"{os.getpid()}\n")
    # keep the Mac awake (not through a closed lid) while this process lives
    subprocess.Popen(["caffeinate", "-i", "-w", str(os.getpid())])

    python = os.path.join(REPO, "venv", "bin", "python")
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1",
               MKL_NUM_THREADS="1", MPLBACKEND="Agg")
    pending = [j for j in jobs if not j.finished()]
    log(out, f"code {commit}; {len(jobs)} jobs, {len(jobs) - len(pending)} already finished; "
             f"estimated {simulate(pending, args.workers, args.mem_gb):.1f} h with {args.workers} workers, {args.mem_gb} GB")
    running = {}   # Popen -> (job, start time)
    failed = []

    def stop(signum, frame):
        log(out, f"stopped by signal {signum}; killing {len(running)} running job(s); restart to resume")
        for p in running:
            os.killpg(p.pid, signal.SIGTERM)   # /usr/bin/time and the Python job under it
        sys.exit(1)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGHUP, signal.SIG_IGN)

    total, done = len(pending), 0
    while pending or running:
        for job in list(pending):
            if fits(job, [j for j, _ in running.values()], args.workers, args.mem_gb):
                os.makedirs(os.path.dirname(job.log), exist_ok=True)
                cmd = ["/usr/bin/time", "-l", python, os.path.join(src, "Code", "run_example.py"),
                       "--M", str(job.M), "--N", str(job.N), "--seed", str(job.seed), "--pruning", job.variant, "--verbose"]
                p = subprocess.Popen(cmd, cwd=src, env=env, stdout=open(job.log, "w"), stderr=open(job.err, "w"), start_new_session=True)
                running[p] = (job, time.time())
                pending.remove(job)
        time.sleep(2)
        for p in [p for p in running if p.poll() is not None]:
            job, start = running.pop(p)
            done += 1
            if job.finished():
                log(out, f"[{done}/{total}] {job.name()}: {time.time() - start:.0f} s")
            else:
                failed.append(job)
                log(out, f"[{done}/{total}] {job.name()}: FAILED (exit {p.returncode}), see {os.path.relpath(job.err, out)}")

    n = write_timings(out)
    log(out, f"all jobs ended, {len(failed)} failed; {n} rows written to timings.csv")
    summarize = os.path.join(REPO, "cluster", "summarize_local.py")
    if os.path.exists(summarize):
        r = subprocess.run([python, summarize, out], cwd=REPO, env=env, capture_output=True, text=True)
        with open(os.path.join(out, "summarize.log"), "w") as f:
            f.write(r.stdout + r.stderr)
        log(out, f"summarize_local.py exited with {r.returncode}; output in summarize.log")
    with open(os.path.join(out, "DONE"), "w") as f:
        f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M}  {n} rows, {len(failed)} failed\n")
    os.remove(os.path.join(out, "runner.pid"))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--set", nargs="+", choices=sorted(SETS), default=["core"])
    parser.add_argument("--workers", type=int, default=5, help="jobs run at once (default 5)")
    parser.add_argument("--mem-gb", type=float, default=20, help="cap on the jobs' estimated memory (default 20)")
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timings-only", action="store_true", help="only rewrite timings.csv from the logs")
    args = parser.parse_args()
    args.out = os.path.abspath(args.out)
    if args.timings_only:
        print(write_timings(args.out), "rows written")
        return
    jobs = make_jobs(args.set, args.out)
    pending = [j for j in jobs if not j.finished()]
    if args.dry_run:
        for variant in PRUNE_NAMES:
            for total in range(2, 7):
                js = [j for j in pending if j.variant == variant and j.M + j.N == total]
                if js:
                    print(f"{variant:9s} {total} rectangles: {len(js):3d} jobs, "
                          f"{sum(j.seconds for j in js) / 3600:5.2f} CPU-h, up to {max(j.gb for j in js):4.1f} GB")
        print(f"{len(pending)} of {len(jobs)} jobs to run, {sum(j.seconds for j in pending) / 3600:.1f} CPU-h, "
              f"about {simulate(pending, args.workers, args.mem_gb):.1f} h with {args.workers} workers and {args.mem_gb} GB")
        return
    run(args, jobs)


if __name__ == "__main__":
    main()
