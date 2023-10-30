# -------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------
import matplotlib.pyplot as plt
from collections import namedtuple
import csv
import random
import time
# import pdb
# pdb.set_trace()

# -------------------------------------------------------------------
# init classes
# -------------------------------------------------------------------

# create prosumer class
class Prosumer:
    # init information for each prosumer
    def __init__(self, tradingType, quantity, price, tradingNumber, transactionStatus, moneyTransfered, transactionPartner, secondPrice, energyTraded, priceTraded):
        self.tradingType = tradingType
        self.quantity = quantity
        self.price = price
        self.tradingNumber = tradingNumber
        self.transactionStatus = transactionStatus
        self.moneyTransfered = moneyTransfered
        self.transactionPartner = transactionPartner
        self.secondPrice = secondPrice
        self.energyTraded = energyTraded
        self.priceTraded = priceTraded

    # update the quantity of energy the prosumer is trading
    def updateQuantity(self, quantity):
        self.energyTraded = quantity

    # update the money transfered for the prosumer
    def updateMoneyTransfered(self, moneyTransfered):
        self.moneyTransfered += moneyTransfered
        # if self.tradingType == "B":
        #     self.moneyTransfered -= moneyTransfered
        # elif self.tradingNumber == "S":
        #     self.moneyTransfered += moneyTransfered

    # change prosumers trading status
    def updateTransactionStatus(self):
        self.transactionStatus = "C"

    # update transactionPartner
    def updateTransactionPartner(self, partner):
        self.transactionPartner = partner

    # swap prices for round 2 of trading
    def secondRoundPrice(self):
        self.price = self.secondPrice

class tradingPeriod:
    def __init__(self, periodNumber, maxPrice, minPrice, maxQuantity, minQuantity, numTraders):
        self.periodNumber = periodNumber
        self.maxPrice = maxPrice
        self.minPrice = minPrice
        self.maxQuantity = maxQuantity
        self.minQuantity = minQuantity
        self.numTraders = numTraders

    def createTraders(self):
        numProsumers = 0
        traders = []
        while numProsumers < self.numTraders:
            tradingType = random.randint(0, 1)
            quantity = random.randint(self.minQuantity, self.maxQuantity)
            price =  round(random.uniform(self.minPrice, self.maxPrice), 2)
            price2 = round(random.uniform(self.minPrice, price), 2)

            if tradingType == 0:
                tType = "B"
            else:
                tType = "S"

            traders.append(Prosumer(tType, quantity, price, numProsumers, "N", 0, -1, price2))

            numProsumers += 1

        return(traders)

# -------------------------------------------------------------------
# init global variables
# -------------------------------------------------------------------

# trading Periods
# P0 = tradingPeriod(0, 0.26, 0.10, 150, 25, 7)
# P1 = tradingPeriod(1, 0.30, 0.12, 200, 45, 4)
# P2 = tradingPeriod(2, 0.28, 0.20, 100, 50, 10)
# P3 = tradingPeriod(3, 0.35, 0.25, 300, 100, 14)
# P4 = tradingPeriod(4, 0.15, 0.05, 75, 10, 5)
# P5 = tradingPeriod(5, 0.16, 0.07, 125, 35, 8)

# tradePeriods = [P0, P1, P2, P3, P4, P5]

# -------------------------------------------------------------------
# functions
# -------------------------------------------------------------------

# iterate through buyers to order the best buyers for this seller
def perferedBuyers(buyers, seller):
    # create lists
    temp = []
    order = []

    # place eligible buyers into a list
    # print(len(buyers))
    for x in buyers:
        # print("price:", x.price, seller.price, "quantity:", x.quantity)
        if x.price >= seller.price and seller.quantity >= x.quantity:
            temp.append(x)

    # using a temp list reorder the list based on the total amount of money they can offer
    num = 0
    while len(temp) > num:
        cost = 0
        index = 0
        count = 0
        for x in temp:
            if x.price * x.quantity > cost:
                index = count
            count += 1
        order.append(temp[index])
        del temp[index]
        num += 1
        # print(len(temp))

    return(order)

def perferedSellers(sellers, buyer, seller, num):
    # create lists
    temp = []
    order = []

    #place eligible sellers into a list
    for x in sellers:
        if x.price <= buyer.price and x.quantity >= buyer.quantity:
            temp.append(x)
            # print(x)

    # using a temp list reorderthe list based on the cheapest sellers available
    while len(temp) > 0:
        cost = 10000
        index = 0
        count = 0
        for x in temp:
            if x.price * x.quantity < cost:
                index = count
            count += 1
        order.append(temp[index])
        del temp[index]
    if order[num].tradingNumber == seller.tradingNumber:
        return(1)
    else:
        return(0)

# place buyers and sellers into their own arrays
def set_buyers_sellers(traders):
    # number of buyers and sellers hard coded
    buyers = []
    sellers = []
    # add an if statement to only include prosumers who tradingStatus is "N"
    for x in traders:
        if x.tradingType == "B" and x.transactionStatus == "N":
            buyers.append(x)
        elif x.tradingType == "S" and x.transactionStatus == "N":
            sellers.append(x)

    return(buyers, sellers)

# finalise transaction between buyer and seller
# return updated trader info        
def transaction(buyer, seller):
    # init variables
    quantityTraded = 0
    cost = 0

    # find amount of energy being transfered and at what cost
    if buyer.quantity >= seller.quantity:
        quantityTraded = seller.quantity
    else:
        quantityTraded = buyer.quantity

    cost = round(quantityTraded * buyer.price, 2)

    # agree on trading price
    # tradingPrice = (abs(buyer.price) + abs(seller.price)) / 2
    tradingPrice = seller.price

    # update prosumers information
    buyer.updateQuantity(quantityTraded)
    buyer.updateMoneyTransfered(-cost)
    buyer.priceTraded = tradingPrice#buyer.price
    seller.priceTraded = tradingPrice#buyer.price
    seller.updateQuantity(quantityTraded)
    seller.updateMoneyTransfered(cost)

    # find out if prosumer is finished trading
    buyer.updateTransactionStatus()
    seller.updateTransactionStatus()

    buyer.updateTransactionPartner(seller.tradingNumber)
    seller.updateTransactionPartner(buyer.tradingNumber)


def matchProsumers(buyers, sellers, num):
    # select a seller
    for sell in sellers:
        # print("NEW SELLER", sell.tradingNumber)
        # time.sleep(2)
        
        # find the best buyers for selected seller
        possibleBuyers = perferedBuyers(buyers, sell)
        # may want to use num here instead of 0
        # print("e", len(possibleBuyers))
        if len(possibleBuyers) > 0:
            while (1):
                for buy in possibleBuyers:
                    # iterating through selected buyers find if this seller is their perfered seller
                    # print("num", num)
                    # print(buy.tradingNumber)
                    if perferedSellers(sellers, buy, sell, num) == 1:
                        # matched prosumers -> update transaction info and del from lists
                        # print("match!!!")
                        transaction(buy, sell)
                        return(1)
                num += 1
        if len(possibleBuyers) == 0:
            sell.updateTransactionStatus()
    return(0)
            
def firstTradingRound(traders):
    # placing buyers and sellers into own array
    buyers, sellers = set_buyers_sellers(traders)
    num = 0
    while len(buyers) > 0 and len(sellers) > 0:
        matchProsumers(buyers, sellers, num)
        buyers, sellers = set_buyers_sellers(traders)

    for x in traders:
        if x.transactionPartner == -1:
            x.transactionStatus = "N"
        # print("Type:", x.tradingType, "Number", x.tradingNumber, "matched prosumer", x.transactionPartner)

def secondTradingRound(traders):
    # placing buyers and sellers into own array
    buyers, sellers = set_buyers_sellers(traders)
    num = 0

    # swap buyers and sellers price to second round prices
    for x in buyers:
        x.secondRoundPrice()

    for x in sellers:
        x.secondRoundPrice()            

    # print("Second Round")
    # print(len(sellers))
    # for x in sellers:
    #     print(x.tradingNumber, x.transactionStatus, x.transactionPartner)

    while len(buyers) > 0 and len(sellers) > 0:
        matchProsumers(buyers, sellers, num)
        buyers, sellers = set_buyers_sellers(traders)

    # for x in traders:
        # print("Type:", x.tradingType, "Number", x.tradingNumber, "matched prosumer", x.transactionPartner)

def data(traders):
    data = []

    # place all the buyers who completed a trade into a list
    for x in traders:
        if x.transactionStatus == "C" and x.tradingType == "B":
            data.append(x)
    # print(len(data))

    if len(data) == 0:
        return 0, 0, 0
    
    # make a list data point
    energyTraded = 0
    maxPrice = 0
    minPrice = 100

    for x in data:
        energyTraded += x.energyTraded
        if x.priceTraded > maxPrice:
            maxPrice = x.priceTraded
        if x.priceTraded < minPrice:
            minPrice = x.priceTraded

    priceRange = maxPrice - minPrice
    if priceRange < 0.10:
        priceRange = 0.10
    # priceRangeInterval = priceRange/5
    priceRangeInterval = priceRange/10

    # print(maxPrice, minPrice, priceRange)

    quantity = []
    tempNum = 0
    # now add aditional boundaries
    if (minPrice-2*priceRangeInterval) >= 0:
        # quantity.append(0.05)
        # quantity.append(0.05)
        quantity.append(0.1)
        quantity.append(0.1)
        tempNum = 1
    elif (minPrice-priceRangeInterval) >= 0:
        # quantity.append(0.05)
        quantity.append(0.1)
        tempNum = 2

    temp = []
    count = 0



    # error handling if no energy was traded this round
    if energyTraded == 0:
        price = []
        return(quantity, price)

    while count < 11:
        energyTradedRound = 0
        for x in data:
            # unhappy with this line here
            # want to find the amount of energy traded in this round
            if ((minPrice+count*priceRangeInterval) <= x.priceTraded and x.priceTraded < (minPrice+(count+1)*priceRangeInterval)):
                energyTradedRound += x.energyTraded
        count += 1

    if tempNum == 1:
        # temp.append(energyTradedRound/(1.2*energyTraded))
        temp.append(energyTradedRound/(1.4*energyTraded))
    if tempNum == 2:
        # temp.append(energyTradedRound/(1.15*energyTraded))
        temp.append(energyTradedRound/(1.3*energyTraded))
    if tempNum == 0:
        # temp.append(energyTradedRound/(1.1*energyTraded))
        temp.append(energyTradedRound/(1.2*energyTraded))
    
    for x in temp:
        quantity.append(x)
    
    quantity.append(0.1)
    quantity.append(0.1)
    # make sure selection of price doesn't get too small
    if len(quantity) < 6:
        while len(quantity) < 10:
            quantity.append(0.1)
    # print("hi", len(quantity))
    if sum(quantity) > 1.0:
        temp = []
        for x in quantity:
            temp.append(x/sum(quantity))
        quantity = []
        for x in temp:
            quantity.append(x)

    price = []
    if tempNum == 1:
        price.append(minPrice - priceRangeInterval)
    if tempNum == 2:
        price.append(minPrice - 2*priceRangeInterval)
        price.append(minPrice - priceRangeInterval)

    x = 0
    while x < (len(quantity) - tempNum):
        price.append(minPrice + priceRangeInterval*x)
        x += 1

    if len(price) > 0:
        globalPrice = []
        globalQuantity = []
        for x in price:
            globalPrice.append(x)
        for x in quantity:
            globalQuantity.append(x)
        globalEnergyTraded = energyTraded
        # print("start")
        # for x in globalQuantity:
        #     print(x)
        # print("end")
        return(quantity, price, energyTraded)

    



# -------------------------------------------------------------------
# main
# -------------------------------------------------------------------

# data set 1
# P1 = Prosumer("B", 50, 0.05, 0, "N", 0, -1, 0.02, 0, 0)
# P2 = Prosumer("B", 75, 0.15, 1, "N", 0, -1, 0.12, 0, 0)
# P3 = Prosumer("B", 100, 0.25, 2, "N", 0, -1, 0.22, 0, 0)
# P4 = Prosumer("B", 150, 0.35, 3, "N", 0, -1, 0.32, 0, 0)
# P5 = Prosumer("B", 200, 0.45, 4, "N", 0, -1, 0.42, 0, 0)
# P6 = Prosumer("S", 50, 0.05, 5, "N", 0, -1, 0.07, 0, 0)
# P7 = Prosumer("S", 75, 0.15, 6, "N", 0, -1, 0.17, 0, 0)
# P8 = Prosumer("S", 100, 0.25, 7, "N", 0, -1, 0.27, 0, 0)
# P9 = Prosumer("S", 150, 0.35, 8, "N", 0, -1, 0.37, 0, 0)
# P10 = Prosumer("S", 200, 0.45, 9, "N", 0, -1, 0.47, 0, 0)

# data set 2
# P1 = Prosumer("B", 50, 0.05, 0, "N", 0, -1, 0.02, 0, 0)
# P2 = Prosumer("B", 75, 0.15, 1, "N", 0, -1, 0.12, 0, 0)
# P3 = Prosumer("B", 100, 0.25, 2, "N", 0, -1, 0.22, 0, 0)
# P4 = Prosumer("B", 150, 0.30, 3, "N", 0, -1, 0.35, 0, 0)
# P5 = Prosumer("B", 200, 0.40, 4, "N", 0, -1, 0.45, 0, 0)
# P6 = Prosumer("S", 50, 0.05, 5, "N", 0, -1, 0.07, 0, 0)
# P7 = Prosumer("S", 75, 0.15, 6, "N", 0, -1, 0.17, 0, 0)
# P8 = Prosumer("S", 100, 0.25, 7, "N", 0, -1, 0.27, 0, 0)
# P9 = Prosumer("S", 150, 0.40, 8, "N", 0, -1, 0.35, 0, 0)
# P10 = Prosumer("S", 200, 0.50, 9, "N", 0, -1, 0.45, 0, 0)

# data set 3
P1 = Prosumer("B", 70, 0.05, 0, "N", 0, -1, 0.25, 0, 0)
P2 = Prosumer("B", 25, 0.30, 1, "N", 0, -1, 0.20, 0, 0)
P3 = Prosumer("B", 80, 0.17, 2, "N", 0, -1, 0.17, 0, 0)
P4 = Prosumer("B", 150, 0.28, 3, "N", 0, -1, 0.13, 0, 0)
P5 = Prosumer("S", 250, 0.22, 4, "N", 0, -1, 0.25, 0, 0)
P6 = Prosumer("S", 30, 0.23, 5, "N", 0, -1, 0.18, 0, 0)
P7 = Prosumer("S", 70, 0.60, 6, "N", 0, -1, 0.23, 0, 0)
P8 = Prosumer("S", 130, 0.29, 7, "N", 0, -1, 0.33, 0, 0)
P9 = Prosumer("S", 80, 0.18, 8, "N", 0, -1, 0.17, 0, 0)
P10 = Prosumer("S", 150, 0.05, 9, "N", 0, -1, 0.07, 0, 0)
traders = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10]

def doubleAuction(traders):
    # for x in traders:
    #     print(x.tradingType, round(x.quantity, 2), round(x.price, 2), x.tradingNumber)
    firstTradingRound(traders)
    # print("First Trading Round Complete")
    # for x in traders:
    #     print(x.tradingNumber, x.transactionStatus, x.transactionPartner)
    
    secondTradingRound(traders)
    # print("Second Trading Round")
    # for x in traders:
    #     print(x.tradingNumber, x.transactionStatus, x.transactionPartner)
    
    return(traders)

doubleAuction(traders)