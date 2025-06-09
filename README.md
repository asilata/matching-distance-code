# README

This repository contains code to compute matching distances between multidimensional persistence modules.
You need ```python 3.9.6```.
We recommend using ```pip``` or  ```conda``` if you prefer. We also recommend using a virtual environment like ```virtualenv```. To make a local environment in the directory you'll work in, for example ```matching-distance-code```:
```
# the first time you make a virtual env, use this command
virtualenv venv
# afterwards, you can activate it like so
source venv/bin/activate
```

To install the requirements, navigate to the ```matching-distance-code``` directory and run the following in the terminal.
```
# after making the env, install the requirements 
pip install -r requirements.txt
```
cluster usage: run ```python3 ./Code/cluster_prune_or_not.py```. You can edit ```Code/settings.py``` to override normal settings, like terminal output, figure output, and system requirements (at your own risk).

## group experiment instructions: 
1. Clone the repo.
2. Open terminal.
3. First time: either install a virtual env as mentioned above with ```virtualenv venv``` (if you have other versions of python you are using in other projects and don't want to mess that up) or don't bother if this is the only python coding project you are using.
4. If you made a virtual env, activate it ```source venv/bin/activate```.
5. First time: install the requirements with ```pip install -r requirements.txt```
6. Navigate to the Code directory: ```cd Code```
7. Run the code by typing ```python ./GROUP_EXPERIMENT.py```
8. If you like, you can see the figures you make for each experiment in the folder GROUP_FIGS.
9. Fill in the GROUP_EXPERIMENT google doc with the results of the three runs (no pruning, the old pruning, and the new pruning)
