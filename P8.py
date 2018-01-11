# -*- coding: utf-8 -*-
# Created by Andrei Kisel
from random import randint


class Constants(object):

    START_PRICE = 10000

    GAS_MAX_OVERHAUL = 100000
    GAS_OVERHAUL_VALUE = 500
    GAS_AMORTIZATION = 9.5
    GAS_FUEL_CONSUMPTION = 0.08
    GAS_ENGINE_LIFETIME = 750000

    DIESEL_MAX_OVERHAUL = 150000
    DIESEL_OVERHAUL_VALUE = 700
    DIESEL_AMORTIZATION = 10.5
    DIESEL_FUEL_CONSUMPTION = 0.06
    DIESEL_ENGINE_LIFETIME = 650000

    GAS = 2.4
    DIESEL = 2.4
    ENGINE_REPLACING_COST = 3000.0

class FuelPrices:

    AI_92 = 2.2
    AI_95 = 2.5
    DIESEL = 2.4


class Car(object):
    """Constructor"""
    all_cars = []
    # Car initialization with all necessary params

    def __init__(self):
        self.name = "car - " + str(len(self.all_cars) + 1)
        # Selection eng type
        if not (len(self.all_cars) + 1) % 3:
            self.eng_type = "diesel"
            self.fuel_consumption = Constants.DIESEL_FUEL_CONSUMPTION
            self.fuel_price = Constants.DIESEL
            self.amortization = Constants.DIESEL_AMORTIZATION
            self.mileage_to_overhaul = Constants.DIESEL_MAX_OVERHAUL
            self.overhaul_price = Constants.DIESEL_OVERHAUL_VALUE
        else:
            self.eng_type = "gas"
            self.fuel_consumption = Constants.GAS_FUEL_CONSUMPTION
            self.fuel_price = Constants.GAS
            self.amortization = Constants.GAS_AMORTIZATION
            self.mileage_to_overhaul = Constants.GAS_MAX_OVERHAUL
            self.overhaul_price = Constants.GAS_OVERHAUL_VALUE
        # Selection fuel tank
        if not (len(self.all_cars) + 1) % 5:
            self.gas_tank_volume = 70
        else:
            self.gas_tank_volume = 60.0
        # Selection price
        self.price = Constants.START_PRICE
        # Divisor - average price of 1 km of run.
        self.mileage_to_util = self.mileage_to_utilisation()
        self.__mileage = 0
        # Random route for every car
        self.route = randint(56000, 286000)
        self.route_price = 0
        self.number_of_fueling = 0
        # Value fuel tank
        self.current_fuel_volume = self.gas_tank_volume
        self.all_cars.append(self)

    # Method for run
    def run(self):
        for _ in range(self.route):
            self.__mileage += 1
            self.current_fuel_volume -= self.fuel_consumption
            # Check
            if self.current_fuel_volume < self.fuel_consumption:
                self.route_price += self.gas_tank_volume * self.fuel_price
                self.current_fuel_volume = self.gas_tank_volume
                self.number_of_fueling += 1
            # Change parameters every 1000 km
            if not self.__mileage % 1000:
                self.price = round(self.price - self.amortization, 2)
            # Add overhaul price to route price
            if not self.__mileage % self.mileage_to_overhaul:
                self.route_price += self.overhaul_price


 # Methods for car state

    def mileage_to_utilisation(self):
        mileage = 0
        price = self.price
        while price > 0:
            mileage += 1000
            if not mileage % 1000:
                price -= self.amortization
            if not mileage % self.mileage_to_overhaul:
                price -= self.overhaul_price
        return mileage

    def mileage(self):
        return self.__mileage

    def residual_value(self):
        return self.price

    def fuelings(self):
        return self.number_of_fueling

    def fuel_price_for_route(self):
        return self.number_of_fueling * (self.fuel_price * self.gas_tank_volume)

    def route_to_utilization(self):
        return self.mileage_to_util - self.__mileage

    # Class with final info


class Engine(object):
    # List of all engines divided by type; 0 - diesel, 1 - gas
    all_engines = [[], []]
    # List of reclaimed engines
    reclaimed_engines = []

    def __init__(self, fuel_type, is_on_car=None):
        self.fuel_type = fuel_type
        self.is_on_car = is_on_car
        self.mileage = 0
        self.price = Constants.ENGINE_REPLACING_COST
        if fuel_type == "diesel":
            self.engine_number = "diesel_" + str(len(self.all_engines[0]) + 1)
            self.all_engines[0].append(self)
            self.engine_lifetime = Constants.DIESEL_ENGINE_LIFETIME
            self.fuel_consumption = Constants.DIESEL_FUEL_CONSUMPTION
        elif fuel_type == "gas":
            self.engine_number = "gas_" + str(len(self.all_engines[1]) + 1)
            self.all_engines[1].append(self)
            self.engine_lifetime = Constants.GAS_ENGINE_LIFETIME
            self.fuel_consumption = Constants.GAS_FUEL_CONSUMPTION
        # Change of fuel consumption every 1000 km
        self.fuel_consumption_delta = self.fuel_consumption * 0.01
        if not self.mileage % 1000:
            self.fuel_consumption += self.fuel_consumption_delta

    @property
    def current_fuel_price(self):
        if self.fuel_type == "gas":
            if self.mileage < 50000:
                self.fuel_price = FuelPrices.AI_92
            else:
                self.fuel_price = FuelPrices.AI_95
        else:
            self.fuel_price = FuelPrices.DIESEL
        return self.fuel_price

    # Calculation of engine conditions in %

    @property
    def engine_condition(self):
        return 100 - (self.mileage/self.engine_lifetime) * 100


class RezSort(object):

    # Method for sorting
    def mysort(self, list_of_cars):
        diesel_cars = []
        gas_cars = []
        dies_names = []
        gas_names = []
        for i in list_of_cars:
            if i.eng_type == "diesel":
                diesel_cars.append(i)
            elif i.eng_type == "gas":
                gas_cars.append(i)
        diesel_cars = sorted(diesel_cars, key=lambda car: car.price)
        gas_cars = sorted(gas_cars, key=lambda car: car.route_to_utilization())
        for i in diesel_cars:
            dies_names.append("{}: {}".format(i.name, i.route_to_utilization()))
        for i in gas_cars:
            gas_names.append("{}: {}".format(i.name, i.price))
        return dies_names, gas_names

    def full_price(self, list_of_cars):
        price = 0.0
        for _ in list_of_cars:
            price += _.price
        return price


for i in range(10):
    Car()

for car in Car.all_cars:
    print("\033[96mname\033[0m:\033[94m{}'\033[0m; \033[96mengine type\033[0m: \033[94m{}\033[0m; "
          "\033[96mtank volume\033[0m: \033[94m{}\033[0m; \033[96mprice\033[0m: \033[94m{}\033[0m;"
          " \033[96mroute\033[0m: \033[94m{}\033[0m.".format(car.name, car.eng_type, car.gas_tank_volume,
                                                             car.price, car.route))
    car.run()


info = RezSort()
print("\033[31mSorted cars\033[0m:", info.mysort(Car.all_cars))
print("\033[32mTotal cost of cars after the run\033[0m:", info.full_price(Car.all_cars))
