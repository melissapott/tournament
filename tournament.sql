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

create table points (
	point int primary key,
	description text
);

create table match (
	id serial primary key,
	playerID int references players(id),
	opponentID int references players(id),
	score int references points(point),
	unique (playerID, opponentID)
);


insert into points (point, description) values (3, 'win');
insert into points (point, description) values (2, 'bye');
insert into points (point, description) values (1, 'draw');
insert into points (point, description) values (0, 'lose');
