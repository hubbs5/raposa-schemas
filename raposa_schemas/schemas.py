# coding: utf-8

# Notes about these schemas
# - Union[] is not a very durable way to check if indicator or comp indicator matches the criteria of another schema
# - Union[] will try to force the field value to work with every option in Union, starting from left to right.
#         --> for instance if you feed indicator = an instance of EMA class into building a SIGNAL class 
#         ---> if SIGNAL had a Union[SMA,EMA] check on indicator, it will assign the EMA class values into an SMA class
# - to avoid this, I am going back to using dictionaries as parameter inputs and indicator inputs. 
# - I wrote custom validation checks for every schema class to avoid this Union problem

# - The custom validation checks make sure that the parametr dictionary for every indicator has 
#         1) the correct number of keys
#         2) the correct keys as compared to the standard outlined in the validation functions in each class
# How to add a new indicator to the website
#     1) create a schema class here
#     2) Before issuing the PR to raposa-schemas, 
#         pip install the branch onto your local raposa-website using pip install -e git+https://git@github.com/hubbs5/raposa-schemas.git@{ branch name }#egg=raposa-schemas
#         pip install the branch onto your local raposa using pip install -e git+https://git@github.com/hubbs5/raposa-schemas.git@{ branch name }#egg=raposa-schemas
#     3) Add the indicator to raposa-website\apps\dash_strategy_builder\dash_app_utils\indicator_divs.py
#         It is not best practice, but you may need to add a special case to 
#         raposa-website\apps\dash_strategy_builder\dash_app_utils\strategy_compilation.py for indicators that do not follow the standard formula
#     4) test to make sure backtests can run with the new indicator on the frontend
#     5) update the bot garage so that it can process the indicator in new strategies
#         update signal_translator() in apps\dash_bot_garage\dash_app_utils\utils.py 

from warnings import warn
from abc import abstractmethod, ABC
from pydantic import BaseModel, validator, Field
from typing import List, Type, Union, Optional, Dict, Any


# List parameters and input ranges for each
# TODO: Best to control these in Django
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


# every_indicator is not used to directly make any dropdowns. But used often to check if an indicator exists.
every_indicator = {
    "Stop Loss": "STOP_PRICE",
    "ATR Stop Loss": "ATR_STOP_PRICE",
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
    "PSAR": "PSAR",
    "HURST": "HURST",
    "Level": "LEVEL",
    "Donchian Channel": "DONCHIAN",
    # "Signal is": "BOOLEAN",
    "Bollinger Bands": "BOLLINGER",
    # "Band Width": "BAND_WIDTH",
    # "Moving Average Distance": "MAD"
}

# every indicator listed in buy-tab dropdown
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
    "PSAR": "PSAR",
    "HURST": "HURST",
    "Donchian Channel": "DONCHIAN",
    "Bollinger Bands": "BOLLINGER",
    # "Band Width": "BAND_WIDTH",
    # "Moving Average Distance": "MAD"
}

# every indicator listed in sell-tab dropdown
sell_indicators = {
    "Stop Loss": "STOP_PRICE",
    "ATR Stop Loss": "ATR_STOP_PRICE",
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
    "PSAR": "PSAR",
    "HURST": "HURST",
    "Donchian Channel": "DONCHIAN",
    "Bollinger Bands": "BOLLINGER",
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
    '''
    Indicators that have to look back in time and the param(s)
    that defines the farthest number of days to look back
    '''
    "SMA": ["period"],
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
    "MAD": ["fastSMA_period", "slowSMA_period"],
    "DONCHIAN": ["period"],
}

relations = {"> or =": "geq", "< or =": "leq", ">": "gt", "<": "lt", "=": "eq"}

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

""" all of these indicator classes have the same number of inputs
as required to run in pyalgotrade"""

"INDICATORS ===================================================="

class AbstractIndicatorModel(BaseModel, ABC):
    name: str = Field(..., description="Name of the indicator")
    params: Dict = Field(..., description="Parameters for the indicator")
    needs_comp: bool = Field(..., description="Does the indicator need a comparison?")
    valid_comps: List = Field(..., description="Valid comparisons for the indicator")

    @abstractmethod
    def param_check(self):
        raise NotImplementedError

def _param_key_check(params, key_standard):
    if len(key_standard) != len(params):
        raise ValueError(
            "Wrong number of parameters used to build indicator - please contact us about this bug." + \
                f"{key_standard} != {list(params.keys())}"
        )
    assert key_standard == list(params.keys()), (
        "Wrong parameters fed to indicator builder - please contact us about this bug." + \
            f"{key_standard} != {list(params.keys())}")


def _period_check(period, min=1, max=1000, description="Period"):
    if not isinstance(period, int):
        raise TypeError(f"{description} must be a positive integer.")
    elif not period > 0:
        raise TypeError(f"{description} must be > zero.")
    elif not period < max:
        raise TypeError(f"{description} must be < {max}")
    elif not period > min:
        raise TypeError(f"{description} must be > {min}")
    return period


def _float_check(value, min=0, max=100, description="Value"):
    if not isinstance(value, float) and not isinstance(value, int):
        raise TypeError(f"{description} must be a number.")
    elif not value > min:
        raise TypeError(f"{description} must be > {min}")
    elif not value < max:
        raise TypeError(f"{description} must be < {max}")
    return value

def _int_check(value, min=0, max=100, description="Value"):
    if not isinstance(value, int):
        raise TypeError(f"{description} must be a number.")
    elif not value > min:
        raise TypeError(f"{description} must be > {min}")
    elif not value < max:
        raise TypeError(f"{description} must be < {max}")
    return value

def _str_check(value: str, values: list, description: str="Value"):
    if not isinstance(value, str):
        raise TypeError(f"{description} must be a string.")
    elif value not in values:
        raise TypeError(f"{description} must be one of {values}")
    return value

def _bool_check(value: bool, description: str="Value"):
    if not isinstance(value, bool):
        raise TypeError(f"{description} must be a boolean.")
    return value

class SMA(AbstractIndicatorModel):
    name: str = "SMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    # param bound >= 2 and < 1000

    @validator("params", always=True)
    def param_check(cls, value):
        key_standard = ["period"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
 
        return value


class EMA(AbstractIndicatorModel):
    name: str = "EMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    
    @validator("params")
    def param_check(cls, value):
        key_standard = ["period"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        
        return value


class MACD(AbstractIndicatorModel):
    name: str = "MACD"
    params: dict = {"fastEMA_period": 10, "slowEMA_period": 20}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "PRICE", "MACD_SIGNAL"]
    # param bound >= 2 and < 1000
    # need to enforce that fastEMA period is > =slowEMAperiod

    @validator("params")
    def param_check(cls, value):
        key_standard = ["fastEMA_period", "slowEMA_period"]
        _param_key_check(value, key_standard)
        _period_check(value["fastEMA_period"], description="MACD fastEMA_period")
        _period_check(value["slowEMA_period"], description="MACD slowEMA_period")
        if value["fastEMA_period"] >= value["slowEMA_period"]:
            raise ValueError(
                "The fast EMA period for MACD must be < the slow EMA period"
            )
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError(
                "The fast EMA period for MACD must be < the slow EMA period"
            )
        return value


class MACD_SIGNAL(AbstractIndicatorModel):
    name: str = "MACD_SIGNAL"
    params: dict = {"fastEMA_period": 10, "slowEMA_period": 20, "signalEMA_period": 9}
    needs_comp: bool = True
    valid_comps: list = ["MACD", "SMA", "EMA"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["fastEMA_period", "slowEMA_period", "signalEMA_period"]
        _param_key_check(value, key_standard)
        _period_check(value["fastEMA_period"], description="MACD Signal fastEMA_period")
        _period_check(value["slowEMA_period"], description="MACD Signal slowEMA_period")
        _period_check(value["signalEMA_period"], description="MACD Signal signalEMA_period")
        if value["fastEMA_period"] >= value["slowEMA_period"]:
            raise ValueError(
                "The fast EMA period for MACD Signal must be < the slow EMA period"
            )
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError(
                "The fast EMA period for MACD Signal must be < the slow EMA period"
            )
        return value


class RSI(AbstractIndicatorModel):
    name: str = "RSI"
    params: dict = {"period": 10}
    needs_comp: bool = True  # will always be level
    valid_comps: list = ["LEVEL"]
    # param period bound >= 2 and < 1000
    # LEVEL for RSI is always between 0 and 100

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])

        return value


class STOP_PRICE(AbstractIndicatorModel):
    name: str = "STOP_PRICE"
    params: dict = {
        "percent_change": 10.1, # will be positive for profit target and neg for stop loss
        "trailing": False,
    }  
    needs_comp: bool = True  # will always be price
    valid_comps: list = ["PRICE"]
    # param bound > -100% and < 10000%
    
    @validator("params")
    def param_check(cls, value):
        key_standard = ["percent_change", "trailing"]
        _param_key_check(value, key_standard)
        _float_check(value["percent_change"], min=-100, max=10000, description="Stop price % change")
        _bool_check(value["trailing"], description="Stop price trailing")
 
        return value


class ATR_STOP_PRICE(AbstractIndicatorModel):
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
    def param_check(cls, value):
        key_standard = ["period", "stop_price_ATR_frac", "trailing"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _float_check(value["stop_price_ATR_frac"], min=-10, max=10, description="ATR stop price fraction")
        _bool_check(value["trailing"], description="ATR stop price trailing")

        return value


class PRICE(AbstractIndicatorModel):
    name: str = "PRICE"
    params: dict = {
        "price_type": "Close",  # must be in ["Open", "High", "Low", "Close", or "Typical"]
    } 
    # TODO: Remove case sensitivity
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "ATR", "PRICE_WINDOW", "BOLLINGER"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["price_type"]
        _param_key_check(value, key_standard)
        _str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Price type")

        return value


class PRICE_WINDOW(AbstractIndicatorModel):
    name: str = "PRICE_WINDOW"
    params: dict = {
        "period": 30,  # Number of days to look back
        "max_or_min": "max",  # must be in ["max" or "min"]
        "price_type": "High",  # must be in ["Open", "High", "Low", "Close", "Typical"]
    }
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]
    # param period bound >= 2 and < 1000

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "max_or_min", "price_type"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _str_check(value["max_or_min"], values=["max", "min"], description="Max or min")
        _str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Price type")

        return value


class ATR(AbstractIndicatorModel):
    name: str = "ATR"
    params: dict = {"period": 20, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["ATR"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "multiple"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _float_check(value["multiple"], description="ATR multiple")
       
        return value


class ATRP(AbstractIndicatorModel):
    name: str = "ATRP"
    params: dict = {"period": 20, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["ATRP"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "multiple"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _float_check(value["multiple"], description="ATR % multiple")

        return value


class LEVEL(AbstractIndicatorModel):
    name: str = "LEVEL"
    params: dict = {"level": 10}
    needs_comp: bool = False  # always is a comparison
    valid_comps: list = None
    # param level bound by 0 and 100
    # might need to be negative for somethings

    @validator("params")
    def param_check(cls, value):
        key_standard = ["level"]
        _param_key_check(value, key_standard)
        # Set min and max to be inclusive of endpoints
        _int_check(value["level"], description="Level value", min=-1, max=101)

        return value


class BOOLEAN(AbstractIndicatorModel):
    name: str = "BOOLEAN"
    params: dict = {"boolean": True}  # or False
    needs_comp: bool = True
    valid_comps: list = ["PSAR"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["boolean"]
        _param_key_check(value, key_standard)
        _bool_check(value["boolean"], description="Boolean")

        return value


class VOLATILITY(AbstractIndicatorModel):
    name: str = "VOLATILITY"
    params: dict = {"period": 252, "multiple": 1}
    needs_comp: bool = True
    valid_comps: list = ["VOLATILITY", "LEVEL"]
    # param period bound >= 2 and < 1000
    # param multiple bound by greather than 0.25 to 10

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "multiple"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _float_check(value["multiple"], description="Volatility multiple")

        return value


class PSAR(AbstractIndicatorModel):
    """
    Parabolic SAR
    """

    name: str = "PSAR"
    params: dict = {
        "type_indicator": "reversal_toUptrend",  # Either 'reversal_toUptrend', 'reversal_toDowntrend'
        "init_acceleration_factor": 0.02,
        "acceleration_factor_step": 0.02,
        "max_acceleration_factor": 0.2,
        "period": 2,  # Number of days to look back to ensure PSAR is in proper range
    }
    needs_comp: bool = True
    # TODO: Can run PSAR vs other comps
    valid_comps: list = ['BOOLEAN']

    @validator("params", always=True)
    def param_check(cls, value):
        key_standard = ["type_indicator", "init_acceleration_factor",
                        "acceleration_factor_step", "max_acceleration_factor",
                        "period"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _str_check(value["type_indicator"], values=["reversal_toUptrend", "reversal_toDowntrend"],
                   description="PSAR type indicator")
        _float_check(value["init_acceleration_factor"], min=0, max=1, description="PSAR initial acceleration factor")
        _float_check(value["acceleration_factor_step"], min=0, max=1, description="PSAR acceleration factor step")
        _float_check(value["max_acceleration_factor"], min=0, max=1, description="PSAR max acceleration factor")


class HURST(AbstractIndicatorModel):
    name: str = "HURST"
    params: dict = {"period": 10, "minLags": 2, "maxLags": 20}
    needs_comp: bool = True
    valid_comps: list = ["LEVEL"]
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # min lags must be less than max lags and both greater than one

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "minLags", "maxLags"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _int_check(value["minLags"], description="HURST Signal minLags")
        _int_check(value["maxLags"], description="HURST Signal maxLags")
        if value["minLags"] >= value["maxLags"]:
            raise ValueError("The minLags period for HURST Signal must be < the maxLags period")
        
        return value


class BOLLINGER(AbstractIndicatorModel):
    name: str = "BOLLINGER"
    params: dict = {
        "period": 20,
        "numSTD": 2,
        "band": "upper", # "band" in ["upper", "middle", "lower"]
        "price_type": "Typical",  # price_type either "Open", "High", "Low", "Close", or "Typical"
    }  
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL", "SMA", "EMA", "MACD"]

    @validator("params")
    def param_check(cls, value):
        key_standard = [
            "period",
            "numSTD",
            "band",
            "price_type",
        ]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _float_check(value["numSTD"], description="Bollinger Band numSTD")
        _str_check(value["band"], values=["upper", "middle", "lower"], description="Bollinger Band band")
        _str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Bollinger Band price_type")
 
        return value


class BAND_WIDTH(AbstractIndicatorModel):
    name: str = "BAND_WIDTH"
    params: dict = {
        "period": 20,
        "numSTD": 2,
        "price_type": "Typical", # price_type either "Open", "High", "Low", "Close", or "Typical"
    }  
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["period", "numSTD", "price_type"]
        _period_check(value["period"])
        _param_key_check(value, key_standard)
        _float_check(value["numSTD"], description="Band Width numSTD")
        _str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Band Width price_type")

        return value


class DONCHIAN(AbstractIndicatorModel):
    name: str = "DONCHIAN"
    params: dict = {"period": 20, "channel": "middle"}
    needs_comp: bool = True
    valid_comps: list = ["PRICE"]

    @validator("params")
    def param_check(cls, value):
        channels = ["upper", "lower", "middle"]
        key_standard = ["period", "channel"]
        _param_key_check(value, key_standard)
        _period_check(value["period"])
        _str_check(value["channel"], values=channels, description="Donchian Channel channel")

        return value


class MAD(AbstractIndicatorModel):
    name: str = "MAD"
    params: dict = {"fastSMA_period": 21, "slowSMA_period": 200}
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["fastSMA_period", "slowSMA_period"]
        _param_key_check(value, key_standard)
        _period_check(value["fastSMA_period"])
        _period_check(value["slowSMA_period"])

        if value["fastSMA_period"] >= value["slowSMA_period"]:
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
        "risk_cap": False
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0
    @validator("params")
    def param_key_check(cls, value):
        key_standard = [
            "period", 
            "risk_coefficient", 
            "max_position_risk_frac", 
            "risk_cap"
        ]
        # validate period
        if not isinstance(value["period"], int):
            raise TypeError("Volatility Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Volatility Sizing period must be > zero")

        # validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError(
                "Volatility Sizing risk coefficient must be a positive number."
            )
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Volatility Sizing risk coefficient must be > zero.")

        # validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError(
                "Volatility Sizing max position risk fraction must be a number."
            )
        elif (
            value["max_position_risk_frac"] <= 0
            or value["max_position_risk_frac"] > 1
        ):
            raise TypeError(
                "Volatility Sizing max position risk fraction must be > zero and < 1."
            )

        # validate risk cap
        if "risk_cap" not in value.keys():
            warn("Volatility Sizing modules without a risk_cap are deprecated and will not be allowed in the future.",
                DeprecationWarning, stacklevel=2)
            value["risk_cap"] = False
        elif not isinstance(value["risk_cap"], bool):
            raise TypeError("Volatility Sizing risk cap must be boolean.")

        return value


class ATRSizing(BaseModel):
    name: str = "ATRSizing"
    params: dict = {
        "period": 20,
        "risk_coefficient": 2, 
        "max_position_risk_frac": 0.02,
        "risk_cap": False
        }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0

    @validator("params")
    def param_key_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "risk_cap"
            ]

        # validate period
        if not isinstance(value["period"], int):
            raise TypeError("ATR Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("ATR Sizing period must be > zero.")

        # validate risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("ATR Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("ATR Sizing risk coefficient must be > zero.")

        # validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError("ATR Sizing max position risk fraction must be a number.")
        elif (
            value["max_position_risk_frac"] <= 0
            or value["max_position_risk_frac"] > 1
        ):
            raise TypeError(
                "ATR Sizing max position risk fraction must be > zero and < 1."
            )

        # validate risk cap
        if "risk_cap" not in value.keys():
            warn("ATR Sizing modules without a risk_cap are deprecated and will not be allowed in the future.",
                DeprecationWarning, stacklevel=2)
            value["risk_cap"] = False
        elif not isinstance(value["risk_cap"], bool):
            raise TypeError("ATR Sizing risk cap must be boolean.")

        return value


class TurtleUnitSizing(BaseModel):
    name: str = "TurtleUnitSizing"
    params: dict = {
        "period": 20,  # used to calculate N
        "risk_coefficient": 2,
        "max_position_risk_frac": 0.02,
        "num_turtle_units": 1,
        "risk_cap": False
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0
    # number of turtle units must be > 0

    @validator("params")
    def param_key_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "num_turtle_units",
        ]

        # validate period
        if not isinstance(value["period"], int):
            raise TypeError("Turtle Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Turtle Sizing period must be > zero")

        # validaet risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("Turtle Sizing risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Turtle Sizing risk coefficient must be > zero.")

        # validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError(
                "Turtle Sizing max position risk fraction must be a number."
            )
        elif (
            value["max_position_risk_frac"] <= 0
            or value["max_position_risk_frac"] > 1
        ):
            raise TypeError(
                "Turtle Sizing max position risk fraction must be > zero and < 1."
            )

        # validate turtle units
        if not isinstance(value["num_turtle_units"], int):
            raise TypeError(
                "Turtle Sizing number of turtle units must be a positive integer."
            )
        elif not value["num_turtle_units"] > 0:
            raise TypeError("Turtle Sizing number of turtle units must be > zero")

        # validate risk cap
        if "risk_cap" not in value.keys():
            warn("Turtle Sizing modules without a risk_cap are deprecated and will not be allowed in the future.",
                DeprecationWarning, stacklevel=2)
            value["risk_cap"] = False
        elif not isinstance(value["risk_cap"], bool):
            raise TypeError("Turtle Sizing risk cap must be boolean.")
        
        return value


class TurtlePyramiding(BaseModel):
    name: str = "TurtlePyramiding"
    params: dict = {
        "period": 20,  # used to calculate N
        "risk_coefficient": 2,
        "max_position_risk_frac": 0.02,
        "max_num_entry_points": 1,
        "delta_N_frac": 0.2,
        "stop_price_N_frac": -2.0,
        "risk_cap": False
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0, 10) but not quite 0
    # max_position risk fraction (0, 1) do not include 0
    # number of turtle units must be > 0

    @validator("params")
    def param_key_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "max_num_entry_points",
            "delta_N_frac",
            "stop_price_N_frac",
            "risk_cap"
        ]

        # validate period
        if not isinstance(value["period"], int):
            raise TypeError("Turtle Sizing period must be a positive integer.")
        elif not value["period"] > 0:
            raise TypeError("Turtle Pyramding period must be > zero")

        # validate risk coefficient
        if not isinstance(value["risk_coefficient"], int) and not isinstance(
            value["risk_coefficient"], float
        ):
            raise TypeError("Turtle Pyramding risk coefficient must be a positive number.")
        elif not value["risk_coefficient"] > 0:
            raise TypeError("Turtle Pyramding risk coefficient must be > zero.")

        # validate max position risk fraction
        if not isinstance(value["max_position_risk_frac"], int) and not isinstance(
            value["max_position_risk_frac"], float
        ):
            raise TypeError(
                "Turtle Pyramding max position risk fraction must be a number."
            )
        elif (
            value["max_position_risk_frac"] <= 0
            or value["max_position_risk_frac"] > 1
        ):
            raise TypeError(
                "Turtle Pyramding max position risk fraction must be > zero and < 1."
            )

        # validate turtle units
        if not isinstance(value["max_num_entry_points"], int):
            raise TypeError(
                "Turtle Pyramding number of turtle units must be a positive integer."
            )
        elif not value["max_num_entry_points"] > 0:
            raise ValueError("Turtle Pyramding number of turtle units must be > zero")

        # validate delta N fraction
        if not isinstance(value["delta_N_frac"], int) and not isinstance(
            value["delta_N_frac"], float
        ):
            raise TypeError(
                "Turtle Pyramding delta N fraction must be a number."
            )
        elif (
            value["delta_N_frac"] <= 0
            or value["delta_N_frac"] > 1
        ):
            raise TypeError(
                "Turtle Pyramding delta N fraction must be > zero and < 1."
            )

        # validate stop price N frac
        if not isinstance(value["stop_price_N_frac"], int) and not isinstance(
            value["stop_price_N_frac"], float
        ):
            raise TypeError(
                "Turtle Pyramding number of turtle units must be a number."
            )

        # validate risk cap
        if "risk_cap" not in value.keys():
            warn("Turtle Pyramding modules without a risk_cap are deprecated and will not be allowed in the future.",
                DeprecationWarning, stacklevel=2)
            value["risk_cap"] = False
        elif not isinstance(value["risk_cap"], bool):
            raise TypeError("Turtle Pyramding risk cap must be boolean.")
        
        return value


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
            raise ValueError(
                f"You have selected more stocks than our interns can process. A Maximum of {max_instruments} instruments can be selected for now."
            )
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
    start_date: str = "2015-03-01"
    end_date: str = "2017-06-04"


class BuyAndHold(BaseModel):
    instr_list: List[str] = ["GE"]
    account_size: int = 100000
    start_date: str = "2015-03-01"
    end_date: str = "2017-06-04"
