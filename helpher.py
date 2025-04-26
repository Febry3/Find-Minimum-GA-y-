import random
import numpy as np
from data import CalculateFitnessTable, Population
from main import CHROMOSOME_LENGTH, POPULATION_SIZE


#konversi biner ke decimal
def biner_to_decimal(chromosome: str)->float:
    result: float = 0
    for i in range(0, len(chromosome)):
        if chromosome[i] == "1": 
            result += 2 ** (len(chromosome) - i - 1)
        
    return result

#mendecode chromosome 11 bit
def decode_chromosome(chromosome: str)->float:
    decimal: float = biner_to_decimal(chromosome)
    decimal = (decimal - 1000) / 100

    return decimal

#ngegenerate populasi secara random dengan batas [-10, 10]
def generate_population_value()->str:
    candidate:str = ''.join(random.choice(['0', '1']) for _ in range(CHROMOSOME_LENGTH))

    while biner_to_decimal(candidate) > 2000:
        candidate = ''.join(random.choice(['0', '1']) for _ in range(CHROMOSOME_LENGTH))

    return candidate

#menginisiasi populasi awal
def generate_initial_population()->list:
    populations: list = []

    for i in range (POPULATION_SIZE):
        populations.append(Population(generate_population_value(), generate_population_value()));

    return populations

#fungsi objective
def calculate_objective_function(x1: int, x2: int)-> float:
    return round(-(np.sin(x1)*np.cos(x2)*np.tan(x1+x2) + (0.75 * np.exp(1 - np.sqrt(x1**2)))), 3)

#fungsi fitness dengan pemodifikasi untuk menghitung peluang dengan nilai fungsi objektif yang kecil memiliki kemungkinan yang besar
def calculate_fitness(populations_obj_values: list)-> float:
    min_obj: float = min(populations_obj_values)
    adjusted_objective_value = [1.0 / (float(pop + abs(min_obj)+1.0)) for pop in populations_obj_values]
    return adjusted_objective_value

def calculate_cumulative(populations_obj_values: list)-> list:
    cum_val: float = populations_obj_values[0]

    data: list = []
    for val in populations_obj_values[1:]:
        cum_val += val
        data.append(cum_val)

    print(data)
    return data

def select_chromosome(random_num: float, populations: list[CalculateFitnessTable])-> CalculateFitnessTable:
    for pop in populations:
        if pop.lower_interval >= random_num <= pop.upper_interval:
            return pop
    return None

def is_already_selected(population: CalculateFitnessTable, populations: list[CalculateFitnessTable])-> bool:
    for val in populations:
  
        if (val.x1+val.x2 == population.x1+population.x2):
            return True
        
    return False




