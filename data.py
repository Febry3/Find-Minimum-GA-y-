from dataclasses import dataclass

@dataclass
class Population:
    x1: str
    x2: str

@dataclass
class InitialPopulationTable:
    id: int
    x1: str
    x2: str
    chromosome: str 
    decoded_x1: float
    decoded_x2: float

@dataclass
class CalculateFitnessTable:
    id: int
    x1: str
    x2: str
    val: float
    fitness: float = 0
    cumulative: float = 0
    lower_interval: float = 0
    upper_interval: float = 0
    