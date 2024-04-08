import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Load the IPL matches dataset
df = pd.read_csv("data/match_info_data.csv")  # Replace "path_to_your_dataset.csv" with the actual path to your dataset

# Sidebar
with st.sidebar:
    st.title("IPL Matches Dashboard\n -By Vadik Amar(20BCS2872) and Shivam Gupta(20BCS7015)")
    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    selected_team1 = st.sidebar.selectbox("Select Team:", df['team1'].unique(),key="team1")
    selected_team2 = st.sidebar.selectbox("Select Team:", df['team2'].unique(),key="team2")
    year_list = list(df.season.unique())[:-1]
    selected_season = st.selectbox('Select a year', year_list)

# Main content
st.title("Interactive IPL Matches Dashboard")

# Display the dataset


# Interactive visualization based on selected attribute

# Count the number of wins for each team
team_wins = df['winner'].value_counts()

# Convert the result to a DataFrame
team_wins_df = pd.DataFrame({'Team': team_wins.index, 'Wins': team_wins.values})

# Sort the DataFrame by the number of wins
team_wins_df = team_wins_df.sort_values(by='Wins', ascending=False)
###################################################################################################################
df_wins = df.dropna(subset=['winner'])

# Step 2: Count the number of wins by state

wins_by_state = df_wins['state'].value_counts().reset_index()
wins_by_state.columns = ['state', 'wins']


# Create choropleth map
fig = px.choropleth(
    wins_by_state,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='state',
    color='wins',
    color_continuous_scale=selected_color_theme
)
fig.update_geos(fitbounds="locations", visible=False)

# Display choropleth map
st.write("## IPL Wins by Indian State")
st.plotly_chart(fig)

# Display the DataFrame using st.dataframe
st.dataframe(team_wins_df, column_order=("Team", "Wins"), hide_index=True, width=None,
             column_config={
                 "Team": st.column_config.TextColumn("Team"),
                 "Wins": st.column_config.ProgressColumn(
                     "Wins",
                     format="%d",
                     min_value=0,
                     max_value=max(team_wins_df['Wins'])
                 )}
             )

########################################################################################################
teams_color={"Chennai Super Kings":"#fcce06","Delhi Capitals":"#2561ae","Punjab Kings":"#ed1f27","Kolkata Knight Riders":"#3a225d","Mumbai Indians":"#004f91","Rajasthan Royals":"pink","Royal Challengers Bangalore":"#d5152c","Sunrisers Hyderabad":"#f7a721","Gujarat Titans":"#000435","Lucknow Super Giants":"#02066F","Rising Pune Supergiants":"black","Gujarat Lions":"orange","Deccan Chargers":"black","Pune Warriors":"grey","Kochi Tuskers Kerala":"purple"}
t1color=teams_color[selected_team1]
t2color=teams_color[selected_team2]
head=df[((df['team1']==selected_team1) & (df['team2']==selected_team2))|((df['team1']==selected_team2) & (df['team2']==selected_team1))]
winner = head.dropna(subset=['winner'])
x=len(winner[winner['winner']==selected_team1])
y=len(winner[winner['winner']==selected_team2])
nr=len(head)-x-y
fig2 = px.pie(names=[selected_team1, selected_team2,"NR"], values=[x,y,nr], hole=0.5, 
             color_discrete_sequence=[t1color, t2color,'white'], 
             labels={'label': 'Head to Head'})

# Streamlit application
st.title('Head to Head Results overall')
st.plotly_chart(fig2, use_container_width=True)

fig_bar = px.bar(x=[selected_team1, selected_team2, 'NR'], 
                 y=[x, y, nr], 
                 color=[selected_team1, selected_team2, 'NR'],
                 color_discrete_map={selected_team1: t1color, selected_team2: t2color, 'NR': 'white'},
                 labels={'x': 'Result', 'y': 'Count'})

# Update layout
fig_bar.update_layout(title='Head to Head Results Overall',
                      xaxis_title='Result',
                      yaxis_title='Count')

# Streamlit application
st.plotly_chart(fig_bar, use_container_width=True)

########################################################################################################

yearwin=df[(df['season']==selected_season) & df['winner'].notna()]
teamdic={"Chennai Super Kings":0,"Delhi Capitals":0,"Punjab Kings":0,"Kolkata Knight Riders":0,"Mumbai Indians":0,"Rajasthan Royals":0,"Royal Challengers Bangalore":0,"Sunrisers Hyderabad":0,"Gujarat Titans":0,"Lucknow Super Giants":0,"Rising Pune Supergiants":0,"Gujarat Lions":0,"Deccan Chargers":0,"Pune Warriors":0,"Kochi Tuskers Kerala":0}
for index, row in yearwin.iterrows():
    if row['winner'] is not None:
        teamdic[row['winner']] += 1

# Convert dictionary to DataFrame for plotting
team_wins_df = pd.DataFrame(list(teamdic.items()), columns=['Team', 'Wins'])

# Create line chart
fig_line = px.line(team_wins_df, x='Team', y='Wins', 
                   title=f'Wins per Team in Season {selected_season}',
                   labels={'Wins': 'Number of Wins'})

# Rotate x-axis labels for better readability
fig_line.update_layout(xaxis_tickangle=-45)

# Show the figure
st.plotly_chart(fig_line, use_container_width=True)


########################################################################################################
df_year=df[df['season']==selected_season]
toss_winner_year=df_year[df_year['toss_winner']==df_year['winner']]
tossloss_year=len(df_year)-len(toss_winner_year)
tosswin_year=len(toss_winner_year)
fig1 = px.pie(names=['Toss Loss', 'Toss Win'], values=[tossloss_year, tosswin_year], hole=0.5, 
             color_discrete_sequence=['#fff999', '#66b3ff'], 
             labels={'label': 'Toss Result'})

# Streamlit application
st.title(f'Toss Winner is Match Winner Visualization in {selected_season}')
st.plotly_chart(fig1, use_container_width=True)


