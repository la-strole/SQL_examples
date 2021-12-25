import sqlite3
import matplotlib.pyplot as plt
import requests
import csv
import sys
import argparse


def main(location, arg):
    # Download fresh csv file

    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    csv_name = "covid_19.csv"
    with open(csv_name, "w") as local_file:
        local_file.write(requests.get(url).text)

    # Copy csv to database
    with open(csv_name, 'r') as local_file:

        rows = csv.reader(local_file)

        headers = next(rows)
        table = [f'{i} TEXT' for i in headers]

        db_name = "covid_19.db"
        # "file::memory:?cache=shared"
        con = sqlite3.connect("file::memory:?cache=shared")

        # Create table on database
        try:
            con.execute(f"CREATE TABLE covid_19 ({', '.join(table)})")
        except sqlite3.OperationalError as e:
            print(e)

        for row in rows:
            for item in range(len(row)):
                if row[item] == '':
                    row[item] = "'0'"
                else:
                    row[item] = row[item].replace("\'", "")
                    row[item] = f"'{row[item]}'"

            # print(row)
            command = f"INSERT INTO covid_19 ({', '.join(headers)}) VALUES ({', '.join(row)});"
            # print(command)
            con.execute(command)

        con.commit()

    # Plot data
    for item in arg:
        assert item in headers, f'Argument {item} is not valid'

    date = []
    data = [[] for i in arg]

    command = f"SELECT date, {', '.join(arg)} FROM covid_19 WHERE location LIKE ?"
    rows = con.execute(command, (location,)).fetchall()
    for row in rows:

        date.append(row[0])
        for i in range(len(arg)):
            data[i].append(float(row[i + 1]))

    con.close()

    count = list(range(len(date)))

    fig, ax = plt.subplots()
    for i in range(len(arg)):
        ax.plot(count, data[i], linestyle='solid', label=f'{arg[i]}')
    ax.set(xlabel='date', ylabel=f'{", ".join(arg)}', title=f"covid in {location} at {date[-1]}")

    ax.legend()
    plt.show()

    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("location", help="location in English ex Russia or Ukraine etc")
    parser.add_argument("arg", nargs='+', type=str, help="tuple of data to plot")

    args = parser.parse_args()

    sys.exit(main(args.location, args.arg))

'''

    Available data for arg
      "iso_code" TEXT,
      "continent" TEXT,
      "location" TEXT,
      "date" TEXT,
      "total_cases" REAL,
      "new_cases" REAL,
      "new_cases_smoothed" REAL,
      "total_deaths" REAL,
      "new_deaths" REAL,
      "new_deaths_smoothed" REAL,
      "total_cases_per_million" REAL,
      "new_cases_per_million" REAL,
      "new_cases_smoothed_per_million" REAL,
      "total_deaths_per_million" REAL,
      "new_deaths_per_million" REAL,
      "new_deaths_smoothed_per_million" REAL,
      "reproduction_rate" REAL,
      "icu_patients" REAL,
      "icu_patients_per_million" REAL,
      "hosp_patients" REAL,
      "hosp_patients_per_million" REAL,
      "weekly_icu_admissions" REAL,
      "weekly_icu_admissions_per_million" REAL,
      "weekly_hosp_admissions" REAL,
      "weekly_hosp_admissions_per_million" REAL,
      "new_tests" REAL,
      "total_tests" REAL,
      "total_tests_per_thousand" REAL,
      "new_tests_per_thousand" REAL,
      "new_tests_smoothed" REAL,
      "new_tests_smoothed_per_thousand" REAL,
      "positive_rate" REAL,
      "tests_per_case" REAL,
      "tests_units" TEXT,
      "total_vaccinations" REAL,
      "people_vaccinated" REAL,
      "people_fully_vaccinated" REAL,
      "total_boosters" REAL,
      "new_vaccinations" REAL,
      "new_vaccinations_smoothed" REAL,
      "total_vaccinations_per_hundred" REAL,
      "people_vaccinated_per_hundred" REAL,
      "people_fully_vaccinated_per_hundred" REAL,
      "total_boosters_per_hundred" REAL,
      "new_vaccinations_smoothed_per_million" REAL,
      "new_people_vaccinated_smoothed" REAL,
      "new_people_vaccinated_smoothed_per_hundred" REAL,
      "stringency_index" REAL,
      "population" REAL,
      "population_density" REAL,
      "median_age" REAL,
      "aged_65_older" REAL,
      "aged_70_older" REAL,
      "gdp_per_capita" REAL,
      "extreme_poverty" REAL,
      "cardiovasc_death_rate" REAL,
      "diabetes_prevalence" REAL,
      "female_smokers" REAL,
      "male_smokers" REAL,
      "handwashing_facilities" REAL,
      "hospital_beds_per_thousand" REAL,
      "life_expectancy" REAL,
      "human_development_index" REAL,
      "excess_mortality_cumulative_absolute" REAL,
      "excess_mortality_cumulative" REAL,
      "excess_mortality" REAL,
      "excess_mortality_cumulative_per_million" REAL
'''
