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

    # Load location of all hospitals.
    locations = pd.read_csv('../data/hospital_locations.csv')
    locations['Latitude'] = locations['Latitude'].round(6)
    locations['Longitude'] = locations['Longitude'].round(6)

    for metric in df.columns[1:-1]:

        # Pivot by the metric with hospital names as columns and datetime as rows.
        pivot = df.pivot_table(columns='ds', index='Name', values=metric)

        # Enrich with location data.
        merged = pd.merge(locations, pivot, on='Name', how='right').fillna('')

        # Write to a csv.
        filename = f'../data/timeseries/{metric}.csv'
        merged.drop(columns=['Address']).to_csv(filename, index=False)


if __name__ == '__main__':
    main()
