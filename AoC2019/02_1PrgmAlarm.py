# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:59:17 2019

@author: redne
"""

prgm = input("Enter data:\n")

data_str = prgm.split(",")
data = [int(i) for i in data_str]
#print(data_str)
#print(data)
data[1] = 12
data[2] = 2
print(data)
print(len(data))

def operate(index):
    print("Running step", index)
    opr_index = index * 4
    if (data[opr_index] == 99):
        print("DATA VALUE 0 IS", data[0])
        return
    in1_index = data[opr_index + 1]
    in2_index = data[opr_index + 2]
    out_index = data[opr_index + 3]
    if (data[opr_index] == 1):
        print("    [+]: in1, in2, out indecies are", in1_index, in2_index, out_index)
        n = data[in1_index] + data[in2_index]
        print("    sum is", n, "with", data[in1_index], "+", data[in2_index])
        data[out_index] = n
    elif (data[opr_index] == 2):
        print("    [x]: in1, in2, out indecies are", in1_index, in2_index, out_index)
        n = data[in1_index] * data[in2_index]
        print("    prod is", n, "with", data[in1_index], "*", data[in2_index])
        data[out_index] = n
    else:
        print("    error at prgm index", index, "data index", opr_index)
    operate(index + 1)

operate(0)