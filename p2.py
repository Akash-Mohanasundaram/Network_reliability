import math
import os
from numpy import binary_repr
import numpy
import networkx as netx
from bokeh.plotting import figure, show
import random

def matrix_to_list(a):
    matrix_lst=[]
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(i<j):
                matrix_lst.append(a[i][j])
    return matrix_lst

def list_to_matrix(matrix_lst):
    adj_matrix=[]
    lst1=[0,matrix_lst[0],matrix_lst[1],matrix_lst[2],matrix_lst[3]]
    lst2=[0,0,matrix_lst[4],matrix_lst[5],matrix_lst[6]]
    lst3=[0,0,0,matrix_lst[7],matrix_lst[8]]
    lst4=[0,0,0,0,matrix_lst[9]]
    lst5=[0]*5
    adj_matrix.append(lst1)
    adj_matrix.append(lst2)
    adj_matrix.append(lst3)
    adj_matrix.append(lst4)
    adj_matrix.append(lst5)
    return(adj_matrix)


def connected_or_not(adj):
    g=netx.Graph()
    g.add_node(0)
    g.add_node(1)
    g.add_node(2)
    g.add_node(3)
    g.add_node(4)
    for i in range(5):
        for j in range(5):
            if adj[i][j] == 1:
                g.add_edge(i,j)
    boolean_value = netx.is_connected(g)
    return boolean_value


netid=[2,0,2,1,5,7,5,3,5,0]
reliability = []
p = 0.05
all_possible_combination_lst=[]
all_possible_combination_int_lst=[]
all_possible_combination_temp_int_lst=[]
for i in range(1024):
    all_possible_combination_lst.append(binary_repr(i,width=10))
    for j in all_possible_combination_lst[i]:
        #print(j)
        all_possible_combination_temp_int_lst.append(int(j))
    all_possible_combination_int_lst.append(all_possible_combination_temp_int_lst)
    all_possible_combination_temp_int_lst=[]



n=4
check=[]
for k in range(1024):
    adj=list_to_matrix(all_possible_combination_int_lst[k])
   
    if (connected_or_not(adj)):
        #print("it is connected")
        check.append(1)
    else:
        #print("No it is not connected")
        check.append(0)
print("\n")
print(f"out of 1024 possibilities {check.count(1)} graphs are connected and {check.count(0)} are not connected")
print("\n")

#calculating reliability for p in [0.05,1]
for k in range(20):
    reliability_temp=0
    prob_array=[]
    for i in netid:
        power_val=math.ceil(i/3)
        prob_array.append(p**power_val)
                                                        
    i=0
    #1024 reliabilities 
    while(i<1024):
        if check[i]==1:     
            #print("1")
            prod=1
            for j in range(10):
                if int(all_possible_combination_int_lst[i][j])==1:   
                    probability=prob_array[j]   
                    #print(f"{prob},connected")                                                      
                else:
                    probability=1-prob_array[j]
                prod*=probability   
            reliability_temp+=prod
        i+=1
    reliability.append(reliability_temp)
    p+=0.05

probability_list=[0.05,0.1,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1]
print("\n")
print("Values for Reliability with varying p")
for i in range(20):
    print(f"p = {probability_list[i]}: Reliability = {reliability[i]}")
print("\n")

plot = figure(title="Reliability vs p", x_axis_label='p', y_axis_label='reliability')
plot.line(probability_list, reliability, line_width=2)
show(plot)

#task 2

p=0.9
k = 0
list_of_all_probabilities = []
individual_reliability = []
collection_of_all_reliabilities=[]
all_reliabilities_list=[]
temp_reliabilities=[]

#for p = 0.9 
for i in netid:
    task2_power_val = math.ceil(i/3)
    list_of_all_probabilities.append(p**task2_power_val)

def inner_inner_loop_calc(all_temp):
    i=0
    task2_temp = 0
    while(i<1024):
        adj=all_temp[i]
        if connected_or_not(list_to_matrix(adj)):     
            prod_task2=1
            for j in range(10):
                if int(all_temp[i][j])==1:  
                    task2_prob = list_of_all_probabilities[j]                
                else:
                    task2_prob = 1-list_of_all_probabilities[j]    
                prod_task2 = prod_task2 * task2_prob   
            task2_temp = task2_temp + prod_task2
        i+=1    
    return task2_temp
    

def inner_loop_calc(all_temp):
    temp_reliabilities=[]
    for k in range(21):
        for i in range(0,k):   #perform the expirement for a total of k random combinations
            random_number_k = random.randint(0,1023)
            adj=all_temp[random_number_k]
            if connected_or_not(list_to_matrix(adj)):
                all_temp[random_number_k]=[0]*10 # Flipping to down state
            else:
                all_temp[random_number_k]=[0,1,0,1,0,1,0,1,0,1] # Flipping to up state
          
        temp_reliabilities.append(inner_inner_loop_calc(all_temp))
    return temp_reliabilities

for i in range(1024):
    all_possible_combination_lst.append(binary_repr(i,width=10))
    for j in all_possible_combination_lst[i]:
        #print(j)
        all_possible_combination_temp_int_lst.append(int(j))
    all_possible_combination_int_lst.append(all_possible_combination_temp_int_lst)
    all_possible_combination_temp_int_lst=[]



#repeating the expirement 21 times to reduce the effect of randomness
for average_val in range(21):
    p = 0.9
    k=0
    all_temp=[]
    all_temp=all_possible_combination_int_lst.copy()
    all_reliabilities_list.append(inner_loop_calc(all_temp))
    temp_reliabilities = []

#Finding average 
overall_average_reliability = []
temp_list=[]
list_elements=[]
overall_average_reliability=[]
temp1_list=[]
for i in range(21):
    for j in range(21):
        temp1_list.append(all_reliabilities_list[j][i])
    list_elements.append(temp1_list)
    temp1_list=[]

for i in range(21):
    sum_of_elements=0
    temp_list=list_elements[i]
    sum_of_elements=sum(temp_list)
    sum_of_elements=sum_of_elements/21
    overall_average_reliability.append(sum_of_elements)

values_of_k = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
print("Values for Average Reliability")
for i in range(0,21): 
    print(f"k = {i}: Average reliability = {overall_average_reliability[i]}")
print("\n")
            
plot2 = figure(title="Reliability of the Network vs k", x_axis_label='k', y_axis_label='average reliability')
plot2.line(values_of_k, overall_average_reliability, line_width=2)
show(plot2)

#change in reliability
changes_in_average_reliability = []
to_be_subtracted=overall_average_reliability[0]
i=0
difference=0
print("Values for Changes in average reliability")
while(i<=20):
    difference = to_be_subtracted - overall_average_reliability[i]
    difference='{:.21f}'.format(difference)
    changes_in_average_reliability.append(difference)
    print(f"k = {values_of_k[i]}: Change in the reliability = {changes_in_average_reliability[i]}")
    i+=1

plot3 = figure(title="Changes in Reliability of the Network vs k", x_axis_label='k', y_axis_label='Changes in average reliability')
plot3.line(values_of_k, changes_in_average_reliability, line_width=2)
show(plot3)


