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

'''
How to add a new strategy option to the site that requires parameters (position sizing, risk management, etc)
    - create the new dropdowns in buy_tab, sell_tab, or strategy_tab
    - create the callbacks buy_tab, sell_tab, or strategy_tab
    - add the new inputs to dash_app_main.build_strategy callback
    - update utils_strategy_compilation.py
    
'''
from typing import List, Union, Optional
from pydantic import BaseModel, validator

# List parameters and input ranges for each
max_signals = 5
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
# - NOTE: all of the keys are what will show up in the dropdown menu, so their capitalization

every_indicator = {
    "Stop Profit": "STOP_PRICE",  # input is constrained to (+)
    "Stop Loss": "STOP_PRICE",  # input numbers are constrained to (-)
    "ATR Stop Profit": "ATR_STOP_PRICE",
    "ATR Stop Loss": "ATR_STOP_PRICE",
    "Price": "PRICE",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "Volatility": "VOLATILITY",
    "PSAR": "PSAR",
    "HURST": "HURST",
}

buy_indicators = {
    "Price": "PRICE",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "Volatility": "VOLATILITY",
    "PSAR": "PSAR",
    "HURST": "HURST",
}

position_sizings = {
    "Equal Allocation": "EqualAllocation",
    "Volatility Allocation": "VOLATILITYSizing",
    "ATR Allocation": "ATRSizing",
    "Turtle Allocation": "TurtleSizing",
    "Turtle Pyramiding": "TurtlePyramiding",
    "No Risk Management": "NoRiskManagement",
}


sell_indicators = {
    "Stop Profit": "STOP_PRICE",  # uses same schema class, but input numbers are constrained to +
    "Stop Loss": "STOP_PRICE",  # uses same schema class, but input numbers are constrained to -
    "ATR Stop Profit": "ATR_STOP_PRICE",
    "ATR Stop Loss": "ATR_STOP_PRICE",
    "Price": "PRICE",
    "SMA": "SMA",
    "EMA": "EMA",
    "MACD": "MACD",
    "MACD Signal": "MACD_SIGNAL",
    "RSI": "RSI",
    "ATR": "ATR",
    "Volatility": "VOLATILITY",
    "PSAR": "PSAR",
    "HURST": "HURST",
}

indicators_with_time_params = {
    "SMA": ["period"],  # Indicators that have to look back in time and the param(s)
    # that defines the farthest number of days to look back
    "EMA": ["period"],
    "MACD": ["slowEMA_period"],
    "MACD_SIGNAL": ["slowEMA_period", "signalEMA_period"],
    "RSI": ["period"],
    "ATR": ["period"],
    "ATR_STOP_PRICE": ["period"],
    "VOLATILITY": ["period"],
    "PSAR": ["period"],
}

relations = {"Greater than": "geq", "Less than": "leq", "Equal to": "eq"}


""" all of these indicator classes have the same number of inputs
as required to run in pyalgotrade"""

"INDICATORS ===================================================="


class SMA(BaseModel):
    name: str = "SMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build SMA")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to SMA signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("SMA period must be a number")
                elif not value[key] > 0:
                    raise TypeError("SMA period must be greater than zero")
        return value


class EMA(BaseModel):
    name: str = "EMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build EMA")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to EMA signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("EMA period must be a number")
                elif not value[key] > 0:
                    raise TypeError("EMA period must be greater than zero")
        return value


class MACD(BaseModel):
    name: str = "MACD"
    params: dict = {"fastEMA_period": 10, "slowEMA_period": 20}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "PRICE"]

    # @validator("params")
    # def param_key_check(cls, value):
    #     key_standard = ["fastEMA_period", "slowEMA_period"]
    #     if len(key_standard) != len(value):
    #         raise ValueError("wrong number of parameters used to build MACD")
    #     else:
    #         for n, key in enumerate(value.keys()):
    #             if key != key_standard[n]:
    #                 raise ValueError(
    #                     "Wrong parameters fed to MACD signal builder - please contact us about this bug"
    #                 )
    #             elif not isinstance(value[key], int):
    #                 raise TypeError("MACD periods must be numbers")
    #             elif not value[key] > 0:
    #                 raise TypeError("MACD inputs must be greater than zero")
    #     return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError("MACD fast EMA period must be less than slow EMA period")
        return value


class MACD_SIGNAL(BaseModel):
    name: str = "MACD_SIGNAL"
    params: dict = {"fastEMA_period": 10, "slowEMA_period": 20, "signalEMA_period": 9}

    needs_comp: bool = False
    valid_comps: list = None

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["fastEMA_period", "slowEMA_period", "signalEMA_period"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build MACD_SIGNAL")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to MACD Signal signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("MACD Signal periods must be numbers")
                elif not value[key] > 0:
                    raise TypeError("MACD Signal inputs must be greater than zero")
        return value

    @validator("params")
    def fast_slow_comparison(cls, value, values):
        if value["slowEMA_period"] <= value["fastEMA_period"]:
            raise ValueError("MACD fast EMA period must be less than slow EMA period")
        return value


class RSI(BaseModel):
    name: str = "RSI"
    params: dict = {"period": 10}
    needs_comp: bool = True  # will always be level
    valid_comps: list = ["LEVEL"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build RSI")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to RSI signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("RSI period must be a number")
                elif not value[key] > 0:
                    raise TypeError("RSI inputs must be greater than zero")
        return value


class STOP_PRICE(BaseModel):
    name: str = "STOP_PRICE"
    params: dict = {
        "percent_change": 10.1
    }  # will be positive for stop profit and neg for stop loss
    needs_comp: bool = True  # will always be price
    valid_comps: list = ["PRICE"]
    # this is used to confirm the param percent chosen matches profit or loss

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["percent_change"]
        if len(key_standard) != len(value):
            raise ValueError(
                "wrong number of parameters used to build stop loss or profit signal"
            )
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to stop signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], float) and not isinstance(
                    value[key], int
                ):
                    raise TypeError("stop loss or stop profit % must be a number")
        return value


class ATR_STOP_PRICE(BaseModel):
    name: str = "ATR_STOP_PRICE"
    params: dict = dict(
        period=20,
        # entry_price=10,
        stop_price_ATR_frac=-2.0,  # positive for stop profit, negative for stop price
    )
    needs_comp: bool = True
    valid_comps: list = ["PRICE"]

    # TODO: Add validators


class PRICE(BaseModel):
    name: str = "PRICE"
    params: dict = {
        "price_type": "Close"
    }  # "High", "Low", or "Close" (always use Adj Close)
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "ATR"]


class ATR(BaseModel):
    name: str = "ATR"
    params: dict = {"period": 20, "multiple": 1}
    needs_comp: bool = False
    valid_comps: list = ["PRICE"]

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["period"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build ATR")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to ATR signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("ATR period and multiple must be a number")
                elif not value[key] > 0:
                    raise TypeError("ATR period must be greater than zero")
        return value


class LEVEL(BaseModel):
    name: str = "LEVEL"
    params: dict = {"level": 10}
    needs_comp: bool = False  # always is a comparison to RSI
    valid_comps: list = None

    @validator("params")
    def param_key_check(cls, value):
        key_standard = ["level"]
        if len(key_standard) != len(value):
            raise ValueError("wrong number of parameters used to build level")
        else:
            for n, key in enumerate(value.keys()):
                if key != key_standard[n]:
                    raise ValueError(
                        "Wrong parameters fed to Level signal builder - please contact us about this bug"
                    )
                elif not isinstance(value[key], int):
                    raise TypeError("RSI level must be a number")
                elif not value[key] > 0:
                    raise TypeError("RSI level input must be greater than zero")
        return value


class BOOLEAN(BaseModel):
    name: str = "BOOLEAN"
    params: dict = {"boolean": True}  # or 'False'
    needs_comp: bool = True
    valid_comps: list = ["PSAR"]


class VOLATILITY(BaseModel):
    name: str = "VOLATILITY"
    params: dict = {"period": 252, "multiple": 1}
    needs_comp: bool = False
    valid_comps: list = ["PRICE", "LEVEL"]


class PSAR(BaseModel):
    """
    Parabolic SAR
    """

    name: str = "PSAR"
    params: dict = {
        "type_indicator": "value",  # Either 'value', 'reversal_toUptrend', 'reversal_toDowntrend'
        "init_acceleration_factor": 0.02,
        "acceleration_factor_step": 0.02,
        "max_acceleration_factor": 0.2,
        "previous_day": False,  # Whether the PSAR returned is for current day (True) or not (for comparison)
        "period": 2,  # Number of days to look back to ensure PSAR is in proper range
    }
    needs_comp: bool = True
    valid_comps: list = ["LEVEL", "PSAR", "PRICE", "BOOLEAN"]


class HURST(BaseModel):
    name: str = "HURST"
    params: dict = {"period": 10, "minLags": 2, "maxLags": 20}
    needs_comps: bool = True
    valid_comps: list = ["LEVEL"]


"classes that can be initial POSITION SIZING or Risk Management (position management during rebalance) ============================================="


class NoRiskManagement(BaseModel):
    name: str = "NoRiskManagement"
    params: dict = {}


class EqualAllocation(BaseModel):
    name: str = "EqAll"
    params: dict = {}


class VOLATILITYSizing(BaseModel):
    name: str = "VOLATILITYSizing"
    params: dict = {
        "period": 256,
        "risk_coefficient": 1,
        "max_position_risk_frac": 0.02,
    }


class ATRSizing(BaseModel):
    name: str = "ATRSizing"
    params: dict = {"period": 20, "risk_coefficient": 2, "max_position_risk_frac": 0.02}


class TurtleSizing(BaseModel):
    name: str = "TurtleSizing"
    params: dict = {
        "period": 20,  # used to calculate N
        "risk_coefficient": 2,
        "max_position_risk_frac": 0.02,
        "num_turtle_units": 1,
    }


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


"SIGNALS ====================================================="


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


"STRATEGY =============================================="


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
    trade_days: List[str] = ["mon", "wed", "fri"]
    trade_frequency: int = 1
    position_sizing_strategy: dict = {"name": "EqAll", "params": {}}
    position_management_strategy: dict = {"name": "EqAll", "params": {}}
    rebalance_days: List[str] = ["wed"]
    rebalance_frequency: int = 4

    # TODO: Add validators for instruments, trade days, etc.
    # https://pydantic-docs.helpmanual.io/usage/validators/
    @validator("trade_frequency")
    def trade_frequency_check(cls, value):
        if value < 1:
            raise ValueError("Trade frequency must be greater than 0.")
        return value

    @validator("instruments")  # make sure this list is not empty
    def instruments_check(cls, value):
        if len(value) == 0:
            raise ValueError("Please select at least one instrument")
        return value

    @validator("rebalance_frequency")  # make sure this list is not empty
    def rebalance_frequency_check(cls, value):
        if value < 1:
            raise ValueError("Rebalance frequency must be greater than 0.")
        return value

    # @validator("position_sizing_params") # If params are present
    # def position_sizing_params(cls, value):
    #     assert value is not None, "If present, a value is required."
    #     return value


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
