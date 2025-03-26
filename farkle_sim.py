from random import randint
import pandas as pd
import numpy as np
import matplotlib
from math import comb, factorial
import json

"""scorings for farkle, based on PlayMonster LLC version"""
single_1 = 100
single_5 = 50
three_of_array = [300, 200, 300, 400, 500, 600]
four_any_number = 1000
five_any_num = 2000
six_any_numb = 3000
straight = 1500
three_pairs = 1500
four_any_and_pair = 1500
two_triples = 2500 

"""calculation for probability to farkle based on i number of dice"""
# farkle_prob = []
# for i in range(1,7):
#     farkle_prob.append(1-(1-((4/6)**i)
#                        +(comb(i,3)*4*((1/6)**3)*((3/6)**(i-3)))
#                        +(comb(i,4)*4*((1/6)**4)*((3/6)**(i-4)))
#                        +(comb(i,5)*4*((1/6)**5)*((3/6)**(i-5)))
#                        +(comb(i,6)*4*((1/6)**6)*((3/6)**(i-6)))
#                        +(comb(i,6)*factorial(4)*((1/6)**6))))

# print(farkle_prob)
#prints this:
farkle_prob = [0.6666666666666666, 0.4444444444444444, 0.2777777777777778, 0.15740740740740744, 0.07716049382716039, 0.02777777777777779]
#to read, this tells us with 1 dice(index 0) we have a 66% chance of Farkling, with 2 dice(index 1) we have a 44% chance of Farkling... etc

"""algorithm to simulate dice rolls for dice amounts 1 - 6"""
#technically, you can roll more than 6 dice but there is no need to limit that in this program.

def roll_die(num_dice):

    
    total_score = 0
    roll_type = "Farkle"
    dice_rolls = [randint(1,6) for i in range(num_dice)]

    #the two auxiliary arrays roll_counts and soring_map are what make this algorithm incredibly fast

    #roll_counts acts like a hash map counting the number of times a specific number is rolled in a given amount of dice
    #for example, rolling 5 dice and getting the sequence [3,3,4,2,1] would get mapped to the roll_counts array as [1,1,2,1,0,0]
    #index 0 corresponds to the amount of 1s, index 1 corresponds to the amount of 2s, and so on 
    roll_counts = [0,0,0,0,0,0]

    #scoring_map helps to interpret the results from roll_counts even further
    #using the roll_counts map above and mapping the same way we did before, scoring_map returns [3,1,0,0,0,0]
    #the way we interpret scoring_map is that at index 0, the value corresponds to the number of unique numbers;
    #at index 1, the value corresponds to the number of pairs;
    #at index 2, the value corresponds to the number of triples;
    #and so on until we reach index 5 where the value corresponds to the number of sextuples
    #this is very useful for scoring, because for some scores we do not necessarily care for WHAT value is rolled, but if it is a quad, triple, straight, etc. 
    scoring_map = [0,0,0,0,0,0]

    #the two for loops below are the most important part of this program, because they give us all of the information to intepret the random rolls
    for j in range(len(dice_rolls)):
        roll_counts[dice_rolls[j]-1] = roll_counts[dice_rolls[j]-1] + 1

    for k in range(6):
        #if statement to prevent case where roll_counts[k]-1 == -1 which will map 0 in roll_counts to index 5 of scoring map
        if roll_counts[k]-1 != -1:
            scoring_map[roll_counts[k]-1] = scoring_map[roll_counts[k]-1] + 1


    #all of the conditional statements below are how the rolls are filtered and classified
    #rolls are scored and renamed from most restrictive roll type (i.e. if you get that roll, it is impossible to get another roll type)
    #to least restrictive roll type (i.e. rolls that may coincide with each other)
    #because of how restrictive some rolls are, this makes the filtering modular! I originally wrote this intending the filtering
    #to only work for rolls with 6 dice, but I found that the cases do not need to be modified for roll amounts 1-5  

    if scoring_map[0] == 6:
        total_score += straight
        roll_type = "straight"
        

    elif scoring_map[5] == 1:
        total_score += six_any_numb
        roll_type = "six of any number"

    elif scoring_map[2] == 2:
        total_score += two_triples
        roll_type = "two triples"

    elif scoring_map[3] == 1: 
        if scoring_map[1] == 1:
            total_score += four_any_and_pair
            roll_type = "four of a kind and a pair"
        else:
            total_score += four_any_number
            roll_type = "four of a kind"

    elif scoring_map[1] == 3:
        total_score += three_pairs
        roll_type = "three pairs"

    elif scoring_map[4] == 1:
        total_score += five_any_num
        roll_type = "five of a kind"

    elif scoring_map[2] == 1:
        for i in range(6):
            if roll_counts[i] == 3:
                total_score += three_of_array[i]
        roll_type = "three of a kind"
    #at this point, we have <= 2 pairs, no triples, no quads, no quintuples, no sextuples
    #now we only care how many 1s and 5s we have

    #the two larger "if" conditionals below handle cases with 1s and 5s rolled that might coincide with other rolls
    if roll_counts[0] != 0 and roll_counts[0]<3:
        #have <=2 1s; <= 2 pairs; no quads; no quintuples; no sextuples; not a straight
        if roll_type == "three of a kind" or roll_type == "four of a kind" or roll_type == "five of a kind":
            total_score += roll_counts[0]*single_1
            roll_type = str(roll_type) + " combo"
        if roll_type == "Farkle":
            total_score += roll_counts[0]*single_1
            roll_type = "1s and/or 5s"

    if roll_counts[4] != 0 and roll_counts[4]<3:
        #have <=2 1s; <= 2 pairs; no quads; no quintuples; no sextuples; not a straight
        if roll_type == "three of a kind" or roll_type == "four of a kind" or roll_type == "five of a kind":
            total_score += roll_counts[4]*single_5
            roll_type = str(roll_type) + " combo"
        if roll_type == "Farkle":
            total_score += roll_counts[4]*single_5
            roll_type = "1s and/or 5s"
    return total_score, roll_type, str(dice_rolls), str(roll_counts), str(scoring_map)


"""storing the simulations in Excel for easy analysis"""
#creating an empty dictionary to hold all of the dataframes containing the simulations for dice rolls of 1-6 dice
results_for_num_die_dict = {}

for j in range(1,7):
    rows = list()
    #the range here can be changed. I just made it 1048576 to test as many as Excel could handle and also because more simulations helps reduce the effect of outliers
    for i in range(1,1048576):
        roll_info = [i]
        roll_info.extend(list(roll_die(j)))
        rows.append(roll_info)

    #using a numpy array here because numpy to pandas makes this a really efficient way to store and read data
    #using just pandas takes forever, whereas I can run this program in less than 5 minutes and produce 6 million simulations
    arr = np.array(rows)
    results_for_num_die_dict["{0}_dice".format(j)] = pd.DataFrame(arr, columns = ["trial","score","roll type", "roll results", "counts of each value", "mapping for score"])


#using ExcelWriter because I am separating data into different sheets in Excel so simulations can be analyzed separately
writer = pd.ExcelWriter("farkle2.xlsx", engine='xlsxwriter')

for name, dice_dataframe in results_for_num_die_dict.items():
    dice_dataframe.to_excel(writer, sheet_name = name, index = False)

writer.close()

print("finished! :)")