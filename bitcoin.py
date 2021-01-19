import ssl
import json

import websocket
import bitstamp.client

import credenciais


def user():
    return bitstamp.client.Trading(username=credenciais.USERNAME,
                                   key=credenciais.KEY,
                                   secret=credenciais.SECRET)


def buy(quantidade):
    trading_client = user()
    trading_client.buy_market_order(quantidade)


def sell(quantidade):
    trading_client = user()
    trading_client.sell_market_order(quantidade)


def on_open(ws):
    print("conexão aberta")

    json_subscribe = """
{
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}
"""

    ws.send(json_subscribe)


def on_close(ws):
    print("conexão fechada")


def on_error(ws, error):
    print("Deu erro")
    print(error)


def on_message(ws, message):
    message = json.loads(message)
    price = message['data']['price']
    print(price)

    if price > 10000:
        sell()
    elif price < 8100:
        buy()
    else:
        print("Aguardar")


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net.",
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})