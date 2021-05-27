from iqBot.bots.botOperations import BotOperations
from logging import error
import time
from iqoptionapi.stable_api import IQ_Option

from iqBot.strats.strats import Strats
from iqBot.bots.bot import Bot

print('Welcome to iqBotApp! \n')
print('Right now, it\'s running on fileConfig auto mode.')
print('This will later have a better implementation but, for now... lol\n')

bot = Bot(operation='call', tool='EURUSD', mode=1, values=[1, 2, 3, 4, 5, 6, 7, 8], active=True, skipsTupleList = [(2, 2),(5, 3)], reverseList = [2, 5], askOpt = 6)
botOps = BotOperations(botInstance=bot)
stratsInstance = Strats()

# Run strat
stratsInstance.askLEDStrat(botOps=botOps, iterations=8)
