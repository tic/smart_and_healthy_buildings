
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
import cv2
import pandas as pd
import utility as util
from time import sleep
import seaborn as sns
import matplotlib.pyplot as plt

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

# Create a heat map for each grid point in the link lab
# if successful, return filepath of image
# on error, return none
def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_path):
    fields_set = set(fields)

    # get sensor information
    print('Reading in sensor registration information...')
    df = pd.read_csv('book_with_grids.csv')

    # grid range 0-199
    datapoints = [
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20,
        [0] * 20
    ]

    print('Iterating across the grid to gather data points...')
    for grid in range(200):
        print(f'[GRID {grid}]')
        sensors_in_grid = df[df['grid'] == grid]

        # for each sensor in the grid
        dps = 0
        for row_id, sensor in sensors_in_grid.iterrows():
            print(f'\tsensor {row_id}')
            sensor_fields = sensor['fields'].split(',')
            device_id_list = [sensor['device_id']]
            # print(sensor_fields)
            # print(fields)
            relevant_fields = list(set(sensor_fields).intersection(fields_set))
            # print(relevant_fields)
            for field in relevant_fields:
                print(f'\t\t{field}')
                with suppress_stdout_stderr():
                    ldf = util.get_lfdf(field, start_datetime, end_datetime, device_id_list)
                if ldf is not None:
                    dps += ldf.shape[0]
                else:
                    print('\t\t\tNo data in time range.')
                # dps += len(ldf) ??
        datapoints[int(grid / 20)][grid % 20] = dps
    print(datapoints)
    dpi_scale_trans = plt.figure().dpi_scale_trans
    plt.clf()

    print('Plotting data on the heatmap...')
    with suppress_stdout_stderr():
        img = cv2.imread('grid.png')
        colors = sns.color_palette("light:#F00", 24, as_cmap=True)
        heatmap = sns.heatmap(
            data=datapoints,
            square=True,
            cmap=colors,
            zorder=2,
            alpha=0.6
        )
        plt.imshow(
            img,
            aspect=heatmap.get_aspect(),
            extent=heatmap.get_xlim() + heatmap.get_ylim(),
            zorder=1,
        )
        plt.xticks(range(20), list("ABCDEFGHIJKLMNOPQRST"))

    print('Exporting heatmap to image...')
    plt.savefig(export_path)
    plt.clf()
    print('Done!')
    return export_path

def deliverable(fields):
    from datetime import datetime
    start_datetime = datetime(2021,1,1) # start datetime
    end_datetime = datetime(2021,9,23) # end datetime
    generate_linklab_heatmap(start_datetime, end_datetime, fields, 'annual_aggregate.png')

def extra_credit(fields):
    from datetime import datetime
    from datetime import timedelta
    frame = 0
    now = datetime.now()
    start_datetime = datetime(2021, 1, 1)
    end_datetime = datetime(2021, 1, 2)

    while end_datetime < now:
        generate_linklab_heatmap(start_datetime, end_datetime, fields, f'img/frame_{frame}.png')
        start_datetime += timedelta(days=1)
        end_datetime += timedelta(days=1)
        frame += 1

def main():
    all_fields = [
        'Concentration_ppm',
        # 'H-Sensor',
        'Humidity_%',
        # 'T-Sensor',
        'Temperature_°C',
        # 'rssi',
        # 'PIR Status',
        'Supply voltage (OPTIONAL)_V',
        # 'Supply voltage availability',
        'Illumination_lx',
        # 'Range select',
        'Supply voltage_V',
        # 'Contact',
        # 'awair_score',
        'co2_ppm',
        'pm2.5_μg/m3',
        'voc_ppb'
    ]
    # deliverable(all_fields) # warning: takes a long time to run
    extra_credit(all_fields)

if __name__ == '__main__':
    main()
