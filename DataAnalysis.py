# -*- coding: utf-8 -*-
"""
Created on Sat May  4 18:26:26 2019

@author: Nufail Ismath
"""

import pandas as pd # data processing, The dataset
import matplotlib.pyplot as mlt
import seaborn as sns
mlt.style.use('fivethirtyeight') #customizing plots with style sheets
import plotly.offline as py #for visualisation
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go #for visualisation

datasets = pd.read_csv('C:\\Users\\User\\Desktop\\Second Year\\SDGP\\Data Science\\datasets.csv') #The path of the datasets
deliveries = pd.read_csv('C:\\Users\\User\\Desktop\\Second Year\\SDGP\\Data Science\\deliveries.csv') #the path of the datasets
head = datasets.head(2)
head1 = deliveries.head(2)

datasets.drop(['umpire3'],axis=1,inplace=True)  #since all the values are NaN
deliveries.fillna(0,inplace=True)     #filling all the NaN values with 0

datasets['team1'].unique()

#Team Abbreviations
datasets.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)

deliveries.replace(['Mumbai Indians','Kolkata Knight Riders','Royal Challengers Bangalore','Deccan Chargers','Chennai Super Kings',
                 'Rajasthan Royals','Delhi Daredevils','Gujarat Lions','Kings XI Punjab',
                 'Sunrisers Hyderabad','Rising Pune Supergiants','Kochi Tuskers Kerala','Pune Warriors','Rising Pune Supergiant']
                ,['MI','KKR','RCB','DC','CSK','RR','DD','GL','KXIP','SRH','RPS','KTK','PW','RPS'],inplace=True)


print('Total Matches Played:',datasets.shape[0])#prints the total match played
print(' \n Venues Played At:',datasets['city'].unique())     #venues played
print(' \n Teams :',datasets['team1'].unique())             #Teams

print((datasets['player_of_match'].value_counts()).idxmax(),' : has most man of the match awards') #print the player who hast the most man of the maych title 
print(((datasets['winner']).value_counts()).idxmax(),': has the highest number of match wins') #print the team which has highest winnings

print('\n############################ Player of the match ############################\n')
matchesPlayed = pd.concat([datasets['team1'],datasets['team2']])
matchesPlayed = matchesPlayed.value_counts().reset_index()
matchesPlayed.columns=['Team','Total Matches']
matchesPlayed['wins']=datasets['winner'].value_counts().reset_index()['winner']
matchesPlayed.set_index('Team',inplace=True)

axis1 = go.Bar(
    x=matchesPlayed.index,              #The index of the matches played
    y=matchesPlayed['Total Matches'],   #total number of matches played
    name='Total Matches'
)
axis2 = go.Bar(
    x=matchesPlayed.index,              #the index of match played
    y=matchesPlayed['wins'],            #the winnings of the team
    name='Matches Won'
)

data = [axis1, axis2]
layout = go.Layout(
    barmode='stack'
)

figure = go.Figure(data=data, layout=layout)
py.iplot(figure, filename='stacked-bar') #saves the data in plotly acount, in this case it saves offline
mlt.subplots(figsize=(10,6)) #plot the plots in a figure.


axis = datasets['player_of_match'].value_counts().head(10).plot.bar(width=.8, color=sns.color_palette('husl',10))  #counts the values corresponding 

# to each batsman and then filters out the top 10 batsman and then plots a bargraph 
axis.set_xlabel('player_of_match') 
axis.set_ylabel('count')
for p in axis.patches:
    axis.annotate(format(p.get_height()), (p.get_x()+0.15, p.get_height()+0.25))
mlt.show()

#top 10 batsmen

top_scores = deliveries.groupby(["match_id", "batsman","batting_team"])["batsman_runs"].sum().reset_index()

#top_scores=top_scores[top_scores['batsman_runs']>100]
top_scores.sort_values('batsman_runs', ascending=0).head(10)
top_scores.nlargest(10,'batsman_runs')


print('\n############################ Best Bowler ############################\n')
#top Bowlers graph
mlt.subplots(figsize=(10,6))
dismissal_kinds = ["bowled", "caught", "lbw", "stumped", "caught and bowled", "hit wicket"]  #since run-out is not creditted to the bowler
counter=deliveries[deliveries["dismissal_kind"].isin(dismissal_kinds)]
axis=counter['bowler'].value_counts()[:10].plot.bar(width=0.8,color=sns.color_palette('hls',10))
axis.set_xlabel('Bowlers')
axis.set_ylabel('Count')
for p in axis.patches:
    axis.annotate(format(p.get_height()), (p.get_x()+0.10, p.get_height()),fontsize=15)
mlt.show()
