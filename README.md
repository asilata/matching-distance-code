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