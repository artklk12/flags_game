from starlette.responses import Response
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi import FastAPI, Request
# from fastapi import WebSocket
import flags.service as service

app = FastAPI()



@app.get("/create_game/{game_id}")
async def root(game_id):
    match_id = service.create_game(game_id)
    return {"game_id": match_id}

@app.get("/game/{game_id}/get_round/{round_id}")
async def root(game_id, round_id):
    r, answers = service.get_round_info(game_id, round_id)
    return {"country": r[0], "answers": answers, "image": r[1], "player1": r[2], "player2": r[3]}

# @app.post("/game/{game_id}/get_round/{round_id}")
# async def root(request: Request, game_id, round_id):
#     body = request.json()
#     service.write_answers(game_id, round_id, player1_id, player1_answer, player2_id, player2_answer)
#     return

# @app.get("/invite/{user_id}")
# async def invite_user(user_id):
#     return {"message": f"Game №:{game_id}"}


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     print('Accepting client connection...')
#     await websocket.accept()
#     while True:
#         try:
#             # Wait for any message from the client
#             await websocket.receive_text()
#             # Send message to the client
#             resp = {'value': 'GAMEPLAY'}
#             await websocket.send_json(resp)
#         except Exception as ex:
#             print('error:', ex)
#             break
#         print('Bye..')