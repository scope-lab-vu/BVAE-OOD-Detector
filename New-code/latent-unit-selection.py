#!/usr/bin/env python3
#Libraries
import os
import numpy as np
import csv
import statistics
seed = 7
np.random.seed(seed)
import prettytable
from prettytable import PrettyTable
from natsort import natsorted
from operator import itemgetter
from welford import Welford


def variance_calculator(path,top_n,w):
    variance = []
    data = []
    latent_unit = []
    latents = []
    with open(path,'r') as csvfile:
        plots = csv.reader(csvfile)
        for row in plots:
            data.append(row)

    for i in range(len(data[0])):
        data1 = []
        latent_unit.append(i)
        for x in range(len(data)):
            data1.append(float(data[x][i]))
        variance_val = statistics.variance(data1)
        variance.append(round(variance_val,6))

    indices, variance_sorted = zip(*sorted(enumerate(variance), key=itemgetter(1),reverse=True))

    t = PrettyTable(['Latent Unit','kl-divergence difference'])
    for i in range(top_n):
        latents.append(indices[i])
        t.add_row([indices[i],variance_sorted[i]])
    print(t)

    return latents

def common_latent_detectors(selected_latents):
    for x in range(0,len(selected_latents),2):
        print(list(set(selected_latents[x]) & set(selected_latents[x+1])))
        return list(set(selected_latents[x]) & set(selected_latents[x+1]))


if __name__ == '__main__':
        run = "-comparison.csv"
        w = Welford()
        top_n = 5
        models = ["30_1.1"]#,"30_1.2","30_1.4","40_1.0","40_1.5"]
        folders = ["precipitation","brightness"]
        for model in models:
            print("--------------------------model:%s----------------------------------------------"%model)
            selected_latent = []
            path = "/home/scope/Carla/CARLA_0.9.6/PythonAPI/TCPS-results/Latent-extraction/" + model + '/'
            for folder in folders:
                data_path = path + folder + run
                print(data_path)
                latents = variance_calculator(data_path,top_n,w)
                selected_latent.append(latents)
            common_latent_detectors(selected_latent)
