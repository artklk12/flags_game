from fastapi import FastAPI, Request, Depends, Response
# from fastapi import WebSocket
import flags.service as service
from core.utils import get_db
from sqlalchemy.orm import Session
from core.db import SessionLocal

app = FastAPI()


@app.middleware("http")
async def db_session_midddleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/create_game/{game_id}/")
async def create_game(game_id, db: Session = Depends(get_db)):
    match_id = await service.create_game(db, game_id)
    return {"game_id": match_id}


@app.get("/game/{game_id}/get_round/{round_id}/")
async def get_round(game_id, round_id, db: Session = Depends(get_db)):
    r, answers = await service.get_round_info(db, game_id, round_id)
    return {"country": r[0].strip(), "answers": answers, "image": r[1], "player1": r[2], "player2": r[3]}


@app.post("/game/{game_id}/get_round/{round_id}/")
async def write_answers(request: Request, game_id, round_id, db: Session = Depends(get_db)):
    body = await request.json()
    await service.write_answers(db, game_id, round_id, body['player_id'], body['player_answer'], body['correct_answer'])
    return

@app.get("/game/{game_id}/")
async def get_results(request: Request, game_id, db: Session = Depends(get_db)):
    body = await request.json()
    user_result, oponent_result = await service.get_match_results(db, game_id, body['user_id'], body['oponent_id'])
    return {"user_result": user_result, 'oponent_result': oponent_result}

@app.post("/add-country/")
async def add_country(request: Request, db: Session = Depends(get_db)):
    body = await request.json()
    await service.create_country(db, body['title'], body['image'])
    return