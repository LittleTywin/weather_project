def degrees_to_direction(deg):
    val=int((deg/22.5)+.5)
    arr=["N","N NE","NE","E NE","E","E SE", "SE", "S SE","S","S SW","SW","W SW","W","W NW","NW","N NW"]
    return (arr[(val % 16)])