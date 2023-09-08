import pytest
import traceback
from copy import deepcopy

from raposa_schemas import schemas

class IndicatorBaseModel:

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

    def _test_valid_schema(self, test_params=None):
        if test_params is not None:
            params = deepcopy(self.params)
            params.update(test_params)
        else:
            params = self.params
        try:
            out = self.schema(params=params)
            success = True
        except:
            out = traceback.format_exc()
            success = False

        assert success, f"{out}"

class TestSMA(IndicatorBaseModel):
    schema = schemas.SMA
    params = {
        "period": 20,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"


class TestEMA(IndicatorBaseModel):
    schema = schemas.EMA
    params = {
        "period": 20,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"


class TestMACD(IndicatorBaseModel):
    schema = schemas.MACD
    params = {
        "fastEMA_period": 12,
        "slowEMA_period": 26,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("fastEMA_period", [0, -1, "a", None])
    def test_invalid_fastEMA_period(self, fastEMA_period):
        '''
        fastEMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"fastEMA_period": fastEMA_period})
        assert failure, f"fastEMA_period = {fastEMA_period} should be invalid\n{out}"

    @pytest.mark.parametrize("slowEMA_period", [0, -1, "a", None])
    def test_invalid_slowEMA_period(self, slowEMA_period):
        '''
        slowEMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"slowEMA_period": slowEMA_period})
        assert failure, f"slowEMA_period = {slowEMA_period} should be invalid\n{out}"


class TestMACDSignal(IndicatorBaseModel):
    schema = schemas.MACD_SIGNAL
    params = {
        "fastEMA_period": 12,
        "slowEMA_period": 26,
        "signalEMA_period": 9,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("fastEMA_period", [0, -1, "a", None])
    def test_invalid_fastEMA_period(self, fastEMA_period):
        '''
        fastEMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"fastEMA_period": fastEMA_period})
        assert failure, f"fastEMA_period = {fastEMA_period} should be invalid\n{out}"

    @pytest.mark.parametrize("slowEMA_period", [0, -1, "a", None])
    def test_invalid_slowEMA_period(self, slowEMA_period):
        '''
        slowEMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"slowEMA_period": slowEMA_period})
        assert failure, f"slowEMA_period = {slowEMA_period} should be invalid\n{out}"

    @pytest.mark.parametrize("signalEMA_period", [0, -1, "a", None])
    def test_invalid_signal_period(self, signalEMA_period):
        '''
        signal_period > 0
        '''
        failure, out = self.catch_invalid_schema({"signalEMA_period": signalEMA_period})
        assert failure, f"signal_period = {signalEMA_period} should be invalid\n{out}"


class TestRSI(IndicatorBaseModel):
    schema = schemas.RSI
    params = {
        "period": 14,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"


class TestStopPrice(IndicatorBaseModel):
    schema = schemas.STOP_PRICE
    params = {
        "percent_change": 10,
        "trailing": False,
    }

    @pytest.mark.parametrize("trailing", [True, False])
    def test_valid_schema(self, trailing):
        self._test_valid_schema({"trailing": trailing})

    @pytest.mark.parametrize("percent_change", [-100, "a", None])
    def test_invalid_percent_change(self, percent_change):
        '''
        percent_change > -100
        '''
        failure, out = self.catch_invalid_schema({"percent_change": percent_change})
        assert failure, f"stop_price = {percent_change} should be invalid\n{out}"

    @pytest.mark.parametrize("trailing", ["a", None])
    def test_invalid_trailing(self, trailing):
        '''
        trailing = True or False
        '''
        failure, out = self.catch_invalid_schema({"trailing": trailing})
        assert failure, f"trailing = {trailing} should be invalid\n{out}"


class TestATRStopPrice(IndicatorBaseModel):
    schema = schemas.ATR_STOP_PRICE
    params = {
        "period": 14,
        "stop_price_ATR_frac": 3,
        "trailing": False,
    }

    @pytest.mark.parametrize("trailing", [True, False])
    def test_valid_trailing(self, trailing):
        self._test_valid_schema({"trailing": trailing})

    @pytest.mark.parametrize("stop_price_ATR_frac", [-9, 1, 1.6, 8])
    def test_valid_stop_price_ATR_frac(self, stop_price_ATR_frac):
        '''
        stop_price_ATR_frac > 0
        '''
        self._test_valid_schema(
            {"stop_price_ATR_frac": stop_price_ATR_frac})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("stop_price_ATR_frac", [-100, "a", None])
    def test_invalid_stop_price_ATR_frac(self, stop_price_ATR_frac):
        '''
        stop_price_ATR_frac > 0
        '''
        failure, out = self.catch_invalid_schema(
            {"stop_price_ATR_frac": stop_price_ATR_frac})
        assert failure, f"stop_price_ATR_frac = {stop_price_ATR_frac} should be invalid\n{out}"


class TestPrice(IndicatorBaseModel):
    schema = schemas.PRICE
    params = {
        "price_type": "Close"
    }

    @pytest.mark.parametrize("price_type", ["Open", "High", "Low", "Close", "Typical"])
    def test_valid_schema(self, price_type):
        self._test_valid_schema({"price_type": price_type})

    @pytest.mark.parametrize("price_type", ["a", None, "high"])
    def test_invalid_price_type(self, price_type):
        '''
        price_type = "Open", "High", "Low", "Close", "Typical"
        '''
        failure, out = self.catch_invalid_schema({"price_type": price_type})
        assert failure, f"price_type = {price_type} should be invalid\n{out}"


class TestPriceWindow(IndicatorBaseModel):
    schema = schemas.PRICE_WINDOW
    params = {
        "period": 20,
        "max_or_min": "max",
        "price_type": "Close",
    }

    @pytest.mark.parametrize("price_type", ["Open", "High", "Low", "Close", "Typical"])
    def test_valid_price_type(self, price_type):
        self._test_valid_schema({"price_type": price_type})

    @pytest.mark.parametrize("max_or_min", ["max", "min"])
    def test_valid_max_or_min(self, max_or_min):
        self._test_valid_schema({"max_or_min": max_or_min})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("price_type", ["a", None, "high"])
    def test_invalid_price_type(self, price_type):
        '''
        price_type = "Open", "High", "Low", "Close", "Typical"
        '''
        failure, out = self.catch_invalid_schema({"price_type": price_type})
        assert failure, f"price_type = {price_type} should be invalid\n{out}"

    @pytest.mark.parametrize("max_or_min", ["a", None, "high"])
    def test_invalid_max_or_min(self, max_or_min):
        '''
        max_or_min = "max", "min"
        '''
        failure, out = self.catch_invalid_schema({"max_or_min": max_or_min})
        assert failure, f"max_or_min = {max_or_min} should be invalid\n{out}"


class TestATR(IndicatorBaseModel):
    schema = schemas.ATR
    params = {
        "period": 14,
        "multiple": 3,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("multiple", [-9, 0, None])
    def test_invalid_multiple(self, multiple):
        '''
        multiple > 0
        '''
        failure, out = self.catch_invalid_schema({"multiple": multiple})
        assert failure, f"multiple = {multiple} should be invalid\n{out}"


class TestATRP(IndicatorBaseModel):
    schema = schemas.ATRP
    params = {
        "period": 14,
        "multiple": 3,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("multiple", [-9, 0, None])
    def test_invalid_multiple(self, multiple):
        '''
        multiple > 0
        '''
        failure, out = self.catch_invalid_schema({"multiple": multiple})
        assert failure, f"multiple = {multiple} should be invalid\n{out}"


class TestLevel(IndicatorBaseModel):
    schema = schemas.LEVEL
    params = {"level": 50}

    @pytest.mark.parametrize("level", [0, 100, 50])
    def test_valid_schema(self, level):
        self._test_valid_schema({"level": level})

    @pytest.mark.parametrize("level", [-1, 101, "a", None])
    def test_invalid_level(self, level):
        '''
        0 <= level <= 100
        '''
        failure, out = self.catch_invalid_schema({"level": level})
        assert failure, f"level = {level} should be invalid\n{out}"


class TestBoolean(IndicatorBaseModel):
    schema = schemas.BOOLEAN
    params = {"boolean": True}

    @pytest.mark.parametrize("boolean", [True, False])
    def test_valid_schema(self, boolean):
        self._test_valid_schema({"boolean": boolean})

    @pytest.mark.parametrize("boolean", ["a", None])
    def test_invalid_boolean(self, boolean):
        '''
        boolean = True or False
        '''
        failure, out = self.catch_invalid_schema({"boolean": boolean})
        assert failure, f"boolean = {boolean} should be invalid\n{out}"


class TestVolatility(IndicatorBaseModel):
    schema = schemas.VOLATILITY
    params = {
        "period": 14,
        "multiple": 3,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"


class TestPSAR(IndicatorBaseModel):
    schema = schemas.PSAR
    params = {
        "type_indicator": "reversal_toUptrend",
        "init_acceleration_factor": 0.02,
        "acceleration_factor_step": 0.02,
        "max_acceleration_factor": 0.2,
        "period": 2,
    }

    @pytest.mark.parametrize("type_indicator", ["reversal_toUptrend", "reversal_toDowntrend"])
    def test_valid_type_indicator(self, type_indicator):
        self._test_valid_schema({"type_indicator": type_indicator})

    @pytest.mark.parametrize("init_acceleration_factor", [0.02, 0.2])
    def test_valid_init_acceleration_factor(self, init_acceleration_factor):
        self._test_valid_schema({"init_acceleration_factor": init_acceleration_factor})

    @pytest.mark.parametrize("acceleration_factor_step", [0.02, 0.2])
    def test_valid_acceleration_factor_step(self, acceleration_factor_step):
        self._test_valid_schema({"acceleration_factor_step": acceleration_factor_step})

    @pytest.mark.parametrize("max_acceleration_factor", [0.02, 0.2])
    def test_valid_max_acceleration_factor(self, max_acceleration_factor):
        self._test_valid_schema({"max_acceleration_factor": max_acceleration_factor})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("type_indicator", ["a", None])
    def test_invalid_type_indicator(self, type_indicator):
        '''
        type_indicator = "reversal_toUptrend", "reversal_toDowntrend"
        '''
        failure, out = self.catch_invalid_schema({"type_indicator": type_indicator})
        assert failure, f"type_indicator = {type_indicator} should be invalid\n{out}"

    @pytest.mark.parametrize("init_acceleration_factor", [-1, 0, "a", None])
    def test_invalid_init_acceleration_factor(self, init_acceleration_factor):
        '''
        0 < init_acceleration_factor <= 0.2
        '''
        failure, out = self.catch_invalid_schema({"init_acceleration_factor": init_acceleration_factor})
        assert failure, f"init_acceleration_factor = {init_acceleration_factor} should be invalid\n{out}"

    @pytest.mark.parametrize("acceleration_factor_step", [-1, 0, "a", None])
    def test_invalid_acceleration_factor_step(self, acceleration_factor_step):
        '''
        0 < acceleration_factor_step <= 0.2
        '''
        failure, out = self.catch_invalid_schema({"acceleration_factor_step": acceleration_factor_step})
        assert failure, f"acceleration_factor_step = {acceleration_factor_step} should be invalid\n{out}"

    @pytest.mark.parametrize("max_acceleration_factor", [-1, 0, "a", None])
    def test_invalid_max_acceleration_factor(self, max_acceleration_factor):
        '''
        0 < max_acceleration_factor <= 0.2
        '''
        failure, out = self.catch_invalid_schema({"max_acceleration_factor": max_acceleration_factor})
        assert failure, f"max_acceleration_factor = {max_acceleration_factor} should be invalid\n{out}"


class TestHurst(IndicatorBaseModel):
    schema = schemas.HURST
    params = {
        "period": 20,
        "minLags": 2,
        "maxLags": 20,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("minLags", [0, -1, "a", None])
    def test_invalid_min_lags(self, minLags):
        '''
        minLags > 0
        '''
        failure, out = self.catch_invalid_schema({"minLags": minLags})
        assert failure, f"minLags = {minLags} should be invalid\n{out}"

    @pytest.mark.parametrize("maxLags", [0, -1, "a", None])
    def test_invalid_max_lags(self, maxLags):
        '''
        maxLags > 0
        '''
        failure, out = self.catch_invalid_schema({"maxLags": maxLags})
        assert failure, f"maxLags = {maxLags} should be invalid\n{out}"

    @pytest.mark.parametrize("minLags, maxLags", [(30, 2), (20, 20)])
    def test_invalid_lag_comparison(self, minLags, maxLags):
        '''
        minLags < maxLags
        '''
        failure, out = self.catch_invalid_schema({"minLags": minLags, "maxLags": maxLags})
        assert failure, f"minLags = {minLags}, maxLags = {maxLags} should be invalid\n{out}"


class TestBollingerBands(IndicatorBaseModel):
    schema = schemas.BOLLINGER
    params = {
        "period": 20,
        "numSTD": 2,
        "band": "upper",
        "price_type": "Close",
    }

    @pytest.mark.parametrize("price_type", ["Open", "High", "Low", "Close", "Typical"])
    def test_valid_price_type(self, price_type):
        self._test_valid_schema({"price_type": price_type})

    @pytest.mark.parametrize("band", ["upper", "lower", "middle"])
    def test_valid_band(self, band):
        self._test_valid_schema({"band": band})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("numSTD", [0, -1, "a", None])
    def test_invalid_std_devs(self, numSTD):
        '''
        numSTD > 0
        '''
        failure, out = self.catch_invalid_schema({"numSTD": numSTD})
        assert failure, f"numSTD = {numSTD} should be invalid\n{out}"

    @pytest.mark.parametrize("price_type", ["a", None, "high"])
    def test_invalid_price_type(self, price_type):
        '''
        price_type = "Open", "High", "Low", "Close", "Typical"
        '''
        failure, out = self.catch_invalid_schema({"price_type": price_type})
        assert failure, f"price_type = {price_type} should be invalid\n{out}"


class TestBandWidth(IndicatorBaseModel):
    schema = schemas.BAND_WIDTH
    params = {
        "period": 20,
        "numSTD": 2,
        "price_type": "Close",
    }

    @pytest.mark.parametrize("price_type", ["Open", "High", "Low", "Close", "Typical"])
    def test_valid_price_type(self, price_type):
        self._test_valid_schema({"price_type": price_type})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("numSTD", [0, -1, "a", None])
    def test_invalid_std_devs(self, numSTD):
        '''
        numSTD > 0
        '''
        failure, out = self.catch_invalid_schema({"numSTD": numSTD})
        assert failure, f"numSTD = {numSTD} should be invalid\n{out}"

    @pytest.mark.parametrize("price_type", ["a", None, "high"])
    def test_invalid_price_type(self, price_type):
        '''
        price_type = "Open", "High", "Low", "Close", "Typical"
        '''
        failure, out = self.catch_invalid_schema({"price_type": price_type})
        assert failure, f"price_type = {price_type} should be invalid\n{out}"


class TestDonchian(IndicatorBaseModel):
    schema = schemas.DONCHIAN
    params = {
        "period": 20,
        "channel": "upper",
    }

    @pytest.mark.parametrize("channel", ["upper", "lower", "middle"])
    def test_valid_channel(self, channel):
        self._test_valid_schema({"channel": channel})

    @pytest.mark.parametrize("period", [0, -1, "a", None])
    def test_invalid_period(self, period):
        '''
        period > 0
        '''
        failure, out = self.catch_invalid_schema({"period": period})
        assert failure, f"period = {period} should be invalid\n{out}"

    @pytest.mark.parametrize("channel", ["a", None, "high"])
    def test_invalid_channel(self, channel):
        '''
        channel = "upper", "lower", "middle"
        '''
        failure, out = self.catch_invalid_schema({"channel": channel})
        assert failure, f"channel = {channel} should be invalid\n{out}"


class TestMAD(IndicatorBaseModel):
    schema = schemas.MAD
    params = {
        "fastSMA_period": 12,
        "slowSMA_period": 26,
    }

    def test_valid_schema(self):
        self._test_valid_schema()

    @pytest.mark.parametrize("fastSMA_period", [0, -1, "a", None])
    def test_invalid_fastSMA_period(self, fastSMA_period):
        '''
        fastSMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"fastSMA_period": fastSMA_period})
        assert failure, f"fastSMA_period = {fastSMA_period} should be invalid\n{out}"

    @pytest.mark.parametrize("slowSMA_period", [0, -1, "a", None])
    def test_invalid_slowSMA_period(self, slowSMA_period):
        '''
        slowSMA_period > 0
        '''
        failure, out = self.catch_invalid_schema({"slowSMA_period": slowSMA_period})
        assert failure, f"slowSMA_period = {slowSMA_period} should be invalid\n{out}"

    @pytest.mark.parametrize("fastSMA_period, slowSMA_period", [(30, 2), (20, 20)])
    def test_invalid_sma_comparison(self, fastSMA_period, slowSMA_period):
        '''
        fastSMA_period < slowSMA_period
        '''
        failure, out = self.catch_invalid_schema({"fastSMA_period": fastSMA_period, "slowSMA_period": slowSMA_period})
        assert failure, f"fastSMA_period = {fastSMA_period}, slowSMA_period = {slowSMA_period} should be invalid\n{out}"
    