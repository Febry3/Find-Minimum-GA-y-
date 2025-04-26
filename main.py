import math
from data import *
from helpher import *
from tabulate import tabulate

CROSSOVER_RATE = 0.69
MUTATION_RATE = 0.1
POPULATION_SIZE = 5
GENERATIONS = 100
BIT_LENGTH = 22
CHROMOSOME_LENGTH = 11

def initialize_poplations()->list :
    data: list = []
    populations: list = generate_initial_population()
    
    for i in range(len(populations)):
        data.append(InitialPopulationTable(i+1, populations[i].x1, populations[i].x2, populations[i].x1 + populations[i].x2, decode_chromosome(populations[i].x1),  decode_chromosome(populations[i].x2)))

    return data

def calculate_fitness_for_all_populations(populations: list)-> list:
    data: list = []

    sum_of_obj_val: int = 0

    for pop in populations:
        objective_val: int = calculate_objective_function(decode_chromosome(pop.x1), decode_chromosome(pop.x2))
        sum_of_obj_val+=objective_val
        data.append(CalculateFitnessTable(pop.id, pop.x1, pop.x2, objective_val))

    #masukkin fitness ke data
    adjusted_data = calculate_fitness([dt.val for dt in data])
    sum_adjusted_data = sum(adjusted_data)
    for i in range(len(data)):
        data[i].fitness = round(adjusted_data[i]/sum_adjusted_data, 3)

    #mengisi attribute cumulative pada array data
    temp: float = 0
    for i in range(len(data)):
        data[i].cumulative = data[i].fitness if i == 0 else (data[i].fitness + temp)
        temp += data[i].fitness 

    for i in range(len(data)):
        data[i].upper_interval = data[i].cumulative  if i == (len(data)-1) else data[i].cumulative
        data[i].lower_interval = 0 if i == 0 else data[i-1].cumulative + 0.001

    return data

def parent_selection(populations: list)-> list:
    selected_populations: list[CalculateFitnessTable] = []

    while len(selected_populations) < 2:
        random_num: float = round(random.uniform(0,1), 3)
        selected_candidate: CalculateFitnessTable = select_chromosome(random_num, populations)
        if(selected_candidate == None): continue

        if (not is_already_selected(selected_candidate, selected_populations) ):
            selected_populations.append(selected_candidate)
    
    return selected_populations

def cross_over(populations: list)-> list:
    cross_point: int = random.randint(1, 21)
    print(f'Cross Point ada pada titik ke-{cross_point}')
    
    if round(random.uniform(0, 1), 1) <= CROSSOVER_RATE:
        is_in_range: bool = False

        chromosome_1: CalculateFitnessTable = populations[0]
        chromosome_2: CalculateFitnessTable = populations[1]

        while (not is_in_range):
            t_chromosome_str_1 = chromosome_1.x1 + chromosome_1.x2
            t_chromosome_str_2 = chromosome_2.x1 + chromosome_2.x2

            t_chromosome_1 = t_chromosome_str_1[:cross_point] + t_chromosome_str_2[cross_point:]
            t_chromosome_2 = t_chromosome_str_2[:cross_point] + t_chromosome_str_1[cross_point:]

            chromosome_1.x1 = t_chromosome_1[:11]
            chromosome_1.x2 = t_chromosome_1[11:]

            chromosome_2.x1 = t_chromosome_2[:11]
            chromosome_2.x2 = t_chromosome_2[11:]
            
            is_in_range = -10 <= decode_chromosome(chromosome_1.x1) <= 10 and -10 <= decode_chromosome(chromosome_1.x2) <= 10 and -10 <= decode_chromosome(chromosome_2.x1) <= 10 and -10 <= decode_chromosome(chromosome_2.x2) <= 10
        
        return [chromosome_1, chromosome_2]
   
    print('Gagal Melakukan Cross Over')
    return populations
    

def mutate(populations: list)-> list:
    for pop in populations:
        chromosome: list = list(pop.x1+pop.x2)
        for i in range(math.floor(MUTATION_RATE * BIT_LENGTH)):
            chromosome[random.randint(0, BIT_LENGTH - 1)] = '1' if chromosome[random.randint(0, BIT_LENGTH - 1)] == '0' else '0'
        
        chromosome = ''.join(chromosome)

        if (not -10 <= decode_chromosome(chromosome[:CHROMOSOME_LENGTH]) <= 10 or not -10 <= decode_chromosome(chromosome[CHROMOSOME_LENGTH:]) <= 10):
            continue

        pop.x1 = chromosome[:CHROMOSOME_LENGTH]
        pop.x2 = chromosome[CHROMOSOME_LENGTH:]

    return populations

def evaluate_populations(populations: list)-> list:
    if populations[0].val < populations[1].val:
        return [populations[0]]
    else:
        return [populations[1]]
    
def regenerate_populations(old_populations: list)-> list:
    new_cross_over: list = cross_over(old_populations)
    new_mutations: list = mutate(old_populations)
    best_chromosome_from_old_population: list = evaluate_populations(old_populations)

    return [new_cross_over[0], new_cross_over[1], new_mutations[0], new_mutations[1], best_chromosome_from_old_population[0]]
    
def generate_step_1_table(populations:list)-> list:
    data: list = []    
    for i in range(len(populations)):
        data.append(InitialPopulationTable(i+1, populations[i].x1, populations[i].x2, populations[i].x1 + populations[i].x2, decode_chromosome(populations[i].x1),  decode_chromosome(populations[i].x2)))

    return data

if __name__=="__main__":
    data: list = initialize_poplations()
    best_chromosome = None
    
    for i in range(GENERATIONS):
        print(f'Iterasi ke-{i+1}\n\n')
        print('Tahap 1: Inisiasi / Regenerate')
        print(tabulate(generate_step_1_table(data), headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Chromosome (22 bits)', 'Decoded x1 Chromosome', 'Decoded x2 Chromosome']))
        data = calculate_fitness_for_all_populations(data)

        print('\n\n\nTahap 1.1: Menghitung Nilai Objektif dan Probabilitas Fitness')
        print(tabulate(data, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))

        data = parent_selection(data)
        print('\n\n\nTahap 2: Seleksi Parent Menggunakan Roullete Selection')
        print(tabulate(data, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))

        print('\n\n\nTahap 3: Crossover')
        data = cross_over(data)
        data = calculate_fitness_for_all_populations(data)
        print(tabulate(data, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))

        print('\n\n\nTahap 4: Mutation')
        data = mutate(data)
        data = calculate_fitness_for_all_populations(data)
        print(tabulate(data, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))

        print('\n\n\nTahap 5: Evaluasi (Chromosome yang unggul pada populasi ini adalah:)')
        current_best_chromosome = evaluate_populations(data)
        print(tabulate(current_best_chromosome, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))

        data = regenerate_populations(data)

        best_chromosome = evaluate_populations([current_best_chromosome[0], best_chromosome[0]]) if best_chromosome != None else current_best_chromosome

    print(f'\n\n\nChromosome Terbaik Setelah {GENERATIONS} Kali Iterasi')
    print(tabulate(best_chromosome, headers=['No', 'x1 (11 bits)', 'x2 (11 bits)', 'Objective Function', 'Fitness[i]', 'Cumulative', 'Lower Bound', 'Upper Bound']))
    print(f'x1: {decode_chromosome(best_chromosome[0].x1)}')
    print(f'x2: {decode_chromosome(best_chromosome[0].x2)}')