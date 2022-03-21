from datetime import datetime
import json
from random import randint, uniform
import string
from sys import argv
from time import sleep, time
from xmlrpc.client import DateTime
import socket

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
                "type" : self.type,
                "production" : {
                    "tankTemperature" : self.TankTemperature,
                    "outsideTemperature" : self.OutsideTemperature,
                    "milkWeight" : self.MilkWeight,
                    "ph" : self.Ph,
                    "k" : self.K,
                    "naci" : self.Naci,
                    "salmonel" : self.Salmonel,
                    "ecoli" : self.Ecoli,
                    "listeria" : self.Listeria,
                    "generatedTime" : str(self.generatedTime)
                }
        }

class Unit:

    number : int
    AutomatonList = []
    nameFile : string

    def __init__(self, number, nameFile):
        self.number = number
        self.nameFile = nameFile
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
                "automatons" : AutomatonDictionary
            }
        }

        json_object = json.dumps(dictionnary)
        
        
        self.nameFile = "/home/paramunite" + str(self.number) + "_" + str(time()) + ".json"
            
        with open(self.nameFile, "w") as outfile:
            outfile.write(json_object)

 

unit = Unit(int(argv[1]),"")

while(True):
	unit.GenerateJsonFile()
	ClientMultiSocket = socket.socket()
	host = '172.20.0.10'
	port = 7777
	print('Waiting for connection response')

	file = open(unit.nameFile, "r")
	data = file.read()

	ClientMultiSocket.connect((host, port))
	ClientMultiSocket.send(data.encode("utf-8"))
	ClientMultiSocket.close()
	sleep(10)
