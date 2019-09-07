curl -XPOST  http://127.0.0.1:5500/add_job -H 'Content-Type: application/json' -d '{ "func":"spider.feixiaohao_spider.collect", "args":[], "trigger":{ "type": "cron", "day_of_week": "*", "hour": "1", "minute": "1", "second": "1" }}'

curl http://127.0.0.1:5500/job_list
