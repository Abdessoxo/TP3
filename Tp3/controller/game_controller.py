import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from dao.game_dao import engine, Base
from model.game import Game
from services.game_service import GameService

app = FastAPI()
game_service = GameService()


class CreateGameData(BaseModel):
    player_name: str
    min_x: int
    max_x: int
    min_y: int
    max_y: int
    min_z: int
    max_z: int


@app.post("/create-game")
async def create_game(game_data: CreateGameData):
    return game_service.create_game(game_data.player_name, game_data.min_x, game_data.max_x, game_data.min_y,
                                    game_data.max_y, game_data.min_z,
                                    game_data.max_z)


@app.get("/get-game")
async def get_game(game_id: int) -> Game:
    return game_service.get_game(game_id)


class JoinGameData(BaseModel):
    game_id: int
    player_name: str


@app.post("/join-game")
async def join_game(game_data: JoinGameData) -> bool:
    game_id = game_data.game_id
    player_name = game_data.player_name
    return game_service.join_game(game_id, player_name)


class AddVesselData(BaseModel):
    game_id: int
    player_name: str
    vessel_type: str
    x: int
    y: int
    z: int


@app.post("/add-vessel")
async def add_vessel(game_data: AddVesselData) -> bool:
    return game_service.add_vessel(game_data.game_id, game_data.player_name, game_data.vessel_type, game_data.x,
                                   game_data.y, game_data.z)


class ShootAtData(BaseModel):
    game_id: int
    shooter_name: str
    vessel_id: int
    x: int
    y: int
    z: int


@app.post("/shoot-at")
async def shoot_at(game_data: ShootAtData) -> bool:
    game_id = game_data.game_id
    shooter_name = game_data.shooter_name
    vessel_id = game_data.vessel_id
    x = game_data.x
    y = game_data.y
    z = game_data.z
    return game_service.shoot_at(game_id, shooter_name, vessel_id, x, y, z)


@app.get("/game-status")
async def get_game_status(game_id: int, player_name: str) -> str:
    game_status = game_service.get_game_status(game_id, player_name)
    return game_status


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"message": f"{exc}"})


@app.get("/favicon.ico")
async def favicon():
    return JSONResponse(status_code=204)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001,debug=True)


app = FastAPI()
BASE_PATH = Path(__file__).resolve().parent.parent
app.mount("/views", StaticFiles(directory=BASE_PATH / 'views'), name="views")
