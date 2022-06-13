# coding: utf-8

# Author: Christian Hubbs
# Email: christian@raposa.co

# This file contains data schemas for type checking API inputs.

"""Notes about these schemas
- Union[] is not a very durable way to check if indicator or comp indicator matches the criteria of another schema
- Union[] will try to force the field value to work with every option in Union, starting from left to right.
        --> for instance if you feed indicator = an instance of EMA class into building a SIGNAL class 
        ---> if SIGNAL had a Union[SMA,EMA] check on indicator, it will assign the EMA class values into an SMA class
- to avoid this, I am going back to using dictionaries as parameter inputs and indicator inputs. 
- I wrote custom validation checks for every schema class to avoid this Union problem

- The custom validation checks make sure that the parametr dictionary for every indicator has 
        1) the correct number of keys
        2) the correct keys as compared to the standard outlined in the validation functions in each class
"""


"""
notes about pydantic and Typing
    - Union from typing allows for entries to be of either type BUT the 
    first listed will be prioritized. This WILL convert entry types.

    Pydantic Classes that are generated with Basemodel have a few ways to see the data
    ex: 
        indicator = SMA(signal_name = 'SMA', period = 2)
        print(SMA.json())
        print(SMA.dict())
        print(SMA.schema_json(indent=2)) # outputs muct more information about the model including default values and field type

    Pydantic fields:
        - if you do not list a default value the field is mandatory
        - you must specify either the type of each field, 
            not really, but there are conseuquences of mixing specification and not in one model see docs)

    - You can make an instance of a class with this code:
        indicator_klass = globals()['PRICE'] 
        params = indicator_klass.__fields__['params']
        # This will make an object of the class that is hard to work with, but can be populated with
        temp_klass = indicator_klass()
        print(temp_klass.params

"""

"""
How to add a new strategy option to the site that requires parameters (position sizing, risk management, etc)
    - create the new dropdowns in buy_tab, sell_tab, or strategy_tab
    - create the callbacks buy_tab, sell_tab, or strategy_tab
    - add the new inputs to dash_app_main.build_strategy callback
    - update utils_strategy_compilation.py
    
"""
from typing import List, Type, Union, Optional
from xmlrpc.client import boolean
from pydantic import BaseModel, validator

# List parameters and input ranges for each
max_signals = 3
max_instruments = 25

signal_count = [
    "First",
    "Second",
    "Third",
    "Fourth",
    "Fifth",
    "Sixth",
    "Seventh",
    "Eigth",
    "Ninth",
    "Tenth",
]

# These dictionaries are used throughout the app. When used in a dropdown, the .key() is used as the label and value of the dropdown.
# in utils.py, when assembling the list of signals, the value of the dropdown is used as the dictionary key, and the output is the name of the
# corresponding SCHEMA class listed at the bottom of this file.
# - NOTE: all of the keys are what will show up in the dropdown menu, so their capitalization matters

every_indicator = {
    "Stop Price": "STOP_PRICE",
    "ATR Stop Price": "ATR_STOP_PRICE",
    "Price": "PRICE",
    "Breakout": "PRICE_WINDOW",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "ATR %": "ATRP",
    "Volatility": "VOLATILITY",
    # "PSAR": "PSAR",
    "HURST": "HURST",
    "Level": "LEVEL",
    # "Bollinger Bands": "BOLLINGER",
    # "Band Width": "BAND_WIDTH", 
    # "Moving Average Distance": "MAD"
}

# buy_indicators and sell_indicators are used in the dropdown menus for buy and sell tabs.
buy_indicators = {
    "Price": "PRICE",
    "Breakout": "PRICE_WINDOW",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "ATR %": "ATRP",
    "Volatility": "VOLATILITY",
    # "PSAR": "PSAR",
    "HURST": "HURST",
    # "Bollinger Bands": "BOLLINGER",
    # "Band Width": "BAND_WIDTH", 
    # "Moving Average Distance": "MAD"
}

sell_indicators = {
    "Stop Price": "STOP_PRICE",
    "ATR Stop Price": "ATR_STOP_PRICE",
    "Price": "PRICE",
    "Breakout": "PRICE_WINDOW",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "ATR %": "ATRP",
    "Volatility": "VOLATILITY",
    # "PSAR": "PSAR",
    "HURST": "HURST",
    # "Bollinger Bands": "BOLLINGER", 
    # "Band Width": "BAND_WIDTH", 
    # "Moving Average Distance": "MAD"
}

position_sizings = {
    "Equal Allocation": "EqualAllocation",
    "Volatility Allocation": "VOLATILITYSizing",
    "ATR Allocation": "ATRSizing",
    "Turtle Allocation": "TurtleUnitSizing",
    "No Risk Management": "NoRiskManagement",
}

position_managements = {
    "Equal Allocation": "EqualAllocation",
    "Volatility Allocation": "VOLATILITYSizing",
    "ATR Allocation": "ATRSizing",
    "Turtle Allocation": "TurtleUnitSizing",
    "Turtle Pyramiding": "TurtlePyramiding",
    "No Risk Management": "NoRiskManagement",
}

indicators_with_time_params = {
    "SMA": ["period"],  # Indicators that have to look back in time and the param(s)
    # that defines the farthest number of days to look back
    "EMA": ["period"],
    "MACD": ["slowEMA_period", "fastEMA_period"],
    "MACD_SIGNAL": ["slowEMA_period", "fastEMA_period," "signalEMA_period"],
    "RSI": ["period"],
    "ATR": ["period"],
    "ATR_STOP_PRICE": ["period"],
    "VOLATILITY": ["period"],
    "PSAR": ["period"],
    "PRICE_WINDOW": ["period"],
    "BOLLINGER": ["period"], 
    "BAND_WIDTH": ["period"], 
    "MAD":["fastSMA_period", "slowSMA_period"]
}

relations = {"> or =": "geq", "< or =": "leq", ">": "gt", "<": "lt", "=": "eq"}


""" all of these indicator classes have the same number of inputs
as required to run in pyalgotrade"""

"INDICATORS ===================================================="


class SMA(BaseModel):
    name: str = "SMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    # param bound >= 2 and < 1000

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build SMA - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to SMA signal builder - please contact us about this bug."
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("SMA period must be a postive integer.")
                elif not value[key] > 0:
                    raise TypeError("SMA period must be > zero.")
        return value


class EMA(BaseModel):
    name: str = "EMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    # param bound >= 2 and < 1000
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build EMA - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to EMA signal builder - please contact us about this bug."
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("EMA period must be a postive integer")
                elif not value[key] > 0:
                    raise TypeError("EMA period must be > zero")
        return value


class MACD(BaseModel):
    name: str = "MACD"
    params: dict = {"fastEMA_period": 10, 
                    "slowEMA_period": 20}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "PRICE", "MACD_SIGNAL"]
    # param bound >= 2 and < 1000
    # need to enforce that fastEMA period is > =slowEMAperiod

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["fastEMA_period", "slowEMA_period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build MACD - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to MACD - please contact us about this bug."
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("MACD periods must be postive integers.")
                elif not value[key] > 0:
                    raise TypeError("MACD inputs must be > zero.")
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError("The fast EMA period for MACD must be < the slow EMA period")
        return value


class MACD_SIGNAL(BaseModel):
    name: str = "MACD_SIGNAL"
    params: dict = {"fastEMA_period": 10, 
                    "slowEMA_period": 20, 
                    "signalEMA_period": 9}
    needs_comp: bool = True 
    valid_comps: list = ["MACD", "SMA", "EMA"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["fastEMA_period", "slowEMA_period", "signalEMA_period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build MACD Signal - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to MACD Signal builder - please contact us about this bug."
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("MACD Signal inputs must be positive integers.")
                elif not value[key] > 0:
                    raise TypeError("MACD Signal inputs must be > zero.")
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError(
                "The fast EMA period for MACD Signal must be < the slow EMA period"
            )
        return value


class RSI(BaseModel):
    name: str = "RSI"
    params: dict = {"period": 10}
    needs_comp: bool = True  # will always be level
    valid_comps: list = ["LEVEL"]
    # param period bound >= 2 and < 1000
    # LEVEL for RSI is always between 0 and 100

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build RSI - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to RSI signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("RSI period must be a positive integer.")
                elif not value[key] > 0:
                    raise TypeError("RSI period must be > zero")
        return value


class STOP_PRICE(BaseModel):
    name: str = "STOP_PRICE"
    params: dict = {
        "percent_change": 10.1, 
        "trailing":False
    }  # will be positive for stop profit and neg for stop loss
    needs_comp: bool = True  # will always be price
    valid_comps: list = ["PRICE"]
    # param bound > -100% and < 10000%
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["percent_change", "trailing"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build stop price signal - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to stop signal builder - please contact us about this bug."
                    )
            if not isinstance(value["percent_change"], float) and not isinstance(
                value["percent_change"], int):
                    raise TypeError("Stop price % change must be a number.")
                
            if not isinstance(value["trailing"], bool):
                raise TypeError("'Trailing' value must be boolean.")
        return value


class ATR_STOP_PRICE(BaseModel):
    name: str = "ATR_STOP_PRICE"
    params: dict = dict(
        period=20,
        stop_price_ATR_frac=-2.0,  # positive for stop profit, negative for stop price
        trailing=False, 
    )
    needs_comp: bool = True
    valid_comps: list = ["PRICE"]
    # param period bound >= 2 and < 1000
    # stop price frac bound by -10 and + 10

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period",  "stop_price_ATR_frac","trailing"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build ATR stop price - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to stop signal builder - please contact us about this bug."
                    )
        if not isinstance(value["period"], int):
            raise TypeError("ATR stop price period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("ATR stop price period must be > zero")
        if not isinstance(value["stop_price_ATR_frac"], float) and not isinstance(
            value["stop_price_ATR_frac"], int):
            raise TypeError("ATR stop price fraction must be a number.")
        if not isinstance(value["trailing"], bool):
                raise TypeError("'Trailing' value must be boolean.")
        return value


class PRICE(BaseModel):
    name: str = "PRICE"
    params: dict = {"price_type": "Close"}  # must be in ["High", "Low", "Close", or "Typical"]
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "ATR"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["price_type"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Price - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to price signal builder - please contact us about this bug"
                    )
        if value["price_type"] not in ["High", "Low", "Close", "Typical"]:
            raise ValueError("Price type must be High, Low, Close, or Typical.")
        return value


class PRICE_WINDOW(BaseModel):
    name: str = "PRICE_WINDOW"
    params: dict = {
        "period": 30,  # Number of days to look back
        "max_or_min": "max",  # must be in ["max" or "min"]
        "price_type": "High",  # must be in ["High", "Low", "Close", "Typical"]
    }
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]
    # param period bound >= 2 and < 1000

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "max_or_min", "price_type"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build price window - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Price Window builder - please contact us about this bug."
                    )
        if not isinstance(value["period"], int):
            raise TypeError("Price Window period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Price Window period must be > zero.")

        if value["max_or_min"] not in ["max" or "min"]:
            raise ValueError("Price window max or min must be...max or min.")

        if value["price_type"] not in ["High", "Low", "Close", "Typical"]:
            raise ValueError("Price type must be High, Low, Close, or Typical.")
        return value


class ATR(BaseModel):
    name: str = "ATR"
    params: dict = {"period": 20, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["ATR"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "multiple"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build ATR - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to ATR signal builder - please contact us about this bug."
                    )

        if not isinstance(value["period"], int):
            raise TypeError("ATR period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("ATR period must be > zero.")

        if not isinstance(value["multiple"], int) and not isinstance(
            value["multiple"], float
        ):
            raise TypeError("ATR multiple must be a positive number.")
        elif not value["multiple"] > 0:
            raise TypeError("ATR multiple must be > zero.")
        return value


class ATRP(BaseModel):
    name: str = "ATRP"
    params: dict = {"period": 20, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["ATRP"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "multiple"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build ATR - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to ATRP signal builder - please contact us about this bug."
                    )
        if not isinstance(value["period"], int):
            raise TypeError("ATRP period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("ATRP period must be > zero")

        if not isinstance(value["multiple"], int) and not isinstance(
            value["multiple"], float
        ):
            raise TypeError("ATRP multiple must be a positive number.")
        elif not value["multiple"] > 0:
            raise TypeError("ATRP multiple must be > zero.")
        return value


class LEVEL(BaseModel):
    name: str = "LEVEL"
    params: dict = {"level": 10}
    needs_comp: bool = False  # always is a comparison
    valid_comps: list = None
    # param level bound by 0 and 100
    # might need to be negative for somethings

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["level"]
        if len(key_standard) != len(value):
            raise ValueError(
                "wrong number of parameters used to build level - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Level signal builder - please contact us about this bug."
                    )
                elif not isinstance(value[key], float) and not isinstance(
                    value[key], int
                ):
                    raise TypeError("Level must be a positive number.")
                elif not value[key] > 0:
                    raise TypeError("Level must be > zero.")
        return value


class BOOLEAN(BaseModel):
    name: str = "BOOLEAN"
    params: dict = {"boolean": True}  # or False
    needs_comp: bool = True
    valid_comps: list = ["PSAR"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["boolean"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build True/False- please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to True/False signal builder - please contact us about this bug."
                    )
                elif not isinstance(value[key], bool):
                    raise TypeError("True/False must be True... or False")
        return value


class VOLATILITY(BaseModel):
    name: str = "VOLATILITY"
    params: dict = {"period": 252, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["VOLATILITY", "LEVEL"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "multiple"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Volatility- please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Volatility signal builder - please contact us about this bug."
                    )
        if not isinstance(value["period"], int):
            raise TypeError("Volatility period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Volatility period must be > zero")

        if not isinstance(value["multiple"], int) and not isinstance(
            value["multiple"], float
        ):
            raise TypeError("Volatility multiple must be a positive number.")
        elif not value["multiple"] > 0:
            raise TypeError("Volatility multiple must be > zero.")
        return value


# class PSAR(BaseModel):
#     """
#     Parabolic SAR
#     """

#     name: str = "PSAR"
#     params: dict = {
#         "type_indicator": "value",  # Either 'value', 'reversal_toUptrend', 'reversal_toDowntrend'
#         "init_acceleration_factor": 0.02,
#         "acceleration_factor_step": 0.02,
#         "max_acceleration_factor": 0.2,
#         "previous_day": False,  # Whether the PSAR returned is for current day (True) or not (for comparison)
#         "period": 2,  # Number of days to look back to ensure PSAR is in proper range
#     }
#     needs_comp: bool = True
#     valid_comps: list = ["LEVEL", "PSAR", "PRICE", "BOOLEAN"]


class HURST(BaseModel):
    name: str = "HURST"
    params: dict = {"period": 10, "minLags": 2, "maxLags": 20}
    needs_comp: bool = True
    valid_comps: list = ["LEVEL"]
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # min lags must be less than max lags and both greater than one

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "minLags", "maxLags"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build HURST - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to HURST - please contact us about this bug."
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("HURST parameters must be positive integers.")
                elif not value[key] > 0:
                    raise TypeError("HURST inputs must be > zero.")
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["maxLags"] <= value["minLags"]:
            raise ValueError(
                "The minLags period for HURST Signal must be < the maxLags period"
            )
        return value


class BOLLINGER(BaseModel): 
    name: str = "BOLLINGER"
    params: dict = {"period": 20, 
                    "numStdDevUpper": 2, 
                    "numStdDevLower": 2, 
                    "price_type":"Typical", # price_type either "High", "Low", "Close", or "Typical"
                    "band": "upper"} #"band" in ["upper", "middle", "lower"]
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]
    
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "numStdDevUpper", "numStdDevLower", "price_type", "band"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Bollinger Band - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to price signal builder - please contact us about this bug"
                    )
        if not isinstance(value["period"], int):
            raise TypeError("Bollinger Band period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Bollinger Band period must be > zero")

        if not isinstance(value["numStdDevUpper"], int) and not isinstance(
            value["numStdDevUpper"], float
        ):
            raise TypeError("Bollinger Band numStdDevUpper must be a positive number.")
        elif not value["numStdDevUpper"] > 0:
            raise TypeError("Bollinger Band numStdDevUpper must be > zero.")
        if not isinstance(value["numStdDevLower"], int) and not isinstance(
            value["numStdDevLower"], float
        ):
            raise TypeError("Bollinger Band numStdDevLower must be a positive number.")
        elif not value["numStdDevLower"] > 0:
            raise TypeError("Bollinger Band numStdDevLower must be > zero.")
        
        if value["price_type"] not in ["High", "Low", "Close", "Typical"]:
            raise ValueError("Price type must be High, Low, Close, or Typical.")
        if value["band"] not in ["upper", "middle", "lower"]:
            raise ValueError("Band must be 'upper', 'middle', or 'lower'.")
        return value
    
class BAND_WIDTH(BaseModel): 
    name: str = "BAND_WIDTH"
    params: dict = {"period": 20, 
                    "numStdDevUpper": 2,
                    "numStdDevLower": 2, 
                    "price_type":"Typical"} # price_type either "High", "Low", "Close", or "Typical"
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]  
    
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "numStdDevUpper", "numStdDevLower", "price_type"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Band Width - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to price signal builder - please contact us about this bug"
                    )
        if not isinstance(value["period"], int):
            raise TypeError("Band Width period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Band Width period must be > zero")

        if not isinstance(value["numStdDevUpper"], int) and not isinstance(
            value["numStdDevUpper"], float
        ):
            raise TypeError("Band Width numStdDevUpper must be a positive number.")
        elif not value["numStdDevUpper"] > 0:
            raise TypeError("Band Width numStdDevUpper must be > zero.")
        if not isinstance(value["numStdDevLower"], int) and not isinstance(
            value["numStdDevLower"], float
        ):
            raise TypeError("Band Width numStdDevLower must be a positive number.")
        elif not value["numStdDevLower"] > 0:
            raise TypeError("Band Width numStdDevLower must be > zero.")
        
        if value["price_type"] not in ["High", "Low", "Close", "Typical"]:
            raise ValueError("Price type must be High, Low, Close, or Typical.")
        return value

class MAD(BaseModel): 
    name: str = "MAD"
    params: dict = {"fastSMA_period": 21, 
                    "slowSMA_period":200}
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]  
    
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["fastSMA_period", "slowSMA_period"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build MAD - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to price signal builder - please contact us about this bug"
                    )
        if not isinstance(value["fastSMA_period"], int):
            raise TypeError("MAD fast period must be a positive integer.")
        elif not value["fastSMA_period"] > 0:
            raise TypeError("MAD fast period must be > zero")
        
        if not isinstance(value["slowSMA_period"], int):
            raise TypeError("MAD slow period must be a positive integer.")
        elif not value["slowSMA_period"] > 0:
            raise TypeError("MAD slow period must be > zero")
        
        if value["fastSMA_period"] > value["slowSMA_period"]:
            raise ValueError(f"fastSMA_period must be < slowSMA_period")

        return value
# Classes that can be initial POSITION SIZING or Risk Management (position management during rebalance) ============================================="


class NoRiskManagement(BaseModel):
    name: str = "NoRiskManagement"
    params: dict = {}


class EqualAllocation(BaseModel):
    name: str = "EqualAllocation"
    params: dict = {}


class VOLATILITYSizing(BaseModel):
    name: str = "VOLATILITYSizing"
    params: dict = {
        "period": 256,
        "risk_coefficient": 1,
        "max_position_risk_frac": 0.02,
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0
    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "risk_coefficient", "max_position_risk_frac"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Volatility Sizing - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Volatility Sizing - please contact us about this bug."
                    )

        #validate period
        if not isinstance(value["period"], int):
            raise TypeError("Volatility Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Volatility Sizing period must be > zero")

        #validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("Volatility Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Volatility Sizing risk coefficient must be > zero.")

        #validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError("Volatility Sizing max position risk fraction must be a number.")
        elif not value["max_position_risk_frac"] > 0 and not value["max_position_risk_frac"] < 1:
            raise TypeError("Volatility Sizing max position risk fraction must be > zero and < 1.")
        
        return value


class ATRSizing(BaseModel):
    name: str = "ATRSizing"
    params: dict = {"period": 20, "risk_coefficient": 2, "max_position_risk_frac": 0.02}
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "risk_coefficient", "max_position_risk_frac"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build ATR Sizing - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to ATR Sizing - please contact us about this bug."
                    )
                    
        #validate period
        if not isinstance(value["period"], int):
            raise TypeError("ATR Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("ATR Sizing period must be > zero.")

        #validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("ATR Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("ATR Sizing risk coefficient must be > zero.")

        #validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError("ATR Sizing max position risk fraction must be a number.")
        elif not value["max_position_risk_frac"] > 0 and not value["max_position_risk_frac"] < 1:
            raise TypeError("ATR Sizing max position risk fraction must be > zero and < 1.")
        
        return value

class TurtleUnitSizing(BaseModel):
    name: str = "TurtleUnitSizing"
    params: dict = {
        "period": 20,  # used to calculate N
        "risk_coefficient": 2,
        "max_position_risk_frac": 0.02,
        "num_turtle_units": 1,
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0
    # number of turtle units must be > 0

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "risk_coefficient", "max_position_risk_frac", "num_turtle_units"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Turtle Sizing - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Turtle Sizing - please contact us about this bug."
                    )
                    
        #validate period
        if not isinstance(value["period"], int):
            raise TypeError("Turtle Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Turtle Sizing period must be > zero")

        #validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("Turtle Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Turtle Sizing risk coefficient must be > zero.")

        #validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError("Turtle Sizing max position risk fraction must be a number.")
        elif not value["max_position_risk_frac"] > 0 and not value["max_position_risk_frac"] < 1:
            raise TypeError("Turtle Sizing max position risk fraction must be > zero and < 1.")

        #validate turtle units
        if not isinstance(value["num_turtle_units"], int):
            raise TypeError("Turtle Sizing number of turtle units must be a positive integer.")
        elif not value["num_turtle_units"] > 0:
            raise TypeError("Turtle Sizing number of turtle units must be > zero")  
        return value

class TurtlePyramiding(BaseModel):
    name: str = "TurtlePyramiding"
    params: dict = {
        "period": 20,  # used to calculate N
        "risk_coefficient": 2,
        "max_position_risk_frac": 0.02,
        "max_num_entry_points": 4,
        "delta_N_frac": 0.5,
        "stop_price_N_frac": -2.0,  # positive for stop profit, negative for stop loss
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position num entry points integer > 0
    # delta N fraction: > 0
    # stop price n fraction sort of like ATR stop price -10 to +10

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period", "risk_coefficient", "max_position_risk_frac", "max_num_entry_points", "delta_N_frac", "stop_price_N_frac"]
        if len(key_standard) != len(value):
            raise ValueError(
                "Wrong number of parameters used to build Turtle Pyramid Sizing - please contact us about this bug."
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Turtle Pyramid Sizing - please contact us about this bug."
                    )
                    
        #validate period
        if not isinstance(value["period"], int):
            raise TypeError("Turtle Pyramid Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Turtle Pyramid Sizing period must be > zero")

        #validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("Turtle Pyramid Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Turtle Pyramid Sizing risk coefficient must be > zero.")

        #validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError("Turtle Pyramid Sizing max position risk fraction must be a number.")
        elif not value["max_position_risk_frac"] > 0 and not value["max_position_risk_frac"] < 1:
            raise TypeError("Turtle Pyramid Sizing max position risk fraction must be > zero and < 1.")

        #validate max num entry points
        if not isinstance(value["max_num_entry_points"], int):
            raise TypeError("Turtle Pyramid Sizing max number of entry points must be an integer.")
        elif not value["max_num_entry_points"] > 0:
            raise TypeError("Turtle Pyramid Sizing max number of entry points must be > zero")

        #validate delta N fraction
        if not isinstance(value["delta_N_frac"], int) and not isinstance(
            value["delta_N_frac"], float
        ):
            raise TypeError("Turtle Pyramid Sizing delta N fraction must be a positive number.")
        elif not value["delta_N_frac"] > 0:
            raise TypeError("Turtle Pyramid Sizing delta N fraction must be > zero.")

        #validate delta N fraction
        if not isinstance(value["stop_price_N_frac"], int) and not isinstance(
            value["stop_price_N_frac"], float
        ):
            raise TypeError("Turtle Pyramid Stop Price N fraction must be a number.")


# SIGNALS =====================================================


class Signal(BaseModel):
    """A Signal is a combination of two indicators"""

    # indicator:  Union[MACD, EMA, MACD, SMA, RSI, STOP_PRICE, PRICE]
    # comp_indicator: Optional[Union[SMA, EMA, MACD, PRICE, LEVEL]]
    ## TODO: add a validation check on indicator and compindicator to make sure these names are correct
    indicator: dict
    comp_indicator: Optional[dict]
    rel: str = "leq"
    short: bool = False

    @validator("comp_indicator")
    def comp_indicator_check(cls, value, values, **kwargs):
        # make sure that if the first indicator needs a comparison indicator, that one was provided
        if value is None and values["indicator"]["needs_comp"]:
            raise ValueError("Indicator chosen needs comparison operator")

        # We also make sure that the provided comp indicator is valid to compare with the first indicator
        elif value is not None:
            if value["name"] not in values["indicator"]["valid_comps"]:
                raise ValueError("invalid comparison indicator chosen for indicator")
        return value

    @validator("rel")
    def relation_must_be_valid(cls, value):
        if value not in list(relations.values()):
            raise ValueError("inquality must be greater than or less than or equal to")
        return value

    # add check to make sure the dict for indicator and dict for comp_indicator have the same keys as the signal


#  STRATEGY ==============================================


class BuySignals(BaseModel):
    """Collect BuySignals into list for multiple signals"""

    signals: List[Signal]

    @validator("signals")
    def num_signals_must_be_valid(cls, value):
        if len(value) > max_signals:
            raise ValueError("too many buy signals added to BuySignals")
        return value


class SellSignals(BaseModel):
    """Collect SellSignals into list for multiple signals"""

    signals: List[Signal]

    @validator("signals")
    def num_signals_must_be_valid(cls, value):
        if len(value) > max_signals:
            raise ValueError("too many buy signals added to BuySignals")
        return value


class StrategySettings(BaseModel):
    """
    Sets high level requirements for backtest.
    Default values are used for the sample strategy demo.
    """

    account_size: float
    init_date: str = ""
    start_date: str = "2010-01-01"
    end_date: str = "2015-12-31"
    instruments: List[str]
    trade_days: List[str] = ["mon", "tue", "wed", "thu", "fri"]
    trade_frequency: int = 1
    position_sizing_strategy: dict = {"name": "EqualAllocation", "params": {}}
    position_management_strategy: dict = {"name": "EqualAllocation", "params": {}}
    rebalance_days: List[str] = ["mon", "tue", "wed", "thu", "fri"]
    rebalance_frequency: int = 1

    # TODO: Add validators for instruments, trade days, etc.
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("trade_frequency")
    def trade_frequency_check(cls, value):
        if not isinstance(value, int) or not value > 0:
            raise TypeError("Trade frequency must be a positive integer.")
        return value

    @validator("instruments")  # make sure this list is not empty
    def instruments_check(cls, value):
        if len(value) == 0:
            raise ValueError("Please select at least one instrument")
        elif len(value) >= max_instruments:
            raise ValueError(f"You have selected more stocks than our interns can process. A Maximum of {max_instruments} instruments can be selected for now.")
        return value

    @validator("rebalance_frequency")  # make sure this list is not empty
    def rebalance_frequency_check(cls, value):
        if not isinstance(value, int) or not value >= 0:
            raise TypeError("Rebalance frequency must be a positive integer.")
        return value
        



# TODO: I don't particularly like layering so many schemas, but I can't
# get the API endpoint to work with multiple class inputs, but this does
# work if we use: requests.post(url, data=complete_strategy.json())


class CompleteStrategy(BaseModel):
    """Specifies an entire strategy"""

    strategy_settings: StrategySettings
    buy_signals: BuySignals
    sell_signals: SellSignals
    email: str


## other classes that are used to make API calls
class PricePlot(BaseModel):
    instr: str = "GE"
    start_date: str = "2015"
    end_date: str = "2017"


class BuyAndHold(BaseModel):
    instr_list: List[str] = ["GE"]
    account_size: int = 100000
    start_date: str = "2015"
    end_date: str = "2017"
