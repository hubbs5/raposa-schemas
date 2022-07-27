from copy import copy
import common

common.importPath()

from raposa_schemas import schemas

class TestATRSizing:
    atr_sizing_dict = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "risk_cap": True
    }

    def testValidSchema(self):
        out = None
        try:
            out = schemas.ATRSizing(params=self.atr_sizing_dict)
            success = True
        except:
            success = False

        assert success, f"Valid schema returns error. Have defaults been updated?\n{out}"

    def testOldValidSchema0(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        atr_sizing_dict = copy(self.atr_sizing_dict)
        del atr_sizing_dict["risk_cap"]
        out = None
        success = False
        try:
            out = schemas.ATRSizing(params=atr_sizing_dict)
            # Default is False
            if not out.params["risk_cap"]:
                success = True
        except:
            pass

        assert success, f"Deprecated schema returns error. Is this expected?\n{out}"

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    def testInvalidSchema0(self):
        '''
        max_position_risk_frac <= 1
        '''
        atr_sizing_dict = copy(self.atr_sizing_dict)
        atr_sizing_dict["max_position_risk_frac"] = 10
        out = None

        try:
            out = schemas.ATRSizing(params=atr_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    def testInvalidSchema1(self):
        '''
        max_position_risk_frac > 0
        '''
        atr_sizing_dict = copy(self.atr_sizing_dict)
        atr_sizing_dict["max_position_risk_frac"] = -1
        out = None

        try:
            out = schemas.ATRSizing(params=atr_sizing_dict)
            failure = False
        except:
            failure = True

        assert failure, f"max_position_risk_frac lower bound not being enforced:\n{out}"

    def testInvalidSchema2(self):
        '''
        period must be > 0
        '''
        atr_sizing_dict = copy(self.atr_sizing_dict)
        atr_sizing_dict["period"] = -1
        out = None

        try:
            out = schemas.ATRSizing(params=atr_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema3(self):
        '''
        risk_coefficient must be > 0
        '''
        atr_sizing_dict = copy(self.atr_sizing_dict)
        atr_sizing_dict["risk_coefficient"] = -1
        out = None

        try:
            out = schemas.ATRSizing(params=atr_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"


class TestVolSizing:
    vol_sizing_dict = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "risk_cap": True
    }

    def testValidSchema(self):
        out = None
        try:
            out = schemas.VOLATILITYSizing(params=self.vol_sizing_dict)
            success = True
        except:
            success = False

        assert success, f"Valid schema returns error. Have defaults been updated?\n{out}"

    def testOldValidSchema0(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        vol_sizing_dict = copy(self.vol_sizing_dict)
        del vol_sizing_dict["risk_cap"]
        out = None
        success = False
        try:
            out = schemas.VOLATILITYSizing(params=vol_sizing_dict)
            # Default is False
            if not out.params["risk_cap"]:
                success = True
        except:
            pass

        assert success, f"Deprecated schema returns error. Is this expected?\n{out}"

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    def testInvalidSchema0(self):
        '''
        max_position_risk_frac <= 1
        '''
        vol_sizing_dict = copy(self.vol_sizing_dict)
        vol_sizing_dict["max_position_risk_frac"] = 10
        out = None

        try:
            out = schemas.VOLATILITYSizing(params=vol_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    def testInvalidSchema1(self):
        '''
        max_position_risk_frac > 0
        '''
        vol_sizing_dict = copy(self.vol_sizing_dict)
        vol_sizing_dict["max_position_risk_frac"] = -1
        out = None

        try:
            out = schemas.VOLATILITYSizing(params=vol_sizing_dict)
            failure = False
        except:
            failure = True

        assert failure, f"max_position_risk_frac lower bound not being enforced:\n{out}"

    def testInvalidSchema2(self):
        '''
        period must be > 0
        '''
        vol_sizing_dict = copy(self.vol_sizing_dict)
        vol_sizing_dict["period"] = -1
        out = None

        try:
            out = schemas.VOLATILITYSizing(params=vol_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema3(self):
        '''
        risk_coefficient must be > 0
        '''
        vol_sizing_dict = copy(self.vol_sizing_dict)
        vol_sizing_dict["risk_coefficient"] = -1
        out = None

        try:
            out = schemas.VOLATILITYSizing(params=vol_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"


class TestTurtleUnitSizing:
    turtle_sizing_dict = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "num_turtle_units": 1,
        "risk_cap": True
    }

    def testValidSchema(self):
        out = None
        try:
            out = schemas.TurtleUnitSizing(params=self.turtle_sizing_dict)
            success = True
        except:
            success = False

        assert success, f"Valid schema returns error. Have defaults been updated?\n{out}"

    def testOldValidSchema0(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        turtle_sizing_dict = copy(self.turtle_sizing_dict)
        del turtle_sizing_dict["risk_cap"]
        out = None
        success = False
        try:
            out = schemas.TurtleUnitSizing(params=turtle_sizing_dict)
            # Default is False
            if not out.params["risk_cap"]:
                success = True
        except Exception as e:
            pass

        assert success, f"Deprecated schema returns error. Is this expected?\n{out}"

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    def testInvalidSchema0(self):
        '''
        max_position_risk_frac <= 1
        '''
        turtle_sizing_dict = copy(self.turtle_sizing_dict)
        turtle_sizing_dict["max_position_risk_frac"] = 10
        out = None

        try:
            out = schemas.TurtleUnitSizing(params=turtle_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    def testInvalidSchema1(self):
        '''
        max_position_risk_frac > 0
        '''
        turtle_sizing_dict = copy(self.turtle_sizing_dict)
        turtle_sizing_dict["max_position_risk_frac"] = -1
        out = None

        try:
            out = schemas.TurtleUnitSizing(params=turtle_sizing_dict)
            failure = False
        except:
            failure = True

        assert failure, f"max_position_risk_frac lower bound not being enforced:\n{out}"

    def testInvalidSchema2(self):
        '''
        period must be > 0
        '''
        turtle_sizing_dict = copy(self.turtle_sizing_dict)
        turtle_sizing_dict["period"] = -1
        out = None

        try:
            out = schemas.TurtleUnitSizing(params=turtle_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema3(self):
        '''
        risk_coefficient must be > 0
        '''
        turtle_sizing_dict = copy(self.turtle_sizing_dict)
        turtle_sizing_dict["risk_coefficient"] = -1
        out = None

        try:
            out = schemas.TurtleUnitSizing(params=turtle_sizing_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"


class TestTurtlePyramiding:
    turtle_pyr_dict = {
        "period": 50,
        "risk_coefficient": 3,
        "max_position_risk_frac": 0.5,
        "max_num_entry_points": 1,
        "delta_N_frac": 0.2,
        "stop_price_N_frac": -2.0,
        "risk_cap": True
    }

    def testValidSchema(self):
        out = None
        try:
            out = schemas.TurtlePyramiding(params=self.turtle_pyr_dict)
            success = True
        except:
            success = False

        assert success, f"Valid schema returns error. Have defaults been updated?\n{out}"

    def testOldValidSchema0(self):
        '''
        Test schema created before risk_cap was introduced
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        del turtle_pyr_dict["risk_cap"]
        out = None
        success = False
        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            # Default is False
            if not out.params["risk_cap"]:
                success = True
        except:
            pass

        assert success, f"Deprecated schema returns error. Is this expected?\n{out}"

    # The following tests are looking to ensure the schema breaks as expected
    # and function by changing one of the parameters at a time
    def testInvalidSchema0(self):
        '''
        max_position_risk_frac <= 1
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["max_position_risk_frac"] = 10
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"max_position_risk_frac upper bound not being enforced:\n{out}"

    def testInvalidSchema1(self):
        '''
        max_position_risk_frac > 0
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["max_position_risk_frac"] = -1
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True

        assert failure, f"max_position_risk_frac lower bound not being enforced:\n{out}"

    def testInvalidSchema2(self):
        '''
        period must be > 0
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["period"] = -1
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema3(self):
        '''
        risk_coefficient must be > 0
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["risk_coefficient"] = -1
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema4(self):
        '''
        stop_price_N_frac must be a number
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["stop_price_N_frac"] = "x"
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"

    def testInvalidSchema5(self):
        '''
        delta_N_frac must be a number
        '''
        turtle_pyr_dict = copy(self.turtle_pyr_dict)
        turtle_pyr_dict["delta_N_frac"] = "y"
        out = None

        try:
            out = schemas.TurtlePyramiding(params=turtle_pyr_dict)
            failure = False
        except:
            failure = True
        
        assert failure, f"{out}"