## Intro

This is a script to load data into a database, using spec files to encode schema of the data.

### Adding Context (to make it interesting)

This can be a script that lives on its own machine, alongside a data pulling script. The data pulling script can be scheduled with a cronjob to periodically download data from an app, and this script can write that data to a database for machine learning training or metrics.

## Requirements

1. Load data from data file to database in one transaction, and track that its been loaded.
2. Throw error if data file is improperly formatted, spec file is missing, or if write transaction fails.
3. Data file loading is idempotent.

## Database Structure

A table for each spec file 
- contains all columns in spec file.
- contains `drop_date` column to help differentiate between rows that originated from different data files.

A `data_loaded` table
- tracks when each data file was loaded into the database.

## Easy Wins

- create index on `data_file` column of `data_loaded` table, since we are querying it for every data file.
- cache spec file fields info into redis or elsewhere in-memory, since we are opening the spec file for every data file.
- protect against SQL injection
  - sanitize SQL inputs with `psycopg2`:
    - ```cur.execute('SELECT * FROM {}'.format(...))``` -> ```cur.execute('SELECT * FROM %s', (user_input,))```
  - use an ORM like SQLAlchemy

## Other Possibilities and Considerations
- Enforce uniqueness on data file names (`data_file` column in `data_loaded`).
- Delete data files after they're loaded into database.
  - If using the data pulling script like above, it could download the data files to a temporary directory.
