class Option:
    def __init__(self, i, ratio1, ratio2, w, name):
        self.index = i
        self.ratio_n = ratio1
        self.ratio_p = ratio2
        self.weight = w
        self.name = name

class Vehicle:
    def __init__(self, i, opt):
        self.index = i
        self.options = opt # An array of bool

class Data:
    def __init__(self, o_number, options_array, v_number, vehicles_array):
        self.options_number = o_number
        self.options = options_array
        self.vehicles_number = v_number
        self. vehicles = vehicles_array

def readFile(file_name):
    f = open(file_name,"r")
    line = f.readline()
    option_number = int(line[8:])
    line = f.readline()
    vehicle_number = int(line[10:])
    
    for _ in range(3):
        line = f.readline()
    
    # Création des options
    options_array = []
    for i in range(option_number):
        array = line.split()
        opt = Option(i, int(array[0]), int(array[1]), int(array[2]), array[3])
        options_array.append(opt)
        line = f.readline()

    for _ in range(2):
        line = f.readline()

    # Création des véhicules
    vehicles_array = []
    for i in range(vehicle_number): # Les véhicules vont de 0 à N-1 et non pas de 1 à N
        array = line.split()
        bool_array = [ bool(int(n)) for n in array[1:] ]
        v = Vehicle(i, bool_array)
        vehicles_array.append(v)
        line = f.readline()

    f.close()
    return Data(option_number, options_array, vehicle_number, vehicles_array)

def exportFile(instance, vehicles_list, folder_name="./instances/"):
    file_name = folder_name + "res_" + str(instance) + ".txt"
    f = open(file_name, 'w')
    f.write("EQUIPE ")
    f.write("J_ai_cru_voir_un_Rominou")
    f.write('\n')
    f.write("INSTANCE ")
    f.write(str(instance))
    f.write('\n')
    
    for v in vehicles_list:
        f.write(str(v.index+1))
        f.write(' ')

    f.close()
    print("Fichier",file_name,"modifie.")
    return

def importSolution(sol_file_name, data_file_name):
    f = open(sol_file_name, 'r')
    for _ in range(3):
        line = f.readline()
    solution = line.split()
    solution = [int(n) for n in solution]
    f.close()
    data = readFile(data_file_name)
    vehicle_list = [data.vehicles[k-1] for k in solution]
    return data, vehicle_list