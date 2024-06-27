
import os
import sys
import termios
import tty
import json
import random
import csv

from datetime import datetime


locs = [
        'Seattle',
        'Bay Area',
        'New York City',
        'Orange County',
        'San Diego County',
        # 'Chicago',
        'Los Angeles'
        ]

typs = [
        'job', 
        'internship'
        ]

ttls = [
        # 'data scientist',
        # 'machine learning engineer',
        # 'data engineer',
        'DS/MLE/DE',
        'software engineer',
        'data analyst',
        'ee/meche/bioe',
        'service'
        ]


def expected_score(player_rating, opponent_rating):
    return 1 / (1 + 10 ** ((opponent_rating - player_rating) / 400))

def update_ratings(player_rating, opponent_rating, result, k=32):
    expected = expected_score(player_rating, opponent_rating)
    updated_rating = player_rating + k * (result - expected)
    return updated_rating

def elo_rating(player1_rating, player2_rating, player1_result, k=32):
    # player1_result should be 1 if player 1 wins, 0 if player 1 loses, and 0.5 if it's a draw
    player1_new_rating = update_ratings(player1_rating, player2_rating, player1_result, k)
    player2_new_rating = update_ratings(player2_rating, player1_rating, 1 - player1_result, k)
    return player1_new_rating, player2_new_rating

def sample_two_keys(dic):
    sample = random.sample(dic.keys(), 2)
    return sample

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError:
            print(f"Error: The file {file_path} is not a valid JSON file.")
            return None

def write_json_file(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully written to {file_path}")
    except IOError:
        print(f"Error: Unable to write to file {file_path}")



if __name__ == "__main__":
    # Check if elos file exists and configure if it does
    elos_path = 'elos.json'
    choice_data_path = 'choice_data.csv'

    if os.path.exists(elos_path):
        elos = load_json_file(elos_path)
    else:
        # Create combinations
        entries = [0]*len(locs)*len(typs)*len(ttls)
        for i, loc in enumerate(locs):
            for j, typ in enumerate(typs):
                for k, ttl in enumerate(ttls):
                    if typ == 'internship' and ttl == 'service': # skip service internship
                        continue
                    entries[len(typs)*len(ttls)*i + len(ttls)*j + k] = loc + ' - ' + typ + ' - ' + ttl

        # Shuffle list
        entries = set(entries) # Converting to set removes duplicates
        entries.remove(0) # Remove skipped entries

        # Assign elos:
        elos = {}
        for entry in entries:
            elos[entry] = 1000

    # Initialize left and right keystrokes
    left, rght, quit = '[', ']', 'q'
    print(f'Press {left} for left. Press {rght} for right. Press {quit} to save and quit.')

    # Start sampling and updating elos
    while True:
        # Sample two
        a, b = sample_two_keys(elos)

        # Choice context loop
        while True:
            print(f'\n\n------------\n{a} | VS. | {b}\n------------')
            print(f"Click '{left}' for left. Click '{rght}' for right. Press {quit} to save and quit.")
            choice = getch()
            print(f'You typed: {choice}')
            if choice == left:
                result = 1
                break
            elif choice == rght:
                result = 0
                break
            elif choice == quit:
                write_json_file(elos, elos_path)
                print('File saved.')
                break
            else:
                print(f'Invalid input. Press {left} for left. Press {rght} for right. Press {quit} to save and quit.')
                continue

        # Check for quit choice
        if choice == quit:
            print('Exiting...')
            break

        # Update elos
        elos[a], elos[b] = elo_rating(elos[a], elos[b], result)
        print("Player 1:", elos[a])
        print("Player 2:", elos[b])

        # Record result
        date, time =  datetime.now().strftime("%m/%d/%Y"), datetime.now().strftime("%I:%M:%S %p")
        with open(choice_data_path, mode='w') as choice_data:
            choice_writer = csv.writer(choice_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            choice_writer.writerow([date, time, elos[a], elos[b], result])
