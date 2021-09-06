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
        systemctl restart runnerbot

        # Check log
            journalctl -u runnerbot.service -f

    runnerclusterbot
        
        sudo nano /etc/systemd/system/runnerclusterbot.service

        systemctl enable runnerclusterbot
        systemctl stop runnerclusterbot
        systemctl status runnerclusterbot
        systemctl restart runnerclusterbot

        # Check log
            journalctl -u runnerclusterbot.service -f    

### Websocket Stream kline

        WebsSocketStreamFutures
    
            nano /etc/systemd/system/websocketstreamfutures.service
    
            systemctl enable websocketstreamfutures
            systemctl stop websocketstreamfutures
            systemctl status websocketstreamfutures
            systemctl restart websocketstreamfutures
    
            # Check log
                journalctl -u websocketstreamfutures.service -f
    
        WebsSocketStreamSpot
    
            nano /etc/systemd/system/websocketstreamspot.service
    
            systemctl enable websocketstreamspot
            systemctl stop websocketstreamspot
            systemctl status websocketstreamspot
            systemctl restart websocketstreamspot
    
            # Check log
                journalctl -u websocketstreamspot.service -f    

## Tuning

    Tuning postgres 13 link

        https://pgtune.leopard.in.ua/#/


# Links
    https://ccxt.pro/
    https://www.npmjs.com/package/redis
    https://gist.github.com/matriphe/87d6f4b4460152e3609e55348f2f8fcc

## Documentazione dizionario Bot
    
    """
    {
        'sleep_func_entry': Funzione della stratrgia di entry che viene valuta per essere eseguita,
        'sleep_func_exit': Funzione della strategia di exit che viene valutata per essere eseguita,
        'taapi': Instanza di taapi per prelevare i dati,
        'symbol': Simbolo da tradare preso dalla strategia,
        'type': Tipologia di strategia long or short,
        'time_frame': Valore timeframe preso dalla strategia,
        'ratio': Valore del ratio presto dalla funzione della strategia,
        'stoploss_value': Valore stoploss preso dalla funzione della strategia,
        'takeprofit_value': Valore dello stop loss preso dalla funzione della strategia,
        'takeprofit': Determina se c'e stato un takeprofit,
        'takeprofit_candle': Valore della candela di takeprofit,
        'stoploss': Determina se c'e stato uno stop loss,
        'stoploss_candle': Valore della candela di stop loss,
        'entry': Determina se è stata trovata un'entry,
        'entry_candle': Candela che viene salvata quando avviene un'entry,
        'entry_function': Determina se è passato in quella determinata funzione,
        'exit_function': Determina se è passato in quella determinata funzione
    }
    """
