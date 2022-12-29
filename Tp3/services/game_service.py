from dao.game_dao import GameDao, VesselType
from model.battlefield import Battlefield
from model.cruiser import Cruiser
from model.destroyer import Destroyer
from model.frigate import Frigate
from model.game import Game
from model.player import Player
from model.submarine import Submarine


class GameService:

    def __init__(self):
        self.game_dao = GameDao()

    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int,
                    max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)

    def join_game(self, game_id: int, player_name: str) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        battle_field = game.players[0].battle_field
        player = Player(player_name, battle_field)
        game.add_player(player)
        self.game_dao.update_game(game)
        return True

    def get_game(self, game_id: int) -> Game:
        return self.game_dao.find_game(game_id)

    def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        player = next((player for player in game.players if player.name == player_name), None)
        if player is None:
            return False
        if vessel_type == VesselType.CRUISER.value:
            vessel = Cruiser((x, y, z), player.battle_field.max_power)
        elif vessel_type == VesselType.DESTROYER.value:
            vessel = Destroyer((x, y, z), player.battle_field.max_power)
        elif vessel_type == VesselType.FRIGATE.value:
            vessel = Frigate((x, y, z), player.battle_field.max_power)
        elif vessel_type == VesselType.SUBMARINE.value:
            vessel = Submarine((x, y, z), player.battle_field.max_power)
        else:
            return False
        player.battle_field.add_vessel(vessel)
        self.game_dao.update_game(game)
        return True

    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        shooter = next(player for player in game.players if player.name == shooter_name)
        target_vessel = next(vessel for vessel in shooter.battle_field.vessels if vessel.id == vessel_id)
        if target_vessel.weapon.shoot_at(x, y, z):
            target_vessel.hits_to_be_destroyed -= 1
        if target_vessel.hits_to_be_destroyed == 0:
            shooter.battle_field.vessels.remove(target_vessel)
            return True
        return False

    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        for player in game.players:
            if player.name == shooter_name:
                if player.battle_field.has_won():
                    return "GAGNE"
                elif player.battle_field.has_lost():
                    return "PERDU"
                else:
                    return "ENCOURS"
        raise ValueError(f"Player with name '{shooter_name}' not found in game with id '{game_id}'")
