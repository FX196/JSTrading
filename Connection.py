import socket
import json


class ExchangeConnection:
    def __init__(self, exchange, team_name='THREESTINKYCOBBLERS'):
        if exchange in ("0", "1", "2"):
            host_name = "test-exch-threestinkycobblers"
            port = 25000 + int(exchange)

        else:
            host_name = "production"
            port = 25000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host_name, port))
        self.stream = s.makefile('rw', 1)

        self.write({"type": "hello", "team": team_name})
        hello = self.read()
        assert hello['type'] == 'hello'

        self.order_id = 0
        self.latest_books = {
            "BOND": [None],
            "VALBZ": [None],
            "VALE": [None],
            "GS": [None],
            "MS": [None],
            "WFC": [None],
            "XLF": [None]
        }

    def read(self, store_last=True):  # read from exchange
        data = self.stream.readline()
        if data == "":
            return None
        else:
            data = json.loads(data)
            if store_last:
                self.last_data = data
                if data["type"] == "book":
                    self.latest_books[data["symbol"]] = data
            return data

    def write(self, data):  # write to exchange
        json.dump(data, self.stream)
        self.stream.write("\n")

    def trade(self, buysell, symbol, price, size):
        trade = {'type': 'add', 'order_id': self.order_id, 'symbol': symbol,
                 'dir': buysell, 'price': price, 'size': size}
        self.order_id += 1
        print(trade)
        self.write(trade)

    def trade_batch(self, trades):
        for buysell, symbol, price, size in trades:
            if buysell and size != 0:
                self.trade(buysell, symbol, price, size)

    def convert(self, buysell, symbol, size):
        trade = {'type': 'convert', 'order_id': self.order_id,
                 'symbol': symbol, 'dir': buysell, 'size': size}
        self.order_id += 1
        print(trade)
        self.write(trade)
