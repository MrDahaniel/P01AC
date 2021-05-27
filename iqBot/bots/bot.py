from logging import warn
from iqoptionapi.stable_api import IQ_Option

class Bot:
    def __init__(self, operation=None, tool=None, mode=None, values=None, active=False, **kwargs) -> None:
        # Account 
        if active:
            self.account = self.__setAccount__() 

        # Order settings 
        self.operation = operation
        self.tool = tool
        self.mode = mode
        self.values = values

        # Report values
        if active:
            self.stats = self.__getStatKeys__()
            self.initialBalance = self.__getInitialBalance__()

        # Kwargs (Skips, MaxLostInARow, etc.)
        # Skips
        if 'skipsTupleList' in kwargs.keys():
            self.skipsDict = self.__setSkipsAfterLost__(kwargs['skipsTupleList'])
        
        # Reverse
        if 'reverseList' in kwargs.keys():
            if isinstance(kwargs['reverseList'], list):
                self.reverseDict = self.__setReverseAfterLost__(kwargs['reverseList'])
            else: 
                raise Exception("reverseList is not a list!")

        if 'askOpt' in kwargs.keys():
            if isinstance(kwargs['askOpt'], int):
                self.askDict = self.__setAskAfterLost__(kwargs['askOpt'])
            else: 
                raise Exception("askOpt is not an int!")

        # Checking integrity of bots.
        if active:
            self.__checkIntegrity__()

    def __getStatKeys__(self):
        return dict.fromkeys(self.values, 0)
    
    def __getInitialBalance__(self):
        return self.account.get_balance()

    def __checkIntegrity__(self):
        '''
        This function is meant to check if the instance of a bot is a valid instance of it.

        This means all operation values are not None and valid.
        '''
        self.__checkOperationIntegrity__()
        self.__checkToolIntegrity__()
        self.__checkModeIntegrity__()
        self.__checkValuesIntegrity__()
    
    def __checkOperationIntegrity__(self):
        validOperations = ['call', 'put']
        if self.operation in validOperations:
            return
        else: 
            raise Exception("Operation has an invalid value. \nValid values are: %s" % validOperations)

    def __checkToolIntegrity__(self):
        if self.tool in self.account.get_all_ACTIVES_OPCODE():
            return
        else:
            raise Exception("Tool has an invalid value.")

    def __checkModeIntegrity__(self):
        validModes = [1, 5]
        if self.mode in validModes:
            return
        else:
            raise Exception("Tool has an invalid value. \nValid values are: %s" % validModes)

    def __checkValuesIntegrity__(self):
        if isinstance(self.values, int) and self.values > 0:
            return
        elif isinstance(self.values, list):
            for value in self.values:
                if isinstance(value, int) and value > 0:
                    pass
                else:
                    raise Exception("Invalid value: %s in values list." % value)

    def __setAccount__(self):
        mail = input("Mail: ")
        password = input("Password: ")

        account = IQ_Option(mail, password)
        check, reason = account.connect()

        if check:
            return account
        else:
            print(reason)
            return None
    
    def __setSkipsAfterLost__(self, tupleList):
        '''
            This functions takes a tuple list of the following form:
                [(lostInRow, numberOfSkips), ...]

            It reads like this:
                After lostInRow do numberOfSkips.
            
            It returns a dictionary of the form:
                {
                    'lostInRow': numberOfSkips,
                    ...
                }
        '''
        skipsDict = {}
        for tuple in tupleList:
            skipsDict[tuple[0]] = tuple[1]

        return skipsDict
 
    def __setReverseAfterLost__(self, lostList):
        '''
            This functions takes a list of the following form:
                []

            It reads like this:
                After lostInRow do reverse.

            It returns a dictionary of the form:
                {
                    'lostInRow': 0,
                    ...
                }
            
        '''
        return dict.fromkeys(lostList, 0)

    def __setAskAfterLost__(self, lostOpt):
        return dict.fromkeys([*range(lostOpt, len(self.values)+1, 1)], 0)