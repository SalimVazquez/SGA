from random import choice, randint
from math import sin
import matplotlib.pyplot as plot

list_selection = []
list_crossover = []
list_mutation = []
list_result = []
numbers_random = []
count_generations = 0

def createList(num_cromosomas):
    global list_selection
    global list_crossover
    global list_mutation

    for i in range(num_cromosomas):
        bit = ''.join(choice('01') for _ in range(num_bits))
        dictSeleccion =  {'Cromo #' : i, 'Poblation': bit, 'X' : 0,'Fitness' : 0, 'Prob':0, 'Exp count': 0, 'Act count': 0},
        dictCrossover =  {'Cromo #' : i, 'Mating pool': bit, 'Crossover Point' : 0, 'Offspring after XOver': 0, 'Value' : 0, 'Fitness' : 0,},
        dictMutation =  {'Cromo #' : i, 'After XOver': 0,  'After XMutation': 0, 'X' : 0, 'Fitness' : 0},
       # the lists extends of the dictionaries
        list_selection.extend(dictSeleccion)
        list_crossover.extend(dictCrossover)
        list_mutation.extend(dictMutation)

def selection():
    global list_selection
    lim_max = 0
    sum_fitness = 0
    prom_fitness = 0
    print('  ___________________________________________________________________________________')
    print('<==============================Selection Generation #',count_generations,'==============================>')
    for i in range(num_cromosomas):
        # Calculate the value of X
        decimal = int(list_selection[i].get('Poblation'),2)
        list_selection[i].update({'X': decimal})
        # Calculate the fitness of the individuals
        fitness = (sin((4*decimal)) + (2*decimal))
        list_selection[i].update({'Fitness':fitness})
        # get the total fitness
        sum_fitness += list_selection[i].get('Fitness')
    #get the average of the fitness
    prom_fitness = (sum_fitness/len(list_selection))

    for i in range(len(list_selection)):
        # get the probability of the individuals
        aux_prob = (list_selection[i].get('Fitness')/sum_fitness)
        # get the Exp count of the individuals
        aux_expected_count = (list_selection[i].get('Fitness')/prom_fitness)
        # update to table
        list_selection[i].update({'Prob': aux_prob, 'Exp count': aux_expected_count})

    # random for calculate the act count
    for i in range(num_cromosomas):
        numbers_random.append(randint(1,100))
    # numbers randoms for calculate the Act count
    for i in range(len(list_selection)):
        # variable set value of the probabilities * 100
        valor_max = 0
        for j in range(len(list_selection)):
            valor_max += (list_selection[j].get('Prob') * 100)
            if numbers_random[i] < valor_max:
                list_selection[j].update({'Act count': list_selection[j].get('Act count')+1})
                break

    posicion = 0
    # Print list of a generation
    printListSeleccion()
    # get the individuals for the cross, depending on the Act count
    for i in range(len(list_selection)):
        if(list_selection[i].get('Act count') != 0 ):
            for j in range(list_selection[i].get('Act count')):
                if posicion < num_cromosomas:
                    list_crossover[posicion].update({'Mating pool':list_selection[i].get('Poblation')})
                    pass
                else:
                    posicion = 0
                    list_crossover[posicion].update({'Mating pool':list_selection[i].get('Poblation')})
                    pass
                posicion +=1

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
        pointer_crossover = randint(1, num_cromosomas-1)
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
        list_crossover[i].update({'Offspring after XOver': chromosome_1, 'Crossover Point': pointer_crossover})
        list_crossover[i+1].update({'Offspring after XOver': chromosome_2, 'Crossover Point': pointer_crossover})
        list_mutation[i].update({'After XOver':chromosome_1})
        list_mutation[i+1].update({'After XOver':chromosome_2})
        
    for i in range(len(list_crossover)):
        chromosome = str(list_crossover[i].get('Offspring after XOver'))
        chromosome = int(chromosome,2)
        list_crossover[i].update({'Value': chromosome})

    for i in range(len(list_crossover)):
        # Calculate the value of X
        decimal = list_crossover[i].get('Value')
        # Calculate the fitness of the individuals
        fitness = (sin((4*decimal)) + (2*decimal))
        list_crossover[i].update({'Fitness': fitness})
    printListCrossover()

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
        actual_bit = ''
        actual_bit = list_mutation[i].get('After XOver')
        # print('=>Prob mutation:',prob_mutation,'\tIndividue:',num_mutation_1)
        if num_mutation_1 < prob_mutation:
            # print(num_mutation_1,' < ',prob_mutation,' Individuo ',i,' mutará')
            # print('Pi: ',prob_gen)
            # print('actualStringBits: ',actual_bit)
            for data in actual_bit:
                # mutation of gen
                numRand = (randint(1,100)/100)
                if prob_gen < numRand:
                    if data == '1':
                        bits_mutation += '0'
                    else:
                        bits_mutation += '1'
                else:
                    bits_mutation += data
            # print('Bit mutado: ',bits_mutation)
            list_mutation[i].update({'After XMutation': bits_mutation})
        else:
            # print(num_mutation_1, '> ',prob_mutation, 'individuo',i, 'no mutara')
            list_mutation[i].update({'After XMutation':actual_bit})

        bits_mutation = ''
        # print('=>Prob mutation:',prob_mutation,'\tIndividue:',num_mutation_2)
        bits_mutation = list_mutation[i+1].get('After XOver')
        if num_mutation_2 < prob_mutation:
            # print(num_mutation_2,' < ',prob_mutation,' Individuo ',i+1,' mutará')
            # print('Pi: ',prob_gen)
            # print('actualStringBits: ',bits_mutation)
            for bit in bits_mutation:
                numRand = (randint(1,100)/100)
                if prob_gen < numRand:
                    if bit=='1':
                        bits_mutation += '0'
                    else:
                        bits_mutation += '1'
                else:
                    bits_mutation += bit
            # print('Bit mutado:',bits_mutation)
            list_mutation[i+1].update({'After XMutation' :bits_mutation})
        else:
            # print(num_mutation_1,' > ',prob_mutation,' Individuo ',i+1,'no mutará')
            list_mutation[i+1].update({'After XMutation': bits_mutation})

    for i in range(len(list_mutation)):
        aux_decimal = int(list_mutation[i].get('After XMutation'),2)
        list_mutation[i].update({'XValue': aux_decimal})
        decimal = list_mutation[i].get('XValue')
        fitness = (sin((4*decimal)) + (2*decimal))
        list_mutation[i].update({'Fitness': fitness})

    # check the max, min and averages
    aux_max = list_mutation[0].get('Fitness')        
    aux_min = list_mutation[0].get('Fitness')
    prom = 0

    for i in range(len(list_mutation)):
        if aux_max < list_mutation[i].get('Fitness'):
            aux_max = list_mutation[i].get('Fitness')
        if aux_min > list_mutation[i].get('Fitness'):
            aux_min = list_mutation[i].get('Fitness')
        prom += list_mutation[i].get('Fitness')

    prom = (prom/num_cromosomas)
    dictResult = {'Num Generation' : count_generations, 'Maximo': aux_max, 'Minimo' : aux_min, 'Promedio' : prom},
    print('GENERACION : ',num_generations,'\tMAXIMO =',aux_max,"\tMINIMO = ",aux_min,"\tPROMEDIO = ",prom,'\n')
    list_result.extend(dictResult)

def updateTables(pobInitial):
    global list_selection
    global list_mutation
    printListMutation()
    for i in range(pobInitial):
        if(list_mutation[i].get('Fitness') >  list_selection[i].get('Fitness')):
            list_selection[i].update({'Initial population':list_mutation[i].get('After XMutation'), })
        list_selection[i].update({'Actual count':0})

def printListSeleccion():
    global list_selection
    global num_generations
    for i in range(len(list_selection)):
        print(list_selection[i])

def printListCrossover():
    global num_generations
    global list_crossover
    for i in range(len(list_crossover)):
        print(list_crossover[i])
    
def printListMutation():
    global num_generations
    global list_mutation
    for i in range(len(list_mutation)):
        print(list_mutation[i])

def printListResult():
    global num_generations
    global list_result
    for i in range(len(list_result)):
        print(list_result[i])

def generateGraphics():
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
aux_prob_mutation = int(input('Ingrese la probabilidad de mutacion: '))
while aux_prob_mutation < 1 or aux_prob_mutation > 100:
    aux_prob_mutation = int(input('Ingrese una probabilidad de mutacion mayor a 0: '))
prob_mutation = aux_prob_mutation
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
    updateTables(num_cromosomas)

printListResult()
generateGraphics()