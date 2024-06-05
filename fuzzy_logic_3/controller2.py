from tank import *
from model import Model_


# Parallel parking


class ParaParkController():

    def __init__(self, tank):
        self.tank = tank
        self.stage = 1
        self.velocity = 0

    def stage_func(self, dist):
        if self.stage == 1: return self.Stage1(dist)
        elif self.stage == 2: return self.Stage2(dist)
        elif self.stage == 3: return self.Stage3(dist)
        elif self.stage == 4: return self.Stage4(dist)

    def make_fuzzy_model(self):
        if self.stage == 1:
            self.model_ = Model_(
            vel=5,
            break_vel=3,
            stop_dist=0.7,
            break_dist=1.2,
        )
        elif self.stage == 2: 
            self.model_ = Model_(
            vel=2,
            break_vel=1,
            stop_dist=1.95,
            break_dist=2.5,
        )
        elif self.stage == 3:
            self.model_ = Model_(
            vel=1.5,
            break_vel=1,
            stop_dist=1,
            break_dist=1.4,
        )
        elif self.stage == 4:
            self.model_ = Model_(
            vel=1,
            break_vel=0.5,
            stop_dist=1,
            break_dist=1.1,
        )

    def turn_right_car(self, vel, vel1, vel2):
        self.tank.go()
        self.tank.leftvelocity =vel1*vel
        self.tank.rightvelocity=vel2*vel
        self.tank.setVelocity()


    def turn_left_car(self, vel, vel1, vel2):
        self.tank.go()
        self.tank.leftvelocity =vel1*vel
        self.tank.rightvelocity=vel2*vel
        self.tank.setVelocity()


    def control(self, dist, proximity_sensors, proximity_sensors_handles):
        while self.stage < 5:
            self.make_fuzzy_model()
            while self.stage_func(dist.get_dist_dic(proximity_sensors, proximity_sensors_handles)):
                pass
            print(f'Stage {self.stage} completed')
            self.stage += 1
        print('Parking completed!')



    def Stage1(self, distances):
        self.prev_val = self.velocity
        # self.model_.model.input['dist'] = distances['NE'] + distances['ES']
        self.model_.model.input['dist'] = 4 - distances['WN']
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
        self.model_.model.input['dist'] = distances['SW']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.turn_right_car(self.velocity, -1.65, -0.4)

        if self.velocity != self.prev_val and self.velocity == 0:
            return False
        else:
            return True
        
    def Stage3(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = distances['SW']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.turn_left_car(self.velocity, -0.6, -1.4)

        if self.velocity != self.prev_val and self.velocity == 0:
            return False
        else:
            return True

    def Stage4(self, distances):
        self.prev_val = self.velocity
        self.model_.model.input['dist'] = distances['NE']
        self.model_.model.compute()
        self.velocity = self.model_.model.output['vel']
        self.velocity = round(self.velocity, 2)
        self.turn_right_car(self.velocity, 1.35, 0.7)

        if self.velocity != self.prev_val and self.velocity == 0:
            return False
        else:
            return True