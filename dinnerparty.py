#Homework 2
#Title: Dinner Party
#Author: Kyle Zalewski

import numpy
import sys
import time
import random

#draw dining table with diners
def drawtable(n, diners):
    half = int(n / 2)

    #print top half of diners
    print("  ", end='')
    for x in range(half):
        if(diners[x] < 10):
            print(' ', diners[x], '', end='')
        else:
            print('',diners[x], '', end='')
    print();

    #print top line of table
    print("+-", end='')
    for x in range(half):
        print("----", end='')
    print("-+", end='')
    print()

    #print sides line
    print("| ", end='')
    for x in range(half):
        print("    ", end='')
    print(" |", end='')
    print()

    #print bottom line of table
    print("+-", end='')
    for x in range(half):
        print("----", end='')
    print("-+")

    #print bottom line of diners
    print("  ", end='')
    for x in range(half):
        if(diners[x + half] < 10):
            print(' ', diners[x + half], '', end='')
        else:
            print('',diners[x + half], '', end='')
    print();

#calculate preference between diners
def calcPreference(p1, p2):
    return preferences[p2-1][p1-1]

#calculate score of passed in table
def scoreTable(diners):
    #side of table variable
    half = int(n/2)

    #initialize score variable
    score = 0

    #score cross-table relationships
    #2 points for relationships that are opposite
    for x in range(half):
        if((diners[x] <= half) != (diners[x + half] <= half)):
            score += 2

    #score adjacent relationships top side
    for x in range(half - 1):
        if((diners[x] <= half) != (diners[x + 1] <= half)):
            score += 1

    #score adjacent relationships bottom side
    for x in range(half - 1):
        if((diners[x + half] <= half) != (diners[x + half + 1] <= half)):
            score += 1

    #score all interpersonal relationships
    for x in range(n):
        #if left exists
        if(x != 0 and x != half):
            #count left side relationship
            score += calcPreference(diners[x], diners[x-1])

        #if right exists
        if(x != (half - 1) and x != (n-1)):
            #count right side relationship
            score += calcPreference(diners[x], diners[x+1])

        #count cross-table relationship for top of table
        if(x < half):
            score += calcPreference(diners[x], diners[x + half])

        #count cross-table relationship for bottom of table
        else:
            score += calcPreference(diners[x], diners[x - half])

    #pass back calculated score
    return score

#switch two diners
def switchDiners(p1, p2):
    diners[p1], diners[p2] = diners[p2], diners[p1]

#random rotate test
def randomRotateTest(preScore):
    #set top left of rotation
    topLeft = random.randint(0, n/2-2)
    cross = int(n/2)
    #determine width of rectangle
    rightBound = (n/2-1) - topLeft
    w = random.randint(1, rightBound)
    #rotate rectangle clockwise
    temp = diners[topLeft]
    diners[topLeft] = diners[topLeft + cross]
    diners[topLeft + cross] = diners[topLeft + cross + w]
    diners[topLeft + cross + w] = diners[topLeft + w]
    diners[topLeft + w] = temp;
    if(scoreTable(diners) < preScore):
        #undo rotation
        temp = diners[topLeft]
        diners[topLeft] = diners[topLeft + w]
        diners[topLeft + w] = diners[topLeft + cross + w]
        diners[topLeft + cross + w] = diners[topLeft + cross]
        diners[topLeft + cross] = temp

#beginning of AI portion
def calcSwitches(t):
    #for spec'd amount of time
    limit = float(t)
    #end time
    end = time.time() + limit

    while time.time() < end:
        #check progressively forward
        for x in range (n - 1):
            #determine if switch will be positive or neutral
            preScore = scoreTable(diners)
            for y in range(x + 1, n - 1):
                switchDiners(x, y)
                postScore = scoreTable(diners)
                #if positive or equal, move on
                if postScore >= preScore:
                    continue
                #if negative revert
                else:
                    switchDiners(x, y)
        #random rotation
        preScore = scoreTable(diners)
        randomRotateTest(preScore)

        #complete randomization
        test = random.sample(diners, n)
        if(scoreTable(diners) < scoreTable(test)):
            for x in range(n):
                diners[x] = test[x]


#read in instance file (specified in cmd line argument)
instance = open(sys.argv[1])

#read in and show number of diners
n = int(instance.readline())
print("Number of diners: ", n)

#create and print matrix
preferences = numpy.loadtxt(instance, dtype= int, delimiter= ' ')
print("Preference matrix: \n", preferences)

#close instance file
instance.close()

#build initial list for diners
diners = [0]*n
for x in range(n):
    diners[x] = x+1

#test diner switch
switchDiners(0, 9)

#calculate necessary switches
#argument is number of seconds to run
calcSwitches(sys.argv[2])

#draw table
print("Dining table:")
drawtable(n, diners)

#calculate and print final score
score = scoreTable(diners)

print("Final Score: ", score)

#print output required by assignment
print("Seating Arrangement:")
print("p s")
for x in range(n):
    print(diners[x], '', end='')
    print(x+1)
