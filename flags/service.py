from sqlalchemy.orm import Session
import random
from .models import Flag, Match, Rounds
from sqlalchemy.sql import text
from sqlalchemy import desc



countries = ['ОАЭ', 'Андорра', 'Афганистан', 'Албания', 'Армения', 'Аргентина', 'Австрия', 'Австралия', 'Азербайджан', 'Барбадос', 'Бельгия', 'Бахрейн', 'Бразилия', 'Беларусь', 'Канада', 'Республика Конго', 'Швейцария', 'Чили', 'Камерун', 'Китай', 'Колумбия', 'Коста-Рика', 'Куба', 'Кипр', 'Чехия', 'Германия', 'Дания', 'Алжир', 'Эквадор', 'Эстония', 'Египет', 'Испания', 'Эфиопия', 'Финляндия', 'Фиджи', 'Франция', 'Англия', 'Шотландия', 'Уэльс', 'Грузия', 'Гибралтар', 'Греция', 'Гватемала', 'Гонконг', 'Гондурас', 'Хорватия', 'Гаити', 'Индонезия', 'Ирландия', 'Израиль', 'Индия', 'Ирак', 'Иран', 'Исландия', 'Италия', 'Ямайка', 'Иордан', 'Япония', 'Кения', 'Кыргызстан', 'КНДР', 'Республика Корея', 'Либерия', 'Латвия', 'Марокко', 'Монако', 'Молдавия', 'Македония', 'Монголия', 'Мьянма', 'Мальта', 'Мексика', 'Малазия', 'Мозамбик', 'Нигер', 'Нигерия', 'Никарагуа', 'Нидерланды', 'Норвегия', 'Панама', 'Перу', 'Оман', 'Филиппины', 'Пакистан', 'Польша', 'Пуэрто-Рико', 'Португалия', 'Парагвай', 'Катар', 'Румыния', 'Сербия', 'Россия', 'Саудовская Аравия', 'Соломонские острова', 'Судан', 'Сингапур', 'Словения', 'Словакия', 'Сан-Марино', 'Сомали', 'Сирия', 'Таиланд', 'Таджикистан', 'Туркменистан', 'Тунис', 'Турция', 'Тайвань', 'Украина', 'Уганда', 'США', 'Уругвай', 'Узбекистан', 'Венесуэла', 'Вьетнам', 'Йемен', 'ЮАР', 'Зимбабве']


async def create_game(db: Session, game_id):
    player_1, player_2 = game_id.split('x')
    match = random.sample(countries, 10)
    newGame = Match(player1=player_1, player2=player_2, round1=match[0], round2=match[1], round3=match[2], round4=match[3], round5=match[4], round6=match[5], round7=match[6], round8=match[7], round9=match[8], round10=match[9])
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

