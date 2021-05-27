import json
from datetime import datetime
from time import sleep
from iqBot.bots.bot import Bot

class BotOperations:
    '''
        This class handles all the posible operations a bot could make.
        It takes a bot instance and with it, makes all operations.

        This is meant to used with iqBot.strats.strats to make a functioning bot.
    '''
    def __init__(self, botInstance = Bot()) -> None:
        # Getting the bot instance.
        self.botInstance = botInstance

        # Last order values.
        # This is meant to keep track of the last orders.
        self.lostInRow = 0
        self.lastOrder = {
            'orderId': None,
            'orderValue': None,
            'orderResult': None 
        }
        self.startTime = datetime.now()
        self.reportFilename = "reports/" + self.startTime.strftime("%m%d%Y%H%M%S") + ".txt"

    # Creates orders.
    def createOrder(self, value, orderOperation = None, retryAction = 'retry'):
        # Checks connection
        self.__checkConnection__()

        # Checks if a different operation has been passed as an argument
        if orderOperation == None:
            orderOperation = self.botInstance.operation
        check, orderId = self.botInstance.account.buy(value, self.botInstance.tool, orderOperation, self.botInstance.mode)
        
        # If the order was good, passes the report of it being ok.
        if check:
            self.__updateLastOrder__(orderId, value)
            print('Order created.')
            print('Order ID: %s' % orderId)
            print('Value: $%s' % value)
        # Else, it calls __retryOrder__ which handles "could not be created" scenario
        else:
            print('Order could not be created.')
            print(orderId)
            self.__retryOrder__(value, orderOperation, retryAction)

    # Order reports

    def reportOrder(self, orderId = None):
        if orderId == None:
            orderId = self.lastOrder['orderId']

        result, profit = self.botInstance.account.check_win_v3(orderId)

        self.lastOrder['orderResult'] = result

        if result == 'win':
            print('Order %s won. Profit $%s' % (self.lastOrder['orderId'], profit))
            self.lostInRow = 0
            self.__updateStats__(self.lastOrder['orderValue'])

        elif result == 'equal':
            print('Order %s tied. Retrying...' % (self.lastOrder['orderId']))
            self.createOrder(self.lastOrder['orderValue'])
            self.reportOrder(self.lastOrder['orderId'])

        elif result == 'loose': 
            print('Order %s lost. Loss $%s' % (self.lastOrder['orderId'], profit))
            self.lostInRow += 1

    def reportExecutionStats(self):
        stats = self.botInstance.stats
        self.__exportExecutionStats__(stats)

        jsonDump = json.dumps(stats, indent=4)
        print('Stats:')
        print(jsonDump)

    # Strats especifics

    def holdOrder(self):
        try:
            skipsDict = self.botInstance.skipsDict
        except Exception:
            raise Exception("Error: No skip settings. Use key word 'skipsTupleList' while creating botInstance.")

        print("Ops lost in a row: ", self.lostInRow)

        try:
            skips = skipsDict[self.lostInRow]
            sleep(60*skips)
            print('Waited %s minutes.' % skips)
        except:
            pass

    def reverseOperation(self):
        try:
            reverseDict = self.botInstance.reverseDict
        except Exception:
            raise Exception("Error: No reverse settings. Use key word 'reverseList' while creating botInstance.")

        print("Ops lost in a row: ", self.lostInRow)

        try:
            reverseDict[self.lostInRow]
            print('Reversing...')
            if self.botInstance.operation == 'call':
                self.botInstance.operation = 'put'
            elif self.botInstance.operation == 'put':
                self.botInstance.operation = 'call'
        except:
            pass

    def askForOrder(self):
        try: 
            askDict = self.botInstance.askDict

        except Exception:
            raise Exception("Error: No ask settings. Use key word 'askOpt' while creating botInstance.")

        try:
            askDict[self.lostInRow]
        
            print("----------------------------------")
            print("Warning! %s operations lost." % self.lostInRow)
            print("----------------------------------")


            while True:
                print("Avalible options:")
                print("0. Do opt: Call.")
                print("1. Do opt: Put.")
                print("2. Exit opt.")

                option = input("Select input: ")

                try:
                    option = int(option)

                    if int(option) == 0:
                        self.botInstance.operation = 'call'
                        return False
                    elif option == 1:
                        self.botInstance.operation = 'put'
                        return False
                    elif option == 2:
                        return True
                    else:
                        print('Invalid input')

                except Exception:
                    print('Invalid input')

        except Exception:
            pass

            

    # Private functions, only meant to be used internally.

    def __updateStats__(self, key):
        self.botInstance.stats[key] += 1

    def __updateLastOrder__(self, orderId, value):
        self.lastOrder['orderId'] = orderId
        self.lastOrder['orderValue'] = value
    
    def __retryOrder__(self, value, orderOperation, action):
        if action == 'retry':
            self.createOrder(value, orderOperation, retryAction=action)
        elif action == 'exit':
            raise Exception("Action was to exit after order failed to create.")

    def __checkConnection__(self):
        if self.botInstance.account.check_connect():
            return
        else:
            print("Connection failed.")
            print("Attempting to reconnect...")
            self.__reconnect__()

    def __updateOperation__(self, operation):
        operation = operation.lower()
        if operation in ['call', 'put']:
            self.botInstance.operation = operation

    def __getProfit__(self):
        return self.botInstance.account.get_balance() - self.botInstance.initialBalance

    def __reconnect__(self):
        print("Reconnecting...")
        check, reason = self.botInstance.account.connect()
        if check:
            print('Reconnected successfully!')
        else:
            print('Reconnection failed.')
            print(reason)
            self.__reconnect__()

    def __exportExecutionStats__(self, stats):
        jsonFile = open(self.reportFilename, 'w')
        jsonObject = json.dumps(stats, indent = 4)
        
        jsonFile.write(jsonObject)

        jsonFile.close()

