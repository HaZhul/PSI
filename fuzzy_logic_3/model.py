import numpy as np
from tank import *

import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Model_:
    def __init__(self, vel, stop_dist, break_dist, break_vel):
        self.vel = vel
        self.stop = stop_dist
        self.break_ = break_dist
        self.break_vel = break_vel
        self.delta_vel = self.vel - self.break_vel
        self.MAX_DIST = 6
        self.model = self.create_fuzzy()


    def create_fuzzy(self):

        dist = ctrl.Antecedent(np.linspace(0, self.MAX_DIST, 200000), 'dist')
        vel = ctrl.Consequent(np.linspace(-self.break_vel, self.vel + self.delta_vel, 2000), 'vel')

    
        dist['s'] = fuzz.trapmf(dist.universe, [0, 0, self.stop, self.stop])
        dist['m'] = fuzz.trapmf(dist.universe, [self.stop, self.stop, self.break_, self.break_])
        dist['l'] = fuzz.trapmf(dist.universe, [self.break_, self.break_, self.MAX_DIST, self.MAX_DIST])

        vel['s'] = fuzz.trimf(vel.universe, [-self.break_vel, 0, self.break_vel])
        vel['m'] = fuzz.trimf(vel.universe, [0, self.break_vel, self.vel])
        vel['l'] = fuzz.trimf(vel.universe, [self.vel - self.delta_vel, self.vel, self.vel + self.delta_vel])

        rules = [
            ctrl.Rule(dist['s'], vel['s']),
            ctrl.Rule(dist['m'], vel['m']),
            ctrl.Rule(dist['l'], vel['l']),
        ]

        ctrl_system = ctrl.ControlSystem(rules)
        model = ctrl.ControlSystemSimulation(ctrl_system)

        return model