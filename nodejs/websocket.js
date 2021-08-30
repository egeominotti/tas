const Binance = require('node-binance-api');
const fs = require('fs');

const binance = new Binance().options({
    APIKEY: 'vyghMLzH2Pvr0TCoV11Equ9kIK2jxL6ZpDh8pyUBz4hvAWXSLWO6rBHbogQmX9lH',
    APISECRET: 'yTmr8uu0w3ARIzTlYadGkWX79BlTHSybzzJeInrWcjUoygP3K7t81j4WXd8amMOM'
});


binance.websockets.candlesticks(['RVNUSDT'], "5m", (candlesticks) => {
    let {e: eventType, E: eventTime, s: symbol, k: ticks} = candlesticks;
    let {
        o: open,
        h: high,
        l: low,
        c: close,
        v: volume,
        n: trades,
        i: interval,
        x: isFinal,
        q: quoteVolume,
        V: buyVolume,
        Q: quoteBuyVolume
    } = ticks;
    if (isFinal) {
        console.info(symbol + " " + interval + " candlestick update");
        console.info("open: " + open);
        console.info("high: " + high);
        console.info("low: " + low);
        console.info("close: " + close);
        console.info("volume: " + volume);
        console.info("isFinal: " + isFinal);
    }
});

