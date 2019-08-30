# coding=utf-8

exchanges = {
    "binance":{
        "period":{
            "1min":"1m",
            "3min":"3m",
            "5min":"5m",
            "10min":"",
            "15min":"15m",
            "30min":"30m",
            "1hour":"1h",
            "2hour":"2h",
            "3hour":"",
            "4hour":"4h",
            "6hour":"6h",
            "8hour":"8h",
            "12hour":"12h",
            "1day":"1d",
            "3day":"3d",
            "1week":"1w",
            "2week":"",
            "1month":"1M"
        },
        "api":{
            "markets":"https://www.binance.com/exchange/public/product",
            "ticker":"https://api.binance.com/api/v1/ticker/24hr?symbol=%s",
            "depth":"https://api.binance.com/api/v1/depth?symbol=%s&limit=%s",
            "kline":"https://api.binance.com/api/v1/klines?symbol=%s&interval=%s&limit=%s"
        }
    },
    "huobi":{
        "period":{
            "1min":"1min",
            "3min":"3min",
            "5min":"",
            "10min":"",
            "15min":"15min",
            "30min":"30min",
            "1hour":"60min",
            "2hour":"",
            "3hour":"",
            "4hour":"4hour",
            "6hour":"",
            "8hour":"",
            "12hour":"",
            "1day":"1day",
            "3day":"",
            "1week":"1week",
            "2week":"",
            "1month":"1mon"
        },
        "api":{
            "markets":"https://api.huobi.pro/v1/common/symbols",
            "ticker":"https://api.huobi.pro/market/detail/merged?symbol=%s",
            "depth":"https://api.huobi.pro/market/depth?symbol=%s&type=%s",
            "kline":"https://api.huobi.pro/market/history/kline?symbol=%s&period=%s&size=%s"
        }
    },
    "okex":{
        "period":{
            "1min":"1min",
            "3min":"3min",
            "5min":"5min",
            "10min":"",
            "15min":"15min",
            "30min":"30min",
            "1hour":"1hour",
            "2hour":"2hour",
            "3hour":"",
            "4hour":"4hour",
            "6hour":"6hour",
            "8hour":"",
            "12hour":"12hour",
            "1day":"1day",
            "3day":"3day",
            "1week":"1week",
            "2week":"",
            "1month":""
        },
        "api":{
            "markets":"https://www.okex.com/v2/spot/markets/products",
            "ticker":"https://www.okex.com/api/v1/ticker.do?symbol=%s",
            "depth":"https://www.okex.com/api/v1/depth.do?symbol=%s&size=%s",
            "kline":"https://www.okex.com/api/v1/kline.do?symbol=%s&type=%s&size=%s"
        }
    },
    "bitfinex":{
        "period":{
            "1min":"1m",
            "3min":"",
            "5min":"5m",
            "10min":"",
            "15min":"15m",
            "30min":"30m",
            "1hour":"1h",
            "2hour":"",
            "3hour":"3h",
            "4hour":"",
            "6hour":"6h",
            "8hour":"",
            "12hour":"12h",
            "1day":"1D",
            "3day":"",
            "1week":"7D",
            "2week":"14D",
            "1month":"1M"
        },
        "api":{
            "markets":"https://api.bitfinex.com/v1/symbols",
            "ticker":"https://api.bitfinex.com/v2/ticker/%s",
            "depth":"",
            "kline":"https://api.bitfinex.com/v2/candles/trade:%s:%s/hist?limit=%s"
        }
    },
    "zb":{
        "period":{
            "1min":"1min",
            "3min":"3min",
            "5min":"5min",
            "15min":"15min",
            "10min":"",
            "30min":"30min",
            "1hour":"1hour",
            "2hour":"2hour",
            "3hour":"",
            "4hour":"4hour",
            "6hour":"6hour",
            "8hour":"",
            "12hour":"12hour",
            "1day":"1day",
            "3day":"3day",
            "1week":"1week",
            "2week":"",
            "1month":""
        },
        "api":{
            "markets":"http://api.zb.cn/data/v1/markets",
            "ticker":"http://api.zb.cn/data/v1/ticker?market=%s",
            "depth":"http://api.zb.cn/data/v1/depth?market=%s&size=%s",
            "kline":"http://api.zb.cn/data/v1/kline?market=%s&type=%s&size=%s"
        }
    },
    "bittrex":{
        "period":{
            "1min":"1min",
            "3min":"3min",
            "5min":"5min",
            "15min":"15min",
            "10min":"",
            "30min":"30min",
            "1hour":"1hour",
            "2hour":"2hour",
            "3hour":"",
            "4hour":"4hour",
            "6hour":"6hour",
            "8hour":"",
            "12hour":"12hour",
            "1day":"1day",
            "3day":"3day",
            "1week":"1week",
            "2week":"",
            "1month":""
        },
        "api":{
            "markets":"https://bittrex.com/api/v1.1/public/getmarkets",
            "ticker":"https://bittrex.com/api/v1.1/public/getticker?market=%s",
            "depth":"",
            "kline":""
        }
    },
    "gateio":{
        "period":{
            "1min":"60",
            "3min":"",
            "5min":"300",
            "10min":"600",
            "15min":"900",
            "30min":"1800",
            "1hour":"3600",
            "2hour":"7200",
            "3hour":"10800",
            "4hour":"14400",
            "6hour":"21600",
            "8hour":"28800",
            "12hour":"43200",
            "1day":"86400",
            "3day":"259200",
            "1week":"604800",
            "2week":"",
            "1month":""
        },
        "api":{
            "markets":"https://data.gateio.io/api2/1/pairs",
            "ticker":"https://data.gateio.io/api2/1/ticker/%s",
            "depth":"https://data.gateio.io/api2/1/orderBook/%s",
            "kline":"https://data.gateio.io/api2/1/candlestick2/%s?group_sec=%s&range_hour=%s"
        }
    }
}