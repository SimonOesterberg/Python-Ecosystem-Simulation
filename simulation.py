from statistics import stdev
import time
import random
import os

from grid import Grid
from creature import Creature
from tqdm import tqdm
from boxchart import box_chart

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

config = {
    "simulation": {
        "visualize": False,
        "num_turns": 10,
        "num_repeats": 10000
    },
    "world": {
        "size": (15,15),
        "empty_cell" : {"entity": "plain", "display": "⬜"},
        "entities": {
            "water": {"entity": "water", "symbol": "💧", "count": 20, "track": False},
            "conifer": {"entity": "conifer", "symbol": "🌲", "count": 5, "track": False},
            "leaf tree": {"entity": "leaf tree","symbol": "🌳", "count": 5, "track": False},
            "grass": {"entity": "grass", "symbol": "🌱", "count": 20, "track": True},
            "fox": {"entity": Creature("fox", "predator", 5, 5), "symbol": "🦊", "count": 5, "track": True},
            "rabbit": {"entity": Creature("rabbit", "prey", 5, 5), "symbol": "🐇", "count": 15, "track": True}
        },
    }
}

def run_simulation(config):
    """
    Run the simulation based on the provided configuration.

    Args:
    - config (dict): Configuration settings for the simulation.

    This function initializes and runs the simulation based on the provided configuration.
    It populates the grid with entities, simulates their interactions over turns and repeats,
    collects statistics, and generates visualizations of the ecosystem.
    """

    clear_terminal()

    run_times = []  # Store the duration of each run
    entity_counts = {}

    for entity in config["world"]["entities"]:
        entity = config["world"]["entities"][entity]
        if entity["track"]:
            entity_counts[entity["symbol"]] = {"initial": entity["count"], "recorded": [0] * config["simulation"]["num_repeats"]}


    progress_bar = tqdm(total=config["simulation"]["num_repeats"], desc="Simulation Progress", unit="repeat")

    for repeat in range(config["simulation"]["num_repeats"]):
        start_time = time.process_time()
        
        world = Grid(config["world"]["size"], config["world"]["empty_cell"])

        # Place entities
        for entity in config["world"]["entities"]:
            entity = config["world"]["entities"][entity]
            world.populate(entity["entity"], entity["symbol"], entity["count"])

        for turn in range(config["simulation"]["num_turns"]):

            # Get all predators and prey in the world
            predators = []
            prey = []

            for row in world.grid:
                for cell in row:
                    if isinstance(cell.entity, Creature):
                        if cell.entity.role == "predator":
                            predators.append(cell)
                        elif cell.entity.role == "prey":
                            prey.append(cell)

            random.shuffle(predators)
            random.shuffle(prey)



            while len(predators) > 0 or len(prey) > 0:

                if config["simulation"]["visualize"]:
                    clear_terminal()
                    print(f"Turn {turn + 1}")
                    world.show()
                    time.sleep(0.1)

                if len(predators) != 0 and len(prey) != 0:
                    active_list = random.choice([predators, prey])
                    active_list_type = "predators" if active_list is predators else "prey"
                elif len(predators) != 0:
                    active_list = predators
                    active_list_type = "predators"
                else:
                    active_list = prey
                    active_list_type = "prey"
                    
                

                creature_cell = active_list[0]
                creature = active_list[0].entity

                if creature.alive:
                    surrounding_cells = creature_cell.get_surrounding_cells()

                    entity_cell_to_eat = None
                    entity_cell_to_drink = None

                    moved = False

                    if active_list_type == "predators":
                        for surrounding_cell in surrounding_cells:
                            entity_cell = surrounding_cell["cell"]
                            entity = entity_cell.entity

                            if (entity_cell_to_drink == None or entity_cell_to_eat == None):
                                if entity_cell_to_eat == None and isinstance(entity, Creature) and entity.role == "prey":
                                    entity_cell_to_eat = entity_cell
                                if entity_cell_to_drink == None and entity == "water":
                                    entity_cell_to_drink = entity_cell
                            else:
                                break
                    
                    elif active_list_type == "prey":
                        for surrounding_cell in surrounding_cells:
                            entity_cell = surrounding_cell["cell"]
                            entity = entity_cell.entity

                            if (entity_cell_to_drink == None or entity_cell_to_eat == None or not moved):
                                if entity_cell_to_eat == None and entity == "grass":
                                    entity_cell_to_eat = entity_cell
                                if entity_cell_to_drink == None and entity == "water":
                                    entity_cell_to_drink = entity_cell
                                if isinstance(entity, Creature) and entity.role == "predator":
                                    prey_x, prey_y = cell.position
                                    predator_x, predator_y = entity_cell.position

                                    x_diff = predator_x - prey_x
                                    y_diff = predator_y - prey_y

                                    move_away_pos = (-1, -1)

                                    if y_diff != 0:
                                        move_away_pos = (prey_x, prey_y + y_diff // abs(y_diff))
                                    elif x_diff != 0:
                                        move_away_pos = (prey_x + prey_y // abs(x_diff), prey_y)

                                    if creature_cell.move(move_away_pos):
                                        moved = True
                            else:
                                break


                    if entity_cell_to_eat != None:
                        creature.consume(entity_cell_to_eat.entity, "food")
                        entity_cell_to_eat.clear()

                        creature_cell.move(entity_cell_to_eat.position)
                        moved = True

                        if entity_cell_to_eat in prey:
                            prey.remove(entity_cell_to_eat)                        

                    if entity_cell_to_drink != None:
                        creature.consume(entity_cell_to_drink.entity, "drink")

                    # Random move only if not moved already
                    if not moved:
                        creature_cell.move("random")

                    creature.update_vitals()
                else:
                    creature_cell.clear()

                del active_list[0]

        # Count occurrences of each type of entity in the grid
        for row in world.grid:
            for cell in row:
                if cell.display in entity_counts:
                    entity_counts[cell.display]["recorded"][repeat] += 1

        end_time = time.process_time()
        duration = end_time - start_time
        run_times.append(duration)
        progress_bar.update(1)

    progress_bar.close()


    clear_terminal()
    
    plot = box_chart(list(entity_counts.values()), entity_counts.keys(), c = ["orange", "white", "green"])

    plot.xlabel('Entities')
    plot.ylabel('Counts')
    plot.title('Initial and Mean Counts of Entities')
    plot.legend()
    plot.tight_layout()
    plot.grid(axis='y', linestyle='--', alpha=0.7, zorder=1)  # Adding a grid behind the bars
    plot.show()

    mean_duration = sum(run_times) / len(run_times)
    std_dev_duration = stdev(run_times) if len(run_times) > 1 else 0

    mean_repeats_per_second = config["simulation"]["num_repeats"] / sum(run_times)
    std_dev_repeats_per_second = mean_repeats_per_second / mean_duration * std_dev_duration

    print(f"Mean repeats per second: {mean_repeats_per_second}")
    print(f"Standard deviation of repeats per second: {std_dev_repeats_per_second}")


run_simulation(config)