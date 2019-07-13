import time

def import_module(module_name):
    """Helper function to import module"""
    import sys
    import os.path as osp
    import importlib
    sys.path.append(osp.join(osp.dirname(__file__), 'strategies'))
    return importlib.import_module(module_name)


class Bot:
    def __init__(self, exchange, strategies):
        self.exchange = exchange
        self.strategies = [import_module(strategy) for strategy in strategies]
        self.filename = exchange+"_"+str(time.strftime("%H:%M:%S", time.gmtime()))
        self.file_obj = open(self.filename, "w")

    def run(self):
        """
        infinite loop while connected
        :return:
        """
        data = self.exchange.read()
        while data:
            self.file_obj.write(data)
            trades = []
            for strategy in self.strategies:
                trades.extend(strategy.trade(self.exchange))
            self.exchange.trade_batch(trades)
            data = self.exchange.read()
