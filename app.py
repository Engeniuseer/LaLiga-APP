import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import Counter

@st.cache(allow_output_mutation=True)
def init(filename):
    return pd.read_csv(filename)


df=init("data/season-1819.csv")
# Emoji from https://getemoji.com/
st.title('⚽️ LALIGA 2018-2019 APP ⚽️')
option = st.sidebar.selectbox('Select your option:',('General','Match','Team'))

if option=='General':
    st.markdown("[DataSource](https://datahub.io/sports-data/spanish-la-liga#readme) link")
    st.write('Database header:')
    st.write(df.head())
    
    st.write('This are all the teams in LaLiga Season 2018-2019:')
    teams_list=np.unique(np.array(df['HomeTeam']))
    st.write(' -'.join(teams_list))
    
    st.markdown("## Goal Distribution")
    plt.subplot(121)
    plt.title('Home Team Goals distribution')
    plt.xlabel('Home Goals')
    plt.ylabel('Density')
    plt.hist(df['FTHG'],bins=np.max(np.array(df['FTHG'])),color=(0.2,0.9,0.5),density=True,align='left')
    plt.subplot(122)
    plt.title('Away Team Goals distribution')
    plt.xlabel('Away Goals')
    plt.ylabel('Density')
    plt.hist(df['FTAG'],bins=np.max(np.array(df['FTAG'])),color=(0.9,0.2,0.5),density=True,align='left')
    st.pyplot()
elif option=='Match':
    teams_list=np.unique(np.array(df['HomeTeam']))
    st.markdown("## Match Statistics")
    match_result=[str(df['FTHG'][i])+str(df['FTAG'][i]) for i in range(len(df))]
    df['MR']=match_result
    freq_dict=Counter(df['MR'].apply(str))
    plt.figure(figsize=(7,7))
    p=sns.jointplot(x =df['FTHG'] ,y=df['FTAG'],kind="hex", space=0, color=(0.3,0.8,0.5)).set_axis_labels("Home Team Goals", "Away Team Goals")
    p.fig.suptitle("Result Distribution")
    st.pyplot()
    
    st.markdown("## Search specific match")
    home = st.selectbox('Select Home Team:',(teams_list))
    away = st.selectbox('Select Away Team:',(teams_list))
    if home!=away:
        c1=df['HomeTeam']==home
        c2=df['AwayTeam']==away
        row=df.where( c1 & c2 )
        st.table(row.dropna()[['Date','HomeTeam','AwayTeam','FTHG','FTAG','HS','AS','HY','AY','HR','AR','HC','AC']])
    else:
        st.write("WARNING: Home team must be different than Away team")
else:
    teams_list=np.unique(np.array(df['HomeTeam']))
    team = st.sidebar.selectbox('Select a team:',(teams_list))
    st.markdown("## %s Statistics"%team)
    th=df.where(df['HomeTeam']==team).dropna()
    ta=df.where(df['AwayTeam']==team).dropna()
    final_league=['Barcelona','Ath Madrid','Real Madrid','Valencia','Getafe','Sevilla','Espanol','Ath Bilbao',
              'Sociedad','Betis','Alaves','Eibar','Leganes','Villarreal','Levante','Valladolid','Celta','Girona',
              'Huesca','Vallecano']
    st.write("-League Position: "+str(final_league.index(team)+1))
    st.write("-Goals scored: "+str(np.sum(th['FTHG'].append(ta['FTAG']))))
    st.write("-Goals received: "+str(np.sum(th['FTAG'].append(ta['FTHG']))))
    st.write("-Average number of yellow cards per match: %.3f"%np.mean(th['HY'].append(ta['AY'])))
    st.write("-Average number of corners per match: %.3f"%np.mean(th['HC'].append(ta['AC'])))
    st.write("-Average number of red cards per match: %.3f"%np.mean(th['HR'].append(ta['AR'])))