# Ecosystem Simulation

This project simulates an ecosystem where creatures interact with their environment, consume resources, and survive based on certain thresholds. It consists of the following files:

- [Files](#files)
  - [grid.py](#gridpy)
  - [creature.py](#creaturepy)
  - [boxchart.py](#boxchartpy)
  - [simulation.py](#simulationpy)
- [How to Use](#how-to-use)
  - [grid.py Example](#gridpy-example)
  - [creature.py Example](#creaturepy-example)
  - [boxchart.py Example](#boxchartpy-example)
  - [simulation.py Example](#simulationpy-example)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Notes](#notes)

## Files

### grid.py

Contains a Grid class that represents the environment as a grid. It populates the grid with different entities and allows for moving entities within the grid.

#### Usage Example

```python
# Example Usage
from grid import Grid

# Initialize a grid with a size of 5x5 and an empty cell entity
my_grid = Grid((5, 5), {"entity": None, "display": "."})

# Populate the grid with entities
my_grid.populate("entity_A", "A", 5)
my_grid.populate("entity_B", "B", 3, coordinates=[(1, 2), (3, 4)])

# Display the grid
my_grid.show()
```
### creature.py
Defines a Creature class that represents the entities within the ecosystem. Creatures have hunger and thirst thresholds and can consume food or water, updating their vital levels.

#### Usage Example
```python
from creature import Creature

# Creating a fox creature with hunger threshold 5 and thirst threshold 5
fox = Creature(species="fox", role="predator", hunger_threshold=5, thirst_threshold=5)

# Simulating the fox consuming food or water
# fox.consume(food_entity, "food")
# fox.consume(water_entity, "water")

# Updating the fox's vital levels
fox.update_vitals()
```

### boxchart.py
Provides a function box_chart to create a box chart using Matplotlib. This chart visualizes data for different labels, displaying initial and average values, as well as minimum and maximum values.

#### Usage Example
``` python
from boxchart import box_chart

# Example data
data = [
    {"initial": 10, "recorded": [8, 9, 7, 4, 6]},  # Data for label 1
    {"initial": 15, "recorded": [8, 6, 10, 12, 12]},  # Data for label 2
    # More data...
]
labels = ["Label 1", "Label 2"]

# Create a box chart
plot = box_chart(data, labels)
plot.show()
```
### simulation.py
The main simulation file. It utilizes the Grid and Creature classes to run a simulation of the ecosystem. It populates the grid with entities, simulates their interactions, collects statistics, and generates visualizations of the ecosystem.

#### Usage Example
Ensure you have Python installed and the necessary dependencies (matplotlib, numpy, tqdm). Then, run the simulation as follows:

``` python
from simulation import run_simulation
from creature import Creature

# Configuration settings for the simulation
config = {
    "simulation": {
        "visualize": True,
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
            "fox": {"entity": Creature("fox", "predator", 5, 5), "symbol": "🦊", "count": 5, "track": True},
            "rabbit": {"entity": Creature("rabbit", "prey", 5, 5), "symbol": "🐇", "count": 15, "track": True}
        },
    }
}

# Running the simulation based on the provided configuration
run_simulation(config)
```

## Configuration
The simulation behavior can be configured using the config dictionary in the simulation.py file. It allows setting parameters such as visualization, number of turns, and world size.

## Dependencies
matplotlib: For data visualization.
numpy: For numerical calculations.
tqdm: For displaying progress bars.

## Notes
The simulation visualizes the ecosystem dynamics and collects statistics on entity counts over multiple repeats.
