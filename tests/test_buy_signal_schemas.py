import pytest
import traceback
from copy import deepcopy

from raposa_schemas import schemas as schemas
from raposa_schemas import indicator_schemas as ischemas

class BuySignalBaseModel:

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


def test_valid_comp_indicator():
    indicator = ischemas.SMA()
    comp_indicator = ischemas.SMA()

    signal = schemas.Signal(
        indicator=indicator,
        comp_indicator=comp_indicator,
        rel="leq",
        short=False
    )

    assert signal.indicator is not None
    assert signal.comp_indicator is not None
    assert signal.comp_indicator["name"] in signal.indicator["valid_comps"]