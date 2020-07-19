import pandas as pd
from bs4 import BeautifulSoup


def parse(filename):

    # Read file and prepare the soup.
    with open(filename) as f:
        soup = BeautifulSoup(f.read().replace(u'\xa0', ' '), 'html.parser')

    # To store counts for every hospital.
    data_rows = []

    # Hospitals are grouped by categories and every category is a table of its own.
    tables = soup.find_all(id="excltable")
    for i, table in enumerate(tables):

        # Some tables are summaries and don't have counts per hospital. Skip them.
        rows = table.find_all('tr')
        if len(rows[2]) < 30:
            continue

        for row in rows:

            tds = row.find_all('td')

            # Skip over empty rows, table headers or rows that are not required like the total row.
            if not tds or len(tds) <= 10 or (tds[0].text is None) or (tds[0].text == '') or (tds[0].text == '\xa0') or (tds[0].text == '#'):
                continue

            # Store the counts after cleanup.
            else:
                data_row = []
                for td in tds:
                    text = ' '.join(td.text.split())
                    data_row.append(text)
                data_rows.append(data_row)

    columns = [
        'ID',
        'Name',
        'Total general',
        'Total HDU',
        'Total ICU',
        'Total ICU Ventilator',
        'Total',
        'Occupied general',
        'Occupied HDU',
        'Occupied ICU',
        'Occupied ICU Ventilator',
        'Occupied total',
        'Available general',
        'Available HDU',
        'Available ICU',
        'Available ICU Ventilator',
        'Available total',
        'Due for discharge general',
        'Due for discharge HDU',
        'Due for discharge ICU',
        'Due for discharge ICU Ventilator',
        'Due for discharge total',
    ]

    # Some rows have empty rows instead of 0. So, filling them with zeros.
    df = pd.DataFrame(data_rows, columns=columns).fillna('0')

    # Change data types of all the count columns.
    df[df.columns[2:]] = df[df.columns[2:]].astype('int')

    # Drop the first column which has serial numbers.
    df = df[df.columns[1:]].sort_values(by='Occupied total', ascending=False)

    # There are some duplicate rows too.
    df.drop_duplicates(inplace=True)

    return df


def main():
    input_filename = '../data/bed_status.html'
    df = parse(input_filename)

    output_filename = '../data/bed_status.csv'
    df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()
