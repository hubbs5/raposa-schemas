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
            "start_date": "2018-01-01",
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "instruments": ["TSLA"],
            "account_size": 5000,
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "rebalance_frequency": 1,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "NoRiskManagement", "params": {}},
        },
    }
    preset2 = {
        "email": "test@test.com",
        "buy_signals": {
            "signals": [
                {
                    "rel": "geq",
                    "short": False,
                    "indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Close"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                    "comp_indicator": {
                        "name": "SMA",
                        "params": {"period": 20},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "rel": "leq",
                    "short": False,
                    "indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Close"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                    "comp_indicator": {
                        "name": "SMA",
                        "params": {"period": 100},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                }
            ]
        },
        "strategy_settings": {
            "end_date": "2020-12-31",
            "init_date": "",
            "start_date": "2019-01-01",
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "instruments": ["ABT", "ABBV", "HCA"],
            "account_size": 15000,
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "rebalance_frequency": 1,
            "position_sizing_strategy": {"name": "NoRiskManagement", "params": {}},
            "position_management_strategy": {
                "name": "ATRSizing",
                "params": {
                    "period": 15,
                    "risk_coefficient": 0.9,
                    "max_position_risk_frac": 0.15,
                },
            },
        },
    }

    preset3 = {
        "email": "test@test.com",
        "buy_signals": {
            "signals": [
                {
                    "rel": "lt",
                    "short": False,
                    "indicator": {
                        "name": "ATR",
                        "params": {"period": 15, "multiple": 1.2},
                        "needs_comp": True,
                        "valid_comps": ["ATR"],
                    },
                    "comp_indicator": {
                        "name": "ATR",
                        "params": {"period": 25, "multiple": 2.5},
                        "needs_comp": True,
                        "valid_comps": ["ATR"],
                    },
                }
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "rel": "lt",
                    "short": False,
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 4},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "EMA",
                        "params": {"period": 10},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                }
            ]
        },
        "strategy_settings": {
            "end_date": "2021-12-31",
            "init_date": "",
            "start_date": "2020-01-01",
            "trade_days": ["wed", "tue", "thu"],
            "instruments": ["SEDG"],
            "account_size": 10000,
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 1,
            "rebalance_frequency": 3,
            "position_sizing_strategy": {
                "name": "VOLATILITYSizing",
                "params": {
                    "period": 12,
                    "risk_coefficient": 2,
                    "max_position_risk_frac": 0.15,
                },
            },
            "position_management_strategy": {"name": "NoRiskManagement", "params": {}},
        },
    }

    preset4 = {
        "email": "test@test.com",
        "buy_signals": {
            "signals": [
                {
                    "rel": "lt",
                    "short": False,
                    "indicator": {
                        "name": "VOLATILITY",
                        "params": {"period": 30, "multiple": 1.5},
                        "needs_comp": True,
                        "valid_comps": ["VOLATILITY", "LEVEL"],
                    },
                    "comp_indicator": {
                        "name": "VOLATILITY",
                        "params": {"period": 15, "multiple": 1.5},
                        "needs_comp": True,
                        "valid_comps": ["VOLATILITY", "LEVEL"],
                    },
                },
                {
                    "rel": "gt",
                    "short": False,
                    "indicator": {
                        "name": "PRICE",
                        "params": {"price_type": "Close"},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                    "comp_indicator": {
                        "name": "EMA",
                        "params": {"period": 26},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                },
            ]
        },
        "sell_signals": {
            "signals": [
                {
                    "rel": "lt",
                    "short": False,
                    "indicator": {
                        "name": "EMA",
                        "params": {"period": 12},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                    "comp_indicator": {
                        "name": "EMA",
                        "params": {"period": 26},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "PRICE"],
                    },
                }
            ]
        },
        "strategy_settings": {
            "end_date": "2022-12-31",
            "init_date": "",
            "start_date": "2021-01-01",
            "trade_days": ["tue", "wed", "thu", "fri"],
            "instruments": ["AAPL", "AMZN", "NFLX", "GOOGL", "META"],
            "account_size": 30000,
            "rebalance_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 4,
            "rebalance_frequency": 4,
            "position_sizing_strategy": {
                "name": "TurtleUnitSizing",
                "params": {
                    "period": 60,
                    "num_turtle_units": 5,
                    "risk_coefficient": 4,
                    "max_position_risk_frac": 0.08,
                },
            },
            "position_management_strategy": {"name": "EqualAllocation", "params": {}},
        },
    }

    if bot_number == 1:
        return preset1
    elif bot_number == 2:
        return preset2
    elif bot_number == 3:
        return preset3
    elif bot_number == 4:
        return preset4
