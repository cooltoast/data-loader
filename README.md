# Data Loader

A script to load data into a database using spec files.

## Getting Started

### Prerequisites

- Python 2 or 3
- Postgres 9.6.8 or above. See https://github.com/CloverHealth/homebrew-tap, or for Postgres 10 do
```
brew install postgresql
```

### Installing

#### Database 
In `setup.sh`, update `<DATABASE>` to your desired database name.
In `config.json`, update `<DATABASE` and `<USER>` as well.

Then run the database setup script:
```
./setup.sh
```

#### Install Packages
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
To load all data files in a directory, you can do:
```
./load.py data/
```

Or to just load specific data file(s):
```
./load.py <file1> <file2> ...
```

### Testing
In the `data` directory are some sample data files. Files of type `testformat1` and `this_should_work` are expected to succeed, and those of type `this_should_fail` are expected to fail due to improper data file formatting.
