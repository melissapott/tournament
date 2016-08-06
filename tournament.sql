-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (
	id serial primary key,
	playerName text);


create table match (
	id serial primary key,
	playerID int references players(id),
	opponentID int references players(id),
	score int,
	unique (playerID, opponentID)
);
