from sqlalchemy.orm import Session
import random
from .models import Flag, Match, Rounds
from sqlalchemy.sql import text
from sqlalchemy import desc



countries = ['usa', 'japan', 'france', 'italy', 'spain', 'brazil']

async def create_game(db: Session, game_id):
    player_1, player_2 = game_id.split('x')
    match = random.sample(countries, 5)
    newGame = Match(player1=player_1, player2=player_2, round1=match[0], round2=match[1], round3=match[2], round4=match[3], round5=match[4])
    db.add(newGame)
    db.commit()
    res = db.query(Match).order_by(desc(Match.id)).first()

    return res.id

async def get_round_info(db: Session, game_id, round_id):
    round_field = f'matches.round{round_id}'
    q = text(f'SELECT title,image,player1,player2 FROM matches LEFT JOIN flags_cards ON {round_field} = flags_cards.title WHERE matches.id = :match_id')
    res = db.execute(q, {'match_id': game_id}).fetchone()
    other = await get_other_countries(res[0].strip())
    return res, other

async def get_other_countries(answer):
    other_countries = countries[:]
    print(other_countries is countries)
    print("Нужынй элемент в списке?", answer in other_countries)
    print("Нужынй элемент в изначальном списке?", answer in countries)
    print(type(other_countries),other_countries, type(answer), answer)
    other_countries.remove(answer)
    other_countries = set(other_countries)
    answers = random.sample(other_countries, 3)
    answers.append(answer)
    random.shuffle(answers)
    return answers

async def write_answers(db: Session, game_id, round_id, player_id, player_answer, correct_answer):
    newRound = Rounds(match_id=game_id, player_id=player_id, round=round_id, player_answer=player_answer, correct_answer=correct_answer)
    db.add(newRound)
    db.commit()
    return

async def get_match_results(db: Session, game_id, user_id, oponent_id):
    user = db.execute(text('SELECT COUNT(player_answer) FROM matches_rounds WHERE match_id = :match_id AND player_id = :player_id AND player_answer = correct_answer'), {'match_id': game_id, 'player_id': user_id}).fetchone()[0]
    oponent = db.execute(text('SELECT COUNT(player_answer) FROM matches_rounds WHERE match_id = :match_id AND player_id = :oponent_id AND player_answer = correct_answer'), {'match_id': game_id, 'oponent_id': oponent_id}).fetchone()[0]
    return user, oponent

async def create_country(db: Session, title, image):
    newCountry = Flag(title=title, image=image)
    db.add(newCountry)
    db.commit()
    return

