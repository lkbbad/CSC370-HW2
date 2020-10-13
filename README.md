# CSC370-HW2

Implementation of genetic programming-based symbolic regression. 

``dataset1`` and ``dataset2`` located in folder ``datasets``, collected data from trial located in folder ``csv``.

``read_in.py``: reads in datasets for genetic algorithm and plots for matplotlib

``gp.py``: genetic programming symbolic regression algorithm module

``tree1.py``: tree class for dataset1 

``tree2:py``: tree class for dataset2

``plots.py``: creates plots in matplotlib

To run genetic algorithm with ``dataset1`` or ``dataset2``, respectively, use the following code:
```
python3 gp.py 1
python3 gp.py 2
```
To generate plots, use the following code:
```
python3 plots.py
```
