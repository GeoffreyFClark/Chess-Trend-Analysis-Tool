def where_eco_code(eco_code):
    if eco_code is None:
        where_clause = ""
    else:
        where_clause = f"WHERE ECOCODE = '{eco_code}' "
    return where_clause

def query1(date_min="JAN-1942", date_max="DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=1):
    intervals = {
        'month': 1, 'quarter': 4, 'year': 1, '2 years': 2,
        '5 years': 5, 'decade': 10
    }
    graph_by_multiplier = intervals.get(graph_by, 1)  # Default to 1 if graph_by is not defined in intervals
    if graph_by=='month' or graph_by=='quarter':
        query = (f"SELECT (COUNT(CASE WHEN MOVES LIKE '{moves}%' THEN 1 END) / COUNT(*)) * 100 AS Popularity, YearGroup AS Year "
             f"FROM (SELECT EXTRACT(YEAR FROM EVENTDATE) as YearGroup, (EXTRACT(Month from EVENTDATE)/ {graph_by_multiplier}) * {graph_by_multiplier} as MonthGroup, MOVES, EVENTDATE "
             f"FROM GAMES2 "
             f"WHERE EVENTDATE BETWEEN TO_DATE('{date_min}', 'MON-YYYY') AND TO_DATE('{date_max}', 'MON-YYYY') AND TURNS BETWEEN {turns_min} and {turns_max}) "
             f"subquery "
             f"GROUP BY YearGroup "
             f"ORDER BY YearGroup")
    else:
        query = (f"SELECT (COUNT(CASE WHEN MOVES LIKE '{moves}%' THEN 1 END) / COUNT(*)) * 100 AS Popularity, YearGroup AS Year "
             f"FROM (SELECT FLOOR(EXTRACT(YEAR FROM EVENTDATE) / {graph_by_multiplier}) * {graph_by_multiplier} as YearGroup, MOVES, EVENTDATE "
             f"FROM GAMES2 "
             f"WHERE EVENTDATE BETWEEN TO_DATE('{date_min}', 'MON-YYYY') AND TO_DATE('{date_max}', 'MON-YYYY') AND TURNS BETWEEN {turns_min} and {turns_max}) "
             f"subquery "
             f"GROUP BY YearGroup "
             f"ORDER BY YearGroup")
    return query

# used in query 2: calculates win rates of all ecocodes.
def WinRates(minGames=1, fetchRows=130):
    query = (f"SELECT ECOCODE, "
                f"SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) AS Wins, "
                f"SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) AS Losses, "
                f"SUM(CASE WHEN RESULT = '1/2-1/2' THEN 0.5 ELSE 0 END) AS DRAWS, "
                f"(SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) "
                f"+ SUM(CASE WHEN RESULT = '1/2-1/2' THEN 0.5 ELSE 0 END)) "
                f"/ (SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) "
                f"+ SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) + "
                f"(2 * SUM(CASE WHEN RESULT = '1/2-1/2' THEN 0.5 ELSE 0 END))) AS WinRate "
             f"FROM GAMES2 GROUP BY ECOCODE HAVING (SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) "
             f"+ SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) + (2 * SUM(CASE WHEN RESULT = '1/2-1/2' THEN 0.5 ELSE 0 END))) >= {minGames} "
             f"ORDER BY WinRate DESC "
             f"FETCH FIRST {fetchRows} ROWS ONLY")
    return query

# used in query 2: calculates average turns in loss of all ecocodes. Can yield average turns in loss for just one eco code as well.
def AvgMovesInLoss(eco_code=None, fetchRows=130):
    where_clause = where_eco_code(eco_code)
    query = (f"SELECT ECOCODE, "
             f"AVG(TURNS) AS AvgMovesInLoss "
             f"FROM GAMES2 "
             f"{where_clause}"
             f"GROUP BY ECOCODE "
             f"ORDER BY AvgMovesInLoss ASC "
             f"FETCH FIRST {fetchRows} ROWS ONLY")
    return query

# query 2: Runs query 2 fully and allows various inputs
def query2(date_min="JAN-1942", date_max="DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=2):
    query = (f"WITH WinRates AS ({WinRates(minGames=1, fetchRows=130)}), "
            f"AvgMovesInLoss AS ({AvgMovesInLoss(fetchRows=130)}), "
            f"GamesInMonthYear AS ({TotalGamesInMonthYear()}) "
            f"SELECT ROUND((COUNT(*) * 100.0) / GamesInMonthYear.Games, 2) AS POPULARITY, "
                f"EXTRACT(MONTH FROM EVENTDATE) AS Month, "
                f"EXTRACT(YEAR FROM EVENTDATE) AS Year "
            f"FROM WinRates "
            f"JOIN AvgMovesInLoss ON WinRates.ECOCODE = AvgMovesInLoss.ECOCODE "
            f"JOIN GAMES2 ON WinRates.ECOCODE = GAMES2.ECOCODE "
            f"JOIN GamesInMonthYear ON EXTRACT(MONTH FROM GAMES2.EVENTDATE) = GamesInMonthYear.Month "
                f"AND EXTRACT(YEAR FROM GAMES2.EVENTDATE) = GamesInMonthYear.Year "
            f"WHERE GAMES2.EVENTDATE <= TO_DATE('{date_max}', 'MON-YYYY') "
                f"AND GAMES2.EVENTDATE >= TO_DATE('{date_min}', 'MON-YYYY') "
            f"GROUP BY EXTRACT(MONTH FROM GAMES2.EVENTDATE), EXTRACT(YEAR FROM GAMES2.EVENTDATE), GamesInMonthYear.Games "
            f"ORDER BY Year, Month")
    return query

# used in query 3
def TotalGamesInMonthYear():
    query = (f"SELECT COUNT(*) AS Games, "
             f"EXTRACT(MONTH FROM EVENTDATE) AS Month, "
             f"EXTRACT(YEAR FROM EVENTDATE) AS Year "
             f"FROM GAMES2 "
             f"GROUP BY EXTRACT(MONTH FROM EVENTDATE), EXTRACT(YEAR FROM EVENTDATE)")
    return query

# used in query 3 and query 4
def UserSelectedGames(date_min="JAN-1942", date_max="DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color=""):
    query = (f"SELECT * FROM GAMES2 "
             f"WHERE WHITEELO >= {elo_min} AND WHITEELO <= {elo_max} "
             f"AND BLACKELO >= {elo_min} AND BLACKELO <= {elo_max} "
             f"AND TURNS >= {turns_min} AND TURNS <= {turns_max} "
             f"AND EVENTDATE >= TO_DATE('{date_min}', 'MON-YYYY') "
             f"AND EVENTDATE <= TO_DATE('{date_max}', 'MON-YYYY')")
    return query

# used in query 3
def DifferenceData():
    query = (f"SELECT ABS(WHITEELO - BLACKELO) AS Difference, "
             f"EXTRACT(YEAR FROM EVENTDATE) AS Year, "
             f"(SUM(CASE WHEN (RESULT = '0-1' AND WHITEELO < BLACKELO) OR (RESULT = '1-0' AND WHITEELO > BLACKELO) THEN 1 ELSE 0 END) / COUNT(*)) AS SampleProbability, "
             f"(1 / (1 + POWER(10, -(ABS(WHITEELO - BLACKELO) / 400)))) AS ExpectedProbability, COUNT(*) AS Occurrences "
             f"FROM UserSelectedGames "
             f"GROUP BY ABS(WHITEELO - BLACKELO), EXTRACT(YEAR FROM EVENTDATE)")
    return query

# used in query 3
def YearTotals():
    query = (f"SELECT Year, "
             f"SUM(SampleProbability * Occurrences) / SUM(Occurrences) AS SampleYearProbability, "
             f"SUM(ExpectedProbability * Occurrences) / SUM(Occurrences) AS ExpectedYearProbability, "
             f"SUM(Occurrences) AS OccurrencesPerYear "
             f"FROM DifferenceData GROUP BY Year")
    return query

# query 3
def query3(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=3):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(elo_min=elo_min, elo_max=elo_max, turns_min=turns_min, turns_max=turns_max, date_min=date_min, date_max=date_max)}), "
             f"DifferenceData AS ({DifferenceData()}), "
             f"YearTotals AS ({YearTotals()}) "
             f"SELECT YEAR, ROUND((SampleYearProbability / ExpectedYearProbability), 3) AS PROPORTION "
             f"FROM YearTotals "
             f"WHERE OccurrencesPerYear >= 250 "
             f"ORDER BY YEAR")
    return query

def EvenlyMatchedGames():
    query = (f"SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, WHITEELO, BLACKELO, TURNS FROM UserSelectedGames "
             f"WHERE ABS(WHITEELO - BLACKELO) <= 50")
    return query

def EachYearsEloStatistics():
    query = (f"SELECT Year, AVG((WHITEELO + BLACKELO) / 2) As AveragePairElo, "
             f"STDDEV((WHITEELO + BLACKELO) / 2) As StdDevPairElo "
             f"FROM EvenlyMatchedGames "
             f"GROUP BY Year")
    return query

def query4(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=4):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(elo_min=elo_min, elo_max=elo_max, turns_min=turns_min, turns_max=turns_max, date_min=date_min, date_max=date_max)}), "
             f"EvenlyMatchedGames AS ({EvenlyMatchedGames()}), "
             f"EachYearsEloStatistics AS ({EachYearsEloStatistics()}) "
             f"SELECT t1.Year, CASE WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) < (t2.AveragePairElo - t2.StdDevPairElo) THEN 'BelowStdDevPair' "
             f"WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) > (t2.AveragePairElo + t2.StdDevPairElo) THEN 'AboveStdDevPair' "
             f"ELSE 'WithinStdDevPair' "
             f"END AS EloGroup, "
             f"AVG(t1.TURNS) AS AverageNumberOfTurns "
             f"FROM EvenlyMatchedGames t1 JOIN EachYearsEloStatistics t2 ON t1.Year = t2.Year "
             f"GROUP BY t1.Year, "
             f"CASE WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) < (t2.AveragePairElo - t2.StdDevPairElo) THEN 'BelowStdDevPair' "
             f"WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) > (t2.AveragePairElo + t2.StdDevPairElo) THEN 'AboveStdDevPair' "
             f"ELSE 'WithinStdDevPair' "
             f"END "
             f"ORDER BY t1.Year ASC")
    return query

def PlayerAndEcoByYear():
    query = (f"(SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, WHITEPLAYER AS Player, ECOCODE "
             f"FROM UserSelectedGames) "
             f"UNION ALL "
             f"(SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, BLACKPLAYER AS Player, ECOCODE "
             f"FROM UserSelectedGames)")
    return query

def EcoRankByYear():
    query = (f"SELECT Year, ECOCODE, RANK() OVER (PARTITION BY Year ORDER BY COUNT(*) DESC) AS Rank FROM PlayerAndECOByYear GROUP BY Year, ECOCODE")
    return query


def query5(date_min="01-JAN-1942", date_max="12-DEC-2023", elo_min=100, elo_max=3900, turns_min=1, turns_max=201, moves="", graph_by="year", player="", opening_color="", queryNumber=5):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(elo_min=elo_min, elo_max=elo_max, turns_min=turns_min, turns_max=turns_max, date_min=date_min, date_max=date_max)}), "
             f"PlayerAndEcoByYear AS ({PlayerAndEcoByYear()}), "
             f"ECORankByYear AS ({EcoRankByYear()}) "
             f"SELECT Year, ECOCODE, Rank "
             f"FROM ECORankByYear "
             f"WHERE RANK <= 3 "
             f"ORDER BY YEAR ASC, RANK ASC ")
    return query

