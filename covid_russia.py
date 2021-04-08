import sqlite3
import sys
import matplotlib.pyplot as plt


def main():
    # open sqlite database from cli arg
    if len(sys.argv) != 2:
        print("usage: covid_russia.py <name_of_sqlite_database.db>")
        return 1

    con = sqlite3.connect(f"{sys.argv[1]}")

    date = []
    cases = []
    deaths = []

    for row in con.execute('SELECT date, total_cases, total_deaths '
                           'FROM covid_table WHERE location LIKE "Russia";'):
        date.append(row[0])
        case = row[1].rstrip('.0')
        death = row[2].rstrip('.0')
        if case != '':
            cases.append(int(row[1].rstrip('.0')))
        else:
            cases.append(0)
        if death != '':
            deaths.append(int(row[2].rstrip('.0')))
        else:
            deaths.append(0)

    count = list(range(len(cases)))
    fig, ax = plt.subplots()
    ax.plot(count, cases, linestyle='solid', label='cases')
    ax.set(xlabel='date', ylabel="cases", title="covid in Russia")
    ax.plot(count, deaths, linestyle='dashed', label='deaths')

    ax.legend()
    plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())
