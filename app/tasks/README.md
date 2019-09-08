## spider 数据采集

### feixoahao_spider 非小号

'''
{
  "func":"spider.feixiaohao_spider.collect",
  "args": [],
  "trigger":{
    "type":"cron",
    "day_of_week":"*",
    "hour":"1",
    "minute":"1",
    "second":"1"
  }
}
'''

### gate_spider 采集gate

```
{
  "func": "spider.gate_spider:collect",
  "args": [],
  "trigger": "interval",
  "minutes": 5
}
```

### huobi_spider 采集huobi

```
{
  "func": "spider.huobi_spider:collect",
  "args": [],
  "trigger": "interval",
  "minutes": 5
}
```

### tushare_spider 采集tushare

```
{
  "func": "spider.tushare_spider:collect_kline",
  "args": ['huobi', 'btc', '15min'],
  "trigger": "interval",
  "minutes": 5
}

{
  "func": "spider.tushare_spider:collect_btc_marketcap",
  "args": ['huobi', 'btc', '15min'],
  "trigger":{
        "type":"cron",
        "day_of_week":"*",
        "hour":"1",
        "minute":"1",
        "second":"1"
    }
}
```

## analysor 指标分析

### td_analysor TD指标

```
{
  "id":"do_analyze_init",
  "func":"analysor.td_analysor.do_analyze",
  "args": [99999],
  "trigger": "date",
  "run_date":"2019-09-08 15:33:05"
}

{
  "func":"analysor.td_analysor.do_analyze",
  "args": [50],
  "trigger": "interval",
  "minutes": 1
}
```