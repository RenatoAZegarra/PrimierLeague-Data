from flask import render_template, session
from flask_app import app
from datetime import datetime
import requests
import json
from flask_app.models.user_model import User
from flask_app.models.team_model import Team

@app.route("/welcome", methods=["GET"])
def welcome():
    if "user_id" not in session:
        return redirect("/")

    # Get the user's team ID from the session
    team_id = session.get("team_id")

    # Get the team's name and stadium picture URL from the database
    team = Team.get_one({"id": team_id})

    # Get the team's matches from the API
    matches_url = f"https://api.football-data.org/v2/teams/{team_id}/matches"
    headers = {'X-Auth-Token': "1154eb28e44c4787a64927a11c930900"}
    matches_response = requests.get(matches_url, headers=headers)
    matches_data = matches_response.json()
    for match in matches_data["matches"]:
        match_date = datetime.strptime(match["utcDate"], "%Y-%m-%dT%H:%M:%SZ")
        match["formattedDate"] = match_date.strftime("%B %e, %Y")

    # Get the team's squad from the API
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
    squad_url = f"https://api.football-data.org/v2/teams/{team_id}"


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

    return render_template("welcome.html", full_name=session.get("full_name"), team=team, matches=matches_data["matches"], squad=squad,
position=position, name=team.name, points=points, games_played=games_played, wins=wins, draws=draws, losses=losses, goals_for=goals_for, goals_against=goals_against, goal_diff=goal_diff)

