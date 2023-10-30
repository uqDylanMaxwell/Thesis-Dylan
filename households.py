production4 = [0, 10, 50, 60, 30, 18, 65, 34, 8, 20]
load4 = [5, 10, 20, 30, 36, 35, 40, 26, 15, 10]

# https://www.finder.com.au/how-much-energy-does-the-average-home-use
# 1 - 908kWh
# 2 - 1393kWh
# 3 - 1644kWh
# 4 - 2074kWh
# 5 - 2430kWh

# https://solarcalculator.com.au/solar-panels/brisbane/#:~:text=Brisbane%20solar%20power,-Sunny%20Brisbane%20is&text=Not%20only%20do%20Brisbane%20solar,21kWh%20of%20electricity%20every%20day.
# PV systems in summer
# 3kW -> 12.6kWh
# 4kW -> 16.8kWh
# 5kW -> 21.0kWh 
# 6.6kW -> 27.7kWh
# 10kW -> 42.0kWh
# [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# [0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2,    2, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0]
sunHours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, 0.25, 0.5, 0.5, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 0.5, 0.5, 0.25, 0.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # 18.5

sunDistribution = []
for x in sunHours:
    sunDistribution.append(round(x/sum(sunHours), 4))

PV3 = []
PV4 = []
PV5 = []
PV6 = []
PV10 = []

def distribute_sun(power, PV):
    for x in sunDistribution:
        PV.append(round(power*x, 2))

distribute_sun(12600, PV3)
distribute_sun(16800, PV4)
distribute_sun(21000, PV5)
distribute_sun(27700, PV6)
distribute_sun(42000, PV10)

load = [0.028, 0.028, 0.026, 0.026, 0.024, 0.024, 0.021, 0.021, 0.02, 0.02, 0.02, 0.02, 0.021, 0.021, 0.026, 0.026, 0.03, 0.03, 0.033, 0.033, 0.035, 0.035, 0.038, 0.038, 0.042, 0.042, 0.043, 0.043, 0.048, 0.048, 0.055, 0.055, 0.058, 0.058, 0.06, 0.06, 0.047, 0.047, 0.04, 0.04, 0.038, 0.038, 0.038, 0.038, 0.034, 0.034, 0.032, 0.032]

loadDistribution = []
for x in load:
    loadDistribution.append(round(x/sum(load), 4))

load1 = []
load2 = []
load3 = []
load4 = []
load5 = []

def distribute_load(watts, load):
    for x in loadDistribution:
        load.append(round(watts*x, 1))

distribute_load(908, load1)
distribute_load(1393, load2)
distribute_load(1644, load3)
distribute_load(2074, load4)
distribute_load(2430, load5)

#UK 05/08/2020
UKSolar = [0,0,0,0,0,0,0,0,0,0,0,0,0,9,84,276,545,823,1180,1610,2170,2810,3340,3860,4340,4670,4830,4600,4900,4750,4410,4050,3520,3290,2960,2660,2190,1600,1130,761,515,267,68,4,1,0,0,0]

