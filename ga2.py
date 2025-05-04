import math
import random

GENERASI = 10000
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.1
PANJANG_CHROMOSOME = 22
JUMLAH_POPULASI = 5
PANJANG_X = 11

def biner_to_decimal(biner):
    result: float = 0
    for i in range(0, len(biner)):
        if biner[i] == "1":
            result += 2 ** (len(biner) - i - 1)

    return result

def decode_chromosome(x):
    decimal = biner_to_decimal(x)
    decimal = (decimal - 1000) / 100

    return decimal

def is_valid_chromosome(chromosome):
  return (-10 <= decode_chromosome(chromosome[:PANJANG_X]) <= 10 and -10 <= decode_chromosome(chromosome[PANJANG_X:]) <= 10)

def inisiasi_populasi():
  populasi = []
  i = 0
  while i < JUMLAH_POPULASI:
    calon_populasi = (''.join(random.choice(['0', '1']) for _ in range(PANJANG_CHROMOSOME)))

    if (is_valid_chromosome(calon_populasi) and not calon_populasi in populasi):
      populasi.append(calon_populasi)
      i+=1

  return populasi

def hitung_fitness(chromosome):
  x1 = decode_chromosome(chromosome[:PANJANG_X])
  x2 = decode_chromosome(chromosome[PANJANG_X:])
  return -1 * (math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + (3/4) * math.exp(1 - math.sqrt(x1*x1)))

def seleksi_turnamen(populasi, pemenang = 2):
  populasi_terpilih = []

  for i in range(2):
    for pop in populasi:
      if (hitung_fitness(pop) == min([hitung_fitness(chrom) for chrom in populasi])):

        populasi_terpilih.append(pop)
        populasi.remove(pop)
        break


  return populasi_terpilih

def cross_over(populasi):
  if (round(random.uniform(0, 1), 1) <= CROSSOVER_RATE):
    while (True):
      titik_potong = random.randint(1, PANJANG_CHROMOSOME - 1)
      chrome1 = populasi[0][:titik_potong] + populasi[1][titik_potong:]
      chrome2 = populasi[1][:titik_potong] + populasi[0][titik_potong:]
      
      if (is_valid_chromosome(chrome1) and is_valid_chromosome(chrome2)):
        break
    return [chrome1, chrome2]
  else:
    return populasi

def mutasi(populasi):
  for i, pop in enumerate(populasi):
    for j in range(math.floor(MUTATION_RATE * PANJANG_CHROMOSOME)):
      list_pop = [k for k in pop]
      rand_int = random.randint(0, 21)
      list_pop[rand_int] = '1' if list_pop[rand_int] == '0' else '0'
      
      chromosome_str = ''.join(list_pop);
      if (is_valid_chromosome(chromosome_str)):
        populasi[j] = chromosome_str
  return populasi

#populasi baru yang berasal dari populasi terbaik
def regenerasi_populasi(populasi, populasi_keseluruhan):
  chromosome_terbaik = populasi[0] if hitung_fitness(populasi[0]) >  hitung_fitness(populasi[0]) else populasi[1]
  populasi_baru = []
  populasi_baru.append(chromosome_terbaik)

  while (len(populasi_baru) < 5):
    
    calon_chromosome = cross_over(mutasi([chromosome_terbaik, chromosome_terbaik]))
    
    for calon in calon_chromosome:
      if (not (calon in populasi_keseluruhan)):
        populasi_baru.append(calon)

  return populasi_baru, chromosome_terbaik


chromosome_paling_baik = ""
populasi_keseluruhan = []
populasi = inisiasi_populasi()
[populasi_keseluruhan.append(pop) for pop in populasi]

for i in range(GENERASI):
  populasi = seleksi_turnamen(populasi)
  populasi = cross_over(populasi)
  populasi = mutasi(populasi)
  populasi, chromosome_terbaik = regenerasi_populasi(populasi, populasi_keseluruhan)
  [populasi_keseluruhan.append(pop) for pop in populasi]
#   print(f"Generasi ke-{i+1}")
#   print(f"Chromosome Terbaik: {chromosome_terbaik}")
#   print(f"Nilai x1: {decode_chromosome(chromosome_terbaik[:PANJANG_X])}")
#   print(f"Nilai x2: {decode_chromosome(chromosome_terbaik[PANJANG_X:])}")
#   print(f"Nilai fitness: {hitung_fitness(chromosome_terbaik)}")
#   print()
  chromosome_paling_baik = chromosome_terbaik if hitung_fitness(chromosome_terbaik) < hitung_fitness(chromosome_paling_baik) else chromosome_paling_baik

print(f"Chromosome Paling Baik: {chromosome_paling_baik}")
print(f"Nilai Objetivenya: {hitung_fitness(chromosome_paling_baik)}")
print(f"Nilai x1: {decode_chromosome(chromosome_paling_baik[:PANJANG_X])}")
print(f"Nilai x2: {decode_chromosome(chromosome_paling_baik[PANJANG_X:])}")