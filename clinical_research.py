import collections
import sys
import pandas
import requests
import sqlite3
import os


def main():
    # download the csv file

    csv_filename = 'clinical_trials.csv'

    path = "https://clinicaltrials.gov/ct2/results/download_fields?cntry=RU&down_count=10000&down_fmt=csv&down_flds=all"
    payload = {'cntry': 'RU', 'down_count': '10000', 'down_fmt': 'csv', 'down_flds': 'all'}
    r = requests.get(path, params=payload)
    if r.status_code != 200:
        print(f'can not download data. status code = {r.status_code}\n', sys.stderr)
        return -1

    with open(csv_filename, 'w') as csv_file:
        csv_file.write(r.text)

    # create database in memory
    con = sqlite3.connect(':memory:')
    cur = con.cursor()

    # copy the data from the csv file to sqlite db in memory with pandas lib
    tables = ['clinical_res']
    pandas.read_csv(csv_filename).to_sql(tables[0], con, if_exists='append', index=False)

    cur.execute(f'SELECT COUNT(rowid) FROM {tables[0]}')
    print(f'total number of lines in DB: {cur.fetchone()[0]}\n')
    # make search in DB
    data = collections.OrderedDict([('Title', '%BRAF%'), ('Status', 'Recruiting')])

    cur.execute(f'SELECT Title, url FROM {tables[0]} WHERE {list(data.keys())[0]} LIKE ? AND '
                f'{list(data.keys())[1]} = ?;', [f'%{data["Title"]}%', data['Status']])

    for num, line in enumerate(cur.fetchall()):
        print(f'{num + 1}\t{line[0]}\t{line[1]}')

    con.close()

    while 1:
        user_inout = input('Do you want to delete csv file from your PC (y/n)')
        if user_inout == 'y' or 'Y':
            try:
                os.remove(f'{csv_filename}')
                break
            except OSError:
                print("Can not delete file", sys.stderr)
                return -1
        elif user_inout == 'n' or 'N':
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
