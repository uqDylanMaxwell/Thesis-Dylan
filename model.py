import math
import random
import numpy
# import pdb
from tradingFunction import *
from households import *
# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------

totalPrice = []
totalQuantity = []
startPrice = 0.01
endPrice = 0.50

currentValue = startPrice
while currentValue < endPrice:
    totalPrice.append(round(currentValue, 2))
    totalQuantity.append(0)
    currentValue += 0.01

class user:
    def __init__(self, number, maxBatteryCapacity, batteryCapacity, preferedCapacity, preferedBatCapacity, prefBatCapTR, load, production, energyTraded, energyRisk, risk, situationalRisk, individualRisk, price1, price2, upperBound, lowerBound, money, household, PVSystem):
        self.number = number
        self.maxBatteryCapacity = maxBatteryCapacity
        # B_C
        self.batteryCapacity = batteryCapacity
        # B_PC - end of the trading round increase/ decrease in battery capacity
        self.preferedCapacity = preferedCapacity
        # B_P - prefered battery capacity in general 
        self.preferedBatCapacity = preferedBatCapacity
        # B_PT - additional battery capacity that needs to be gained
        self.prefBatCapTR = prefBatCapTR
        self.load = load
        self.production = production
        self.energyTraded = energyTraded
        self.energyRisk = energyRisk
        self.risk = risk
        self.situationalRisk = situationalRisk
        self.individualRisk = individualRisk
        self.price1 = price1
        self.price2 = price2
        self.upperBound = upperBound
        self.lowerBound = lowerBound
        self.money = money
        self.household = household
        self.PVSystem = PVSystem
        self.refPoint = 0
        self.gridTrades = 0
        self.totalValue = 0
        self.successfulTrades = 0
    
    # update price2
    def updatePrice2(self):
        Lp = 0.2 # still need to decide how to set number
        if self.energyTraded != 0:
            if self.energyTraded > 0:
                # selling
                self.price2 = round(Lp*self.risk + self.price1, 2)
            else:
                # buying
                self.price2 = round(-Lp*self.risk + self.price1, 2)

    # update money
    def updateMoney(self, money):
        self.money += money

    # update battery capacity
    def updateBatteryCapacity(self, energy):
        self.batteryCapacity += energy

    # calculate energy to trade this round
    def energyTrade(self, currentTradingPeriod):
        # remove peak hours 6pm-9pm
        if currentTradingPeriod >= 42:
            T = 1
        else: 
            T = 42 - (currentTradingPeriod % 42)
        self.batteryCapacity += self.production - self.load
        # self.energyTraded = (self.preferedCapacity + self.production - self.batteryCapacity - self.load)/T
        self.energyTraded = (self.preferedBatCapacity - self.batteryCapacity)/T
        # print("this one:", self.energyTraded)
        # if abs(self.energyTraded) > 50:
        #     print(self.preferedCapacity, self.production, self.batteryCapacity, self.load)

    # update risk
    def updateRisk(self, currentTradingPeriod):
        # find the amount of data to needed to hit pref battery capacity
        # divide this by number of periods till 6pm
        # use this number to trade


        # placeholder for number of trading rounds until peak times
        T = 48 - (currentTradingPeriod % 48)
        # set B_PT
        self.prefBatCapTR = (self.preferedBatCapacity-self.batteryCapacity)/ T
        # print("1", self.preferedBatCapacity, self.batteryCapacity, self.prefBatCapTR, T)
        # set B_PC
        # self.preferedCapacity = self.batteryCapacity + self.prefBatCapTR
        # set E_T
        # self.energyTraded = self.preferedCapacity + self.production - self.batteryCapacity - self.load
        # print("2", self.energyTraded)
        # set E_%
        if self.prefBatCapTR == 0:
            self.energyRisk = 0.5
        else:
            self.energyRisk = (abs((self.energyTraded-self.prefBatCapTR) / self.prefBatCapTR)) + 1
        # set R_s
        # print(round(self.energyTraded, 2), round(self.prefBatCapTR, 2), round(self.energyRisk, 2))
        self.situationalRisk = round(0.15*math.log(0.515*self.energyRisk)+0.6, 2)
        # set risk
        self.risk = self.individualRisk + (self.situationalRisk - 0.5)

    # rand price for first iteration
    def randPrice(self):
        self.price1 = round(random.uniform(0.1, 0.8), 2)
        self.price2 = round(random.uniform(0.05, self.price1), 2)

# buy
U0 = user(0, 8000, 5980, 5990, 6000, 0, 0, 0, 0, 0, 0, 0, 0.3, 0.3, 0.08, 0, 0, 0, 3, 3)
U1 = user(1, 8000, 2800, 2820, 3000, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.3, 0.09, 0, 0, 0, 5, 3)
U2 = user(2, 8000, 6700, 6730, 7000, 0, 0, 0, 0, 0, 0, 0, 0.6, 0.28, 0.10, 0, 0, 0, 1, 5)
U3 = user(3, 13500, 9280, 9300, 10000, 0, 0, 0, 0, 0, 0, 0, 0.55, 0.28, 0.15, 0, 0, 0, 2, 4)
U4 = user(4, 8000, 5950, 5955, 6000, 0, 0, 0, 0, 0, 0, 0, 0.7, 0.32, 0.10, 0, 0, 0, 4, 4)
U5 = user(5, 8000, 5300, 5310, 5400, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.32, 0.09, 0, 0, 0, 3, 4)
U6 = user(6, 13500, 6500, 6540, 8000, 0, 0, 0, 0, 0, 0, 0, 0.35, 0.31, 0.08, 0, 0, 0, 2, 3)
U7 = user(7, 13500, 4980, 4990, 5000, 0, 0, 0, 0, 0, 0, 0, 0.6, 0.30, 0.07, 0, 0, 0, 2, 5)
U8 = user(8, 8000, 5150, 5170, 5500, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.29, 0.07, 0, 0, 0, 3, 4)
U9 = user(9, 13500, 10900, 10905, 11000, 0, 0, 0, 0, 0, 0, 0, 0.30, 0.45, 0.08, 0, 0, 0, 5, 4)
#sell
U10 = user(10, 13500, 7550, 7530, 7500, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.10, 0.09, 0, 0, 0, 1, 5)
U11 = user(11, 20000, 17000, 16970, 16000, 0, 0, 0, 0, 0, 0, 0, 0.4, 0.09, 0.10, 0, 0, 0, 2, 5)
U12 = user(12, 13500, 8700, 8670, 8500, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.18, 0.11, 0, 0, 0, 4, 3)
U13 = user(13, 20000, 18050, 18030, 18000, 0, 0, 0, 0, 0, 0, 0, 0.45, 0.12, 0.12, 0, 0, 0, 3, 5)
U14 = user(14, 20000, 14325, 14300, 13000, 0, 0, 0, 0, 0, 0, 0, 0.55, 0.08, 0.10, 0, 0, 0, 4, 5)
U15 = user(15, 40000, 33900, 33950, 32000, 0, 0, 0, 0, 0, 0, 0, 0.52, 0.10, 0.09, 0, 0, 0, 5, 6.6)
U16 = user(16, 13500, 6600, 6550, 6500, 0, 0, 0, 0, 0, 0, 0, 0.56, 0.10, 0.08, 0, 0, 0, 2, 5)
U17 = user(17, 20000, 13400, 13360, 13000, 0, 0, 0, 0, 0, 0, 0, 0.53, 0.11, 0.07, 0, 0, 0, 1, 5)
U18 = user(18, 20000, 12070, 12040, 12000, 0, 0, 0, 0, 0, 0, 0, 0.6, 0.12, 0.10, 0, 0, 0, 3, 6.6)
U19 = user(19, 40000, 40000, 39500, 34000, 0, 0, 0, 0, 0, 0, 0, 0.5, 0.09, 0.11, 0, 0, 0, 5, 10)

users = [U0, U1, U2, U3, U4, U5, U6, U7, U8, U9, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19]


def main():
    # work through first iteration that has no data
    for user in users:
        # need to make sure their are both buyers and sellers in first iteration
        user.energyTrade(42)
        # user.randPrice()
        # print(user.number, user.energyTraded, user.price1, user.price2)
    quantity, price, energyTraded, avgQuantity = trade()

    avgPrice = numpy.median(price)
    # avgQuantity = numpy.median(quantity)
    # avgQuantity = 50

    # iterate for the rest of the model
    numTradingPeriod = 5


    # figure out what happened to price and quantity after round 13
    # check trading function to see if something is stopping it more people should be trading than currently are
    # could be an issue with present information
    # is there a world where i only look at trading excess energy? -> might be better
    # check out if pricing is logical -> i think too much at the bounds needs to be better spread

    # things get weird from trading round 13 always
    currentTradingPeriod = 1
    while currentTradingPeriod < numTradingPeriod:
        print("NEW TRADING ROUND:", currentTradingPeriod)
        print("post trade value:", "number, buy/sell, price 1, traded price, price 1 value, traded price value")
        for user in users:
            updateProsumer(user, currentTradingPeriod)
            user.energyTrade(currentTradingPeriod)
            # print(user.energyTraded)
            user.updateRisk(currentTradingPeriod)
            upper, lower = setBounds(user, avgPrice)
            user.price1 = optimiseValue(upper, lower, quantity, price, user, avgQuantity, energyTraded)
            # print(user.number, round(user.price1, 2), round(user.energyTraded, 2))
            user.updatePrice2()
            # print(user.price2)
        currentTradingPeriod += 1
        
        # save data incase no energy is traded
        tempQuantity = []
        tempPrice = []
        for x in quantity:
            tempQuantity.append(x)
        for x in price:
            tempPrice.append(x)
        tempEnergyTraded = energyTraded
        tempAvgQuantity = avgQuantity


        quantity, price, energyTraded, avgQuantity = trade()

        if price == 0:
            price = []
            quantity = []
            for x in tempPrice:
                price.append(x)
            for x in tempQuantity:
                quantity.append(x)
            energyTraded = tempEnergyTraded
            avgQuantity = tempAvgQuantity

        

        avgPrice = numpy.median(price)
        # print(avgPrice)
        # avgQuantity = numpy.median(quantity)
        # avgQuantity = 50
        # for x in totalQuantity:
        #     print(x)
        
# update data
def updateData(quantity, price):
    indexQuantity = 0
    indexTotalQuantity = 0

    for x in totalPrice:
        for y in price:
            y2 = round(y, 2)
            if x == y2:
                totalQuantity[indexTotalQuantity] += round(quantity[indexQuantity], 2)
            indexQuantity += 1
        indexQuantity = 0
        indexTotalQuantity += 1 

# collect data for all prosumers trading and complete trade using tradingFunction.py
def trade():
    traders = []
    for user in users:
        if user.energyTraded != 0:
            # print(user.number, user.energyTraded )
            if user.energyTraded > 0:
                tradingType = "S"
            else:
                tradingType = "B"
            traders.append(Prosumer(tradingType, abs(user.energyTraded), user.price1, user.number, "N", 0, -1, user.price2, 0, 0))
    # run doubleAuction and change it to return needed info
    traders = doubleAuction(traders)
    # return traders with quanity traded and at what price and update users
    numofTraders = 0
    for x in traders:
        if x.transactionStatus == "C":
            numofTraders += 1
        # print(x.priceTraded, x.price, x.tradingType)
        
        for y in users:
            if x.tradingNumber == y.number:
                # update money and battery capacity
                y.updateBatteryCapacity(x.energyTraded)
                y.updateMoney(x.priceTraded*x.energyTraded)

                # trade excess energy on grid
                if x.transactionStatus == "N":
                    if x.tradingType == "B":
                        y.updateBatteryCapacity(x.quantity)
                    elif x.tradingType == "S":
                        y.updateBatteryCapacity(-x.quantity)
                    y.gridTrades += 1
                    
                # store long term PT info
                if x.transactionStatus == "C":
                    y.successfulTrades += 1
                    y.totalValue += valueFunction(y, y.refPoint, x.priceTraded)
                
                # print("post trade value:", y.number, x.tradingType, round(y.preferedBatCapacity, 2), round(y.batteryCapacity, 2), round(x.priceTraded, 2), round(x.quantity, 2), round(valueFunction(y, y.refPoint, x.priceTraded), 3))
                print("post trade value:", y.number, x.tradingType, round(x.price, 2), round(x.priceTraded, 2), round(valueFunction(y, y.refPoint, x.price), 3), round(valueFunction(y, y.refPoint, x.priceTraded), 3), round(y.refPoint, 2), round(y.energyTraded, 2))

    # return a function of price and quantity
    quantity, price, energyTraded = data(traders)
    if numofTraders == 0:
        numofTraders = 1


    avgQuantity = energyTraded / numofTraders
    if price == 0:
        return(quantity, price, energyTraded, avgQuantity)

    updateData(quantity, price)
    return(quantity, price, energyTraded, avgQuantity)


# update prosumers El, Ep
def updateProsumer(user, tradingRound):
    # this data needs to come from seperate data for load and production
    # in a seperate file create accurate data for households of 2,3,4,5 for a 24 hour period
    # when calling data select rand within a reasonable range of that data
    if user.PVSystem == 3:
        production = PV3[(tradingRound - 1) % 48]
        user.production = round(random.uniform(0.95*production, 1.05*production), 2)
    if user.PVSystem == 4:
        production = PV4[(tradingRound - 1) % 48]
        user.production = round(random.uniform(0.95*production, 1.05*production), 2)
    if user.PVSystem == 5:
        production = PV5[(tradingRound - 1) % 48]
        user.production = round(random.uniform(0.95*production, 1.05*production), 2)
    if user.PVSystem == 6.6:
        production = PV6[(tradingRound - 1) % 48]
        user.production = round(random.uniform(0.95*production, 1.05*production), 2)
    if user.PVSystem == 10:
        production = PV10[(tradingRound - 1) % 48]
        user.production = round(random.uniform(0.95*production, 1.05*production), 2)

    if user.household == 1:
        load = load1[(tradingRound - 1) % 48]
        user.load = round(random.uniform(0.95*load, 1.05*load), 2)
    if user.household == 2:
        load = load2[(tradingRound - 1) % 48]
        user.load = round(random.uniform(0.95*load, 1.05*load), 2)
    if user.household == 3:
        load = load3[(tradingRound - 1) % 48]
        user.load = round(random.uniform(0.95*load, 1.05*load), 2)
    if user.household == 4:
        load = load4[(tradingRound - 1) % 48]
        user.load = round(random.uniform(0.95*load, 1.05*load), 2)
    if user.household == 5:
        load = load5[(tradingRound - 1) % 48]
        user.load = round(random.uniform(0.95*load, 1.05*load), 2)

# set trading bounds
def setBounds(user, avgPrice):
    # current bounds have no relation to average price of last trade
    L_magnitude = 0.05*user.risk + 0.1
    # print(user.energy)
    if user.energyTraded != 0:
        if user.energyTraded > 0:
            # selling
            L_horizontal_shift = -(1-L_magnitude)*user.risk+(1-0.5*L_magnitude)
        else:
            # buying
            L_horizontal_shift = (1-L_magnitude)*user.risk+0.5*L_magnitude
    L_upper = round(L_horizontal_shift + 0.5*L_magnitude, 2) * (avgPrice / 0.5)
    L_lower = round(L_horizontal_shift - 0.5*L_magnitude, 2) * (avgPrice / 0.5)
    return(L_upper, L_lower)

# the decision weight
def pi(energyPercentage, energyTraded, user):
    # k = (1 / 20) * (energyTraded * energyPercentage) / abs(user.energyTraded)
    k = (1 / 20) * (energyTraded) / abs(user.energyTraded)

    # now rank k as a probability 
    if k == 0:
        x = 0
    else:
        x = round(0.15*math.log(0.515*(k))+0.6, 2)
    # print(k, x)

    # decision weight s curve
    return(-3.7584*x**4+5.2669*x**3-1.04*x**2+0.3533*x+0.106)

#the value function
def valueFunction(user, refPoint, price):
    # print(user.number, refPoint)
    # find the value at any given price
    # if the user is selling
    if user.energyTraded > 0:
        # shift the value function st the ref point is the origin
        log = refPoint - 10 ** (-0.5 / 0.4)
        quad = refPoint - (0.4 / 18) ** 0.5
        # print("value", quad, price)
        if price < quad:
            value = 0.1
        elif price >= quad and price < refPoint:
            value = 18*(price - quad) ** 2 + 0.1
        elif price >= refPoint:
            value = 0.4*math.log10(price - log) + 1
        
    # if the user is buying
    if user.energyTraded < 0:
        # shift the value function st the ref point is the origin
        log = -refPoint - 10 ** (-0.5 / 0.4)
        quad = refPoint + (0.4 / 18) ** 0.5

        if price > quad:
            value = 0.1
        elif price <= quad and price > refPoint:
            value = 18*(price - quad) ** 2 + 0.1
        elif price <= refPoint:
            value = 0.4*math.log10(-price - log) + 1
    # print(refPoint, value)
    return value

# use optimisation to find the price of maximum value
def optimiseValue2(upper, lower, quantity, price, user, avgQuantity, energyTraded):
    # find max value price
    count = 0
    index = 0
    max = 0
    refPoint = (upper + lower) / 2
    while count < len(price):

        # print(pi(quantity[count], energyTraded, user), valueFunction(user, refPoint, price[count]))
        if user.energyTraded > 0:
            
            # selling
            if (pi(quantity[count], energyTraded, user)*valueFunction(user, refPoint, price[count])) > max:
                index = count
                max = pi(quantity[count], energyTraded, user)*valueFunction(user, refPoint, price[count])
            count += 1
        if user.energyTraded < 0:
            # buying
            if ((1 - pi(quantity[count], abs(energyTraded), user))*valueFunction(user, refPoint, price[count])) > max:
                index = count
                max = (1 - pi(quantity[count], energyTraded, user))*valueFunction(user, refPoint, price[count])
            count += 1
          
    return price[index]

# use optimisation to find the price of maximum value
def optimiseValue(upper, lower, quantity, price, user, avgQuantity, energyTraded):
    # re-organise data
    # select prices closest to bounds
    tempUpper = 100
    tempLower = 100
    indexUpper = 0
    indexLower = 0
    count = 0
    quantityPercentage = abs(user.energyTraded/avgQuantity)
    # print(user.number, round(user.risk, 2), round(upper, 2), round(lower, 2), round(quantityPercentage, 2))

    # aims to select upper and lower bound indexs of price array based on smallest difference from price array
    for x in price:
        b_upper = abs(x-upper)
        if b_upper < tempUpper:
            tempUpper = b_upper
            indexUpper = count
        b_lower = abs(x-lower)
        if b_lower < tempLower:
            tempLower = b_lower
            indexLower = count
        count += 1
    
    if indexUpper == indexLower:
        indexUpper += 1
    

    # create new arrays within the selected bounds
    tempPrice = []
    temp = indexLower
    

    while temp < indexUpper:
        tempPrice.append(price[temp])
        temp += 1

    # this code places increases quanitity with new price bound e.g. add up all previous trading quantities before that price
    temp = indexLower
    tempQuantity = []
    while temp < indexUpper:
        energy = 0
        a = 0
        for x in quantity:
            if a > temp:
                break
            energy += x
            a += 1
        tempQuantity.append(energy)
        temp += 1

    # iterate through lists and select best price
    boundRange = indexUpper - indexLower
    count = 0
    index = 0
    max = 0
    min = 100
    difference = 10
    # print("bound", boundRange)
    # print("quantity", round(quantityPercentage, 2))
    refPoint = (upper + lower) / 2
    user.refPoint = refPoint
    # print("start")
    while count < boundRange:
        # print(pi(quantity[count], energyTraded, user), valueFunction(user, refPoint, price[count]), user.energyTraded)
        if user.energyTraded > 0:
            # selling
            if ((1 - pi(quantity[count], energyTraded, user))*valueFunction(user, refPoint, tempPrice[count])) > max:
                index = count
                max = (1 - pi(quantity[count], energyTraded, user))*valueFunction(user, refPoint, tempPrice[count])
            count += 1
        if user.energyTraded < 0:
            # buying
            
            # print(":", tempPrice[count], pi(quantity[count], abs(energyTraded), user), valueFunction(user, refPoint, tempPrice[count]))
            if ((pi(quantity[count], abs(energyTraded), user))*valueFunction(user, refPoint, tempPrice[count])) > max:
                index = count
                max = (pi(quantity[count], energyTraded, user))*valueFunction(user, refPoint, tempPrice[count])
            count += 1

    return tempPrice[index]
    # price1 = round(0.15*math.log(0.515*quantityPercentage)+0.6, 2)


main()

