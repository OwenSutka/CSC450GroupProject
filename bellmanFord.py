############################################################
# Name: Owen Sutka
# Date Last Altered: 02/20/2020
# Class: CSC 450
# Teacher: Dr. Timofeyev
# Assignment: Assignment #5 - Dijkstra's
# Assignment Due Date: 02/21/20
# Purpose: To illustrate the least cost paths formation that
#    A network will calculate
############################################################

# Requirements for Dijkstra's code:
############################################################

############################################################


# Libraries
import sys
import csv

# Constants


# Global Variables
global nodeNames, edgeNamesWeights # set as global cuz its like cheating
nodeNames = []  # initialize (unnecessary in python but we wildin)
edgeNamesWeights = {} # format is uu:0,uv:7,ux:3 ......
nodeGraphs = {} # keep track of all the node graphs:=

# Variables
newValues = {}
# Error and Warning cases           ---- Not really used
############################################################ #OWEN
def errorChoose(errorInt=-1):
    # You can choose whatever error you need and it will produce the relevant result
    errorCase = {
        -1: "Unknown Error",
        1:  "VALUE ERROR: The input provided was in a different format than expected.",
        2:  "NODE NAME ERROR: Node Name specified is not in list of known nodes.",
        3:  "INPUT FILE ERROR: No input file specified. Cannot create node list or edge list.",
        4:  "",
        5:  ""
    }
    # Prints an error statement
    print("\n{}\n".format(errorCase.get(errorInt, "Unknown Error at errorChoose")))
    return

def warningChoose(warningInt=-1):
    # You can choose whatever warning you need and it will produce the relevant result
    warningCase = {
        -1: "Unknown Warning...",
        1:  "Input file unspecified. Will be entering Generic Mode...",
        2:  "No initial node specified on startup. Will need to be specified...",
        3:  ""
    }
    # Prints an warning statement
    print("\nWARNING: {}\n".format(warningCase.get(warningInt, "Unknown Error at warningChoose")))
    return
############################################################ # OWEN


# Functions         -- Very much used
############################################################ #OWEN
# This function will take the csv file name as input and will find it and assign some of the global variables some values
def processCSV(inputFile):
    # Initialize the rows from the csv
    dataRows = []
    tempDict = {}
    # make sure to alter the global and not local variables for accessing later
    global nodeNames, edgeNamesWeights
    # Check if there is an input file, if not ask for one
    if(inputFile == -1):
        errorChoose(3)
        while(inputFile == -1):
            try:
                inputFile = str(input("Please, provide the input file's name: "))
                break
            except ValueError:
                inputFile = -1
                errorChoose(1)
    # open and parse data from file so that we have every edge and their weights
    with open(inputFile, 'rt') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            dataRows.append(row)
        # get the node names
        nodeNames = dataRows[0][1:len(dataRows[0])]
        # from each column pull the weight for each other node and itself. Works and is clean
        for i in range(1, len(dataRows[0])):
            for j in range(i,len(dataRows[0])):
                # Including edge cost and name in the dictionary
                edgeName = str(dataRows[0][i] + dataRows[0][j])
                edgeCost = int(dataRows[i][j])
                edgeNamesWeights[edgeName] = edgeCost
                # This had to be used because python ONLY uses pointers to values and it couldn't iterate a dictionary that changes size every iteration
                tempDict[edgeName] = edgeCost
        # now make more robust and easier to use by placing the reverse name for each node
        for i in tempDict:
            if(i[0] != i[1]):
                edgeNamesWeights[str(i[1]+i[0])] = edgeNamesWeights[i]
############################################################ # CHRIS (with EBONI pair programming)  
############################################################ # CHRIS (with EBONI pair programming)  
def checkForNewPath():
    # global nodeGraphs,newValues
    for X in nodeNames:
        for A in nodeNames:
            min = 99999
            for B in nodeNames:
                if(min > nodeGraphs[X][X+B]+nodeGraphs[X][B+A]):
                    min = nodeGraphs[X][X+B]+nodeGraphs[X][B+A]            
            if(min < nodeGraphs [X][X+A]):
                nodeGraphs[X][X+A] = min
                newValues[X+A] = min

    

############################################################ # EBONI (with CHRIS pair programming)
def dv_algorithm():
    # generate base graphs
    for node in nodeNames:
        new_dict = {}
        for key in edgeNamesWeights.keys():
            if(node in key[0]):
                new_dict[key] = edgeNamesWeights[key]
                newValues[key] = edgeNamesWeights[key]
            else:
                new_dict[key] = 9999
        nodeGraphs[node] = new_dict
    # while there are updated values
    while( newValues):
        for key in newValues.keys():
            for node in nodeNames:
                if(key[0] != node):
                    nodeGraphs[node][key] = newValues[key]
        
        newValues.clear()
        # do the minimization, and add values to newValues if needed
        checkForNewPath()
printResult()
############################################################ #OWEN
# Take in csv file fro mcommand line
if(len(sys.argv) >= 2):
    inputFile = str(sys.argv[1])
    # Normal Function
    # pulls in CSV data
    processCSV(inputFile)
    # initialize step # CHRIS, EBONI
    dv_algorithm()
else:
    print("This program requires a csv file to be specified at run time")

    
############################################################

