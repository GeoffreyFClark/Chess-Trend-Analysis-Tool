def create_sql_query(date_min=1950, date_max=2023, elo_min=100, elo_max=2900, turns_min=1, turns_max=201, moves="", data_metric="winrate", graph_by='year', player=None, opening_color='white'):
    intervals = {
        'month': 1, 'quarter': 4, 'year': 1, '2 years': 2, 
        '5 years': 5, 'decade': 10
    }
    graph_by_multiplier = intervals.get(graph_by, 1)  # Default to 1 if graph_by is not defined in intervals
    
    # Base clauses
    select_clause = "SELECT "
    if graph_by=="month" or graph_by=="quarter":
        from_clause = "FROM (SELECT EXTRACT(YEAR FROM EVENTDATE) as YearGroup, FLOOR(EXTRACT(MONTH FROM EVENTDATE) / {}) * {} as MonthGroup, RESULT, EVENTDATE, MOVES FROM games2 ".format(graph_by_multiplier, graph_by_multiplier)
    else:
        from_clause = "FROM (SELECT FLOOR(EXTRACT(YEAR FROM EVENTDATE) / {}) * {} as YearGroup, RESULT, EVENTDATE, MOVES FROM games2 ".format(graph_by_multiplier, graph_by_multiplier)
    where_clause = "WHERE EVENTDATE BETWEEN TO_DATE('{}', 'YYYY') AND TO_DATE('{}', 'YYYY') AND TURNS BETWEEN {} AND {} ".format(date_min, date_max, turns_min, turns_max)
    

    # Modify based on elo range
    if elo_min != 100 or elo_max != 2900:
        where_clause += "AND WHITEELO BETWEEN {} AND {} AND BLACKELO BETWEEN {} AND {} ".format(elo_min, elo_max, elo_min, elo_max)
    
    # Modify based on player selection
    if player:
        player_field = 'BlackPlayer' if opening_color == 'black' else 'WhitePlayer'
        where_clause += "AND {} = '{}' ".format(player_field, player)
    
    # Modify based on data metric
    if data_metric == 'winrate':
        win_condition = '0-1' if opening_color == 'black' else '1-0'
        draw_condition = '1/2-1/2'
        select_clause += "((SUM(CASE WHEN RESULT = '{}' THEN 1 WHEN RESULT = '{}' THEN 0.5 ELSE 0 END) / COUNT(RESULT)) * 100) AS Winrate, YearGroup as Year ".format(win_condition, draw_condition)
        where_clause += "AND MOVES LIKE '{}%' ".format(moves)
    elif data_metric == 'popularity':
        select_clause += "(COUNT(case when moves LIKE '" + moves +"%' THEN 1 END)/(COUNT(*)))*100 as Popularity, YearGroup as Year  "
        

    if graph_by=="month" or graph_by=="quarter":
        group_order_clause = "GROUP BY YearGroup, MonthGroup ORDER BY YearGroup, MonthGroup"
        select_clause += ", MonthGroup as Month "
    else:
        group_order_clause = "GROUP BY YearGroup ORDER BY YearGroup"
    
    # Combine all clauses to form the final query
    query = select_clause + from_clause + where_clause + ") " + group_order_clause
    return query
