"""
This is a very rudimentary way to create the default bots for
users without accounts. (or who have not saved their bots).

Currently hard-coded. But we could maek it more dynamic.
"""


def get_default_bot(bot_number):
    preset1 = {
        "email": "test@test.com",
        "buy_signals": {
            "signals": [
                {
                    "rel": "leq",
                    "short": False,
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 3},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Close"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "rel": "geq",
                    "short": False,
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 5},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Close"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                }
            ]
        },
        "strategy_settings": {
            "end_date": "2019-12-31",
            "init_date": "",
            "start_date": "2016-01-01",
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "instruments": ["TSLA"],
            "account_size": 10000,
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "rebalance_frequency": 1,
            "position_sizing_strategy": {
                "name": "TurtlePyramiding",
                "params": {
                    "period": 10,
                    "delta_N_frac": 0.5,
                    "risk_coefficient": 0.8,
                    "stop_price_N_frac": -8,
                    "max_num_entry_points": 10,
                    "max_position_risk_frac": 0.5,
                },
            },
            "position_management_strategy": {"name": "EqualAllocation", "params": {}},
        },
    }

    preset2 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "init_date": "2017-10-11",
            "start_date": "2018-01-01",
            "end_date": "2019-12-31",
            "instruments": ["GE"],
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {
                "name": "VOLATILITYSizing",
                "params": {
                    "period": 356,
                    "risk_coefficient": 1,
                    "max_position_risk_frac": 0.04,
                },
            },
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "rebalance_frequency": 1,
        },
        "buy_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 10},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "SMA",
                        "params": {"period": 50},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "rel": "geq",
                    "short": False,
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 30},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "SMA",
                        "params": {"period": 50},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "rel": "geq",
                    "short": False,
                }
            ]
        },
        "email": "test@test.com",
    }

    preset3 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "init_date": "2004-10-11",
            "start_date": "2005-01-01",
            "end_date": "2007-12-31",
            "instruments": ["JPM"],
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "EqualAllocation", "params": {}},
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "rebalance_frequency": 1,
        },
        "buy_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "SMA",
                        "params": {"period": 20},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "EMA",
                        "params": {"period": 50},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "rel": "geq",
                    "short": False,
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "HURST",
                        "params": {"period": 10, "minLags": 2, "maxLags": 20},
                        "needs_comp": True,
                        "valid_comps": ["LEVEL"],
                    },
                    "comp_indicator": {
                        "name": "LEVEL",
                        "params": {"level": 30},
                        "needs_comp": False,
                        "valid_comps": None,
                    },
                    "rel": "lt",
                    "short": False,
                }
            ]
        },
        "email": "test@test.com",
    }

    preset4 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "init_date": "2016-11-21",
            "start_date": "2017-01-01",
            "end_date": "2019-12-31",
            "instruments": ["AMZN"],
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {
                "name": "VOLATILITYSizing",
                "params": {
                    "period": 30,
                    "risk_coefficient": 1,
                    "max_position_risk_frac": 0.02,
                },
            },
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "rebalance_frequency": 1,
        },
        "buy_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "ATRP",
                        "params": {"period": 25, "multiple": 1},
                        "needs_comp": True,
                        "valid_comps": ["PRICE"],
                    },
                    "comp_indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Low"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                    "rel": "lt",
                    "short": False,
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "RSI",
                        "params": {"period": 25},
                        "needs_comp": True,
                        "valid_comps": ["LEVEL"],
                    },
                    "comp_indicator": {
                        "name": "LEVEL",
                        "params": {"level": 30},
                        "needs_comp": False,
                        "valid_comps": None,
                    },
                    "rel": "lt",
                    "short": False,
                }
            ]
        },
        "email": "test@test.com",
    }
    if bot_number == 1:
        return preset1
    elif bot_number == 2:
        return preset2
    elif bot_number == 3:
        return preset3
    elif bot_number == 4:
        return preset4
