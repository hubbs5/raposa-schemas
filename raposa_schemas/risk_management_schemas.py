from warnings import warn
from abc import abstractmethod, ABC
from pydantic import BaseModel, validator, Field
from typing import List, Type, Union, Optional, Dict, Any

from . import validators as v


class AbstractRiskManagementModel(BaseModel, ABC):
    name: str = Field(..., description="Name of the risk management module.")
    params: dict = Field(..., description="Parameters for the risk management module.")

    @abstractmethod
    def param_check(self):
        raise NotImplementedError

class NoRiskManagement(AbstractRiskManagementModel):
    name: str = "NoRiskManagement"
    params: dict = {}

    def param_check(self):
        pass


class EqualAllocation(AbstractRiskManagementModel):
    name: str = "EqualAllocation"
    params: dict = {}

    def param_check(self):
        pass

class VOLATILITYSizing(AbstractRiskManagementModel):
    name: str = "VOLATILITYSizing"
    params: dict = {
        "period": 252,
        "risk_coefficient": 1,
        "max_position_risk_frac": 0.02,
        "risk_cap": False
    }
    # param period bound >= 2 and < 1000 for min lags and max lags as well
    # risk coefficient: (0,10) but not quite 0
    # max_position risk fraction (0,1) do not include 0
    @validator("params")
    def param_check(cls, value):
        key_standard = [
            "period", 
            "risk_coefficient", 
            "max_position_risk_frac", 
            "risk_cap"
        ]
        new_key = ["risk_cap"]
        v.param_key_check(value, key_standard, deprecation_exception=new_key)
        v.period_check(value["period"], min=2, max=1000)
        v.float_check(value["risk_coefficient"], min=0, max=10)
        v.float_check(value["max_position_risk_frac"], min=0, max=1.001)
        if "risk_cap" not in value.keys():
            value["risk_cap"] = False
        v.bool_check(value["risk_cap"])

        return value


class ATRSizing(AbstractRiskManagementModel):
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
    def param_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "risk_cap"
            ]
        deprecated = ["risk_cap"]
        v.param_key_check(value, key_standard, deprecation_exception=deprecated)
        v.period_check(value["period"], min=2, max=1000)
        v.float_check(value["risk_coefficient"], description="ATR Sizing risk coefficient", min=0, max=10)
        v.float_check(value["max_position_risk_frac"], description="ATR Sizing max position risk fraction", min=0, max=1.001)
        if "risk_cap" not in value.keys():
            value["risk_cap"] = False

        v.bool_check(value["risk_cap"])

        return value


class TurtleUnitSizing(AbstractRiskManagementModel):
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
    def param_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "num_turtle_units",
            "risk_cap",
        ]
        new_key = ["risk_cap"]
        v.param_key_check(value, key_standard, deprecation_exception=new_key)
        v.period_check(value["period"], min=2, max=1000)
        v.float_check(value["risk_coefficient"], description="ATR Sizing risk coefficient", min=0, max=10)
        v.float_check(value["max_position_risk_frac"], description="ATR Sizing max position risk fraction", min=0, max=1.001)
        v.int_check(value["num_turtle_units"], description="Turtle Sizing number of turtle units", min=0, max=1000)
        if "risk_cap" not in value.keys():
            value["risk_cap"] = False

        v.bool_check(value["risk_cap"])
        
        return value


class TurtlePyramiding(AbstractRiskManagementModel):
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
    def param_check(cls, value):
        key_standard = [
            "period",
            "risk_coefficient",
            "max_position_risk_frac",
            "max_num_entry_points",
            "delta_N_frac",
            "stop_price_N_frac",
            "risk_cap"
        ]
        new_key = ["risk_cap"]
        v.param_key_check(value, key_standard, deprecation_exception=new_key)
        v.period_check(value["period"], min=2, max=1000)
        v.float_check(value["risk_coefficient"], description="ATR Sizing risk coefficient", min=0, max=10)
        v.float_check(value["max_position_risk_frac"], description="ATR Sizing max position risk fraction", min=0, max=1.001)
        v.int_check(value["max_num_entry_points"], description="Turtle Pyramiding number of turtle units", min=0, max=10)
        v.float_check(value["delta_N_frac"], description="Turtle Pyramiding delta N fraction", min=0, max=1.001)
        v.float_check(value["stop_price_N_frac"], description="Turtle Pyramiding stop price N fraction", min=-100)
        if "risk_cap" not in value.keys():
            value["risk_cap"] = False

        v.bool_check(value["risk_cap"])

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