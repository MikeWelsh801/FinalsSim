import csv

PATH = "./NN Stuff\\"


def get_field_names(team_stats):
    # make header file
    visit_header = team_stats['Team']
    home_header = [] + team_stats['Team']

    for i, val in enumerate(visit_header):
        visit_header[i] = 'V' + val
        home_header[i] = 'H' + val

    fieldnames = visit_header[1:] + home_header[1:] + ['Home/Away Wins']
    return fieldnames


def generate_training_data(game_logs, team_stats, year):
    """Generates the training data from the game logs and team_stats
    tables and writes it to a file."""
    fieldnames = get_field_names(team_stats)

    with open(f"{PATH}NBA_Training_Data_{year}.csv", 'w', newline='') \
            as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fieldnames)
        # replace the game info with stats
        for game in game_logs:
            home_team = game[1]
            home_team_stats = team_stats[home_team]
            visiting_team = game[0]
            visiting_team_stats = team_stats[visiting_team]

            row = visiting_team_stats[1:] + home_team_stats[1:] + [game[2]]
            csv_writer.writerow(row)


def generate_prediction_data(home, visiting, team_stats, year):
    fieldnames = get_field_names(team_stats)

    # prediction file for home team's home games
    with open(f"{PATH}{home}_at_home_prediction_{year}.csv", 'w', newline='') \
            as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fieldnames)

        home_team_stats = team_stats[home]
        visiting_team_stats = team_stats[visiting]
        row = visiting_team_stats[1:] + home_team_stats[1:] + ['NA']
        csv_writer.writerow(row)

    # prediction file for visting team's home games
    with open(f"{PATH}{visiting}_at_home_prediction_{year}.csv", 'w',
              newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(fieldnames)

        home_team_stats = team_stats[visiting]
        visiting_team_stats = team_stats[home]
        row = visiting_team_stats[1:] + home_team_stats[1:] + ['NA']
        csv_writer.writerow(row)
