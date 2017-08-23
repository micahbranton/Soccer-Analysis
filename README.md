# Football Analytics

Get information from football games for different competitions and leverage data visualization to statistically analyze and visualize the performance of football teams and players. The scripts are written and intended to use with Python 3.

## Getting Started

### 1. Clone Repo

`git clone https://github.com/andrebrener/football_data.git`

### 2. Install Packages Required

Go in the directory of the repo and run:
```pip install -r requirements.txt```

### 3. Enjoy the repo :)

## What can you do?

### 1. Get Games Data
- Insert Constants in constants.py.
  - Select start & end dates.
  - Select competition from the competition dictionary.
- Run [game_data.py](https://github.com/andrebrener/football_data/blob/master/game_data.py).
- A directory named `game_data` will be created in the repo with a csv file named `games_data_{start_date}_{end_date}.csv`.
- This csv will contain the data for the games of the selected competition and dates including:
  - Date of the game.
  - Home & away teams.
  - Result of the game.
  - Total shots and shots on goal.
  - Percentage ball possessions.
  - Fouls and yellow & red cards.
  - Team who made the first goal.
  - Team that was 2-0 in any moment of the game. This value is null if no team complies with this condition.
  - Number of penalties per team.
  
 ### 2. Passes Map
  This graph shows the average location of the players and the pass distribution of the team during the game. By running [passes_map.py](https://github.com/andrebrener/football_data/blob/master/other_graphs/map_passes/passes_map.py), the csv must be in the format as [this one](https://github.com/andrebrener/football_data/blob/master/other_graphs/map_passes/river_valle.csv).
  
![img](http://i.imgur.com/6NuthFi.png)

### 3. Radars
This graph compares teams/players in many aspects of the game at the same time. By running [radars_graph.py](https://github.com/andrebrener/football_data/blob/master/radars/radars_graph.py), the csv must be in the format as [this one](https://github.com/andrebrener/football_data/blob/master/radars/players_data_2016.csv).

![img](http://i.imgur.com/Wr5ofJt.png)

### 4. Players Under or Overperforming
 This graph shows if the player was over or underperforming compared to what he was expected to. By running [over_under_perform.py](https://github.com/andrebrener/football_data/blob/master/other_graphs/performance_vs_xg/over_under_perform.py), the csv must be in the format as [this one](https://github.com/andrebrener/football_data/blob/master/other_graphs/performance_vs_xg/rodrigo_mora_xg.csv).
  
![img](http://i.imgur.com/T8EZ6nl.png)

 ### 5. Team & Player Analysis
The [season_analysis.py](https://github.com/andrebrener/football_data/blob/master/season_analysis.py) script is used to compare teams and [team_players_comparison.py](https://github.com/andrebrener/football_data/blob/master/other_graphs/compare_team_players/team_players_comparison.py) compares the players. After running the scripts, you will get a series un graphs with their comparison in different aspects of the game. The options for these graphs are:
- Change titles and subtitles of graphs.
- Define a team/player that you want to be remarked from the rest.
- The maximum number of teams/players in the graph.

![img](http://i.imgur.com/qaJvp8r.png)

  
### 6. Get Analysis for Player when on & off the Pitch
- Insert Constants in constants.py.
  - Select start & end dates.
  - Select competition from the competition dictionary.
- Run [player_in_goals.py](https://github.com/andrebrener/football_data/blob/master/player_in_goals.py).
- A directory named `player_in_goals` will be created in the repo with a csv file named `games_data_{start_date}_{end_date}.csv`.
- This csv will contain the data for the players of the selected competition and dates including:
  - Name and team of the player. More than one player with exactly the same name in the same team will make that data invalid.
  - Minutes on and off the pitch.
  - Total team goals for and against.
  - Team goals for and against with the player in the pitch.
  

  



  

 



