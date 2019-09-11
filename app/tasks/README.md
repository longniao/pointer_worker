## 执行脚本

```
curl -XPOST  http://127.0.0.1:5500/add_job -H 'Content-Type: application/json' -d '{ "func":"spider.feixiaohao_spider.collect", "args":[], "trigger":{ "type": "cron", "day_of_week": "*", "hour": "1", "minute": "1", "second": "1" }}'

curl http://127.0.0.1:5500/job_list
```

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
  "func": "spider.gate_spider.collect",
  "args": [],
  "trigger": "interval",
  "minutes": 5
}
```

### huobi_spider 采集huobi

```
{
  "func": "spider.huobi_spider.collect",
  "args": [],
  "trigger": "interval",
  "minutes": 5
}
```

### tushare_spider 采集tushare

```
{
  "func": "spider.tushare_spider.collect_kline",
  "args": ["gateio", "btcusdt", "20130101", "20190909"],
  "trigger": "date",
  "run_date":"2019-09-08 15:33:05"
}
{
  "id":"spider.tushare_spider.collect_kline.date.huobi",
  "func": "spider.tushare_spider.collect_kline",
  "args": ["huobi", "btcusdt", "20130101", "20190909"],
  "trigger": "date",
  "run_date":"2019-09-08 15:33:05"
}


{
  "func": "spider.tushare_spider.collect_kline",
  "args": ["huobi", "btcusdt"],
  "trigger":{
        "type":"cron",
        "day_of_week":"*",
        "hour":"1",
        "minute":"5",
        "second":"1"
    }
}
{
  "id":"spider.tushare_spider.collect_kline.cron.huobi",
  "func": "spider.tushare_spider.collect_kline",
  "args": ["huobi", "btcusdt"],
  "trigger":{
        "type":"cron",
        "day_of_week":"*",
        "hour":"1",
        "minute":"5",
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

{
  "func":"analysor.kdj_analysor.do_analyze",
  "args": [50],
  "trigger": "interval",
  "minutes": 1
}
```
