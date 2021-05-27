from iqoptionapi.stable_api import IQ_Option
from iqBot.bots.bot import Bot
from iqBot.bots.botOperations import botOperations

newBot = Bot(operation="call", tool='EURUSD', mode=1, values=[1], active=True)
botOps = botOperations(botInstance=newBot)

IQ_Option.check_connect