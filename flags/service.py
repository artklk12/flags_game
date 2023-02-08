import sqlite3
import random


conn = sqlite3.connect('flags.db', check_same_thread=False)
cursor = conn.cursor()

countries = ['usa', 'japan', 'france', 'italy', 'spain', 'brazil']

def create_game(game_id):
    player_1, player_2 = game_id.split('x')
    match = random.sample(countries, 5)
    print(match)
    cursor.execute('INSERT INTO matches (player1, player2, round1, round2, round3, round4, round5) VALUES (?, ?, ?, ?, ?, ?, ?)', (player_1, player_2, match[0], match[1], match[2], match[3], match[4],))
    conn.commit()
    game_id = cursor.lastrowid
    return game_id

def get_round_info(game_id, round_id):
    round_field = f'matches.round{round_id}'
    print(round_field, game_id)
    cursor.execute(f'SELECT title,image, player1,player2 FROM matches LEFT JOIN flags_cards ON {round_field} = flags_cards.title WHERE matches.id = ?', (game_id,))
    r = cursor.fetchone()
    other = get_other_countries(r[0])
    print(r)
    return r, other

def get_other_countries(answer):
    print(answer)
    other_countries = countries[:]
    other_countries.remove(answer)
    other_countries = set(other_countries)
    answers = random.sample(other_countries, 3)
    answers.append(answer)
    random.shuffle(answers)
    print(answers)
    return answers
