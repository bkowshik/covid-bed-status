# Aggregate


## Workflow

### Download all hourly files

```bash
# Get into the data directory.
cd covid-bed-status/data/

# Create a new directory to download all reports.
mkdir -p 'downloads' && cd 'downloads'

# Recursively download all files into the folder.
gsutil -m cp -r gs://covid-bed-status/downloads/bbmp/* .
```

### Merge into timeseries data

```bash
tree ../data/timeseries/

../data/timeseries/
├── Available HDU.csv
├── Available ICU Ventilator.csv
├── Available ICU.csv
├── Available general.csv
├── Available total.csv
├── Due for discharge HDU.csv
├── Due for discharge ICU Ventilator.csv
├── Due for discharge ICU.csv
├── Due for discharge general.csv
├── Due for discharge total.csv
├── Occupied HDU.csv
├── Occupied ICU Ventilator.csv
├── Occupied ICU.csv
├── Occupied general.csv
├── Occupied total.csv
├── Total HDU.csv
├── Total ICU Ventilator.csv
├── Total ICU.csv
├── Total general.csv
└── Total.csv

0 directories, 20 files
```