import pytest
import traceback
from copy import deepcopy

from raposa_schemas.risk_management_schemas import *

class RiskManagementBaseModel:

    def catch_invalid_schema(self, new_params):
        params = deepcopy(self.params)
        params.update(new_params)
        try:
            out = self.schema(params=params)
            failure = False
        except:
            out = traceback.format_exc()
            failure = True

        return failure, out

    def _test_valid_schema(self, test_params=None, 
                           test_deprecated_param: str=None):
        params = deepcopy(self.params)
        if test_params is not None:
            params.update(test_params)
        if test_deprecated_param is not None:
            del params[test_deprecated_param]
        
        try:
            out = self.schema(params=params)
            success = True
        except:
            out = traceback.format_exc()
            success = False

        assert success, f"{out}"

class TestATRSizing(RiskManagementBaseModel):
    schema = ATRSizing
    params = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "risk_cap": True
    }

    @pytest.mark.parametrize("max_position_risk_frac", [0.01, 1])
    def test_valid_schema(self, max_position_risk_frac):
        self._test_valid_schema({"max_position_risk_frac": max_position_risk_frac})

    def test_deprecated_valid_schema(self):
        self._test_valid_schema(test_deprecated_param="risk_cap")

    @pytest.mark.parametrize("max_position_risk_frac", [-1, 0, 2, "k", None])
    def test_invalid_max_position_risk_frac(self, max_position_risk_frac):
        '''
        0 < max_position_risk_frac <= 1
        '''
        failure, out = self.catch_invalid_schema({"max_position_risk_frac": max_position_risk_frac})
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    @pytest.mark.parametrize("period", [-1, 0, "k", None])
    def test_invalid_period(self, period):
        '''
        period must be > 0
        '''

        failure, out = self.catch_invalid_schema({"period": period})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("risk_coefficient", [-1, 0, "k", None])
    def test_invalid_risk_coefficient(self, risk_coefficient):
        '''
        risk_coefficient must be > 0
        '''

        failure, out = self.catch_invalid_schema({"risk_coefficient": risk_coefficient})
        
        assert failure, f"{out}"


class TestVolSizing(RiskManagementBaseModel):
    schema = VOLATILITYSizing
    params = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "risk_cap": True
    }

    @pytest.mark.parametrize("max_position_risk_frac", [0.01, 1])
    def test_valid_schema(self, max_position_risk_frac):
        self._test_valid_schema({"max_position_risk_frac": max_position_risk_frac})

    def test_old_valid_schema(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        self._test_valid_schema(test_deprecated_param="risk_cap")

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    @pytest.mark.parametrize("max_position_risk_frac", [-1, 0, 2, "l", None])
    def test_invalid_max_position_risk_frac(self, max_position_risk_frac):
        '''
        0 < max_position_risk_frac <= 1
        '''
        failure, out = self.catch_invalid_schema({"max_position_risk_frac": max_position_risk_frac})

        assert failure, f"max_position_risk_frac lower bound not being enforced:\n{out}"

    @pytest.mark.parametrize("period", [-1, 0, "l", None])
    def test_invalid_period(self, period):
        '''
        period must be > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("risk_coefficient", [-1, 0, "k", None])
    def test_invalid_risk_coef(self, risk_coefficient):
        '''
        risk_coefficient must be > 0
        '''
        failure, out = self.catch_invalid_schema({"risk_coefficient": risk_coefficient})
        
        assert failure, f"{out}"


class TestTurtleUnitSizing(RiskManagementBaseModel):
    schema = TurtleUnitSizing
    params = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "num_turtle_units": 1,
        "risk_cap": True
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    def test_old_valid_schema(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        self._test_valid_schema(test_deprecated_param="risk_cap")


    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    @pytest.mark.parametrize("max_position_risk_frac", [-1, 0, 2])
    def test_invalid_max_position_risk_frac(self, max_position_risk_frac):
        '''
        0 < max_position_risk_frac <= 1
        '''
        failure, out = self.catch_invalid_schema({"max_position_risk_frac": max_position_risk_frac})
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    @pytest.mark.parametrize("period", [-1, 0, "l", None])
    def test_invalid_period(self, period):
        '''
        period must be > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("risk_coefficient", [-1, 0, "l", None])
    def test_invalid_risk_coefficient(self, risk_coefficient):
        '''
        risk_coefficient must be > 0
        '''
        failure, out = self.catch_invalid_schema({"risk_coefficient": risk_coefficient})
        
        assert failure, f"{out}"


class TestTurtlePyramiding(RiskManagementBaseModel):
    schema = TurtlePyramiding
    params = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "max_num_entry_points": 1,
        "delta_N_frac": 0.2,
        "stop_price_N_frac": -2.0,
        "risk_cap": True
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    def test_old_valid_schema(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        self._test_valid_schema(test_deprecated_param="risk_cap")

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    @pytest.mark.parametrize("max_position_risk_frac", [-1, 0, 2, "l", None])
    def test_invalid_max_position_risk_frac(self, max_position_risk_frac):
        '''
        0 < max_position_risk_frac <= 1
        '''
        failure, out = self.catch_invalid_schema({"max_position_risk_frac": max_position_risk_frac})
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    @pytest.mark.parametrize("period", [-1, 0, "l", None])
    def test_invalid_period(self, period):
        '''
        period must be > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("risk_coefficient", [-1, 0, "l", None])
    def test_invalid_risk_coefficient(self, risk_coefficient):
        '''
        risk_coefficient must be > 0
        '''
        failure, out = self.catch_invalid_schema({"risk_coefficient": risk_coefficient})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("stop_price_N_frac", ["x", None])
    def test_invalid_stop_price_N_frac_type(self, stop_price_N_frac):
        '''
        stop_price_N_frac must be a number
        '''
        failure, out = self.catch_invalid_schema({"stop_price_N_frac": stop_price_N_frac})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("delta_N_frac", [-1, 0, None, "X"])
    def testInvalidSchema5(self, delta_N_frac):
        '''
        0 < delta_N_frac <= 1
        '''
        failure, out = self.catch_invalid_schema({"delta_N_frac": delta_N_frac})
        
        assert failure, f"{out}"

    @pytest.mark.parametrize("max_num_entry_points", [-1, 0, None, "X"])
    def test_invalid_max_num_entry_points(self, max_num_entry_points):
        '''
        max_num_entry_points must be an integer > 0
        '''
        failure, out = self.catch_invalid_schema({"max_num_entry_points": max_num_entry_points})

        assert failure, f"{out}"