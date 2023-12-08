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
        "num_repeats": 1000
    },
    "world": {
        "size": (15,15),
        "empty_cell" : {"entity": "plain", "display": "⬜"},
        "entities": {
            "water": {"entity": "water", "symbol": "💧", "count": 20, "track": False},
            "conifer": {"entity": "conifer", "symbol": "🌲", "count": 5, "track": False},
            "leaf tree": {"entity": "leaf tree","symbol": "🌳", "count": 5, "track": False},
            "grass": {"entity": "grass", "symbol": "🌱", "count": 20, "track": True},
            "fox": {"entity": Creature("fox", "predator", 15, 15), "symbol": "🦊", "count": 5, "track": True},
            "rabbit": {"entity": Creature("rabbit", "prey", 15, 15), "symbol": "🐇", "count": 15, "track": True}
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
            entity_counts[entity["symbol"]] = {"initial": entity["count"], "recorded": []}

    progress_bar = tqdm(total=config["simulation"]["num_repeats"], desc="Simulation Progress", unit="repeat")

    for repeat in range(config["simulation"]["num_repeats"]):
        start_time = time.process_time()
        
        world = Grid(config["world"]["size"], config["world"]["empty_cell"])

        # Place entities
        for entity in config["world"]["entities"]:
            entity = config["world"]["entities"][entity]
            world.populate(entity["entity"], entity["symbol"], entity["count"])

        for turn in range(config["simulation"]["num_turns"]):

            creature_dict = []

            for row in world.grid:
                for cell in row:
                    if isinstance(cell.entity, Creature):
                        creature_dict.append({"cell" : cell,
                                               "creature": cell.entity})

            random.shuffle(creature_dict)

            for creature_object in creature_dict:
                if config["simulation"]["visualize"]:
                    clear_terminal()
                    print(f"Turn {turn + 1}")
                    world.show()
                    time.sleep(0.1)

                creature_cell = creature_object["cell"]
                creature = creature_object["creature"]

                if creature.alive:
                    surrounding_cells = creature_cell.get_surrounding_cells()

                    entity_cell_to_eat = None
                    entity_cell_to_drink = None

                    moved = False

                    for surrounding_cell in surrounding_cells:
                        entity_cell = surrounding_cell["cell"]
                        entity = entity_cell.entity

                        if (entity_cell_to_drink == None or entity_cell_to_eat == None):
                            if (
                                entity_cell_to_eat == None and (
                                    creature.role == "predator" and isinstance(entity, Creature) and entity.role == "prey" or
                                    creature.role == "prey" and entity == "grass"
                                )
                            ):
                                entity_cell_to_eat = entity_cell

                            if entity_cell_to_drink == None and entity == "water":
                                entity_cell_to_drink = entity_cell
                        else:
                            break

                    if entity_cell_to_eat != None:
                        creature.consume(entity_cell_to_eat.entity, "food")
                        entity_cell_to_eat.clear()

                        creature_cell.move(entity_cell_to_eat.position)

                        moved = True

                    if entity_cell_to_drink != None:
                        creature.consume(entity_cell_to_drink.entity, "drink")
                    
                    for surrounding_cell in surrounding_cells:
                        entity = surrounding_cell["cell"].entity

                        if creature.role == "prey" and isinstance(entity, Creature) and entity.role == "predator":
                            predator = surrounding_cell["cell"]

                            prey_x, prey_y = cell.position
                            predator_x, predator_y = predator.position

                            x_diff = predator_x - prey_x
                            y_diff = predator_y - prey_y

                            move_away_pos = (-1, -1)

                            if y_diff != 0:
                                move_away_pos = (prey_x, prey_y + y_diff // abs(y_diff))
                            elif x_diff != 0:
                                move_away_pos = (prey_x + prey_y // abs(x_diff), prey_y)

                            if creature_cell.move(move_away_pos):
                                moved = True

                    # Random move only if not moved already
                    if not moved:
                        creature_cell.move("random")
                else:
                    creature_cell.clear()

        # Count occurrences of each type of entity in the grid
        for row in world.grid:
            for cell in row:
                if cell.display in entity_counts:
                    entity_type = cell.display
                    recorded_list = entity_counts[entity_type]["recorded"]
                    while len(recorded_list) <= repeat:
                        recorded_list.append(0)
                    entity_counts[entity_type]["recorded"][repeat] += 1

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