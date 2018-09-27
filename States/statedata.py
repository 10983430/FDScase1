import shapefile #the pyshp module
import pandas as pd
import numpy as np
from matplotlib import pyplot as p

sf = shapefile.Reader('states/states.shp')

fields = [x[0] for x in sf.fields][1:]
records = sf.records()
shps = [s.points for s in sf.shapes()]

electionResults = pd.read_csv("electionResults.csv")
population = pd.read_csv("population.csv", sep=';')
ethnicity = pd.read_csv("ethnicity.csv")
income = pd.read_csv("income.csv", sep=';')
electionVotes = pd.read_csv("electionVotes.csv")

states = pd.DataFrame(columns=fields, data=records)
states = states.assign(coords=shps)
ethnicity.rename(columns={'Location': 'State'}, inplace=True)
states.rename(columns={'STATE_NAME': 'State'}, inplace=True)
states = pd.merge(states, electionResults, on=['State'], how='outer')
states = pd.merge(states, population, on=['State'], how='outer')
states = pd.merge(states, ethnicity, on=['State'], how='outer')
states = pd.merge(states, income, on=['State'], how='outer')
states = pd.merge(states, electionVotes, on=['STATE_ABBR'], how='outer')

states = states.drop('Total', 1)
states = states.drop('DRAWSEQ', 1)
states = states.drop('STATE_FIPS', 1)
states = states.drop('SUB_REGION', 1)
states = states.drop('Unnamed: 4', 1)

states = states.drop(states.index[52])
states = states.drop(states.index[53])
states = states.drop(states.index[36])
states = states.drop(states.index[43])

states.rename(columns={'STATE_ABBR': 'State abbreviation'}, inplace=True)
states.rename(columns={'coords': 'Coordinates'}, inplace=True)

states = states.sort_values(by=['State'])
states = states.reset_index(drop=True)

states.to_json('stateData.json', orient='records', lines=True)
