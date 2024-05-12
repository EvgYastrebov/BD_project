-- Информация о матче из matches
CREATE VIEW matches_info AS
SELECT h_team.team_name AS home_team, a_team.team_name AS away_team, m.team_h_goals AS home_goals, m.team_a_goals AS away_goals
FROM matches m
JOIN teams h_team ON m.team_id_h = h_team.id
JOIN teams a_team ON m.team_id_a = a_team.id;

-- Информация о минутах игрока в матче 
CREATE VIEW player_minuties AS
SELECT p.player_name, ps.minutes, h_team.team_name AS home_team, a_team.team_name AS away_team
FROM player_statictics ps
JOIN players p ON ps.player_id = p.id
JOIN matches m ON ps.match_id = m.id
JOIN teams h_team ON m.team_id_h = h_team.id
JOIN teams a_team ON m.team_id_a = a_team.id;

-- Информация о турнирах в который учавствует команда
CREATE VIEW team_tournament_inf AS
SELECT t.team_name, tournaments.tournament_name
FROM team_tournaments tt
JOIN teams t ON tt.team_id = t.id
JOIN tournaments ON tt.tournament_id = tournaments.id;
