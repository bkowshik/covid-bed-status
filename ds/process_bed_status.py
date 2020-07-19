import pandas as pd
from bs4 import BeautifulSoup


def main():
    input_filename = '../data/bed_status.html'
    with open(input_filename) as f:
        soup = BeautifulSoup(f.read().replace(u'\xa0', ' '), 'html.parser')

    data_rows = []

    tables = soup.find_all(id="excltable")
    for i, table in enumerate(tables):

        # if i not in [1, 2, 3, 4, ]:
        #     continue

        rows = table.find_all('tr')

        # Skip when the table does not have counts per hospital.
        if len(rows[2]) < 30:
            continue

        for row in rows:

            tds = row.find_all('td')

            # Skip over empty rows or rows that are not required like the total row.
            if not tds or len(tds) <= 10 or (tds[0].text is None) or (tds[0].text == '') or (tds[0].text == '\xa0'):
                continue

            # Store the header row as columns of the DataFrame.
            elif tds[0].text == '#':
                columns = [' '.join(td.text.split()) for td in tds]

            # Store the datasets.
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
    df[df.columns[3:]] = df[df.columns[3:]].astype('int')

    # Drop the first column which has serial numbers.
    df = df[df.columns[1:]].sort_values(by='Occupied total', ascending=False)

    # There are some duplicate rows too.
    df.drop_duplicates(inplace=True)

    output_filename = '../data/bed_status.csv'
    df.to_csv(output_filename, index=False)


if __name__ == '__main__':
    main()
