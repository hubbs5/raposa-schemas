'''
This file contains functions that validate the inputs to the schemas.
'''

import warnings

def param_key_check(params, key_standard, deprecation_exception: list=[], *args, **kwargs):
    """
    Checks that the parameters fed to the schema builder are correct.
    """
    keys = list(params.keys())

    if key_standard != keys:

        if len(deprecation_exception) > 0:
            _ = [keys.append(k) for k in key_standard if k not in keys]
            if kwargs.get("warning", True):
                msg = kwargs.get("warning_message", f"Modules without {deprecation_exception} are deprecated.")
                warnings.warn(msg, DeprecationWarning)
    
    if len(key_standard) != len(keys):

        raise ValueError(
            "Wrong number of parameters used to build indicator - please contact us about this bug." + \
                f"{key_standard} != {keys}"
        )
    assert key_standard == keys, (
        "Wrong parameters fed to indicator builder - please contact us about this bug." + \
            f"{key_standard} != {keys}")


def period_check(period, min=1, max=1000, description="Period"):
    if not isinstance(period, int):
        raise TypeError(f"{description} must be a positive integer.")
    elif not period > 0:
        raise TypeError(f"{description} must be > zero.")
    elif not period < max:
        raise TypeError(f"{description} must be < {max}")
    elif not period > min:
        raise TypeError(f"{description} must be > {min}")
    return period


def float_check(value, min=0, max=100, description="Value"):
    if not isinstance(value, float) and not isinstance(value, int):
        raise TypeError(f"{description} must be a number.")
    elif not value > min:
        raise TypeError(f"{description} must be > {min}")
    elif not value < max:
        raise TypeError(f"{description} must be < {max}")
    return value

def int_check(value, min=0, max=100, description="Value"):
    if not isinstance(value, int):
        raise TypeError(f"{description} must be a number.")
    elif not value > min:
        raise TypeError(f"{description} must be > {min}")
    elif not value < max:
        raise TypeError(f"{description} must be < {max}")
    return value

def str_check(value: str, values: list, description: str="Value"):
    if not isinstance(value, str):
        raise TypeError(f"{description} must be a string.")
    elif value not in values:
        raise TypeError(f"{description} must be one of {values}")
    return value

def bool_check(value: bool, description: str="Value"):
    if not isinstance(value, bool):
        raise TypeError(f"{description} must be a boolean.")
    return value