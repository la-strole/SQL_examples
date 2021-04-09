import sqlite3
import sys
import matplotlib.pyplot as plt
import requests
import pandas


def main():
    # download fresh csv file
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    csv_name = "covid_19.csv"
    with open(csv_name, "w") as local_file:
        local_file.write(requests.get(url).text)

    # copy csv to database
    db_name = "covid_19.db"
    table_names = ['covid_19']

    file_db = open(db_name, "w").close()
    con = sqlite3.connect(db_name)

    pandas.read_csv(csv_name).to_sql(table_names[0], con, if_exists='append', index=False)

    date = []
    cases = []
    deaths = []

    location = 'Russia'

    for row in con.execute('SELECT date, new_cases, total_deaths '
                           'FROM {} WHERE location LIKE ?;'.format(table_names[0]), [location]):
        date.append(row[0])
        case = row[1]
        death = row[2]
        if case:
            cases.append(int(row[1]))
        else:
            cases.append(0)
        if death:
            deaths.append(int(row[2]))
        else:
            deaths.append(0)

    con.close()

    count = list(range(len(cases)))
    fig, ax = plt.subplots()
    ax.plot(count, cases, linestyle='solid', label='cases')
    ax.set(xlabel='date', ylabel="cases", title=f"covid in {location}")
    ax.plot(count, deaths, linestyle='dashed', label='deaths')

    ax.legend()
    plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())
