import math

class NPIValidation():

    def __init__(self, npi):
        self.npi = npi
        self.npiLength = len(str(self.npi))
        if (self.npiLength == 10):
            self.npiFirstNine = str(self.npi)[0:9]
            self.npiCheckDigit = str(self.npi)[9]
            self.npiEveryFristNumber = self.npiFirstNine[1::2]

    def checkNPI(self):
        if (self.npiLength == 10):
           results = self.checkDigit()
        else:
           results = False

        return results

    def everyOtherNumber(self):
        npiEveryOtherNumber = self.npiFirstNine[::-1][::2]

        doubleEveryOtherNumber = []
        npiEveryOtherNumber = self.npiFirstNine[::-1][::2]

        for i in range(len(npiEveryOtherNumber)):
            doubleEveryOtherNumber.append(int(npiEveryOtherNumber[::-1][i])*2)
            if (i < len(self.npiEveryFristNumber)):
                doubleEveryOtherNumber.append(int(self.npiEveryFristNumber[i]))

        return doubleEveryOtherNumber

    def everyFristNumber(self):
        doubleEveryOtherNumber = self.everyOtherNumber()

        for r in range(len(doubleEveryOtherNumber)):
            if (int(doubleEveryOtherNumber[r])>9):
                doubleEveryOtherNumber.append(int(str(doubleEveryOtherNumber[r])[0]))
                doubleEveryOtherNumber.append(int(str(doubleEveryOtherNumber[r])[1]))
                doubleEveryOtherNumber.pop(r)

        doubleEveryOtherNumber.append(24)

        return doubleEveryOtherNumber

    def npiMath(self):
        doubleEveryOtherNumber = self.everyFristNumber()
        total = 0  

        for numbers in range(0, len(doubleEveryOtherNumber)):
            total = total + doubleEveryOtherNumber[numbers]
        
        roundUpTotal = int(self.round_up(total,-1))

        checkDigit = roundUpTotal-total
        
        return checkDigit

    def checkDigit(self):
        checkDigit = self.npiMath()
        if checkDigit == int(self.npiCheckDigit):
            results = True
        else:
            results = False
        
        return results

    def round_up(self, n, decimals=0): 
        multiplier = 10 ** decimals 
        return math.ceil(n * multiplier) / multiplier