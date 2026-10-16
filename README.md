# Switch points of bi-persistence matching distance

This repository contains code to compute the exact matching distance between two
rectangle-decomposable 2-parameter persistence modules, from the paper

> Robyn Brooks, Celia Hacker, Claudia Landi, Barbara I. Mahler, Elizabeth R. Stephenson.
> _Switch points of bi-persistence matching distance._ 2026.

## Setting up

You need Python 3; the code was tested with Python 3.9.6.

1. Get the code.

   ```
   git clone https://github.com/asilata/matching-distance-code.git
   ```

2. Go into the directory:

   ```
   cd matching-distance-code
   ```

3. The first time, make a virtual environment, a private Python installation for this code, so
   that it does not interfere with anything else on your computer:

   ```
   python3 -m venv match_dist_venv
   ```

   Then activate it. Do this again every time you open a new terminal:

   ```
   source match_dist_venv/bin/activate
   ```

   (On Windows: `match_dist_venv\Scripts\activate`.)

4. The first time, install the requirements:

   ```
   pip install -r requirements.txt
   ```

## Running the code

The small example of the paper (Figure 6):

```
python run_example.py --toy
```

This prints two approximations of the matching distance from below (from lines through pairs of
critical values, and from a grid of lines), then the exact matching distance and the line on
which it is attained.

Two random modules, here with 2 and 1 rectangles. The seed picks the modules, and the same seed
always gives the same modules:

```
python run_example.py --M 2 --N 1 --seed 13
```

Examples 2.12–2.14 of Bapat et al., [arXiv:2210.12868](https://arxiv.org/abs/2210.12868):

```
python run_example.py --example 2.14
```

Options you can add to any of these:

- `--figure` saves pictures of the two modules and of the line on which the distance is
  attained, in the folder `output/figures/`.
- `--plot-candidates` saves pictures of the candidate switch points of Algorithms 3, 5 and 7.
- `--pruning` chooses which superfluous candidate switch points are discarded before the
  distance is computed: `none`, `section4` (Section 4) or `all` (Sections 4 and 5, the
  default). `--pruning compare` runs all three. The distance is the same each time; pruning
  only saves time.
- `--help` lists all the options.

The running time grows quickly with the number of rectangles. With the default pruning, on a
recent laptop (an Apple M2 Pro), it takes about a second for 2 rectangles in total, up to 10
seconds for 3, up to 2 minutes for 4, up to 10 minutes for 5, and from a minute to about 40
minutes for 6. Without pruning (`--pruning none`, and so also `--pruning compare`) it is many
times slower and needs much more memory: with 5 or 6 rectangles, more than a laptop has.

## Your own modules

A module is a list of rectangles, and each rectangle is written as its top-right corner followed
by its bottom-left corner: `[(6, 6), (0, 0)]` is the square with corners (0, 0) and (6, 6). For
a rectangle that is unbounded on one side, use a large number such as 10<sup>8</sup> (written `10**8` in Python) for that side.

To compute the matching distance between your own modules, open `my_example.py` in any text
editor, replace the modules `M` and `N` with yours, save it, and run

```
python my_example.py
```

It prints the matching distance and the line on which it is attained. In `my_example.py`,
`run_one(M, N, "none")` or `run_one(M, N, "section4")` changes the pruning.

## Where things are

The two files at the top, `run_example.py` and `my_example.py`, are the ones to run. The code
they use is in the folder `matching_distance/`:

- `switch_points.py`: Algorithms 1–7 of the paper, which compute the candidate switch points
  and discard the superfluous ones.
- `distance.py`: the approximations and the exact matching distance.
- `modules.py`: rectangles, modules, lines and the weighted bottleneck distance.
- `experiment.py`: `run_one` and the pruning variants.
- `examples.py`, `plot.py` and `settings.py`: the examples, the pictures and a few switches.

To check that everything works, run the tests (about 20 seconds):

```
pytest
```

## Authors and license

The code was written by Asilata Bapat, Robyn Brooks, Celia Hacker, Claudia Landi, Barbara I.
Mahler and Elizabeth R. Stephenson. It is released under the MIT license; see [LICENSE](LICENSE).

## AI Disclosure

The authors made use of AI to debug and clean up the code.
