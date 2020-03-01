#!/usr/bin/python3
######################################################################################################################
##      File:           dv_algorithm.py                                                                             ##
##      Authors:        Yinghao Lin, Owen Sutka, Eboni Williams                                                     ##
##      Last Revised:   February 28, 2020                                                                           ##
##      Class:          Computer Science 450: Computer Networks                                                     ##
##      Teacher:        Dr. Andrey Timofeyev                                                                        ##
##      Assignment:     Assignment #6 - Group Project                                                               ##
##      Due Date:       March 2, 2020                                                                               ##
##      Usage:          Use python 3                                                                                ##
##                      In order for this program to work, a csv file must be provided that demonstrates the        ##
##                      topology of the network that is to be analyzed.                                             ##
##                      Example:    python dv_algorithm.py topology.csv                                             ##
##      Purpose:        This program computes the distance vectors for nodes in a given network using the           ##
##                      Bellman-Ford equation in the distance-vector algorithm. The resulting distance vectors are  ##
##                      are printed out.                                                                            ##
##      Dependencies:   sys, csv                                                                                    ##
##      Sources:        none                                                                                        ##
######################################################################################################################
################################## Requirements for Distance Vector Code Submission ##################################
######################################################################################################################
# 1. First, your program has to read the costs of all links in a given network from given file (provided on
#    Moodle). In this file, the first row and the first column refer to the names of the nodes (from u to z). 
#    Other cells show the cost of links between the row node and the column node (meaning two nodes are neighbors).
# 2. Your program has to take the name of the topology file as a command line argument.
# 3. Next, your program has to calculate distance vectors for nodes in the network using distance-vector algorithm
#    discussed in class (Bellman-Ford). Final converged distance vector for each node has to be provided as an output.
# 4. Distance vector estimates must be calculated using Bellman-Ford equation.
# 5. Please, comment your code thoroughly, explaining the steps of the distance-vector algorithm and the overall flow
#    of your program (e.g. parsing of input file, updating distance vectors, etc.) In addition, please, properly 
#    specify any sources you have used.
# 6. Create a "readme.pdf" with the name of each group member and the explanation of the responsibilities. In 
#    addition, specify Python version and provide instructions on how to run your program.
# 7. Submit zipped folder with your Python source code and the readme.pdf file on Moodle. Only one submission per
#    group required.
######################################################################################################################
################################################## LIBRARY IMPORTS ###################################################
import sys
import csv
##################################################### VARIABLES ######################################################
#------------------------------------------------------Constants------------------------------------------------------
infinity = 99999
#---------------------------------------------------Global Variables--------------------------------------------------
global nodeNames, edgeNamesWeights # set as global cuz its like cheating
nodeNames = []  # initialize the list of nodes in network(unnecessary in python but we wildin)
edgeNamesWeights = {} # format is src_dest:cost (e.g. uu:0,uv:7,ux:3 ......)
nodeGraphs = {} # keep track of the graphsfor every nodes
newValues = {}  # a list to keep track of updates that need to be used
##################################################### FUNCTIONS ######################################################
#-----------------------------------------------Error and Warning cases-----------------------------------------------           
# ---- Not really used
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#OWEN
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
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
#----------------------------------------------------Data Functions---------------------------------------------------
# ---- Very much used
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#OWEN
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
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#OWEN
# This function prints the distance vectors for the nodes in the algorithm 
def printResult():
    for node in nodeGraphs:
        # Created the initial prijtout and then pulled a pathList dictionary out of the big boi dictionary
        printLine = "Distance vector for node {}:".format(node)
        pathList = nodeGraphs.get(str(node))

        # This here is because the input data from the nodeGraphs was formatted in a way that it was out of order. This will ensure it is always in order
        # Dictionary was completely unsorted no matter what I did so we are using a list instead (yay i want to die)
        pathListNames = []
        newCostsList = []
        # pulling all the path names...
        for path in pathList:
            pathListNames.append(path)
        # Sorted them...
        pathListNames.sort()

        # now going through and creating a new list for us to use that is sorted...
        for i in range(0, len(pathListNames)):
            newCostsList.append(pathListNames[i])
            newCostsList.append(pathList.get(pathListNames[i]))

        # Now is the actual printing of the important stuffs
        for i in range(0, int(len(newCostsList)/2)):
            pathName = newCostsList[i*2]           
            if (pathName[0] == node):
                printLine = printLine + " " + str(newCostsList[i*2+1])
        print(printLine)
	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#CHRIS
# (with EBONI pair programming)  
# This function checks to see if a node can find a lower-cost path to other nodes based on the current values sent to
# it from the other nodes. That is, this function implements the Bellman-Ford equation to update the distance vectors
# for each node.
def checkForNewPath():
    # for every node, check against the other nodes.
    for srcNode in nodeNames:
        for destNode in nodeNames:
            # find the minimum distance vector
            minimum = infinity
            for midNode in nodeNames:
                if(minimum > nodeGraphs[srcNode][srcNode+midNode]+nodeGraphs[srcNode][midNode+destNode]):
                    minimum = nodeGraphs[srcNode][srcNode+midNode]+nodeGraphs[srcNode][midNode+destNode]
            # if the minimum distance is less than the current distance, update it
            # and notify network that there has been an update
            if(minimum < nodeGraphs [srcNode][srcNode+destNode]):
                nodeGraphs[srcNode][srcNode+destNode] = minimum
                newValues[srcNode+destNode] = minimum
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#EBONI
# (with CHRIS pair programming)
# This function implements the distance vector algorithm by performing the initialization step, the notifying the
# network of changes, and the updating of the other nodes with new costs. The actual minimum cost estimation is done
# in the 'checkForNewPath' function.
def dv_algorithm():
    # initialize each node's graph
    for node in nodeNames:
        new_dict = {}
        for key in edgeNamesWeights.keys():
            if(node in key[0]):
                new_dict[key] = edgeNamesWeights[key]
                # let network know there has been an update
                newValues[key] = edgeNamesWeights[key]
            else:
                new_dict[key] = infinity
        nodeGraphs[node] = new_dict
    # while there is an update event
    # note: if dictionary is empty, this loop is not entered.
    while(newValues):
        # update each node with the new costs from the update
        for key in newValues.keys():
            for node in nodeNames:
                if(key[0] != node):
                    nodeGraphs[node][key] = newValues[key]
        # remove the update events from the dictionary to show
        # they have been implemented.
        newValues.clear()
        # check to see if any values need to change based on the update
        checkForNewPath()
    # print out the distance vectors
    printResult()
##################################################### MAIN PROGRAM ######################################################
# Take in csv file from command line
if(len(sys.argv) >= 1):
    #inputFile = str(sys.argv[1])
    inputFile = "topology.csv"                  #### FIX
    # Normal Function
    # pulls in CSV data
    processCSV(inputFile)
    # run the distance-vector algorithm
    dv_algorithm()
else: # let user knnow a file is needed
    print("This program requires a csv file to be specified at run time")
##########################################################################################################################
