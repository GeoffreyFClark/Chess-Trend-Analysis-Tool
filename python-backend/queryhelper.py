def where_eco_code(eco_code):
    if eco_code is None:
        where_clause = ""
    else:
        where_clause = f"WHERE ECOCODE = '{eco_code}' "
    return where_clause

def query1(date="23-OCT-1980"):
    query = (f"SELECT (COUNT(CASE WHEN MOVES LIKE 'd4 d5 c4%' THEN 1 END) / (COUNT(*))) * 100 AS Popularity, YearGroup AS Year "
             f"FROM (SELECT FLOOR(EXTRACT(YEAR FROM EVENTDATE) / 2) * 2 as YearGroup, RESULT, EVENTDATE, WHITEPLAYER, MOVES "
             f"FROM GAMES2 "
             f"WHERE NOT EXISTS (SELECT 1 FROM GAMES2 G2 WHERE G2.WHITEPLAYER = GAMES2.WHITEPLAYER AND G2.EVENTDATE < TO_DATE('{date}', 'DD-MON-YYYY'))) "
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
def query2(min_Games=1, start_date="JAN-2018", end_date="DEC-2023", fetch_Rows=130):
    query = (f"WITH WinRates AS ({WinRates(minGames=min_Games, fetchRows=fetch_Rows)}), "
            f"AvgMovesInLoss AS ({AvgMovesInLoss(fetchRows=fetch_Rows)}), "
            f"GamesInMonthYear AS ({TotalGamesInMonthYear()}) "
            f"SELECT ROUND((COUNT(*) * 100.0) / GamesInMonthYear.Games, 2) AS POPULARITY, "
                f"EXTRACT(MONTH FROM EVENTDATE) AS Month, "
                f"EXTRACT(YEAR FROM EVENTDATE) AS Year "
            f"FROM WinRates "
            f"JOIN AvgMovesInLoss ON WinRates.ECOCODE = AvgMovesInLoss.ECOCODE "
            f"JOIN GAMES2 ON WinRates.ECOCODE = GAMES2.ECOCODE "
            f"JOIN GamesInMonthYear ON EXTRACT(MONTH FROM GAMES2.EVENTDATE) = GamesInMonthYear.Month "
                f"AND EXTRACT(YEAR FROM GAMES2.EVENTDATE) = GamesInMonthYear.Year "
            f"WHERE GAMES2.EVENTDATE <= TO_DATE('{end_date}', 'MON-YYYY') "
                f"AND GAMES2.EVENTDATE >= TO_DATE('{start_date}', 'MON-YYYY') "
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
def UserSelectedGames(low_white_elo=246, high_white_elo=3958, low_black_elo=246, high_black_elo=3958, low_turn=1, high_turn=201, start_date="01-JAN-1942", end_date = "01-JAN-2024"):
    query = (f"SELECT * FROM GAMES2 "
             f"WHERE WHITEELO >= {low_white_elo} AND WHITEELO <= {high_white_elo} "
             f"AND BLACKELO >= {low_black_elo} AND BLACKELO <= {high_black_elo} "
             f"AND TURNS >= {low_turn} AND TURNS <= {high_turn} "
             f"AND EVENTDATE >= TO_DATE('{start_date}', 'DD-MON-YYYY') "
             f"AND EVENTDATE <= TO_DATE('{end_date}', 'DD-MON-YYYY')")
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
def query3(low_white_elo=246, high_white_elo=3958, low_black_elo=246, high_black_elo=3958, low_turn=1, high_turn=201, start_date="01-JAN-1942", end_date = "01-JAN-2024"):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(low_white_elo=low_white_elo, high_white_elo=high_white_elo, low_black_elo=low_black_elo, high_black_elo=high_black_elo, low_turn=low_turn, high_turn=high_turn, start_date=start_date, end_date=end_date)}), "
             f"DifferenceData AS ({DifferenceData()}), "
             f"YearTotals AS ({YearTotals()}) "
             f"SELECT YEAR, ROUND((SampleYearProbability / ExpectedYearProbability), 3) AS POPULARITY "
             f"FROM YearTotals "
             f"WHERE OccurrencesPerYear >= 250 "
             f"ORDER BY YEAR")
    return query

def EvenlyMatchedGames():
    query = (f"SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, WHITEELO, BLACKELO, TURNS FROM UserSelectedGames "
             f"WHERE WHITEELO - BLACKELO <= 50 AND WHITEELO - BLACKELO <= 50")
    return query

def EachYearsEloStatistics():
    query = (f"SELECT year, AVG((WHITEELO + BLACKELO) / 2) As AveragePairElo, "
             f"STDDEV((WHITEELO + BLACKELO) / 2) As StdDevPairElo "
             f"FROM EvenlyMatchedGames "
             f"GROUP BY YEAR")
    return query

def query4(low_white_elo=246, high_white_elo=3958, low_black_elo=246, high_black_elo=3958, low_turn=1, high_turn=201, start_date="01-JAN-1942", end_date = "01-JAN-2024"):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(low_white_elo=low_white_elo, high_white_elo=high_white_elo, low_black_elo=low_black_elo, high_black_elo=high_black_elo, low_turn=low_turn, high_turn=high_turn, start_date=start_date, end_date=end_date)}), "
             f"EvenlyMatchedGames AS ({EvenlyMatchedGames()}), "
             f"EachYearsEloStatistics AS ({EachYearsEloStatistics()}) "
             f"SELECT t1.Year, CASE WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) < (t2.AveragePairElo - t2.StdDevPairElo) THEN 'BelowStdDevPair' "
             f"WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) > (t2.AveragePairElo - t2.StdDevPairElo) THEN 'AboveStdDevPair' "
             f"ELSE 'WithinStdDevPair' "
             f"END AS EloGroup, "
             f"AVG(t1.TURNS) AS AverageNumberOfTurns "
             f"FROM EvenlyMatchedGames t1 JOIN EachYearsEloStatistics t2 ON t1.Year = t2.Year "
             f"GROUP BY t1.Year, "
             f"CASE WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) < (t2.AveragePairElo - t2.StdDevPairElo) THEN 'BelowStdDevPair' "
             f"WHEN ((t1.WHITEELO + t1.BLACKELO) / 2) > (t2.AveragePairElo - t2.StdDevPairElo) THEN 'AboveStdDevPair' "
             f"ELSE 'WithinStdDevPair' "
             f"END "
             f"ORDER BY t1.Year")
    return query

def PlayerAndEcoByYear():
    query = (f"(SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, WHITEPLAYER AS Player, ECOCODE, COUNT(*) AS GameCount "
             f"FROM UserSelectedGames "
             f"GROUP BY EXTRACT(YEAR FROM EVENTDATE), WHITEPLAYER, ECOCODE) "
             f"UNION ALL "
             f"(SELECT EXTRACT(YEAR FROM EVENTDATE) AS Year, BLACKPLAYER AS Player, ECOCODE, COUNT(*) AS GameCount "
             f"FROM UserSelectedGames "
             f"GROUP BY EXTRACT(YEAR FROM EVENTDATE), BLACKPLAYER, ECOCODE)")
    return query

def EcoRankByYear():
    query = (f"SELECT Year, ECOCODE, RANK() OVER (PARTITION BY Year ORDER BY COUNT(*) DESC) AS Rank FROM PlayerAndECOByYear GROUP BY Year, ECOCODE")
    return query

def query5(low_white_elo=246, high_white_elo=3958, low_black_elo=246, high_black_elo=3958, low_turn=1, high_turn=201, start_date="01-JAN-1942", end_date = "01-JAN-2024"):
    query = (f"WITH UserSelectedGames AS ({UserSelectedGames(low_white_elo=low_white_elo, high_white_elo=high_white_elo, low_black_elo=low_black_elo, high_black_elo=high_black_elo, low_turn=low_turn, high_turn=high_turn, start_date=start_date, end_date=end_date)}), "
             f"PlayerAndEcoByYear AS ({PlayerAndEcoByYear()}), "
             f"ECORankByYear AS ({EcoRankByYear()}) "
             f"SELECT Year, ECOCODE, Rank "
             f"FROM ECORankByYear "
             f"WHERE RANK <= 3 "
             f"ORDER BY YEAR ASC, RANK ASC ")
    return query

