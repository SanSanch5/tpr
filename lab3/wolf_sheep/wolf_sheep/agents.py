import random

from mesa import Agent

from wolf_sheep.random_walk import RandomWalker


class Sheep(RandomWalker):
    '''
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    '''

    energy = None
    priority = 1

    def __init__(self, pos, model, moore, energy=None):
        super().__init__(pos, model, moore=moore)
        self.energy = energy
        self.gender = random.choice(["m", "f"])

    def step(self):
        '''
        A model step. Move, then eat grass and reproduce.
        '''
        self.random_move()

        # Reduce energy
        self.energy -= 1

        # If there is grass available, eat it
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        grass_patch = [obj for obj in this_cell
                       if isinstance(obj, GrassPatch)][0]
        if grass_patch.fully_grown:
            self.energy += self.model.sheep_gain_from_food
            grass_patch.fully_grown = False

        # Death
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        elif self.energy >= self.model.sheep_reproduce:
            another_sheeps = [obj for obj in this_cell
                             if isinstance(obj, Sheep) and
                             obj.gender != self.gender and
                             obj.energy >= self.model.sheep_reproduce]
            if len(another_sheeps) > 0:
                another_sheep = random.choice(another_sheeps)
                # Create a new sheep:
                self.energy -= self.model.sheep_reproduce
                another_sheep.energy -= self.model.sheep_reproduce
                lamb = Sheep(self.pos, self.model, self.moore, random.randrange(2 * self.model.sheep_gain_from_food))
                self.model.grid.place_agent(lamb, self.pos)
                self.model.schedule.add(lamb)


class Wolf(RandomWalker):
    '''
    A wolf that walks around, reproduces (asexually) and eats sheep.
    '''

    energy = None
    priority = 0

    def __init__(self, pos, model, moore, energy=None):
        super().__init__(pos, model, moore=moore)
        self.energy = energy
        self.gender = random.choice(["m", "f"])

    def step(self):
        self.random_move()
        self.energy -= 1

        # If there are sheep present, eat one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        sheep = [obj for obj in this_cell if isinstance(obj, Sheep)]
        if len(sheep) > 0:
            sheep_to_eat = random.choice(sheep)
            self.energy += self.model.wolf_gain_from_food

            # Kill the sheep
            self.model.grid._remove_agent(self.pos, sheep_to_eat)
            self.model.schedule.remove(sheep_to_eat)

        # Death or reproduction
        if self.energy < 0:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        elif self.energy >= self.model.wolf_reproduce:
            another_wolves = [obj for obj in this_cell
                              if isinstance(obj, Wolf) and
                              obj.gender != self.gender and
                              obj.energy >= self.model.sheep_reproduce]
            if len(another_wolves) > 0:
                another_wolf = random.choice(another_wolves)
                # Create a new wolf cub
                self.energy -= self.model.wolf_reproduce
                another_wolf.energy -= self.model.wolf_reproduce
                cub = Wolf(self.pos, self.model, self.moore, random.randrange(2 * self.model.wolf_gain_from_food))
                self.model.grid.place_agent(cub, cub.pos)
                self.model.schedule.add(cub)


class GrassPatch(Agent):
    '''
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    '''

    def __init__(self, pos, model, fully_grown, countdown):
        '''
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        '''
        super().__init__(pos, model)
        self.fully_grown = fully_grown
        self.countdown = countdown

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1
