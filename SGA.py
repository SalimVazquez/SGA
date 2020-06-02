from random import choice, randint
from math import sin, pow
import matplotlib.pyplot as plot
import numpy as numpy

list_selection = []
list_crossover = []
list_mutation = []
list_result = []
list_padre_hijo = []
numbers_random = []
count_generations = 0

def print_list_selection(total_fitness, prom_fitness):
    for i in range(len(list_selection)):
        print(list_selection[i])
    print('Total fitness:',total_fitness,'\nAverage fitness:',prom_fitness)

def print_list_crossover():
    for i in range(len(list_crossover)):
        print(list_crossover[i])

def print_list_mutation():
    for i in range(len(list_mutation)):
        print(list_mutation[i])

def print_list_result():
    for i in range(len(list_result)):
        print(list_result[i])

def print_padre_hijo():
    print('<===Mejores resultados===>')
    for i in range(len(list_padre_hijo)):
        print(list_padre_hijo[i])

def createList(num_cromosomas):
    global list_selection
    global list_crossover
    global list_mutation

    for i in range(num_cromosomas):
        bit = ''.join(choice('01') for _ in range(num_bits))
        dict_selection =  {'Cromo #' : i, 'Poblation': bit, 'X' : 0,'Fitness' : 0, 'Prob':0, 'Exp count': 0, 'Act count': 0},
        dict_crossover =  {'Cromo #' : i, 'Mating pool': bit, 'Crossover Point' : 0, 'Offspring after XOver': 0, 'Value' : 0, 'Fitness' : 0,},
        dict_mutation =  {'Cromo #' : i, 'After XOver': 0,  'After XMutation': 0, 'X' : 0, 'Fitness' : 0},
        dict_padre_hijo = {'Bits padre':0, 'Fitness padre':0,'Bits hijo':0, 'Fitness hijo':0, 'Mejor fitness':0,'CadenaBits':0},
       # the lists extends of the dictionaries
        list_selection.extend(dict_selection)
        list_crossover.extend(dict_crossover)
        list_mutation.extend(dict_mutation)
        list_padre_hijo.extend(dict_padre_hijo)

def conversion_genotype_fenotype(aux_bits_pob, x_min, x_max):
    fenotype = 0
    aux_range = (x_max - x_min)
    Dx = aux_range/pow(2, len(aux_bits_pob))
    x = int(aux_bits_pob, 2)
    if x_min > x_max:
        fenotype = x_max + (x*Dx) # convertion of binary to decimal, after multiply DX, then we add the initial value of x
    else:
        fenotype = x_min + (x*Dx) # convertion of binary to decimal, after multiply DX, then we add the initial value of x
    return fenotype

def selection():
    global list_selection
    lim_max = 0
    sum_fitness = 0
    prom_fitness = 0
    print('  ___________________________________________________________________________________')
    print('<==============================Selection Generation #',count_generations,'==============================>')
    for i in range(num_cromosomas):
        # Calculate the value of X
        aux_bits_pob = list_selection[i].get('Poblation')
        x_value = conversion_genotype_fenotype(aux_bits_pob, x_min, x_max)
        list_selection[i].update({'X': x_value})
        # Calculate the fitness of the individuals
        fitness = (sin((4*x_value)) + (2*x_value))
        list_selection[i].update({'Fitness':fitness})
        # get the total fitness
        sum_fitness += list_selection[i].get('Fitness')
    #get the average of the fitness
    prom_fitness = (sum_fitness/len(list_selection))

    # calculate the prob and expected count
    for i in range(len(list_selection)):
        list_selection[i].update({'Prob': list_selection[i].get('Fitness')/sum_fitness})
        list_selection[i].update({'Exp count': list_selection[i].get('Fitness')/prom_fitness})
    # numbers randoms for actual count
    number_aleatory = numpy.random.randint(1,100,size=num_cromosomas)
    # actual count
    total_exp_count = 0
    i = 0

    for i in range(len(list_selection)):
        aux_exp_count = list_selection[i].get('Exp count')
        rounded_exp_count = round(aux_exp_count)
        total_exp_count += rounded_exp_count
        if total_exp_count <= num_cromosomas:
            list_selection[i].update({'Actual count': rounded_exp_count})
        else:
            break
    print_list_selection(sum_fitness, prom_fitness)
    position = 0
    for i in range(len(list_selection)):
        if list_selection[i].get('Actual count') != 0:
            for j in range(list_selection[i].get('Actual count')):
                list_crossover[position].update({'Mating pool': list_selection[i].get('Poblation')})
                list_padre_hijo[position].update({'Bits padre': list_selection[i].get('Poblation'), 'Fitness': list_selection[i].get('Fitness')})
                position+=1

def crossover():
    # variables auxiliar 
    chromosome_1 = ''
    chromosome_2 = ''
    aux_chromosome_1 = ''
    aux_chromosome_2 = ''
    global list_crossover
    global list_mutation
    print('  ___________________________________________________________________________________')
    print('<==============================Crossover Generation #',count_generations,'==============================>')
    for i in range(0, len(list_crossover), 2): # jumps of 2 positions
        # pointer of crossover in the bits
        pointer_crossover = randint(1, num_bits)
        # get the individual bits
        chromosome_1 = list_crossover[i].get('Mating pool')[0:pointer_crossover]
        # get the next individual bits
        chromosome_2 = list_crossover[i+1].get('Mating pool')[0:pointer_crossover]
        # get the last bits of the individual
        aux_chromosome_1 = list_crossover[i].get('Mating pool')[pointer_crossover:len(list_crossover[i].get('Mating pool'))]
        # get the last bits of the next individual
        aux_chromosome_2 = list_crossover[i+1].get('Mating pool')[pointer_crossover:len(list_crossover[i+1].get('Mating pool'))]
        # crossover 
        chromosome_1 = chromosome_1+aux_chromosome_2
        # crossover 
        chromosome_2 = chromosome_2+aux_chromosome_1
        # insert data in dictionary
        list_crossover[i].update({'Offspring after XOver': chromosome_1, 'Crossover Point': pointer_crossover})
        list_crossover[i+1].update({'Offspring after XOver': chromosome_2, 'Crossover Point': pointer_crossover})
        list_mutation[i].update({'After XOver':chromosome_1})
        list_mutation[i+1].update({'After XOver':chromosome_2})
        
    for i in range(len(list_crossover)):
        chromosome = str(list_crossover[i].get('Offspring after XOver'))
        chromosome = conversion_genotype_fenotype(chromosome, x_min, x_max)
        list_crossover[i].update({'Value': chromosome})

    for i in range(len(list_crossover)):
        # Calculate the value of X
        decimal = list_crossover[i].get('Value')
        # Calculate the fitness of the individuals
        fitness = (sin((4*decimal)) + (2*decimal))
        list_crossover[i].update({'Fitness': fitness})
    print_list_crossover()

def mutation():
    global list_mutation
    global count_generations
    numRand = 0
    print('  ___________________________________________________________________________________')
    print('<==============================Mutation Generation #',count_generations,'==============================>')
    for i in range(0, len(list_mutation), 2):
        # number random for mutation of the chromosome 1
        num_mutation_1 = (randint(1,100)/100)
        # number random for mutation of the chromosome 2
        num_mutation_2 = (randint(1,100)/100)
        bits_mutation = ''
        actual_bit = list_mutation[i].get('After XOver')
        if num_mutation_1 < prob_mutation:
            for data in actual_bit:
                # mutation of gen
                numRand = (randint(1,100)/100)
                if numRand < prob_gen:
                    if data == '1':
                        bits_mutation += '0'
                    else:
                        bits_mutation += '1'
                else:
                    bits_mutation += data
            list_mutation[i].update({'After XMutation': bits_mutation})
        else:
            list_mutation[i].update({'After XMutation':actual_bit})

        bits_mutation = list_mutation[i+1].get('After XOver')
        if num_mutation_1 < prob_mutation:
            for bit in bits_mutation:
                numRand = (randint(1,100)/100)
                if numRand < prob_gen:
                    if bit=='1':
                        bits_mutation += '0'
                    else:
                        bits_mutation += '1'
                else:
                    bits_mutation += bit
            list_mutation[i+1].update({'After XMutation' :bits_mutation})
        else:
            list_mutation[i+1].update({'After XMutation': bits_mutation})

    for i in range(len(list_mutation)):
        aux_bits = list_mutation[i].get('After XMutation')
        x_value = conversion_genotype_fenotype(aux_bits, x_min, x_max)
        list_mutation[i].update({'XValue': x_value})
        fitness = (sin((4*x_value)) + (2*x_value))
        list_mutation[i].update({'Fitness': fitness})
        list_padre_hijo[i].update({'Bits hijo': aux_bits, 'Fitness hijo': fitness})
        if list_padre_hijo[i].get('Fitness hijo') > list_padre_hijo[i].get('Fitness padre'):
            list_padre_hijo[i].update({'Mejor fitness': list_padre_hijo[i].get('Fitness hijo'), 'CadenaBits':list_padre_hijo[i].get('Bits hijo')})
        else:
            list_padre_hijo[i].update({'Mejor fitness': list_padre_hijo[i].get('Fitness padre'), 'CadenaBits':list_padre_hijo[i].get('Bits padre')})

    print_list_mutation()
    print_padre_hijo()

def updateTables():
    for i in range(num_cromosomas):
        if list_padre_hijo[i].get('Fitness hijo') > list_padre_hijo[i].get('Fitness padre'):
            list_selection[i].update({'Poblation': list_padre_hijo[i].get('Bits hijo')})
        else:
            list_selection[i].update({'Poblation': list_padre_hijo[i].get('Bits padre')})
        list_selection[i].update({'X':0, 'Fitness':0, 'Prob':0, 'Exp count':0, 'Act count':0})
    
    maximo = list_padre_hijo[0].get('Mejor fitness')
    minimo = list_padre_hijo[0].get('Mejor fitness')
    suma_fitness = list_padre_hijo[0].get('Mejor fitness')

    for i in range(1, len(list_padre_hijo)):
        aux_fitness = list_padre_hijo[i].get('Mejor fitness')

        if maximo < aux_fitness:
            maximo = aux_fitness
        if minimo > aux_fitness:
            minimo = aux_fitness
        
        suma_fitness += aux_fitness

    aux_prom = suma_fitness/num_cromosomas
    dictionaryResult = {'Num generation':count_generations, 'Maximo': maximo, 'Minimo': minimo, 'Promedio': aux_prom},
    print('GENERACION : ',count_generations,'\tMAXIMO =',maximo,"\tMINIMO = ",minimo,'\tTotal fitness',suma_fitness," \tPROMEDIO = ",aux_prom,'\n')
    list_result.extend(dictionaryResult)

def generate_graphics(scaleXMin, scaleXMax):
    global count_generations
    maximos = []
    minimos = []
    promedios = []
    generations = []
    for i in range(count_generations):
        maximos.append(list_result[i].get('Maximo'))
        minimos.append(list_result[i].get('Minimo'))
        promedios.append(list_result[i].get('Promedio'))
        generations.append(i+1)
    plot.plot(generations, maximos, color="blue", linewidth=2, linestyle="-", label="maximos")
    plot.plot(generations, minimos, color="red", linewidth=2, linestyle="--", label="minimos")
    plot.plot(generations, promedios, color="black", linewidth=2, linestyle="-.", label="maximos")
    plot.legend(loc='upper right')
    plot.xlabel('Generaciones')
    plot.ylabel('Fitness')
    plot.title('SGA - Simple Algorithm Genetic')
    limits = [scaleXMin, scaleXMax, min(minimos)-100, max(maximos)+100]
    plot.axis(limits)
    plot.grid()
    plot.show()

# Numbers of Chromosomes in the algorithm
aux_cromo = int(input('Ingrese el tamaño de la poblacion: '))
while aux_cromo < 1 or aux_cromo%2 != 0:
    aux_cromo = int(input('Por favor ingrese un numero mayor a 0 y par: '))
num_cromosomas = aux_cromo
# Limit bit string values
aux_bits = int(input('Ingrese el numero de bits a utilizar en los cromosomas: '))
while aux_bits < 1:
    aux_bits = int(input('Por favor ingrese un numero mayor a 0: '))
num_bits = aux_bits
# Numbers of iterations in the algorithm
aux_generations = int(input('Ingrese el numero de generaciones a realizar: '))
while aux_generations < 1:
    aux_generations = int(input('Por favor ingrese un numero mayor a 0: '))
num_generations = aux_generations
# Values max and mins of X
aux_x_min = float(input('Ingrese el valor minimo de X: '))
while aux_x_min < 1:
    aux_x_min = float(input('Por favor ingrese un valor mayor a 0 para el minimo de X: '))
x_min = aux_x_min
aux_x_max = float(input('Ingrese el valor maximo de X: '))
while aux_x_max < 1:
    aux_x_max = float(input('Por favor ingrese un valor mayor a 0 para el maximo de X: '))
x_max = aux_x_max
# probability of mutation of a chromosome
aux_prob_mutation = int(input('Ingrese la probabilidad de mutacion: '))
while aux_prob_mutation < 1 or aux_prob_mutation > 100:
    aux_prob_mutation = int(input('Ingrese una probabilidad de mutacion mayor a 0: '))
prob_mutation = aux_prob_mutation
# probability of mutation of a chromosome
aux_prob_gen = int(input('Ingrese la probabilidad de mutacion de un gen: '))
while aux_prob_gen < 1 or aux_prob_gen > 100:
    aux_prob_gen = int(input('Ingrese una probabilidad de mutacion mayor a 0: '))
prob_gen = (aux_prob_gen/100)  

createList(num_cromosomas)
for i in range(num_generations):
    count_generations += 1
    selection()
    crossover()
    mutation()
    updateTables()
print('<================Margenes de grafica=================>')
XScaleMin = float(input('Ingrese el margen minimo de X a mostrar en el grafico:'))
XScaleMax = float(input('Ingrese el margen maximo de X a mostrar en el grafico:'))
print_list_result()
generate_graphics(XScaleMin, XScaleMax)