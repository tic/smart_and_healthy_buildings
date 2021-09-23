
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

def grid_num_to_coord(grid):
    letters = 'ABCDEFGHIJKLMNOPQRST'
    # return (letter, number)
    # return (column, row)
    return ()


# Create a heat map for each grid point in the link lab
# if successful, return filepath of image
# on error, return none
def generate_linklab_heatmap(start_datetime, end_datetime, fields, export_path):
    # get sensor information
    fields_set = set(fields)
    import pandas as pd
    df = pd.read_csv('book_with_grids.csv')

    # grid range 0-199
    import utility as util
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
    for grid in range(200):
        sensors_in_grid = df[df['grid'] == grid]

        # for each sensor in the grid
        dps = 0
        for row_id, sensor in sensors_in_grid.iterrows():
            sensor_fields = sensor['fields'].split(',')
            device_id_list = [sensor['device_id']]
            relevant_fields = list(set(sensor_fields).intersection(fields_set))
            for field in relevant_fields:
                with suppress_stdout_stderr():
                    ldf = util.get_lfdf(field, start_datetime, end_datetime, device_id_list)
                if ldf is not None:
                    dps += ldf.shape[0]
                # dps += len(ldf) ??
        datapoints[int(grid / 20)][grid % 20] = dps

    print(datapoints)
    import seaborn as sns
    # img = mpimg.imread('grid.png')
    # plt.figure(img)


    import matplotlib.pyplot as plt
    with suppress_stdout_stderr():
        import cv2
        img = cv2.imread('grid.png')
        colors = sns.color_palette("Reds", 18)
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
    plt.savefig(export_path)


from datetime import datetime
start_datetime= datetime(2021,9,22) # start datetime
end_datetime= datetime(2021,9,23) # end datetime
generate_linklab_heatmap(start_datetime, end_datetime, ['Illumination_lx'], 'img/heatmap.png')
