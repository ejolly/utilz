"""
Functions that exist purely to save boilerplate.
"""

__all__ = ["mpinit", "randdf", "parseargs"]

import numpy as np
import pandas as pd
import argparse


def mpinit(figsize=(8, 6), subplots=(1, 1)):
    """
    Setup matplotlib subplots boilerplate

    Args:
        figsize (tuple, optional): Figure size. Defaults to (8, 6).
        subplots (tuple, optional): subplot grid size. Defaults to (1, 1).

    Returns:
        tuple ((Figure, Axes)): matplotlib figure handle and axes
    """
    if "plt" not in dir():
        import matplotlib.pyplot as plt
    f, ax = plt.subplots(*subplots, figsize=figsize)
    return f, ax


def randdf(size=(10, 3), columns=["A", "B", "C"], func=None, *args, **kwargs):
    """
    Generate a dataframe with random data and alphabetic columns, Default to np.random.randn. Specify another function and size will be passed in as a kwarg.

    Args:
        size (tuple, optional): Defaults to (10,3).
        columns (list, optional): Defaults to ["A","B","C"].
        func (callable, optional): function to generate data. Must take a kwarg "size" that accepts a tuple; Default np.random.randn
        *args/**kwargs: arguments and keyword arguments to func
    """

    if len(columns) != size[1]:
        raise ValueError("Length of column names must match number of columns")

    if func is None:
        data = np.random.rand(*size)
    else:
        data = func(*args, size=size, **kwargs)

    return pd.DataFrame(data, columns=columns)


# TODO: Test me and check out how docstring looks
def parseargs(*arg_tuples: list) -> dict:
    """
    Quickly setup and use an argument parser to parse command line arguments. Useful as a one-liner added to the top of an interactive script or notebook to quickly make it useable at the command line instead. Desired arguments should be passed in as tuples containing 3 values:

        (argument name as a string, argument type/True or False, argument help string)

    The outputted dictionary will contain keys as the argument names, and values as the inputted values. Argument names will auto-convert '-' to '_' and strip any '--' prefixes.

    To create positional command-line inputs the second tuple element should be a python type:

    >>> parsed_args = arparser(('name', str, 'the username to print'))

    >>> parsed_args['name'] # to retreive the value which will be a string

    For boolean flags the first element should begin with '--' prefix, and second element should True or False:

    >>> parsed_args = argparser(('--dry-run', True, 'setup the script but dont execute')

    >>> parsed_args['dry_run'] # True

    Returns:
        dict: a dictionary containing keys for the argument names and values as the captured inputs
    """

    parser = argparse.ArgumentParser()

    for tup in arg_tuples:

        arg_name, arg_type, arg_help = tup

        if isinstance(arg_type, type):
            # User is defining the type of argument, e.g. str
            parser.add_argument(arg_name, type=arg_type, help=arg_help)

        elif isinstance(arg_type, bool):
            # User is passing in True or False so convert to store_true/store_false
            assert arg_name.startswith("--"), "Prefix boolean flags with '--'"
            action_dict = {True: "store_true", False: "store_false"}
            parser.add_argument(arg_name, action=action_dict[arg_type], help=arg_help)

    return parser.parse_args()
