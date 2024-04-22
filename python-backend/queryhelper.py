def where_eco_code(eco_code):
    if eco_code is None:
        where_clause = ""
    else:
        where_clause = f"WHERE ECOCODE = '{eco_code}' "
    return where_clause


# calculates win rates of all ecocodes.
def WinRates(minGames=1, fetchRows=130):
    query = (f"SELECT ECOCODE, "
                f"SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) AS Wins, "
                f"SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) AS Losses, "
                f"ROUND(SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END) / (SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) "
                    f"+ SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END)), 2) AS WinRate "
             f"FROM GAMES2 GROUP BY ECOCODE HAVING (SUM(CASE WHEN RESULT = '0-1' THEN 1 ELSE 0 END) "
             f"+ SUM(CASE WHEN RESULT = '1-0' THEN 1 ELSE 0 END)) >= {minGames} "
             f"ORDER BY WinRate DESC "
             f"FETCH FIRST {fetchRows} ROWS ONLY")
    return query


# calculates average turns in loss of all ecocodes. Can yield average turns in loss for just one eco code as well.
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

def TotalGamesInMonthYear():
    query = (f"SELECT COUNT(*) AS Games, "
             f"EXTRACT(MONTH FROM EVENTDATE) AS Month, "
             f"EXTRACT(YEAR FROM EVENTDATE) AS Year "
             f"FROM GAMES2 "
             f"GROUP BY EXTRACT(MONTH FROM EVENTDATE), EXTRACT(YEAR FROM EVENTDATE)")
    return query


# query 2: Runs query 2 fully and allows various inputs
def query2(min_Games=1, start_date="JAN-2018", end_date="DEC-2023", fetch_Rows=130):
    query = (f"WITH WinRates AS ({WinRates(minGames=min_Games, fetchRows=fetch_Rows)}), "
            f"AvgMovesInLoss AS ({AvgMovesInLoss(fetchRows=fetch_Rows)}), "
            f"GamesInMonthYear AS ({TotalGamesInMonthYear()}) "
            f"SELECT ROUND((COUNT(*) * 100.0) / GamesInMonthYear.Games, 2) AS RiskyPlaysPercent, "
                f"EXTRACT(MONTH FROM EVENTDATE) AS Month, "
                f"EXTRACT(YEAR FROM EVENTDATE) AS Year "
            f"FROM WinRates "
            f"JOIN AvgMovesInLoss ON WinRates.ECOCODE = AvgMovesInLoss.ECOCODE "
            f"JOIN GAMES2 ON WinRates.ECOCODE = GAMES2.ECOCODE "
            f"JOIN GamesInMonthYear ON EXTRACT(MONTH FROM GAMES2.EVENTDATE) = GamesInMonthYear.Month "
                f"AND EXTRACT(YEAR FROM GAMES2.EVENTDATE) = GamesInMonthYear.Year "
            f"WHERE GAMES2.EVENTDATE <= TO_DATE('{end_date}', 'MON-YYYY') "
                f"AND GAMES2.EVENTDATE >= TO_DATE('{start_date}', 'MON-YYYY')"
            f"GROUP BY EXTRACT(MONTH FROM GAMES2.EVENTDATE), EXTRACT(YEAR FROM GAMES2.EVENTDATE), GamesInMonthYear.Games "
            f"ORDER BY Year, Month")
    print(query)
    return query

