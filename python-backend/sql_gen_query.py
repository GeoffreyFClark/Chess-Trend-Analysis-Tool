def create_sql_query(date_min, date_max, elo_min, elo_max, turns_min, turns_max, moves, data_metric, graph_by, player=None, black_opening=False):
    # Determine the proper interval for the graph_by input
    graph_by_multiplier = 1  
    if isinstance(graph_by, str):
        if graph_by == 'month':
            graph_by_multiplier = 1/12
        elif graph_by == 'quarter':
            graph_by_multiplier = 1/4
        elif graph_by == 'year':
            graph_by_multiplier = 1
        elif graph_by == '2 years':
            graph_by_multiplier = 2
        elif graph_by == '5 years':
            graph_by_multiplier = 5
        elif graph_by == 'decade':
            graph_by_multiplier = 10
        else:
            try:
                graph_by_multiplier = int(graph_by)  
            except ValueError:
                graph_by_multiplier = 1  

    if data_metric == 'winrate':
        win_condition = '0-1' if black_opening else '1-0'
        base_query_line1 = f"SELECT (SUM(CASE WHEN RESULT = '{win_condition}' THEN 1 ELSE 0 END)/COUNT(RESULT))*100 as Winrate, "
    else:
        base_query_line1 = f"SELECT (COUNT(case when MOVES LIKE '{moves}%' THEN 1 END)/COUNT(*))*100 as Popularity, "

    base_query_line1 += "YearGroup as Year "
    base_subquery = f"FROM (SELECT FLOOR(EXTRACT(YEAR FROM EVENTDATE) / {graph_by_multiplier}) * {graph_by_multiplier} as YearGroup, RESULT, EVENTDATE, MOVES\nFROM games2\n"

    # Constructing WHERE clause
    base_query_line2 = f"WHERE EVENTDATE BETWEEN TO_DATE('{date_min}', 'YYYY') AND TO_DATE('{date_max}', 'YYYY') AND TURNS BETWEEN {turns_min} AND {turns_max} "

    # Elo filtering
    if elo_min != 100 or elo_max != 2900:  
        base_query_line2 += f"AND WHITEELO BETWEEN {elo_min} AND {elo_max} AND BLACKELO BETWEEN {elo_min} AND {elo_max} "

    # Player filtering
    if player:
        player_field = 'BlackPlayer' if black_opening else 'WhitePlayer'
        base_query_line2 += f"AND {player_field} = '{player}' "

    base_subquery += base_query_line2
    base_query_line3 = ") subquery\nGROUP BY YearGroup\nORDER BY YearGroup"
    query = base_query_line1 + base_subquery + base_query_line3
    return query
