import subprocess

with open("unicorn_hunting.txt") as f:
    next(f)   # skip header M N seed

    for line in f:
        if not line.strip():
            continue
        M, N, seed = line.split()
        print(f"Running UNICORN_HUNT.py {M} {N} {seed}")
        subprocess.run(["python", "UNICORN_HUNT.py", M, N, seed])
