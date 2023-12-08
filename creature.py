class Creature():
    def __init__(self, species, role, hunger_threshold, thirst_threshold):
        """
        Initialize a Creature object.

        Args:
        - species (str): The species of the creature.
        - role (str): The role of the creature (predator or prey).
        - hunger_threshold (int): The threshold at which the creature dies of hunger.
        - thirst_threshold (int): The threshold at which the creature dies of thirst.

        Attributes:
        - hunger (int): Represents the creature's hunger level.
        - thirst (int): Represents the creature's thirst level.
        - alive (bool): Indicates if the creature is alive or dead.
        - species (str): The species of the creature.
        - role (str): The role of the creature (predator or prey).
        - hunger_threshold (int): The threshold at which the creature dies of hunger.
        - thirst_threshold (int): The threshold at which the creature dies of thirst.
        """
        self.hunger = 0
        self.thirst = 0               
        self.alive = True

        self.species = species
        self.role = role
        self.hunger_threshold = hunger_threshold, 
        self.thirst_threshold = thirst_threshold
                
    def consume(self, entity, type):
        """
        Simulate the creature consuming food or water.

        Args:
        - entity: The entity (food or water) being consumed.
        - type (str): The type of entity being consumed ('food' or 'water').
        """

        if isinstance(entity, Creature):
            entity.alive = False

        if type == "food":
            self.hunger = 0
        elif type == "water":
            self.thirst = 0
 
    def update_vitals(self):
        """
        Update the creature's hunger and thirst levels.

        This function increments the creature's hunger and thirst levels.
        If either level surpasses the respective threshold, the creature dies.
        """
        self.hunger += 1
        self.thirst += 1

        if self.hunger >= self.hunger_threshold or self.thirst >= self.thirst_threshold:
            self.alive = False