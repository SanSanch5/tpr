'''
Wolf-Sheep Predation Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
'''

import random

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from wolf_sheep.agents import Sheep, Wolf, GrassPatch
from wolf_sheep.schedule import RandomActivationByBreed


class WolfSheepPredation(Model):
    '''
    Wolf-Sheep Predation Model
    '''

    verbose = False  # Print-monitoring

    def __init__(self, height=20, width=20,
                 initial_sheep=150, initial_wolves=10,
                 sheep_reproduce=1, wolf_reproduce=40,
                 wolf_gain_from_food=15,
                 grass_regrowth_time=20, sheep_gain_from_food=4):
        '''
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Энергия для генерации новой овечки, забираемая у родителей 
            wolf_reproduce: --//-- волчонка --//--
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass
        '''

        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {"Wolves": lambda m: m.schedule.get_breed_count(Wolf),
             "Sheep": lambda m: m.schedule.get_breed_count(Sheep)})

        # Create sheep:
        for i in range(self.initial_sheep):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.sheep_gain_from_food)
            sheep = Sheep((x, y), self, True, energy)
            self.grid.place_agent(sheep, (x, y))
            self.schedule.add(sheep)

        # Create wolves
        for i in range(self.initial_wolves):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            energy = random.randrange(2 * self.wolf_gain_from_food)
            wolf = Wolf((x, y), self, True, energy)
            self.grid.place_agent(wolf, (x, y))
            self.schedule.add(wolf)

        # Create grass patches
        for agent, x, y in self.grid.coord_iter():

            fully_grown = random.choice([True, False])

            if fully_grown:
                countdown = self.grass_regrowth_time
            else:
                countdown = random.randrange(self.grass_regrowth_time)

            patch = GrassPatch((x, y), self, fully_grown, countdown)
            self.grid.place_agent(patch, (x, y))
            self.schedule.add(patch)

        self.running = True

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        if self.verbose:
            print([self.schedule.time,
                   self.schedule.get_breed_count(Wolf),
                   self.schedule.get_breed_count(Sheep)])

    def run_model(self, step_count=200):

        if self.verbose:
            print('Initial number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Initial number sheep: ',
                  self.schedule.get_breed_count(Sheep))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print('')
            print('Final number wolves: ',
                  self.schedule.get_breed_count(Wolf))
            print('Final number sheep: ',
                  self.schedule.get_breed_count(Sheep))
