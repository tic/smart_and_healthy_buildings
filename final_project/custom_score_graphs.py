# This file generates graphs showing Link Lab air quality data and AWAIR scores,
# and shows how our subscores fare over time in comparison.

import utility as util
import pandas as pd
import utility as util
from datetime import datetime, timedelta
import seaborn as sn
import matplotlib.pyplot as plt
import csv
import numpy as np
from pylab import savefig
from matplotlib.colors import LogNorm
import math
import os

from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


from awair_scores import compute_component_subscores, compute_subscores
def score_during_period(start, end, device):
    with suppress_stdout_stderr():
        temp_data = util.get_lfdf(
            'Temperature_°C',
            start,
            end,
            [device]
        )
        humi_data = util.get_lfdf(
            'Humidity_%',
            start,
            end,
            [device]
        )
        co2_data = util.get_lfdf(
            'co2_ppm',
            start,
            end,
            [device]
        )
        voc_data = util.get_lfdf(
            'voc_ppb',
            start,
            end,
            [device]
        )
        pm25_data = util.get_lfdf(
            'pm2.5_μg/m3',
            start,
            end,
            [device]
        )
        awair_data = util.get_lfdf(
            'awair_score',
            start,
            end,
            [device]
        )
    if temp_data is None or humi_data is None or co2_data is None or voc_data is None or pm25_data is None or awair_data is None:
        return None
    temp = round(temp_data['value'].mean(), 2)
    humi = round(humi_data['value'].mean(), 2)
    co2  = round(co2_data['value'].mean(), 2)
    voc  = round(voc_data['value'].mean(), 2)
    pm25 = round(pm25_data['value'].mean(), 2)
    awair = round(awair_data['value'].mean(), 2)

    css = compute_component_subscores(temp, humi, co2, voc, pm25)
    final_list = list(round(x, 2) for x in compute_subscores(css))
    final_list.append(awair)
    print(final_list)
    return final_list

def generate_two_year_plots(year1, year2, filename, show_plot=False):
    df = pd.read_csv("book_with_grids.csv",encoding= 'unicode_escape')
    device = 'awair-3509'

    times = []
    environmental_scores = ([], [], [])
    occupational_scores = ([], [], [])
    overall_scores = ([], [], [])
    awair_scores = ([], [], [])

    def append_scores(i, env, ocu, ove, awair):
        environmental_scores[i].append(env)
        occupational_scores[i].append(ocu)
        overall_scores[i].append(ove)
        awair_scores[i].append(awair)

    fig, axes = plt.subplots(1, 2, sharex=False, figsize=(15,7))
    fig.suptitle(f'AQI Subscore Comparison - {year1} vs {year2}')
    plt.setp(axes, ylim=(60, 100))

    axes[0].set_title(f'Grid 52 {year1}')
    axes[1].set_title(f'Grid 52 {year2}')

    axes[0].set_ylabel('AQI', fontsize=16)
    axes[1].set_xlabel('Time', fontsize=16)

    years = [year1, year2]
    for i in range(2):
        times = []
        start_time_range = datetime(years[i], 1, 1, 0, 0, 0)
        end_time_range = datetime(years[i] + 1, 1, 1, 0, 0, 0)
        try:
            chunk_start = start_time_range
            while chunk_start < end_time_range:
                print(chunk_start)
                times.append(chunk_start)
                chunk_end = chunk_start + timedelta(minutes=60)
                if chunk_end > end_time_range:
                    chunk_end = end_time_range
                result = score_during_period(chunk_start, chunk_end, device)
                if result is None:
                    append_scores(i, None, None, None, None)
                else:
                    append_scores(i, *result)
                chunk_start = chunk_end
        except KeyboardInterrupt:
            print()

        # Label the plot
        axes[i].tick_params(axis='x', labelsize=8, rotation=45)

        # print(times)
        # print(environmental_scores[i])
        # print(occupational_scores[i])
        # print(awair_scores[i])

        # Add data to the graph
        sn.lineplot(ax=axes[i],x=times, y=environmental_scores[i])
        sn.lineplot(ax=axes[i],x=times, y=occupational_scores[i])
        sn.lineplot(ax=axes[i],x=times, y=awair_scores[i])

    sn.set()
    plt.legend(labels=['Environmental AQI', 'Occupational AQI', 'AWAIR Score'])
    with suppress_stdout_stderr():
        # plt.savefig("../Project/Plots/co2_ppm_2021_11_23",format='pdf')
        if show_plot:
            plt.show()
        plt.savefig(filename)

    print('===========================')

def generate_triple_subplot(start_time_range, end_time_range, minutes_to_jump, filename, show_plot=False):

    df = pd.read_csv("book_with_grids.csv",encoding= 'unicode_escape')
    # device = list(df[df["grid"]==51]["device_id"])[3]
    # print(list(df[df["grid"]==51]["device_id"]))
    devices = ['70886b123b81', 'awair-3509', '70886b1234a0']

    # scores = score_during_period(start, end, list(df[df["grid"]==51]["device_id"])[3])
    # device_row = next(df[df["device_id"] == device].iterrows())[1]
    # fields = device_row['fields'].split(',')

    times = []
    environmental_scores = ([], [], [])
    occupational_scores = ([], [], [])
    overall_scores = ([], [], [])
    awair_scores = ([], [], [])

    def append_scores(i, env, ocu, ove, awair):
        environmental_scores[i].append(env)
        occupational_scores[i].append(ocu)
        overall_scores[i].append(ove)
        awair_scores[i].append(awair)


    fig, axes = plt.subplots(1, 3, sharex=True, figsize=(15,7))
    fig.suptitle('AQI Subscore Comparison')
    plt.setp(axes, ylim=(60, 100))

    axes[0].set_title('Grid 51')
    axes[1].set_title('Grid 52')
    axes[2].set_title('Grid 71')

    axes[0].set_ylabel('AQI', fontsize=16)
    axes[1].set_xlabel('Time', fontsize=16)

    for i in range(3):
        times = []
        try:
            chunk_start = start_time_range
            while chunk_start < end_time_range:
                times.append(chunk_start)
                chunk_end = chunk_start + timedelta(minutes=minutes_to_jump)
                if chunk_end > end_time_range:
                    chunk_end = end_time_range
                result = score_during_period(chunk_start, chunk_end, devices[i])
                if result is None:
                    append_scores(i, None, None, None)
                else:
                    append_scores(i, *result)
                    chunk_start = chunk_end
        except KeyboardInterrupt:
            pass

        # Label the plot
        axes[i].tick_params(axis='x', labelsize=8, rotation=45)

        # Add data to the graph
        sn.lineplot(ax=axes[i],x=times, y=environmental_scores[i])
        sn.lineplot(ax=axes[i],x=times, y=occupational_scores[i])
        sn.lineplot(ax=axes[i],x=times, y=awair_scores[i])

    sn.set()
    plt.legend(labels=['Environmental AQI', 'Occupational AQI', 'AWAIR Score'])
    with suppress_stdout_stderr():
        # plt.savefig("../Project/Plots/co2_ppm_2021_11_23",format='pdf')
        if show_plot:
            plt.show()
        plt.savefig(filename)
    print('===========================')

if __name__ == '__main__':

    try:
        generate_triple_subplot(
            datetime(2021, 10, 15, 14, 0, 0),
            datetime(2021, 10, 15, 15, 0, 0),
            1,
            'figures/slide15.durationA.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 11, 17, 13, 30, 0),
            datetime(2021, 11, 17, 15, 0, 0),
            1,
            'figures/slide15.durationB.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 11, 22, 11, 30, 0),
            datetime(2021, 11, 22, 12, 45, 0),
            1,
            'figures/slide15.durationC.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 10, 20, 16, 30, 0),
            datetime(2021, 10, 20, 18, 0, 0),
            1,
            'figures/slide15.durationD.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 10, 15, 0, 0, 0),
            datetime(2021, 10, 16, 0, 0, 0),
            5,
            'figures/slide18.durationA.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 11, 17, 0, 0, 0),
            datetime(2021, 11, 18, 0, 0, 0),
            5,
            'figures/slide18.durationB.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 11, 22, 0, 0, 0),
            datetime(2021, 11, 23, 0, 0, 0),
            5,
            'figures/slide18.durationC.png'
        )
    except Exception:
        pass

    try:
        generate_triple_subplot(
            datetime(2021, 10, 20, 0, 0, 0),
            datetime(2021, 10, 21, 0, 0, 0),
            5,
            'figures/slide18.durationD.png'
        )
    except Exception:
        pass

    try:
        generate_two_year_plots(2020, 2021, 'figures/slide11.durationA.png')
    except Exception:
        pass
