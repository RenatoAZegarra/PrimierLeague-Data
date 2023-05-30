from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.team_model import Team 
from datetime import datetime
import requests
import json


@app.route('/league_table')
def league_table():
    if "user_id" not in session:
        return redirect("/")
    url = "https://api.football-data.org/v4/competitions/PL/standings"

    payload = ""
    headers = {"X-Auth-Token": "1154eb28e44c4787a64927a11c930900"}

    response = requests.request("GET", url, data=payload, headers=headers)
    # Retrieve data from API

    # Parse JSON data into a Python object
    data = json.loads(response.content)

    standings = data['standings'][0]['table']

    table_data = []

    for team in standings:
        position = team['position']
        team_id = team['team']['id']
        team_crest = team['team']['crest']
        name = team['team']['name']
        points = team['points']
        games_played = team['playedGames']
        wins = team['won']
        draws = team['draw']
        losses = team['lost']
        goal_diff = team['goalDifference']

        row = {
            "Position": position,
            "Team": name,
            "Points": points,
            "Games Played": games_played,
            "Wins": wins,
            "Draws": draws,
            "Losses": losses,
            "Goal Difference": goal_diff,
            "team_crest": team_crest,
            "team_id": team_id,
        }
        table_data.append(row)

    # Render HTML template with league table
    return render_template('league_table.html', table_data=table_data)

@app.route('/team/<team_id>')
def team_stats(team_id):
    if "user_id" not in session:
        return redirect("/")

    # Retrieve team data from the database
    team = Team.get_one({"id": team_id})
    if not team:
        return "Team not found"

    # Retrieve the last 10 matches from the API
    url = f"https://api.football-data.org/v2/teams/{team_id}/matches"
    headers = {'X-Auth-Token': "1154eb28e44c4787a64927a11c930900"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Filter the matches to only include the last 5
    last_five_matches = data['matches'][-5:]

    # Extract the relevant information for each match
    match_data = []
    for match in last_five_matches:
        date_str = match['utcDate']
        date_obj = datetime.fromisoformat(date_str)
        date = date_obj.strftime('%B %e, %Y')
        home_team = match['homeTeam']['name']
        away_team = match['awayTeam']['name']
        home_score = match['score']['fullTime']['homeTeam']
        away_score = match['score']['fullTime']['awayTeam']
        match_data.append((date, home_team, away_team, home_score, away_score))
    

    # Retrieve the standings from the API
    url = "https://api.football-data.org/v4/competitions/PL/standings"
    headers = {"X-Auth-Token": "1154eb28e44c4787a64927a11c930900"}
    response = requests.get(url, headers=headers)
    data = response.json()

    # Find the position of the team in the standings
    selected_team = None
    for team_standings in data['standings'][0]['table']:
        if team_standings['team']['id'] == int(team_id):
            position = team_standings['position']
            selected_team = team_standings
            break

    # Check if the selected team was found in the standings data
    if selected_team is None:
        return "Team not found in standings"

    # Extract the relevant data for the selected team
    points = selected_team['points']
    games_played = selected_team['playedGames']
    wins = selected_team['won']
    draws = selected_team['draw']
    losses = selected_team['lost']
    goals_for = selected_team['goalsFor']
    goals_against = selected_team['goalsAgainst']
    goal_diff = selected_team['goalDifference']

    url = f"https://api.football-data.org/v2/teams/{team_id}"
    headers = {'X-Auth-Token': "1154eb28e44c4787a64927a11c930900"}
    response = requests.get(url, headers=headers)
    team_data = response.json()
    squad = team_data['squad']
    for player in squad:
        dob = datetime.strptime(player["dateOfBirth"], "%Y-%m-%dT%H:%M:%SZ")
        player["formattedDob"] = dob.strftime("%B %e, %Y")
    if dob is None:
        player["formattedDob"] = player['dateOfBirth']
    # Render the table on the website using HTML and CSS
    return render_template('team_stats.html', team=team, match_data=match_data, position=position, name=team.name, points=points, games_played=games_played, wins=wins, draws=draws, losses=losses, goals_for=goals_for, goals_against=goals_against, goal_diff=goal_diff, squad=squad)

# def team_stats(team_id):
#     if "user_id" not in session:
#         return redirect("/")
    
#     url = f"https://api.football-data.org/v2/teams/{team_id}/matches"
#     headers = {'X-Auth-Token': "1154eb28e44c4787a64927a11c930900"}
#     response = requests.get(url, headers=headers)
#     data = response.json()

#     # Filter the matches to only include the last 5
#     last_five_matches = data['matches'][-10:]

#     # Extract the relevant information for each match
#     match_data = []
#     for match in last_five_matches:
#         date = match['utcDate']
#         home_team = match['homeTeam']['name']
#         away_team = match['awayTeam']['name']
#         home_score = match['score']['fullTime']['homeTeam']
#         away_score = match['score']['fullTime']['awayTeam']
#         match_data.append((date, home_team, away_team, home_score, away_score))
    
#     url = "https://api.football-data.org/v4/competitions/PL/standings"

#     payload = ""
#     headers = {"X-Auth-Token": "1154eb28e44c4787a64927a11c930900"}

#     response = requests.request("GET", url, data=payload, headers=headers)
#     # Retrieve data from API

#     # Parse JSON data into a Python object
#     data = json.loads(response.content)

#     standings = data['standings'][0]['table']

#     # Find the team name in the standings data
#     for team in standings:
#         if team['team']['id'] == int(team_id):
#             name = team['team']['name']
#             position = team['position']
#             break

#     # Extract the data for the selected team from the standings data
#     selected_team = standings[position - 1]
#     points = selected_team['points']
#     games_played = selected_team['playedGames']
#     wins = selected_team['won']
#     draws = selected_team['draw']
#     losses = selected_team['lost']
#     goals_for = selected_team['goalsFor']
#     goals_against = selected_team['goalsAgainst']
#     goal_diff = selected_team['goalDifference']

#     url = f"https://api.football-data.org/v2/teams/{team_id}"
#     headers = {'X-Auth-Token': "1154eb28e44c4787a64927a11c930900"}
#     response = requests.get(url, headers=headers)
#     team_data = response.json()
#     squad = team_data['squad']

#     # Render the table on the website using HTML and CSS
#     return render_template('team_stats.html', match_data=match_data, name=name, points=points, games_played=games_played, wins=wins, draws=draws, losses=losses, goals_for=goals_for, goals_against=goals_against, goal_diff=goal_diff, squad=squad, position=position)


