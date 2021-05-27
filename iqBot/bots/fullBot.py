from iqoptionapi.stable_api import IQ_Option
import time

class BotFunc:
    def __init__(self) -> None:
        self.settings = {
            'tool': '',
            'operation': '',
            'mode': ''
        }
        self.account = None
        self.values = None
        self.lastOrder = {
            'orderId': None,
            'orderValue': None,
            'orderResult': None
        }
        self.stats = {}
        self.initialBal = None
        self.lostCounter = 0
        self.lostCounterLimit = 0
        self.lostInRow = 0
        self.skips = {}
        self.maxLostInARow = {}
    
    # def setSkipsKeyLostKey(self, skipsList, maxLostList):
    #     counter = 0
    #     skipDic = {}
    #     maxLostDic = {}

    #     for numSkips in skipsList:
    #         skipDic[counter] = numSkips
    #         counter += 1
        
    #     self.skips = skipDic

    #     counter = 0

    #     for numMax in maxLostList:
    #         maxLostDic[counter] = numMax
    #         counter += 1

    #     self.maxLostInARow = maxLostDic
    #     self.lostCounterLimit = len(maxLostList)

    # def setInitialBal(self):
    #     self.initialBal = self.account.get_balance()

    # def getProfit(self):
    #     return self.account.get_balance() - self.initialBal

    # def setSettings(self, tool, operation = 'call', mode = 1):
    #     self.settings['tool'] = tool
    #     self.settings['operation'] = operation
    #     self.settings['mode'] = mode

    # def setWorkValues(self, newValues):
    #     self.values = newValues

    # def setAccount(self, mail, password):
    #     newAccount = IQ_Option(mail, password)
    #     check, reason = newAccount.connect()

    #     if check:
    #         self.account = newAccount
    #     else: 
    #         print('Account could not be set: %s' % (reason))

    # def setLastOrder(self, orderId, orderValue):
    #     self.lastOrder['orderId'] = orderId
    #     self.lastOrder['orderValue'] = orderValue

    # def setLastOrderResult(self, orderResult):
    #     self.lastOrder['orderResult'] = orderResult

    # def setStatWonLost(self):
    #     self.stats = {'won': 0, 'lost': 0}

    # def setStatValues(self):
    #     self.stats = dict.fromkeys(self.values, 0)

    # def updateStats(self, key):
    #     self.stats[key] += 1

    # def checkCon(self):
    #     if not self.account.check_connect():
    #         print('Reconnection...')
    #         check,reason = self.account.connect()
    #         if check:
    #             print('Reconnect successfully')
    #         else:
    #             if reason=='error_password':
    #                 print('Error Password')
    #             else:
    #                 print('No Network')
    #             return False
    #     return True

    # def reconnect(self):
    #     if not self.account.check_connect():
    #         print('Reconnecting...')
    #         check, reason = self.account.connect()
    #         if check:
    #             print('Reconnect successfully!')
    #         else:
    #             print('Reconnection failed.')
    #             print(reason)
    #             self.reconnect()

    # def createOrder(self, value):

    #     check, id = self.account.buy(value, self.settings['tool'], self.settings['operation'], self.settings['mode'])

    #     if check:
    #         self.setLastOrder(id, value)
    #         print('Order created.')
    #         print('Order ID: %s' % id)
    #         print('Value: $%s' % value)
    #     else:
    #         print('Order could not be created.')
    #         print(id)
    #         self.setLastOrderResult('invalid')
    
    # def createOrderV2(self, value = 1, operation = 'call'):
    #     check, id = self.account.buy(value, self.settings['tool'], operation, self.settings['mode'])

    #     if check:
    #         self.setLastOrder(id, value)
    #         print('Order created.')
    #         print('Order ID: %s' % id)
    #         print('Value: $%s' % value)
    #     else:
    #         print('Order could not be created.')
    #         print(id)
    #         self.setLastOrderResult('invalid')

    # def reportOrder(self):
    #     if self.lastOrder['orderResult'] == 'invalid':
    #         self.reconnect()
    #         self.createOrder(self.lastOrder['orderValue'])

    #     result, profit = self.account.check_win_v3(self.lastOrder['orderId'])

    #     self.setLastOrderResult(result)

    #     if result == 'win':
    #         print('Order %s won. Profit $%s' % (self.lastOrder['orderId'], profit))
    #         self.lostCounter = 0
    #         self.lostInRow = 0
    #         self.updateStats(self.lastOrder['orderValue'])
    #     elif result == 'equal':
    #         print('Order %s tied. Retrying...' % (self.lastOrder['orderId']))
    #         self.createOrder(self.lastOrder['orderValue'])
    #         self.reportOrder()
    #     elif result == 'loose': 
    #         print('Order %s lost. Loss $%s' % (self.lastOrder['orderId'], profit))
    #         self.lostInRow += 1

    # def reportOrderV2(self):
    #     if self.lastOrder['orderResult'] == 'invalid':
    #         self.reconnect()
    #         self.reportOrderV2(self.lastOrder['orderValue'])

    #     result, profit = self.account.check_win_v3(self.lastOrder['orderId'])

    #     self.setLastOrderResult(result)

    #     if result == 'win':
    #         print('Order %s won. Profit $%s' % (self.lastOrder['orderId'], profit))
    #         self.updateStats('won')
    #     elif result == 'loose': 
    #         print('Order %s lost. Loss $%s' % (self.lastOrder['orderId'], profit))
    #         self.updateStats('lost')
    
    # def reportOrder(self):
    #     if self.lastOrder['orderResult'] == 'invalid':
    #         self.reconnect()
    #         self.createOrder(self.lastOrder['orderValue'])

    #     result, profit = self.account.check_win_v3(self.lastOrder['orderId'])

    #     self.setLastOrderResult(result)

    #     if result == 'win':
    #         print('Order %s won. Profit $%s' % (self.lastOrder['orderId'], profit))
    #         self.lostCounter = 0
    #         self.lostInRow = 0
    #         self.updateStats(self.lastOrder['orderValue'])
    #     elif result == 'equal':
    #         print('Order %s tied. Retrying...' % (self.lastOrder['orderId']))
    #         self.createOrder(self.lastOrder['orderValue'])
    #         self.reportOrder()
    #     elif result == 'loose': 
    #         print('Order %s lost. Loss $%s' % (self.lastOrder['orderId'], profit))
    #         self.lostInRow += 1

    def holdOrder(self):
        print('lostCounter: %s' % (self.lostCounter))
        print('lostInARow: %s' % (self.lostInRow))

        if self.lostCounterLimit == self.lostCounter:
            return
            
        print('maxLostInARow: %s' % (self.maxLostInARow[self.lostCounter]))

        if self.lostInRow == self.maxLostInARow[self.lostCounter]:
            time.sleep(60*self.skips[self.lostCounter])
            print('Waited %s minutes' % (self.skips[self.lostCounter]))
            self.lostCounter += 1
            self.lostInRow = 0  

    def reverseOrder(self):
        if self.lostCounterLimit == self.lostCounter:
            return
            
        print('lostCounter: %s' % (self.lostCounter))
        print('lostInARow: %s' % (self.lostInRow))
        print('maxLostInARow: %s\n' % (self.maxLostInARow[self.lostCounter]))


        if self.lostInRow == self.maxLostInARow[self.lostCounter]:
            if self.settings['operation'] == 'call':
                self.settings['operation'] = 'put'
            elif self.settings['operation'] == 'put':
                self.settings['operation'] = 'call'

            print('Changing to %s...\n' % self.settings['operation'])
            self.lostCounter += 1
            self.lostInRow = 0