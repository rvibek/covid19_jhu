import pandas as pd
from urllib.parse import urljoin
import sys

country =  sys.argv[1]
baseurl = "https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/"
confirmed = "time_series_covid19_confirmed_global.csv"
deaths = "time_series_covid19_deaths_global.csv"
recovered = "time_series_covid19_recovered_global.csv"


states = [('confirmed', "time_series_covid19_confirmed_global.csv"),
          ('deaths', "time_series_covid19_deaths_global.csv"),
          ('recovered', "time_series_covid19_recovered_global.csv")]

def makedf(state, stateurl, country):
    df = pd.read_csv(stateurl)
    df = df[df['Country/Region'] == country]
    # df['status'] = state
    df.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
    df=pd.melt(df, id_vars='Country/Region', #['Lat', 'Long'],
        value_vars=list(df.columns[1:]), var_name='date', value_name=state)
    df['date'] = pd.to_datetime(df.date)
    df.set_index('date', inplace=True)
    return(df)

dfs = []
for state, stateurl in states:
    dfs.append(makedf(state, urljoin(baseurl, stateurl), country))

for df in dfs:
    df.drop('Country/Region', axis=1, inplace=True)

dfmerged = pd.concat(dfs, axis=1)

dfmerged_daily = dfmerged.diff(periods=1)
dfmerged_daily .columns = ['new_cases', 'new_deaths', 'new_recovered']

dfmerged_7avg = dfmerged_daily.rolling(7).mean()
dfmerged_7avg.columns = ['7day_avg_cases', '7day_avg_deaths', '7day_avg_recovered']

dfmerged_final = pd.concat([dfmerged, dfmerged_daily, dfmerged_7avg], axis=1)

filename = "/home/rvibek/git/covid19_jhu/"+country.lower()+'_covid19JHU.csv'
dfmerged_final.to_csv(filename)
