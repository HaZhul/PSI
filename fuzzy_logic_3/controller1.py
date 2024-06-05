from tank import *
from model import Model_


# Perpendicular parking

class PerpParkController():

    def __init__(self, tank):

        self.tank = tank
        self.stage = 1
        self.velocity = 0

    def stage_func(self, dist):
        if self.stage == 1: return self.Stage1(dist)
        elif self.stage == 2: return self.Stage2(dist)
        elif self.stage == 3: return self.Stage3(dist)
        elif self.stage == 4: return self.Stage4(dist)
        elif self.stage == 5: return self.Stage5(dist)

    def make_fuzzy_model(self):
        if self.stage == 1:
            self.model_ = Model_(
            vel=10,
            break_vel=3,
            stop_dist=1.55,
            break_dist=2.05,
        )
        elif self.stage == 2: 
            self.model_ = Model_(
            vel=5,
            break_vel=2,
            # stop_dist=1.15,
            stop_dist=1.1,
            break_dist=3,
        )
        elif self.stage == 3:
            self.model_ = Model_(
            vel=4,
            break_vel=2,
            stop_dist=1.5,
            break_dist=2,
        )
        elif self.stage == 4:
            self.model_ = Model_(
            vel=0.5,
            break_vel=0.1,
            stop_dist=4,
            break_dist=5,
        )
        elif self.stage == 5:
            self.model_ = Model_(
            vel=2,
            break_vel=1,
            stop_dist=0.7,
            break_dist=1.2,
        )

    def control(self, dist, proximity_sensors, proximity_sensors_handles):
        while self.stage < 6:
            self.make_fuzzy_model()
            while self.stage_func(dist.get_dist_dic(proximity_sensors, proximity_sensors_handles)):
                pass
            print(f'Stage {self.stage} completed')
            self.stage += 1
        print('Parking completed!')



    def Stage1(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = distances['NW']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.tank.forward(self.velocity)

        if self.velocity != self.prev_val and self.velocity == 0:
            return False
        else:
            return True


    def Stage2(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = distances['NE']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.tank.turn_left(-self.velocity)

        if self.velocity != self.prev_val and self.velocity == 0:
            return False
        else:
            return True
        
    def Stage3(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = distances['SE']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.tank.backward(self.velocity)


        if self.velocity == 0:
            return False
        else:
            return True

    def Stage4(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = 6.5 - distances['WS']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = self.velocity
        self.tank.turn_left(-self.velocity)

        if distances['WS'] > 2.3:
            return False
        else:
            return True
        
    def Stage5(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = 4 - (distances['NW'] + distances['NE'])/2
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = self.velocity
        self.tank.backward(self.velocity)

        if self.velocity != self.prev_val and round(self.velocity, 2) == 0:
            return False
        else:
            return True

