from core.db import Base
from sqlalchemy import Column, String, Integer, ForeignKey, BigInteger
from sqlalchemy.orm import relationship


class Flag(Base):
    __tablename__ = 'flags_cards'

    title = Column(String, primary_key=True, index=True, unique=True)
    image = Column(String)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    player1 = Column(BigInteger)
    player2 = Column(BigInteger)
    round1 = Column(String)
    round2 = Column(String)
    round3 = Column(String)
    round4 = Column(String)
    round5 = Column(String)
    round6 = Column(String)
    round7 = Column(String)
    round8 = Column(String)
    round9 = Column(String)
    round10 = Column(String)


class Rounds(Base):
    __tablename__ = 'matches_rounds'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    match_id = Column(Integer, ForeignKey('matches.id'))
    match = relationship('Match')
    player_id = Column(BigInteger)
    round = Column(Integer)
    player_answer = Column(String)
    correct_answer = Column(String)


