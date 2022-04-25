'''
This is a very rudimentary way to create the default bots for
users without accounts. (or who have not saved their bots).

Currently hard-coded. But we could maek it more dynamic.
'''

def get_default_bot(bot_number):
    preset1 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "start_date": "2015-01-01",
            "end_date": "2017-12-31",
            "instruments": ["ABT"],
            "trade_days": ["mon", "tue"],
            "trade_frequency": 1,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "EqualAllocation", "params": {}},
            "rebalance_days": ["fri", "wed", "thu", "tue", "mon"],
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
                        "name": "STOP_PRICE",
                        "params": {"percent_change": -10},
                        "needs_comp": True,
                        "valid_comps": ["PRICE"],
                    },
                    "comp_indicator": {
                        "name": "PRICE",
                        "params": {'price_type': 'High'},
                        "needs_comp": True,
                        "valid_comps": ["SMA", "EMA", "MACD", "ATR"],
                    },
                    "rel": "leq",
                    "short": False,
                }
            ]
        },
        "email": "test@test.com",
    }

    preset2 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "start_date": "2018-01-01",
            "end_date": "2019-12-31",
            "instruments": ["GE"],
            "trade_days": ["mon", "fri"],
            "trade_frequency": 2,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "VOLATILITYSizing",
                                             "params": {
                                                 "period": 356,
                                                 "risk_coefficient": 1,
                                                 "max_position_risk_frac": 0.04,
                                             }},
            "rebalance_days": ["fri", "wed", "thu", "tue", "mon"],
            "rebalance_frequency": 2,
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
            "start_date": "2005-01-01",
            "end_date": "2007-12-31",
            "instruments": ["ATVI"],
            "trade_days": ["mon", "tue", "wed"],
            "trade_frequency": 3,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "VOLATILITYSizing",
                                             "params": {
                                                 "period": 90,
                                                 "risk_coefficient": 0.7,
                                                 "max_position_risk_frac": 0.05,
                                             }},
            "rebalance_days": ["fri", "wed", "thu", "tue", "mon"],
            "rebalance_frequency": 3,
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
                        "name": "SMA",
                        "params": {"period": 10},
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
        "email": "test@test.com",
    }

    preset4 = {
        "strategy_settings": {
            "account_size": 10000.0,
            "start_date": "2017-01-01",
            "end_date": "2019-12-31",
            "instruments": ["AMZN"],
            "trade_days": ["mon", "tue", "wed", "thu", "fri"],
            "trade_frequency": 4,
            "position_sizing_strategy": {"name": "EqualAllocation", "params": {}},
            "position_management_strategy": {"name": "VOLATILITYSizing",
                                             "params": {
                                                 "period": 30,
                                                 "risk_coefficient": 1,
                                                 "max_position_risk_frac": 0.02,
                                             }},
            "rebalance_days": ["fri", "wed", "thu", "tue", "mon"],
            "rebalance_frequency": 4,
        },
        "buy_signals": {
            "signals": [
                {
                    "indicator": {
                        "name": "SMA",
                        "params": {"period": 30},
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
                        "name": "SMA",
                        "params": {"period": 60},
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
