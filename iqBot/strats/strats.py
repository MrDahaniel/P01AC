from iqBot.indicators.ichimoku import ichimokuHandle
from iqBot.bots.botOperations import BotOperations

class Strats:
    def stratReport(self, botOps = BotOperations()):
        print('\nStrat report:')
        print('Account initial balance: %s' % botOps.botInstance.initialBalance)
        print('Account current balance: %s' % botOps.botInstance.account.get_balance())
        print('---------------------------------------------')
        print('Account profit: $%s\n' % botOps.__getProfit__())

    def baseLEDStrat(self, botOps = BotOperations(), iterations = 1):

        print('Executing baseLEDStrat...\n')

        for _iteration in range(0, iterations):
            for currentVal in botOps.botInstance.values:
                botOps.createOrder(currentVal)
                botOps.reportOrder()
            
                if botOps.lastOrder['orderResult'] == 'win':
                    break

            botOps.reportExecutionStats()
            self.stratReport(botOps=botOps)


        print('Execution completed')

    def holdLEDStrat(self, botOps = BotOperations(), iterations = 1):

        print('Executing holdLEDStrat...\n')

        for _iteration in range(0, iterations):
            for currentVal in botOps.botInstance.values:
                botOps.createOrder(currentVal)
                botOps.reportOrder()
                botOps.holdOrder()
            
                if botOps.lastOrder['orderResult'] == 'win':
                    break

            botOps.reportExecutionStats()
            self.stratReport(botOps=botOps)

    def reverseLEDStrat(self, botOps = BotOperations(), iterations = 1):

        print('Executing reverserLEDStrat...\n')

        for _iteration in range(0, iterations):
            for currentVal in botOps.botInstance.values:
                botOps.createOrder(currentVal)
                botOps.reportOrder()
                botOps.reverseOperation()

                if botOps.lastOrder['orderResult'] == 'win':
                    break
            
            botOps.reportExecutionStats()
            self.stratReport(botOps=botOps)

    def holdReverseLEDStrat(self, botOps = BotOperations(), iterations = 1):

        print('Executing holdReverseLEDStrat...\n')

        for _iteration in range(0, iterations):
            for currentVal in botOps.botInstance.values:
                botOps.createOrder(currentVal)
                botOps.reportOrder()
                botOps.holdOrder()
                botOps.reverseOperation()

                if botOps.lastOrder['orderResult'] == 'win':
                    break
            
            botOps.reportExecutionStats()
            self.stratReport(botOps=botOps)

    def askLEDStrat(self, botOps = BotOperations(), iterations = 1):
        
        print('Executing askLEDStrat...')

        originalOperation = botOps.botInstance.operation

        for _iteration in range(0, iterations):
            for currentVal in botOps.botInstance.values:
                botOps.createOrder(currentVal)
                botOps.reportOrder()
                response = botOps.askForOrder()

                if response:
                    break
            
                if botOps.lastOrder['orderResult'] == 'win':
                    
                    break

            botOps.reportExecutionStats()
            self.stratReport(botOps=botOps)

    # def tenkanLEDStrat(self, botInstance = BotFunc(), ichimokuInstance = ichimokuHandle(), iterations = 1):

    #     print('Executing tenkanLEDStrat...\n')

    #     for iteration in range(0, iterations):
    #         botInstance.createOrderV2(botInstance.values, ichimokuInstance.tenkanOperation())
    #         print('')
    #         botInstance.reportOrderV2()
    #         print('')
    #         self.stratReport(botInstance)

    #         print('Stats:')
    #         print(dumps(botInstance.stats, indent=4))

    # def tenkanListLEDStrat(self, botInstance = BotFunc(), ichimokuInstance = ichimokuHandle(), iterations = 1):

    #     print('Executing tenkanListLEDStrat...\n')

    #     for iteration in range(0, iterations):
    #         for currentVal in botInstance.values:
    #             botInstance.createOrderV2(currentVal, ichimokuInstance.tenkanOperation())
    #             print('')
    #             botInstance.reportOrder()
    #             print('')

    #             if botInstance.lastOrder['orderResult'] == 'win':
    #                 break

    #         self.stratReport(botInstance)

    #         print('Stats:')
    #         print(dumps(botInstance.stats, indent=4))