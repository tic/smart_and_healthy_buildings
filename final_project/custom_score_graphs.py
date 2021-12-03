# This file generates graphs showing Link Lab air quality data and AWAIR scores,
# and shows how our subscores fare over time in comparison.

import utility as util
import pandas as pd
import utility as util
from datetime import datetime
import seaborn as sn
import matplotlib.pyplot as plt
import csv
import numpy as np
from pylab import savefig
from matplotlib.colors import LogNorm
import math
import os

def generate_linklab_data():


    df = pd.read_csv("book_with_grids.csv",encoding= 'unicode_escape')
    start = datetime(2021,8,24,5,0,0)
    end = datetime(2021,11,30,5,0,0)
    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('co2_ppm',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('co2_ppm-11/23/2021')
    plt.setp(axes, ylim=(350, 700))
    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/co2_ppm_2021_11_23",format='pdf')
    plt.show()

    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('voc_ppb',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('voc-11/23/2021')
    plt.setp(axes, ylim=(350, 700))
    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/voc_2021_11_23",format='pdf')
    plt.show()

    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('pm2.5_μg/m3',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('pm2.5_11/23/2021')

    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/pm2.5_2021_11_23",format='pdf')
    plt.show()


    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('Humidity_%',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('Humidity_11/23/2021')

    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/Humidity_2021_11_23",format='pdf')
    plt.show()


    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('Temperature_°C',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('Temperature_11/23/2021')

    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/Temperature_2021_11_23",format='pdf')
    plt.show()


    new_time_1 = []
    new_time_2 = []
    new_time_3 = []
    time_1 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==51]["device_id"]))['time'])
    count_1 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==51]["device_id"]))['value'])

    for i in range(len(time_1)):
        naive = time_1[i].replace(tzinfo=None)
        new_time_1.append(naive)

    time_2 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==52]["device_id"]))['time'])
    count_2 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==52]["device_id"]))['value'])

    for i in range(len(time_2)):
        naive = time_2[i].replace(tzinfo=None)
        new_time_2.append(naive)

    time_3 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==71]["device_id"]))['time'])
    count_3 = list(util.get_lfdf('awair_score',start,end,list(df[df["grid"]==71]["device_id"]))['value'])

    for i in range(len(time_3)):
        naive = time_3[i].replace(tzinfo=None)
        new_time_3.append(naive)

    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('awair_score_11/23/2021')

    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')
    sn.lineplot(ax=axes[0],x=new_time_1, y=count_1)
    sn.lineplot(ax=axes[1],x=new_time_2, y=count_2)
    sn.lineplot(ax=axes[2],x=new_time_3, y=count_3)
    sn.set()
    axes[0].set_ylabel('Value',fontsize=16)
    axes[0].set_xlabel('Day Time',fontsize=16)
    axes[1].set_ylabel('Value',fontsize=16)
    axes[1].set_xlabel('Day Time',fontsize=16)
    axes[2].set_ylabel('Value',fontsize=16)
    axes[2].set_xlabel('Day Time',fontsize=16)
    axes[0].tick_params(axis='x', labelsize=8, rotation=45)
    axes[1].tick_params(axis='x', labelsize=8, rotation=45)
    axes[2].tick_params(axis='x', labelsize=8, rotation=45)
    plt.savefig("../Project/Plots/awair_score_2021_11_23",format='pdf')
    plt.show()

if __name__ == '__main__':

    generate_linklab_data()
