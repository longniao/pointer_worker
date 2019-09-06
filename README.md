# pointer_worker

```
# https://github.com/mrjbq7/ta-lib
brew install ta-lib
pip install TA-Lib
```

```
# cron定时调度（某一定时时刻执行）
{
    "func":"spider.feixiaohao_spider.collect",
    "args":[],
    "trigger":{
        "type": "cron",
        "day_of_week": "*",
        "hour": "*",
        "minute": "*",
        "second": "1"
    }
}

# interval 间隔调度（每隔多久执行）
{
    "func":"spider.feixiaohao_spider.collect",
    "args":[],
    "trigger": "interval",
    "seconds": 15
}

# date 定时调度（作业只会执行一次）
{
    "func":"spider.feixiaohao_spider.collect",
    "args":["20180101", "20180201"],
    "trigger": "date",
    "run_date":"2019-09-06 15:39:40"
}
```