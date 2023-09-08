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
