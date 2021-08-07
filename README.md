### TAS = Trading Analytics Sytem

### Django / VueJs

### Link util
    https://pypi.org/project/Backtesting/
    https://github.com/glassnode/glassnode-api-python-client
    https://github.com/jesse-ai/jesse

### Run project

    - make build
    - make up

### CoreUI

    npm install
    npm run serve

### Service

    gunicorn

        sudo nano /etc/systemd/system/gunicorn.service

        # Check log
            
            journalctl -u gunicorn.service -f

    balanceuserupdate
        
        sudo nano /etc/systemd/system/balanceuserupdate.service
        systemctl enable balanceuserupdate
        systemctl status balanceuserupdate
        systemctl status balanceuserupdate.service

        # Check log
            journalctl -u balanceuserupdate.service -f
    
    runnerbot
        
        sudo nano /etc/systemd/system/runnerbot.service
        systemctl enable runnerbot
        systemctl status runnerbot
        systemctl status runnerbot.service

        # Check log
            journalctl -u runnerbot.service -f
    
    websocketstream

        sudo nano /etc/systemd/system/websocketstream.service
        sudo systemctl enable websocketstream
        sudo systemctl status websocketstream

        # Check log
            journalctl -u websocketstream.service -f

## Tuning

    Tuning postgres 13 link

        https://pgtune.leopard.in.ua/#/
