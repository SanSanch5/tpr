from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement

from wolf_sheep.agents import Wolf, Sheep, GrassPatch
from wolf_sheep.model import WolfSheepPredation


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    agent_cell_objs_without_grass = [obj for obj in agent.model.grid.get_cell_list_contents([agent.pos])
                                     if not isinstance(obj, GrassPatch)]

    sorted(agent_cell_objs_without_grass, key=lambda a: a.priority)
    if type(agent) is Sheep:
        # portrayal["Shape"] = "sheep.png"
        portrayal["Shape"] = "circle"
        portrayal["r"] = 0.7
        portrayal["Color"] = "Blue" if agent.gender == "m" else "Red"
        # https://icons8.com/web-app/433/sheep
        # portrayal["scale"] = 0.9
        portrayal["Layer"] = 1
        # portrayal["text"] = round(agent.energy)

        if agent_cell_objs_without_grass.index(agent) == 0:
            energies = str(round(agent.energy))
            for a in [obj for obj in agent_cell_objs_without_grass if obj != agent]:
                energies += "/" + str(a.energy)
            portrayal["text"] = energies
            portrayal["text_color"] = "Black"

    elif type(agent) is Wolf:
        portrayal["Shape"] = "rect"
        portrayal["h"] = 0.7
        portrayal["w"] = 0.7
        portrayal["Color"] = "Blue" if agent.gender == "m" else "Red"
        # portrayal["Shape"] = "wolf.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        # portrayal["scale"] = 0.9
        portrayal["Layer"] = 2

        if agent_cell_objs_without_grass.index(agent) == 0:
            energies = str(round(agent.energy))
            for a in [obj for obj in agent_cell_objs_without_grass if obj != agent]:
                energies += "/" + str(a.energy)
            portrayal["text"] = energies
            portrayal["text_color"] = "Black"

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = "#00AA00"
        else:
            portrayal["Color"] = "#D6F5D6"
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        # portrayal["text"] = agent.countdown
        # portrayal["text_color"] = "Black"
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


class AnimalsCount(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''
    def __init__(self):
        pass

    def render(self, model):
        wolves_m = model.schedule.get_breed_men_count(Wolf)
        sheep_m = model.schedule.get_breed_men_count(Sheep)
        wolves_f = model.schedule.get_breed_female_count(Wolf)
        sheep_f = model.schedule.get_breed_female_count(Sheep)
        return "Волки: %d Волчихи: %d Бараны: %d Овечки: %d" % (wolves_m, wolves_f, sheep_m, sheep_f)

canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 800, 800)
text_element = AnimalsCount()
chart_element = ChartModule([{"Label": "Wolves", "Color": "#AA0000"},
                             {"Label": "Sheep", "Color": "#666666"}])

server = ModularServer(WolfSheepPredation, [text_element, canvas_element, chart_element],
                       "Волки и овцы")
# server.launch()
