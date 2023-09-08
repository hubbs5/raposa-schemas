from warnings import warn
from abc import abstractmethod, ABC
from pydantic import BaseModel, validator, Field
from typing import List, Type, Union, Optional, Dict, Any

from .validators import *

class AbstractIndicatorModel(BaseModel, ABC):
    name: str = Field(..., description="Name of the indicator")
    params: Dict = Field(..., description="Parameters for the indicator")
    needs_comp: bool = Field(..., description="Does the indicator need a comparison?")
    valid_comps: List = Field(..., description="Valid comparisons for the indicator")

    @abstractmethod
    def param_check(self):
        raise NotImplementedError


class SMA(AbstractIndicatorModel):
    name: str = "SMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    # param bound >= 2 and < 1000

    @validator("params", always=True)
    def param_check(cls, value):
        key_standard = ["period"]
        param_key_check(value, key_standard)
        period_check(value["period"])
 
        return value


class EMA(AbstractIndicatorModel):
    name: str = "EMA"
    params: dict = {"period": 10}
    needs_comp: bool = True
    valid_comps: list = ["SMA", "EMA", "MACD", "PRICE"]
    
    @validator("params")
    def param_check(cls, value):
        key_standard = ["period"]
        param_key_check(value, key_standard)
        period_check(value["period"])
        
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
        param_key_check(value, key_standard)
        period_check(value["fastEMA_period"], description="MACD fastEMA_period")
        period_check(value["slowEMA_period"], description="MACD slowEMA_period")
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
        param_key_check(value, key_standard)
        period_check(value["fastEMA_period"], description="MACD Signal fastEMA_period")
        period_check(value["slowEMA_period"], description="MACD Signal slowEMA_period")
        period_check(value["signalEMA_period"], description="MACD Signal signalEMA_period")
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
        param_key_check(value, key_standard)
        period_check(value["period"])

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
        param_key_check(value, key_standard)
        float_check(value["percent_change"], min=-100, max=10000, description="Stop price % change")
        bool_check(value["trailing"], description="Stop price trailing")
 
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
        param_key_check(value, key_standard)
        period_check(value["period"])
        float_check(value["stop_price_ATR_frac"], min=-10, max=10, description="ATR stop price fraction")
        bool_check(value["trailing"], description="ATR stop price trailing")

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
        param_key_check(value, key_standard)
        str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Price type")

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
        param_key_check(value, key_standard)
        period_check(value["period"])
        str_check(value["max_or_min"], values=["max", "min"], description="Max or min")
        str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Price type")

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
        param_key_check(value, key_standard)
        period_check(value["period"])
        float_check(value["multiple"], description="ATR multiple")
       
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
        param_key_check(value, key_standard)
        period_check(value["period"])
        float_check(value["multiple"], description="ATR % multiple")

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
        param_key_check(value, key_standard)
        # Set min and max to be inclusive of endpoints
        int_check(value["level"], description="Level value", min=-1, max=101)

        return value


class BOOLEAN(AbstractIndicatorModel):
    name: str = "BOOLEAN"
    params: dict = {"boolean": True}  # or False
    needs_comp: bool = True
    valid_comps: list = ["PSAR"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["boolean"]
        param_key_check(value, key_standard)
        bool_check(value["boolean"], description="Boolean")

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
        param_key_check(value, key_standard)
        period_check(value["period"])
        float_check(value["multiple"], description="Volatility multiple")

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
        param_key_check(value, key_standard)
        period_check(value["period"])
        str_check(value["type_indicator"], values=["reversal_toUptrend", "reversal_toDowntrend"],
                   description="PSAR type indicator")
        float_check(value["init_acceleration_factor"], min=0, max=1, description="PSAR initial acceleration factor")
        float_check(value["acceleration_factor_step"], min=0, max=1, description="PSAR acceleration factor step")
        float_check(value["max_acceleration_factor"], min=0, max=1, description="PSAR max acceleration factor")


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
        param_key_check(value, key_standard)
        period_check(value["period"])
        int_check(value["minLags"], description="HURST Signal minLags")
        int_check(value["maxLags"], description="HURST Signal maxLags")
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
        param_key_check(value, key_standard)
        period_check(value["period"])
        float_check(value["numSTD"], description="Bollinger Band numSTD")
        str_check(value["band"], values=["upper", "middle", "lower"], description="Bollinger Band band")
        str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Bollinger Band price_type")
 
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
        period_check(value["period"])
        param_key_check(value, key_standard)
        float_check(value["numSTD"], description="Band Width numSTD")
        str_check(value["price_type"], values=["Open", "High", "Low", "Close", "Typical"], description="Band Width price_type")

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
        param_key_check(value, key_standard)
        period_check(value["period"])
        str_check(value["channel"], values=channels, description="Donchian Channel channel")

        return value


class MAD(AbstractIndicatorModel):
    name: str = "MAD"
    params: dict = {"fastSMA_period": 21, "slowSMA_period": 200}
    needs_comp: bool = True
    valid_comps: list = ["PRICE", "LEVEL"]

    @validator("params")
    def param_check(cls, value):
        key_standard = ["fastSMA_period", "slowSMA_period"]
        param_key_check(value, key_standard)
        period_check(value["fastSMA_period"])
        period_check(value["slowSMA_period"])

        if value["fastSMA_period"] >= value["slowSMA_period"]:
            raise ValueError(f"fastSMA_period must be < slowSMA_period")

        return value