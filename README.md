### TAS = Trading Analytics Sytem

### Django / VueJs

### Link util
    https://pypi.org/project/Backtesting/
    https://github.com/glassnode/glassnode-api-python-client
    https://github.com/jesse-ai/jesse

### Run project
    - make build
    - make up

### Crontab Taapi

    * * * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '1m'
    */5 * * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '5m'
    */15 * * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '15m'
    */30 * * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '30m'
    0 * * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '1h'
    0 */2 * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '2h'
    0 */4 * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '4h'
    0 */8 * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '8h'
    0 */12 * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '12h'
    0 1 * * *  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '1d'
    0 0 * * 0  /home/tas/venv/bin/python3 /home/tas/manage.py taapiRecordData --tf '1w'
