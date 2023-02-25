from cmath import cos
from mimetypes import init
from handle_files import *
from copy import deepcopy
from math import floor
from random import randint


def main():
    instance = 4
    data, initial_solution = importSolution(
        "./instances/res_"+str(instance)+".txt", "./instances/cs"+str(instance)+".txt")
    print("Optimizing instance", instance)
    print("############################################################")
    #solution = multipleLocalDescent(data, initial_solution, 1250, instance)
    solution = globalDescent(data, initial_solution, 1, 1500, 0.1, instance)
    exportFile(instance, solution, "./instances/")
    return


def testAlgorithm(algo):
    for i in range(1, 16):
        file_name = "./instances/cs" + str(i) + ".txt"
        folder_name = "./" + algo.__name__ + "/"
        data = readFile(file_name)
        solution = algo(data)
        exportFile(i, solution, folder_name)
    return


########################################################################
#    ALGO 1
########################################################################

def algo1(data):
    hp_number = 0
    solution = [None for _ in range(data.vehicles_number)]
    vehicles_placed = []
    while('HP' in data.options[hp_number].name):
        hp_number += 1
        if hp_number >= data.options_number:
            break

    current_index = 0
    for v in data.vehicles:
        for hp in range(hp_number):
            if v.options[hp]:  # Si le véhicule a une option HP on l'insère
                # Décalage dans le tableau
                current_index += data.options[hp].ratio_p
                current_index = current_index % data.vehicles_number
                while (solution[current_index] is not None):  # On cherche une place libre
                    current_index += 1
                    current_index = current_index % data.vehicles_number
                solution[current_index] = v
                vehicles_placed.append(v.index)
                break

    # Tous les véhicules avec une hp ont été placés, on insère les autres
    current_index = 0
    for i in range(data.vehicles_number):
        if i not in vehicles_placed:  # Si le véhicule n'a pas été ajouté
            while (solution[current_index] is not None):  # On cherche une place libre
                current_index += 1
            solution[current_index] = data.vehicles[i]

    return solution


########################################################################
#    ALGO 2
########################################################################

def algo2(data):
    hp_number = 0
    solution = [None for _ in range(data.vehicles_number)]
    vehicles_placed = []
    while('HP' in data.options[hp_number].name):
        hp_number += 1
        if hp_number >= data.options_number:
            break

    current_index = 0
    for opt in range(data.options_number):
        for v in data.vehicles:
            # Si le véhicule a l'option hp consideree et n'est pas encore place
            if v.options[opt] and v.index not in vehicles_placed:
                # Décalage dans le tableau
                current_index += data.options[opt].ratio_p
                current_index = current_index % data.vehicles_number
                while (solution[current_index] is not None):  # On cherche une place libre
                    current_index += 1
                    current_index = current_index % data.vehicles_number
                solution[current_index] = v
                vehicles_placed.append(v.index)

    # Tous les véhicules avec une option ont été placés, on insère les autres
    current_index = 0
    for i in range(data.vehicles_number):
        if i not in vehicles_placed:  # Si le véhicule n'a pas été ajouté
            while (solution[current_index] is not None):  # On cherche une place libre
                current_index += 1
            solution[current_index] = data.vehicles[i]

    return solution


########################################################################
#    COST FUNCTION
########################################################################

def costFunction(data, list):
    cost = 0
    for opt in data.options:  # For each option
        for i in range(data.vehicles_number):  # For each window
            window_cost = -opt.ratio_n
            for j in range(i, i+opt.ratio_p):  # For each item in the window
                if j >= data.vehicles_number:
                    delta = 0
                else:
                    delta = int(list[j].options[opt.index])
                window_cost += delta
            cost += opt.weight * max(0, window_cost)
    return cost


########################################################################
#    ALGO DESCENT
########################################################################

def localDescent(data, initial_solution, move_index):
    buffer_solution = deepcopy(initial_solution)
    solution = deepcopy(initial_solution)
    min_cost = costFunction(data, initial_solution)
    for i in range(data.vehicles_number-1):
        new_index = (move_index+i) % data.vehicles_number
        v = buffer_solution.pop(new_index)
        new_index = (move_index+i+1) % data.vehicles_number
        buffer_solution.insert(new_index, v)
        new_cost = costFunction(data, buffer_solution)
        if new_cost < min_cost:
            min_cost = new_cost
            solution = deepcopy(buffer_solution)
    return solution, min_cost


def multipleLocalDescent(data, initial_solution, n, instance):
    print("Starting", n, "local descents")
    solution = deepcopy(initial_solution)
    old_cost = costFunction(data, initial_solution)
    print("initial cost :", old_cost)
    move_index = 0
    for i in range(n):
        solution, new_cost = localDescent(data, solution, move_index)
        print(i+1, '/', n, 'new cost :', new_cost)
        if new_cost == old_cost:  # Si le poids n'a pas change
            move_index = (move_index+1) % data.vehicles_number
        old_cost = new_cost

        if (i != 0 and i % 100 == 0):
            exportFile(instance, solution, "./inst/")
            print("Exported with a cost of", new_cost)
    return solution


def partShuffle(initial_solution, proportion):
    shuffled_solution = deepcopy(initial_solution)
    n = floor(proportion*len(initial_solution))
    for _ in range(n):
        i = randint(0, len(initial_solution)-1)
        v = shuffled_solution.pop(i)
        i = randint(0, len(initial_solution)-1)
        shuffled_solution.insert(i, v)
    return shuffled_solution


def globalDescent(data, initial_solution, m, n, proportion, instance):
    print("Starting", m, "global descents")
    solution = deepcopy(initial_solution)
    best_local_solution = deepcopy(initial_solution)
    best_local_min = costFunction(data, initial_solution)
    for i in range(m):
        print("Global :", i+1, "/", m)
        solution = partShuffle(solution, proportion)
        solution = multipleLocalDescent(data, solution, n, instance)

        if costFunction(data, solution) < best_local_min:
            best_local_min = costFunction(data, solution)
            best_local_solution = deepcopy(solution)

    print("Best local cost found :", best_local_min)
    return best_local_solution


if __name__ == '__main__':
    main()
