from datetime import datetime
import json
from random import randint, uniform
from sys import argv
from time import sleep, time
from xmlrpc.client import DateTime

class Automaton :

    number : int
    #random de 47648 a 47663
    type : int
    
    TankTemperature : float
    OutsideTemperature : float
    MilkWeight : int
    Ph : float
    K : int
    Naci : float
    Salmonel : int
    Ecoli : int
    Listeria : int
    generatedTime: DateTime

    def __init__(self, number):
        self.number = number
        self.type = randint(47648, 47663)

    def Generate(self):
        self.TankTemperatureGenerate()
        self.OutsideTemperatureGenerate()
        self.MilkWeightGenerate()
        self.PhGenerate()
        self.KGenerate()
        self.NaciGenerate()
        self.SalmonelGenerate()
        self.EcoliGenerate()
        self.ListeriaGenerate()
        self.generatedTime = datetime.utcnow()
    
    # Entre	2,5	et	4	degrés	par	dixième	de	degré
    def TankTemperatureGenerate(self):
        self.TankTemperature = round(uniform(2.5, 4), 2)
    
    # Entre	8	et	14degrés		par	dixième	de	degré
    def OutsideTemperatureGenerate(self):
        self.OutsideTemperature = round(uniform(8, 14), 2)

    # Entre	3512	kg	et	4607kg	par		incrément	de	1	kilo
    def MilkWeightGenerate(self):
        self.MilkWeight = randint(3512, 4607)
    
    # Entre	6,8	et	7,2	par	incrément de 1/10
    def PhGenerate(self):
        self.Ph = round(uniform(6.8, 7.2), 2)
    
    # Entre	35mg et	47	mg	/litres	par	pas	 de	1	mg
    def KGenerate(self):
        self.K = randint(35, 47)
    
    # Entre	1g	et	1,7	g	part	litre	par	pas de	0,1g
    def NaciGenerate(self):
        self.Naci = round(uniform(1, 1.7), 1)
    
    # Entre	17	et	37	ppm	,	par	incrément	de	1	ppm
    def SalmonelGenerate(self):
        self.Salmonel = randint(17, 37)
    
    # Entre	35	et	49	ppm	,	par	incrément	de	1	ppm
    def EcoliGenerate(self):
        self.Ecoli = randint(35, 49)
    
    # Entre	28 et 54 ppm	,	par	incrément	de	1	ppm
    def ListeriaGenerate(self):
        self.Listeria = randint(28, 54)
    
    def DictionnaryGenerate(self):
        return {
                "number" : self.number,
                "production" : {
                    "type" : self.type,
                    "TankTemperature" : self.TankTemperature,
                    "OutsideTemperature" : self.OutsideTemperature,
                    "MilkWeight" : self.MilkWeight,
                    "Ph" : self.Ph,
                    "K" : self.K,
                    "Naci" : self.Naci,
                    "Salmonel" : self.Salmonel,
                    "Ecoli" : self.Ecoli,
                    "Listeria" : self.Listeria,
                    "generatedTime" : str(self.generatedTime)
                }
        }

class Unit:

    number : int
    AutomatonList = []

    def __init__(self, number):
        self.number = number
        for i in range(10):
            self.AutomatonList.append(Automaton(i+1))

    def GenerateJsonFile(self):
        AutomatonDictionary = []

        for Automaton in self.AutomatonList:
            Automaton.Generate()
            AutomatonDictionary.append(Automaton.DictionnaryGenerate())
        
        dictionnary = {
            "unit" : {
                "number" : self.number,
                "Automaton" : AutomatonDictionary
            }
        }

        json_object = json.dumps(dictionnary)
        
        nameFile = "paramunite" + str(self.number) + "_" + str(time()) + ".json"

        if len(argv) > 2:
            # « paramunite _ »<numéro		unité> « _ »<date	unix	epoch> « .json »
            nameFile = argv[2] + "/" + nameFile
            
        with open(nameFile, "w") as outfile:
            outfile.write(json_object)

        print(json.loads(json_object))
        print(json.loads(json_object))

unit = Unit(int(argv[1]))

while(True):
    unit.GenerateJsonFile()
    sleep(60)