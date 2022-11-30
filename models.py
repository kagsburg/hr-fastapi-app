# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, String, TIMESTAMP, Table, Time, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BetStatu(Base):
    __tablename__ = 'bet_status'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))


class Group(Base):
    __tablename__ = 'groups'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class MatchStatu(Base):
    __tablename__ = 'match_status'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP)


class TransactionType(Base):
    __tablename__ = 'transaction_type'

    id = Column(INTEGER(11), primary_key=True)
    type = Column(INTEGER(11), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class User(Base):
    __tablename__ = 'users'

    id = Column(INTEGER(11), primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    otp = Column(String(100), nullable=False)
    device_info = Column(String(255))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))


class Team(Base):
    __tablename__ = 'teams'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255), nullable=False)
    flag = Column(String(255))
    group_id = Column(ForeignKey('groups.id'), nullable=False, index=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    group = relationship('Group')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(INTEGER(11), primary_key=True)
    type_id = Column(ForeignKey('transaction_type.id'), nullable=False, index=True)
    user_id = Column(INTEGER(11), nullable=False)
    amount = Column(BIGINT(20), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    type = relationship('TransactionType')


t_wallet = Table(
    'wallet', metadata,
    Column('id', INTEGER(11), nullable=False),
    Column('user_id', ForeignKey('users.id'), nullable=False, index=True),
    Column('amount', BIGINT(20), nullable=False, server_default=text("0")),
    Column('created_at', TIMESTAMP),
    Column('updated_at', TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
)


class Match(Base):
    __tablename__ = 'matches'

    id = Column(INTEGER(11), primary_key=True)
    host_id = Column(ForeignKey('teams.id'), nullable=False, index=True)
    guest_id = Column(ForeignKey('teams.id'), nullable=False, index=True)
    winner = Column(INTEGER(11), nullable=False)
    status = Column(ForeignKey('match_status.id'), nullable=False, index=True)
    date_of_match = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    guest = relationship('Team', primaryjoin='Match.guest_id == Team.id')
    host = relationship('Team', primaryjoin='Match.host_id == Team.id')
    match_statu = relationship('MatchStatu')


class Bet(Base):
    __tablename__ = 'bets'

    id = Column(INTEGER(11), primary_key=True)
    match_id = Column(ForeignKey('matches.id'), nullable=False, index=True)
    Author_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    win_team_id = Column(ForeignKey('teams.id'), index=True)
    counter_id = Column(ForeignKey('users.id'), index=True)
    bet_amount = Column(BIGINT(20), nullable=False)
    bet_status = Column(INTEGER(11), nullable=False)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    Author = relationship('User', primaryjoin='Bet.Author_id == User.id')
    counter = relationship('User', primaryjoin='Bet.counter_id == User.id')
    match = relationship('Match')
    win_team = relationship('Team')
