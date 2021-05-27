import time
from iqBot.bots.fullBot import BotFunc

class ichimokuHandle:
    def __init__(self, botInstance = BotFunc()) -> None:
        self.account = botInstance.account
        self.tool = botInstance.settings['tool']
    
    def __getCandles(self, nCandles) -> list:
        return self.account.get_candles(self.tool, 60, nCandles, time.time()) 

    def tenkanOperation(self) -> str:
        candles = self.__getCandles(9)
        minVal = min([candle['min'] for candle in candles])
        maxVal = max([candle['max'] for candle in candles])
        exitVal = candles[-1]['close']
        
        if (minVal+maxVal)/2 < exitVal:
            print('\nOperation: Call')
            return 'call'
        else:
            print('\nOperation: Put')
            return 'put'
        
