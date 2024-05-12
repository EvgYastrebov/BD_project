import psycopg2
import sqlite3
import Config as cfg
import random
from faker import Faker
import matplotlib.pyplot as plt

class Database:
    def __init__(self):
        self.__conn = psycopg2.connect(database = cfg.db_name, user = cfg.db_user,  password = cfg.db_password, host = cfg.db_host)

    def CreateDb(self):
        cur = self.__conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS players (
	        id BIGSERIAL NOT NULL PRIMARY KEY,
	        player_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(player_name) BETWEEN 1 and 50),
	        team_id BIGINT NOT NULL REFERENCES teams)''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            date DATE,
            team_id_h BIGINT NOT NULL REFERENCES teams,
            team_id_a BIGINT NOT NULL REFERENCES teams,
            team_h_goals INTEGER NOT NULL CHECK (team_h_goals >= 0),
            team_a_goals INTEGER NOT NULL CHECK (team_a_goals >= 0),
            team_h_xg NUMERIC NOT NULL CHECK (team_h_xG >= 0.0),
            team_a_xg NUMERIC NOT NULL CHECK (team_a_xG >= 0.0),
            tournament_id BIGINT NOT NULL REFERENCES tournaments	
        )''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS player_statictics (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            match_id BIGINT NOT NULL REFERENCES matches,
            player_id BIGINT NOT NULL REFERENCES players,
            minutes INTEGER NOT NULL CHECK (minutes >= 0),
            shots INTEGER NOT NULL CHECK (shots >= 0),
            xg NUMERIC NOT NULL CHECK (xG >= 0.0),
            goals INTEGER NOT NULL CHECK (goals >= 0),
            key_passes INTEGER NOT NULL  CHECK (key_passes >= 0),
            xa NUMERIC NOT NULL  CHECK (xA >= 0.0),
            assistes INTEGER NOT NULL  CHECK (assistes >= 0)
        )''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            team_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(team_name) BETWEEN 1 and 50)
        )''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS tournaments (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            tournament_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(tournament_name) BETWEEN 1 and 50)
        )''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS team_tournaments (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            tournament_id BIGINT NOT NULL REFERENCES tournaments,
            team_id BIGINT NOT NULL REFERENCES teams
        )''')

        cur.execute('''
        CREATE TABLE IF NOT EXISTS players_history (
            id BIGSERIAL NOT NULL PRIMARY KEY,
            player_id BIGINT NOT NULL REFERENCES players,
            player_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(player_name) BETWEEN 1 and 50),
            team_id BIGINT NOT NULL REFERENCES teams,
            history_dttm DATE
        )''')
        self.__conn.commit()  

    def AddDataPlayer(self, player_name, team_id):
        try:
            cur = self.__conn.cursor()

            cur.execute(f"SELECT COUNT(*) as player_name FROM players WHERE player_name = %s", (player_name,))
            res = cur.fetchone()
            if res[0] > 0:
                return (False, "Игрок с таким player_name уже существует")

            cur.execute('''
                INSERT INTO players (player_name, team_id) 
                VALUES (%s, %s) 
            ''', (player_name, team_id))
            self.__conn.commit()

        except sqlite3.Error as e:
            return (False, str(e))

        return (True, '')
    
    def AddDataMatches(self, date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO matches (date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            ''', (date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False
        return True
    
    def AddDataPlayerStatictics(self, match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assistes):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO player_statictics (match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assistes) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ''', (match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assistes))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False
        return True

    def AddDataTeams(self, team_name):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT COUNT(*) as team_name FROM teams WHERE team_name = %s", (team_name,))
            res = cur.fetchone()
            if res[0] > 0:
                return (False, "Команда с таким team_name уже существует")

            cur.execute('''
                INSERT INTO teams (team_name) 
                VALUES (%s) 
            ''', (team_name,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return (False, str(e))
        return (True, '')
    
    def AddDataTournaments(self, tournament_name):
        try:
            cur = self.__conn.cursor()
            cur.execute("SELECT COUNT(*) as tournament_name FROM tournaments WHERE tournament_name = %s", (tournament_name,))
            res = cur.fetchone()
            if res[0] > 0:
                return (False, "Команда с таким team_name уже существует")

            cur.execute('''
                INSERT INTO tournaments (tournament_name) 
                VALUES (%s) 
            ''', (tournament_name,))
            self.__conn.commit()
        except sqlite3.Error as e:
            return (False, str(e))
        return (True, '')

    def AddDataTeamTournaments(self, tournament_id, team_id):
        try:
            cur = self.__conn.cursor()
            cur.execute('''
                INSERT INTO team_tournaments (tournament_id, team_id) 
                VALUES (%s, %s) 
            ''', (tournament_id, team_id))
            self.__conn.commit()
        except sqlite3.Error as e:
            return False
        return True

    def GetDataPlayerStatisticsByPlayerId(self):
        try:
            cur = self.__conn.cursor()
            cur.execute(f"SELECT match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assistes FROM player_statictics")
            res = cur.fetchall()
            if not res:
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
        return False
    

def GeneratePlayersData(num_players):
    players_data = []
    for _ in range(num_players):
        player_name = fake.name()
        team_id = random.randint(1, 10)  # Assuming there are 10 teams
        players_data.append((player_name, team_id))
    return players_data

def GenerateMatchesData(num_matches):
    matches_data = []
    for _ in range(num_matches):
        date = fake.date()
        team_id_h = random.randint(1, 10)
        team_id_a = random.randint(1, 10)
        team_h_goals = random.randint(0, 5)
        team_a_goals = random.randint(0, 5)
        team_h_xg = round(random.uniform(0.0, 5.0), 2)
        team_a_xg = round(random.uniform(0.0, 5.0), 2)
        tournament_id = random.randint(1, 3)
        matches_data.append((date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id))
    return matches_data

def GeneratePlayerStatisticsData(num_stats, num_players, num_matches):
    player_statistics_data = []
    for _ in range(num_stats):
        match_id = random.randint(1, num_matches)
        player_id = random.randint(1, num_players)
        minutes = random.randint(0, 90)
        shots = random.randint(0, 10)
        xg = round(random.uniform(0.0, 3.0), 2)
        goals = random.randint(0, 3)
        key_passes = random.randint(0, 5)
        xa = round(random.uniform(0.0, 3.0), 2)
        assists = random.randint(0, 3)
        player_statistics_data.append((match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assists))
    return player_statistics_data

def GenerateTeamsData(num_teams):
    teams_data = []
    for _ in range(num_teams):
        team_name = fake.company()
        teams_data.append(team_name)
    return teams_data

def GenerateTournamentsData(num_tournaments):
    tournaments_data = []
    for _ in range(num_tournaments):
        tournament_name = fake.word()
        tournaments_data.append(tournament_name)
    return tournaments_data

def GenerateTeamTournamentsData(num_team_tournaments, num_teams, num_tournaments):
    team_tournaments_data = []
    for _ in range(num_team_tournaments):
        tournament_id = random.randint(1, num_tournaments)
        team_id = random.randint(1, num_teams)
        team_tournaments_data.append((tournament_id, team_id))
    return team_tournaments_data


fake = Faker()
dbase = Database()

for team in GenerateTeamsData(10):
    dbase.AddDataTeams(team)

for tournament in GenerateTournamentsData(3):
    dbase.AddDataTournaments(tournament)

for player_name, team_id in GeneratePlayersData(30):
    dbase.AddDataPlayer(player_name, team_id)

for date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id in GenerateMatchesData(30):
    dbase.AddDataMatches(date, team_id_h, team_id_a, team_h_goals, team_a_goals, team_h_xg, team_a_xg, tournament_id)

for tournament_id, team_id in GenerateTeamTournamentsData(10, 10, 3):
    dbase.AddDataTeamTournaments(tournament_id, team_id)

for match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assists in GeneratePlayerStatisticsData(30, 30, 30):
    dbase.AddDataPlayerStatictics(match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assists)


xg_all = []
goals_all = []
key_passes_all = []
xa_all = []
for match_id, player_id, minutes, shots, xg, goals, key_passes, xa, assists in dbase.GetDataPlayerStatisticsByPlayerId():
    xg_all.append(xg)
    goals_all.append(goals)
    key_passes_all.append(key_passes)
    xa_all.append(xa)

plt.scatter(xg_all, goals_all)
plt.xlabel('xG')
plt.ylabel('Goals')
plt.title('Goals vs Expected Goals')
plt.show()

plt.scatter(key_passes_all, xa_all)
plt.xlabel('key_passes')
plt.ylabel('xA')
plt.title('key_passes vs xA')
plt.show()
