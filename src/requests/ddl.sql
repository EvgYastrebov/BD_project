CREATE TABLE IF NOT EXISTS players (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	player_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(player_name) BETWEEN 1 and 50),
	team_id BIGINT NOT NULL REFERENCES teams
);

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
);

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
);

CREATE TABLE IF NOT EXISTS teams (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	team_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(team_name) BETWEEN 1 and 50)
);


CREATE TABLE IF NOT EXISTS tournaments (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	tournament_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(tournament_name) BETWEEN 1 and 50)
);

CREATE TABLE IF NOT EXISTS team_tournaments (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	tournament_id BIGINT NOT NULL REFERENCES tournaments,
	team_id BIGINT NOT NULL REFERENCES teams
);

CREATE TABLE IF NOT EXISTS players_history (
	id BIGSERIAL NOT NULL PRIMARY KEY,
	player_id BIGINT NOT NULL REFERENCES players,
	player_name VARCHAR(50) NOT NULL UNIQUE CHECK(LENGTH(player_name) BETWEEN 1 and 50),
	team_id BIGINT NOT NULL REFERENCES teams,
	history_dttm DATE
);
