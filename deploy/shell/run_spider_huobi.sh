#! /bin/bash
cd /data/wwwroot/pointer_spider

export WORKON_HOME=/home/work/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source /usr/local/bin/virtualenvwrapper.sh

source /home/work/.virtualenvs/python3/bin/activate
python run.py huobi