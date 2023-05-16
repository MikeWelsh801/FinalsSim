from bs4 import BeautifulSoup
import requests
import csv
import argparse
from generate_data import generate_training_data, generate_prediction_data

PATH = "./NN Stuff\\"
YEAR = 2020


def parse_table(table):
    """Gets all the elements in a table"""
    table_dict = {}

    # get all the rows and parse elements
    for row in table.findAll('tr'):
        row_list = []

        for element in row.findAll(lambda tag:
                                   tag.name == 'th' or tag.name == 'td'):
            row_list.append(element.text.strip('*'))

        table_dict[row_list[1]] = row_list
    return table_dict


def parse_game_log(table):
    """Gets all the elements in a game log table"""
    table_list = []
    if table is None:
        return table_list

    # get all the rows and parse elements
    for row in table.findAll('tr'):
        row_list = []

        for element in row.findAll(lambda tag:
                                   tag.name == 'th' or tag.name == 'td'):
            row_list.append(element.text.strip('*'))

        table_list.append(row_list)
    return table_list


def build_team_stats_csv():
    """This creates a csv file containing the correct team stats
    information."""
    url = \
        f"https://www.basketball-reference.com/leagues/NBA_{YEAR}.html"
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')

    # extract table from the website
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id')
                      and tag['id'] == 'per_poss-team')
    opponent_table = soup.find(lambda tag: tag.name == 'table'
                               and tag.has_attr('id')
                               and tag['id'] == 'per_poss-opponent')

    # this parses the tables into a dictionary mapping team names to
    # a list of statistics. Will need to merge team and opponent stats
    # later
    table_dict = parse_table(table)
    opponent_table_dict = parse_table(opponent_table)
    team_stats = {}

    # add opp tag to the headers in opponent table for neural net compatability
    for i, tag in enumerate(opponent_table_dict['Team']):
        opponent_table_dict['Team'][i] += " Opp"

    with open(f"{PATH}team_stats_{YEAR}.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # this merges the two tables and formats everything correctly for the
        # csv file
        for team in table_dict.keys():
            row = [table_dict[team][1]] + table_dict[team][4:] + \
                opponent_table_dict[team][4:]
            csv_writer.writerow(row)
            team_stats[team] = row

    return team_stats


def parse_game_logs():
    """parses all of the game log tables for the current year and writes them
    to a csv"""
    months = ['october', 'november', 'december', 'january', 'february',
              'march', 'april', 'may']

    with open(f"{PATH}game_log_{YEAR}.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # write the first row/headers
        csv_writer.writerow(['Visitor/Neutral', 'Home/Neutral',
                             'Home/Away Wins'])

        game_logs = []
        for month in months:
            url = \
                f"https://www.basketball-reference.com/leagues/" \
                f"NBA_{YEAR}_games-{month}.html"
            source = requests.get(url).text
            if source is None:
                year = int(YEAR) - 1
                url = \
                    f"https://www.basketball-reference.com/leagues/" \
                    f"NBA_{YEAR}_games-{month}-{year}.html"
            source = requests.get(url).text

            soup = BeautifulSoup(source, 'lxml')

            # extract table from the website
            table = soup.find(lambda tag: tag.name == 'table'
                              and tag.has_attr('id')
                              and tag['id'] == 'schedule')
            table_list = parse_game_log(table)

            for row in table_list[1:]:
                winner = ''
                # check that the games aren't still being played, the scores
                # will be blank for scheduled games that haven't been played
                if row[3] == '':
                    return game_logs

                # winner is based on the scores for the game
                if int(row[3]) > int(row[5]):
                    winner = 'A'
                else:
                    winner = 'H'
                # visiting team, away team, winner
                game_row = [row[2], row[4], winner]
                csv_writer.writerow(game_row)
                game_logs.append(game_row)

    return game_logs


def main():
    """Start of the program. This will get the correct webpage and parse
    everything given the NBA year as a command line argument."""
    parser = argparse.ArgumentParser()

    # add -p flag to generate predict csv
    parser.add_argument('year')
    parser.add_argument("-p", "--predict", nargs=2,
                        metavar=("home_team", "visiting_team"),
                        help="Generate prediction data. Must include home team"
                        " and away team")
    args = parser.parse_args()
    global YEAR
    YEAR = args.year

    team_stats = build_team_stats_csv()
    if args.predict:
        home_team = args.predict[0]
        visiting_team = args.predict[1]
        print(f"Generating prediction data for {home_team}"
              f" and {visiting_team} for the {YEAR} season.")
        generate_prediction_data(home_team, visiting_team, team_stats, YEAR)
        return

    game_logs = parse_game_logs()
    generate_training_data(game_logs, team_stats, YEAR)


if __name__ == '__main__':
    main()
