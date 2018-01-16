import random


class Constants(object):

    class EngineType(object):
        DIESEL = 'Diesel'
        GASOLINE = 'Gasoline'
        NEW_ENGINE_COST = 3000

    class DiesCarParam(object):

        CONSUMPTION = 6
        COST_OF_GAS = 1.8
        AMORTISATION = 10.5
        KMS_TILL_REPAIR = 150000
        COST_OF_REPAIR = 700

    class GasCarParam(object):

        CONSUMPTION = 8
        COST_OF_GAS_95 = 2.4
        COST_OF_GAS_92 = 2.2
        AMORTISATION = 9.5
        KMS_TILL_REPAIR = 100000
        COST_OF_REPAIR = 500
        FUEL_CHANGE = 50000

    class CommonCarParam(object):

        COST = 10000
        CONS_INCREMENT = 0.01
        TACHOGRAPH = 0


    class CarTanks(object):

        COMMON_TANK = 60
        CUSTOM_TANK = 75


    class CarParkConst(object):

        DEF_CARS_QUANTITY = 0
        PLACES = 500
        LIST_OF_CARS = None
        TOTAL_COST = 0
        TOTAL_CREDIT = 0
        DIESEL_CARS = None
        GASOLINE_CARS = None
        SORTED_GASOLINE = None
        SORTED_DIESEL = None



    class RaceConst(object):

        LENGTH = 0
        GAS_COST_TOTAL = 0
        QUANTITY_OF_GAS_RES = 0
        TOTAL_REPAIR_COST = 0





class GasolineCar(object):

    # Class ancestor of Car class creates gasoline cars

    def __init__(self,

                 engine_kind=Constants.EngineType.GASOLINE,

                 gas_consumption=Constants.GasCarParam.CONSUMPTION,

                 gas_cost=Constants.GasCarParam.COST_OF_GAS_92,

                 amortisation=Constants.GasCarParam.AMORTISATION,

                 km_till_rep=Constants.GasCarParam.KMS_TILL_REPAIR,

                 repair=Constants.GasCarParam.COST_OF_REPAIR):

        self.engine_kind = engine_kind

        self.gas_consumption = gas_consumption

        self.gas_cost = gas_cost

        self.amortisation = amortisation

        self.km_till_rep = km_till_rep

        self.repair = repair





class DieselCar(object):

    # Class ancestor of Car class creates diesel cars

    def __init__(self,

                 engine_kind=Constants.EngineType.DIESEL,

                 gas_consumption=Constants.DiesCarParam.CONSUMPTION,

                 gas_cost=Constants.DiesCarParam.COST_OF_GAS,

                 amortisation=Constants.DiesCarParam.AMORTISATION,

                 km_till_rep=Constants.DiesCarParam.KMS_TILL_REPAIR,

                 repair=Constants.DiesCarParam.COST_OF_REPAIR):

        self.engine_kind = engine_kind

        self.gas_consumption = gas_consumption

        self.gas_cost = gas_cost

        self.amortisation = amortisation

        self.km_till_rep = km_till_rep

        self.repair = repair





class Car(GasolineCar, DieselCar):

    # Car - main class inheritor for all machines, car_quantity allows to know how many cars were created

    car_quantity = 1



    def __init__(self,

                 gas_tank=Constants.CarTanks.COMMON_TANK,

                 cost=Constants.CommonCarParam.COST,

                 consumption_increment=Constants.CommonCarParam.CONS_INCREMENT,

                 tachograph=Constants.CommonCarParam.TACHOGRAPH,

                 engine_kind=Constants.EngineType.GASOLINE,

                 gas_consumption=Constants.GasCarParam.CONSUMPTION,

                 gas_cost=Constants.GasCarParam.COST_OF_GAS_92,

                 amortisation=Constants.GasCarParam.AMORTISATION,

                 km_till_rep=Constants.GasCarParam.KMS_TILL_REPAIR,

                 repair=Constants.GasCarParam.COST_OF_REPAIR):

        # Construction of Car

        super(Car, self).__init__(engine_kind,

                                  gas_consumption,

                                  gas_cost,

                                  amortisation,

                                  km_till_rep,

                                  repair)

        self.gas_tank = gas_tank

        self.cost = cost

        self.consumption_increment = consumption_increment

        self._tachograph = tachograph

        self.tank_custom()

        self.diesel_car()

        Car.car_quantity += 1



    def tank_custom(self):

        # Method for change volume of gasoline tank for every 5 car

        if Car.car_quantity % 5 == 0:

            self.gas_tank = Constants.CarTanks.CUSTOM_TANK



    def diesel_car(self):

        # Method which initialize creation of the diesel car

        if Car.car_quantity % 3 == 0:

            DieselCar.__init__(self)



    def ride(self, kilometres):

        assert kilometres > 0

        self._tachograph = kilometres



    @property

    def tachograph(self):

        return self._tachograph





class Race(object):

    # Class Race makes all actions which happens with car during race.

    lock_var = 0



    def __init__(self,

                 length=Constants.RaceConst.LENGTH,

                 gas_cost_total=Constants.RaceConst.GAS_COST_TOTAL,

                 quantity_of_gas_res=Constants.RaceConst.QUANTITY_OF_GAS_RES,

                 total_rep_cost=Constants.RaceConst.TOTAL_REPAIR_COST):

        self.length = length

        self.gas_cost_total = gas_cost_total

        self.quantity_of_gas_res = quantity_of_gas_res

        self.total_rep_cost = total_rep_cost



    def actions_with_car(self, car):

        # Returns results of all changes with car

        self.random_route()

        for step in range(0, self.length, 100):

            if car.cost < 0 and Race.lock_var == 0:

                self.engine_change(car)

                Race.lock_var += 1

            self.gas_restore(car, step)

            self.amortisation(car, step)

            self.repair_car(car, step)



    def random_route(self):

        # Creates random route for car

        self.length = random.randint(55000, 286000)

        return self.length



    def gas_restore(self, car, step):

        # Returns how many time car was fueled and quantity of refuels

        if step >= Constants.GasCarParam.FUEL_CHANGE and car.engine_kind == 'Gasoline':

            car.gas_cost = Constants.GasCarParam.COST_OF_GAS_95

        if step != 0 and step % 1000 == 0:

            car.gas_consumption = self.consumption_increment(car)

            car.ride(step)

        car.gas_tank -= car.gas_consumption

        if car.gas_tank <= 0:

            self.quantity_of_gas_res += 1

            self.gas_cost_total += car.gas_cost

            car.cost -= car.gas_cost



    @staticmethod

    def amortisation(car, step):

        # Returns cost of car after race

        if step != 0 and step % 1000 == 0:

            car.cost -= car.amortisation

        return car.cost



    @staticmethod

    def consumption_increment(car):

        # Returns new consumption of gasoline after race

        car.gas_consumption += car.gas_consumption * car.consumption_increment

        return car.gas_consumption



    @staticmethod

    def km_till_destroy(car):

        # Returns how many km car can make till utilisation

        if car.cost >= 0:

            cost_of_before = 0

            natural_amortisation = 1000 / (car.amortisation + 10 * car.gas_cost)

            kms_destroy = car.cost * natural_amortisation

            rep_decrement = kms_destroy // car.km_till_rep

            cost_of_before = car.cost - rep_decrement * car.repair

            kms_destroy = int(cost_of_before * natural_amortisation)

        else:

            kms_destroy = "Warning! Residual cost of your car is negative. " \
                          "Factory can\'t warrant when your car will be out of work!"

        return kms_destroy



    def repair_car(self, car, step):

        # Returns cost of repair

        if step != 0 and step % car.km_till_rep == 0:

            self.total_rep_cost += car.repair

            car.cost -= car.repair



    @staticmethod

    def engine_change(car):

        # Changes broken engine on new resets fuel type for gasoline cars

        car.cost -= Constants.EngineType.NEW_ENGINE_COST

        if car.engine_kind == 'Gasoline':

            car.gas_cost = Constants.GasCarParam.COST_OF_GAS_92





class CarPark(object):

    # Class CarPark

    def __init__(self,

                 create_cars=Constants.CarParkConst.DEF_CARS_QUANTITY,

                 places=Constants.CarParkConst.PLACES,

                 list_of_cars=Constants.CarParkConst.LIST_OF_CARS,

                 total_cost=Constants.CarParkConst.TOTAL_COST,

                 total_credit=Constants.CarParkConst.TOTAL_CREDIT,

                 diesel_cars=Constants.CarParkConst.DIESEL_CARS,

                 gasoline_cars=Constants.CarParkConst.GASOLINE_CARS,

                 sorted_gasoline=Constants.CarParkConst.SORTED_GASOLINE,

                 sorted_diesel=Constants.CarParkConst.SORTED_DIESEL):

        self.places = places

        self.create_cars = create_cars

        self.list_of_cars = list_of_cars

        self.total_cost = total_cost

        self.diesel_cars = diesel_cars

        self.gasoline_cars = gasoline_cars

        self.sorted_gasoline = sorted_gasoline

        self.sorted_diesel = sorted_diesel

        self.total_credit = total_credit



    def fill_car_park(self):

        # Fills park by cars

        self.list_of_cars = []

        for _ in range(self.create_cars):

            self.list_of_cars.append(Car())

        self.places -= len(self.list_of_cars)



    def car_statistic(self):

        # Returns stats of cars in park

        for car in self.list_of_cars:

            route = Race()

            route.actions_with_car(car)

            print ("Since creation car has made: {} km." \
                  "\nNow cost of car is: {}." \
                  "\nSince creation quantity of refuels: {}." \
                  "\nTotal cost of fuel: {}." \
                  "\nFull utilisation of car happens in: {}." \
                  "\nTotal cost of repairs: {}.\n" \
                  .format(route.length, car.cost,

                        route.quantity_of_gas_res,

                        route.gas_cost_total,

                        route.km_till_destroy(car),

                        route.total_rep_cost))



    def list_creation_gas(self):

        # Creates dicts of results for gasoline cars

        self.gasoline_cars = [Race().km_till_destroy(car) for car in self.list_of_cars

                              if car.engine_kind == 'Gasoline']



    def list_creation_dies(self):

        # Creates dicts of results for diesel cars

        self.diesel_cars = [car.cost for car in self.list_of_cars if car.engine_kind == 'Diesel']



    def sorting_of_list_gas(self):

        # Sorts results for gasoline cars

        self.list_creation_gas()

        self.sorted_gasoline = sorted(self.gasoline_cars, reverse=True)



    def sorting_of_list_dies(self):

        # Sorts results for diesel cars

        self.list_creation_dies()

        self.sorted_diesel = sorted(self.diesel_cars, reverse=True)



    def printing_sorted_res_gas_cars(self):

        # Returns results of sorting of gasoline cars

        self.sorting_of_list_gas()

        for element in self.sorted_gasoline:

            print ("KMs left till utilisation: {}".format(element))



    def printing_sorted_res_dies_cars(self):

        # Returns results of sorting of diesel cars

        self.sorting_of_list_dies()

        for element in self.sorted_diesel:

            if element > 0:

                print ("Cost of car: {}".format(element))

            else:

                print ("Credit of car: {}".format(abs(element)))



    def total_car_cos(self):

        # Returns total cost of cars in the park

        for car in self.list_of_cars:

            if car.cost > 0:

                self.total_cost += car.cost

            else:

                self.total_credit += abs(car.cost)

        print ("\nAt the moment total cost of cars is equal to {}." \
              "\nTotal credit for your cars is equal to {}. ".format(self.total_cost, self.total_credit))



    def car_park_stat(self):

        # Returns quantity of empty places in the park and how many cars are already in park

        print ("\nAt the moment park contains {} cars.\nEmpty places {}".format(self.create_cars, self.places))





if __name__ == '__main__':

    MinskTaxi = CarPark(10)

    MinskTaxi.fill_car_park()

    MinskTaxi.car_statistic()

    MinskTaxi.printing_sorted_res_gas_cars()

    MinskTaxi.printing_sorted_res_dies_cars()

    MinskTaxi.total_car_cos()

    MinskTaxi.car_park_stat()

