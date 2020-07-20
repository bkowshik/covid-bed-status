import datetime
import glob
from pathlib import Path

import pandas as pd

from parse_bed_status import parse


def main():

    df = pd.DataFrame([])

    files = sorted(glob.glob('../data/downloads/*.html'))
    for file in files:

        # Making it a Path object for easier operations.
        file = Path(file)

        # Extract datetime in YYYY-MM-DD HH:MM format.
        file_ds = datetime.datetime.strptime(file.name.replace('.html', ''), '%Y-%m-%d %H:%M:%S')
        ds = datetime.datetime.strftime(file_ds, '%Y-%m-%d %H:00')

        file_df = parse(file)
        file_df['ds'] = ds
        print(file, file_df.shape)

        df = df.append(file_df)

    for metric in df.columns[1:-1]:

        # Pivot by the metric with hospital names as columns and datetime as rows.
        pivot = df.pivot_table(columns='ds', index='Name', values=metric)

        # Sort columns in descending order of the metric.
        # pivot = pivot.reindex(pivot.sum().sort_values(ascending=False).index, axis=1)

        # Write to a csv.
        filename = f'../data/timeseries/{metric}.csv'
        pivot.to_csv(filename)


if __name__ == '__main__':
    main()
