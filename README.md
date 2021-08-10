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
    
    service --status-all

    gunicorn

         nano /etc/systemd/system/daphne.service
         systemctl enable daphne
         systemctl stop daphne
         systemctl status daphne

        # Check log
            
            journalctl -u daphne.service -f

    balanceuserupdate
        
        nano /etc/systemd/system/balanceuserupdate.service
        systemctl enable balanceuserupdate
        systemctl stop balanceuserupdate
        systemctl status balanceuserupdate

        # Check log
            journalctl -u balanceuserupdate.service -f
    
    runnerbacktesting
        
        nano /etc/systemd/system/runnerbacktesting.service

        systemctl enable runnerbacktesting
        systemctl stop runnerbacktesting
        systemctl status runnerbacktesting

        # Check log
            journalctl -u runnerbacktesting.service -f

    runnerbot
        
        sudo nano /etc/systemd/system/runnerbot.service

        systemctl enable runnerbot
        systemctl stop runnerbot
        systemctl status runnerbot

        # Check log
            journalctl -u runnerbot.service -f
    
    websocketstream

        nano /etc/systemd/system/websocketstream.service

        systemctl enable websocketstream
        systemctl stop websocketstream
        systemctl status websocketstream

        # Check log
            journalctl -u websocketstream.service -f

## Tuning

    Tuning postgres 13 link

        https://pgtune.leopard.in.ua/#/
