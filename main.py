import time
import argparse

import errno
from socket import error as socket_error

from Connection import ExchangeConnection
from Bot import Bot


def main(strategies, exchange):
    """
    Run bot with strategies as input
    :param strategies:
    :param test:
    :return:
    """
    exchange_connection = ExchangeConnection(exchange)  # flag for testing
    print("Successfully Connected to %s" % exchange)
    bot = Bot(exchange_connection, strategies)
    print("Bot Initialized")
    bot.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('strategies')
    parser.add_argument('-e', '--exchange', type=str)
    args = parser.parse_args()

    strategies = args.strategies.split(',')
    exchange = args.exchange

    print("Using strategies:", strategies)
    print("Echanging in:", exchange)

    while True:
        try:
            main(strategies, exchange)
        except socket_error as serr:
            if serr.errno != errno.ECONNREFUSED:
                raise serr
            print("Connection Failed, Sleeping...")
            time.sleep(1)
