from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

from model.air_missile_launcher import AirMissileLauncher
from model.battlefield import Battlefield
from model.cruiser import Cruiser
from model.destroyer import Destroyer
from model.frigate import Frigate
from model.game import Game
from model.player import Player
from model.submarine import Submarine
from model.surface_missile_launcher import SurfaceMissileLauncher
from model.torpedos_launcher import TorpedoLauncher
from model.vessel import Vessel
from model.weapon import Weapon

engine = create_engine('sqlite:///Tp3.db')
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)


class GameEntity(Base):
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    players = relationship("PlayerEntity", back_populates="game", cascade="all, delete-orphan")


class PlayerEntity(Base):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship("GameEntity", back_populates="players")
    battle_field = relationship("BattlefieldEntity", back_populates="player", uselist=False,
                                cascade="all, delete-orphan")


class VesselEntity(Base):
    __tablename__ = 'vessel'
    id = Column(Integer, primary_key=True)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(String, nullable=False)
    battlefield_id = Column(Integer, ForeignKey("battlefield.id"), nullable=False)
    battlefield = relationship("BattlefieldEntity", back_populates="vessels")
    weapon = relationship("WeaponEntity", back_populates="vessel", uselist=False, single_parent=True)


class BattlefieldEntity(Base):
    __tablename__ = 'battlefield'
    id = Column(Integer, primary_key=True)
    min_x = Column(Integer)
    min_y = Column(Integer)
    min_z = Column(Integer)
    max_x = Column(Integer)
    max_y = Column(Integer)
    max_z = Column(Integer)
    max_power = Column(Integer)
    player_id = Column(Integer, ForeignKey("player.id"), nullable=False)
    player = relationship("PlayerEntity", back_populates="battle_field")
    vessels = relationship("VesselEntity", back_populates="battlefield", cascade="all, delete-orphan")


class VesselType(Enum):
    CRUISER = "Cruiser"
    DESTROYER = "Destroyer"
    FRIGATE = "Frigate"
    SUBMARINE = "Submarine"


class WeaponEntity(Base):
    __tablename__ = 'weapon'
    id = Column(Integer, primary_key=True)
    ammunitions = Column(Integer)
    range = Column(Integer)
    type = Column(String, nullable=False)
    vessel_id = Column(Integer, ForeignKey("vessel.id"), nullable=False)
    vessel = relationship("VesselEntity", back_populates="weapon", uselist=False, single_parent=True)


class WeaponType(Enum):
    AIRMISSILELAUNCHER = "AirMissileLauncher"
    SURFACEMISSILELAUNCHER = "SurfaceMissileLauncher"
    TORPEDOLAUNCHER = "TorpedoLauncher"


def map_to_game_entity(game: Game) -> GameEntity:
    game_entity = GameEntity()
    if game.get_id() is not None:
        game_entity.id = game.get_id()
    for player in game.get_players():
        player_entity = PlayerEntity()
        player_entity.id = player.id
        player_entity.name = player.get_name()
        battlefield_entity = map_to_battlefield_entity(
            player.get_battlefield())
        vessel_entities = \
            map_to_vessel_entities(map_to_battlefield_entity(player.get_battlefield()).id,
                                   player.get_battlefield().vessels)
        battlefield_entity.vessels = vessel_entities
        player_entity.battle_field = battlefield_entity
        game_entity.players.append(player_entity)
    return game_entity


def map_to_vessel_entities(battlefield_id: int, vessels: list[Vessel]) \
        -> list[VesselEntity]:
    vessel_entities: list[VesselEntity] = []
    for vessel in vessels:
        vessel_entity = map_to_vessel_entity(battlefield_id, vessel)
        vessel_entities.append(vessel_entity)

    return vessel_entities


def map_to_vessel_entity(battlefield_id: int, vessel: Vessel) -> VesselEntity:
    vessel_entity = VesselEntity()
    weapon_entity = WeaponEntity()

    weapon_entity.ammunitions = vessel.weapon.ammunitions
    weapon_entity.range = vessel.weapon.range
    weapon_entity.type = type(vessel.weapon).__name__

    vessel_entity.weapon = weapon_entity
    vessel_entity.type = type(vessel).__name__
    vessel_entity.hits_to_be_destroyed = vessel.hits_to_be_destroyed
    vessel_entity.coord_x = vessel.coordinates[0]
    vessel_entity.coord_y = vessel.coordinates[1]
    vessel_entity.coord_z = vessel.coordinates[2]
    vessel_entity.battle_field_id = battlefield_id
    return vessel_entity


def map_to_player_entity(player: Player) -> PlayerEntity:
    player_entity = PlayerEntity()
    player_entity.id = player.id
    player_entity.name = player.name
    player_entity.battle_field = map_to_battlefield_entity(
        player.get_battlefield())
    return player_entity


def map_to_battlefield_entity(battlefield: Battlefield) -> BattlefieldEntity:
    battlefield_entity = BattlefieldEntity()

    battlefield_entity.max_x = battlefield.max_x
    battlefield_entity.max_y = battlefield.max_y
    battlefield_entity.max_z = battlefield.max_z
    battlefield_entity.min_x = battlefield.min_x
    battlefield_entity.min_y = battlefield.min_y
    battlefield_entity.min_z = battlefield.min_z
    battlefield_entity.max_power = battlefield.max_power
    return battlefield_entity


def create_player(self, player: Player) -> int:
    player_entity = map_to_player_entity(player)
    self.db_session.add(player_entity)
    self.db_session.commit()
    return player_entity.id


def update_player(self, player: Player) -> None:
    player_entity = map_to_player_entity(player)
    self.db_session.merge(player_entity)
    self.db_session.commit()


def create_vessel(self, vessel: Vessel) -> int:
    vessel_entity = map_to_vessel_entity(vessel)
    self.db_session.add(vessel_entity)
    self.db_session.commit()
    return vessel_entity.id


def update_vessel(self, vessel: Vessel) -> None:
    vessel_entity = map_to_vessel_entity(vessel)
    self.db_session.merge(vessel_entity)
    self.db_session.commit()


def map_to_battlefield(battlefield_entity: BattlefieldEntity) -> Battlefield:
    battlefield = Battlefield(
        battlefield_entity.max_x, battlefield_entity.max_y,
        battlefield_entity.max_z, battlefield_entity.max_power)
    battlefield.id = battlefield_entity.id
    battlefield.min_x = battlefield_entity.min_x
    battlefield.min_y = battlefield_entity.min_y
    battlefield.min_z = battlefield_entity.min_z
    return battlefield


def map_to_player(player_entity: PlayerEntity) -> Player:
    player = Player(name=player_entity.name, battle_field=map_to_battlefield(player_entity.battle_field))
    player.id = player_entity.id
    return player


def map_to_game(game_entity: GameEntity) -> Game:
    game = Game(id=game_entity.id)
    game.players = [map_to_player(player_entity) for player_entity in game_entity.players.all()]
    return game


import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


class GameDao:
    def __init__(self):
        Base.metadata.create_all(bind=engine)
        self.db_session = Session()

    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id

    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)

    def update_game(self, game: Game) -> None:
        game_entity = map_to_game_entity(game)
        self.db_session.merge(game_entity)
        self.db_session.commit()

