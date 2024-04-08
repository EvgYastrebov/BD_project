-- 1) Получаем всех игроков в АПЛ которые забили гол или отдали голевой пас в туре

SELECT players.player_name, player_statictics.goals, player_statictics.assistes 
FROM players
INNER JOIN player_statictics ON players.id = player_statictics.player_id
INNER JOIN matches ON player_statictics.match_id = matches.id
WHERE matches.tournament_id = 1 AND matches.date >= '2024-04-06' AND matches.date <= '2024-04-07' AND (player_statictics.goals > 0 OR player_statictics.assistes > 0);


--  2) Получаем топ 10 игроков в АПЛ которые не забили, имея наибольший xG в туре

SELECT players.player_name, player_statictics.shots, player_statictics.xg
FROM players
INNER JOIN player_statictics ON players.id = player_statictics.player_id
INNER JOIN matches ON player_statictics.match_id = matches.id
WHERE matches.tournament_id = 1 AND matches.date >= '2024-04-06' AND matches.date <= '2024-04-07' AND player_statictics.goals = 0
ORDER BY player_statictics.xg DESC
LIMIT 10


-- 3) Получаем игроков которые в среднем делают не менее 3 ключевых пеердач за матч

SELECT player_name FROM players
WHERE players.id IN (
		SELECT player_id
		FROM player_statictics
		GROUP BY player_id
		HAVING AVG(key_passes) >= 3
)


-- 4) Получем топ 5 команд с лучшей защитой в домашних матчах

SELECT m.team_id_h, t.team_name, ROUND(AVG(m.team_a_goals), 2) AS avg_goals_against, ROUND(AVG(m.team_a_xg), 2) AS avg_xg_against
FROM matches m
JOIN teams t ON m.team_id_h = t.id
WHERE m.team_id_h IN (
    SELECT team_id_h
    FROM matches
    GROUP BY team_id_h
    ORDER BY AVG(team_a_goals)
    LIMIT 5
)
GROUP BY m.team_id_h, t.team_name
ORDER BY avg_xg_against ASC


-- 5) Получем топ 5 команд с худшей разницей забито/создано в выездных матчах

SELECT m.team_id_a, t.team_name, ROUND(AVG(m.team_a_goals), 2) AS avg_goals, ROUND(AVG(m.team_a_xg), 2) AS avg_xg, (ROUND(AVG(m.team_a_goals), 2) - ROUND(AVG(m.team_a_xg), 2)) AS delta
FROM matches m
JOIN teams t ON m.team_id_a = t.id
WHERE m.team_id_a IN (
    SELECT team_id_a
    FROM matches
    GROUP BY team_id_a
    ORDER BY AVG(team_a_goals) - AVG(team_a_xg)
    LIMIT 5
)
GROUP BY m.team_id_a, t.team_name
ORDER BY delta ASC


-- 6) Получить топ 5 матчей с наибольшим количеством голов в 31м туре АПЛ

SELECT m.id, m.date, t_h.team_name, t_a.team_name, m.team_h_goals, m.team_a_goals
FROM matches m
INNER JOIN teams t_h ON m.team_id_h = t_h.id
INNER JOIN teams t_a ON m.team_id_a = t_a.id
WHERE m.id IN (
	SELECT matches.id
	FROM matches
	WHERE  matches.tournament_id = 1 AND matches.date >= '2024-04-06' AND matches.date <= '2024-04-07'
	GROUP BY matches.id
	ORDER BY (team_h_goals + team_a_goals) DESC
	LIMIT 5
)
GROUP BY m.id, t_h.team_name, t_a.team_name
ORDER BY (team_h_goals + team_a_goals) DESC


-- 7) Получить лучшего игрока по xg+xa из Арсенала в матчах АПЛ за отрезок

SELECT p.player_name, SUM(ps.xg) + SUM(ps.xa) AS xg_and_xa
FROM player_statictics p_stat
INNER JOIN players p ON p.id = p_stat.player_id
INNER JOIN matches m ON p_stat.match_id = m.id
WHERE m.tournament_id = 1 AND m.date >= '2024-03-30' AND m.date <= '2024-04-07' AND p.team_id = 1
GROUP BY p.player_name
ORDER BY xg_and_xa DESC
LIMIT 1;


-- 8) Получить игроков которые сыграли меньше 60 минут в 31м туре АПЛ

SELECT p.player_name, p_team.team_name, p_stat.minutes
FROM players p
INNER JOIN player_statictics p_stat ON p.id = p_stat.player_id
INNER JOIN matches m ON p_stat.match_id = m.id
INNER JOIN teams p_team ON p.team_id = p_team.id
WHERE m.tournament_id = 1 AND m.date >= '2024-04-06' AND m.date <= '2024-04-07' AND p_stat.minutes < 60
ORDER BY p_stat.minutes DESC


-- 9) Получить матчи в которых игрок сделал минимум гол+пас

SELECT m.date, p.player_name, p_team.team_name, p_stat.goals, p_stat.assistes
FROM players p
INNER JOIN player_statictics p_stat ON p.id = p_stat.player_id
INNER JOIN matches m ON p_stat.match_id = m.id
INNER JOIN teams p_team ON p.team_id = p_team.id
WHERE m.tournament_id = 1 AND p_stat.goals >= 1 AND p_stat.assistes >= 1
ORDER BY p_stat.goals + p_stat.assistes DESC


-- 10) Получить топ 10 лучших бомбардиров АПЛ

SELECT p.player_name, p_team.team_name, SUM(p_stat.goals) AS goals
FROM players p
INNER JOIN player_statictics p_stat ON p.id = p_stat.player_id
INNER JOIN matches m ON p_stat.match_id = m.id
INNER JOIN teams p_team ON p.team_id = p_team.id
WHERE m.tournament_id = 1
GROUP BY p.player_name, p_team.team_name
ORDER BY goals DESC
LIMIT 10
