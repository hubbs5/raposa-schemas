import common

common.importPath()

from raposa_schemas import schemas

class ATRSchemaTest:

    def testValidATRSchema(self):
        atr_sizing_dict = {
            "period": 50,
            "risk_coefficient": 3,
            "max_position_risk_frac": 0.5
        }

        pos_sizing = schemas.ATRSizing(**atr_sizing_dict)

    def testInvalidATRSchema(self):
        atr_sizing_dict = {
            "period": 50,
            "risk_coefficient": 3,
            "max_position_risk_frac": 1.5
        }

        pos_sizing = schemas.ATRSizing(**atr_sizing_dict)