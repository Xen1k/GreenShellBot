
STATS_FILE_NAME = 'statistics.txt'

def update_overall_connections():
    '''Increase overall connnections number and write to file (+1)'''
    overall_connections = get_overall_connections()
    with open(STATS_FILE_NAME, 'w') as f:
        f.truncate(0)
        f.write(str(overall_connections + 1))

def get_overall_connections():
    with open(STATS_FILE_NAME) as f:
        return [int(x) for x in f][0]

