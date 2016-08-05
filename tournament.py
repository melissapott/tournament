#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from match;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players;")
    result = c.fetchone()
    DB.close()
    return result[0]

def registerPlayer(name):
    # connect to the database, insert a player name into the players table
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (playername) values (%s)", (name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    c.execute("select players.id, playerName, (select count(match.id) from match where players.id = match.playerID and score >= 3) as wins, (select count(match.id) from match where players.id = match.playerID) as matches from players group by id order by wins desc, matches;")
    result = c.fetchall()
    DB.close()
    return result

    # This function is hard coded to return the count of '3' scores as wins to satisfy the requirements of the testing routine without regard to ties or byes.  In a more robust application
    # the function would have returned a 'score' or 'standing' as well as a match count.  In that case, the first subselect would have been written as (select sum(score) from match....)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into match (playerID, opponentID, score) values (%s,%s,%s);", (winner, loser, 3))
    c.execute("insert into match (playerID, opponentID, score) values (%s,%s,%s);", (loser, winner, 0))
    DB.commit()
    DB.close()

    # we are inserting the values of 3 for win and 0 for lose in this case.  In a more robust application, we may have situations which
    # require the scoring of "draws" and "byes", which won't count for as much as a true win.  
    # we are also inserting two records into the table, because each player (in this case 2) has a result from the match.  If it were
    # a Hungry Hippos game, we would insert 4 records with the number of marbles for each hippo, or n records for each of n players of Monoply with their bank balance.
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # first, get a list of all the players to loop through, in order of standings,
    # duplicate the list for opponents, and create a blank list for pairings
    players = playerStandings() 
    pairings = []
        
    # loop through all the players one at a time and try to find them the closest match
    for p in players:
        # make sure this player hasn't already been paired with someone else
        if [i for i in pairings if p[0] == i[0] or p[0] == i[2]]:
            # the player is already paired, so move on to the next
            continue

        else:
            # get a list of possible opponents who haven't been matched with the player previously, and aren't currently paired with someone else
            DB = connect()
            c = DB.cursor()
            c.execute("select id, playerName, (select sum(score) from match where players.id = match.playerID) as score from players where id not in (select playerID from match where opponentID = %s) and id <> %s group by id order by score desc;", ((p[0],),(p[0])))
            opponents = c.fetchall()

            for o in opponents:
                # now check to see if the opponent in question is already in the current pairing list
                if [i for i in pairings if i[0] == o[0] or i[2] == o[0]]:
                    # the opponent has already been paired, move to the next
                    continue
                else:
                    pairings.append((p[0],p[1],o[0],o[1]))
                    break

    # NOTE:  Because this function returns player pairings based on rank of players who have not played each other, once a clear winner has been reached assuming each player is paired with another
    # only once, it will return a list with a length less than the total player count/2.  For this reason, it could be used in a counting function to calculate the number of necessary rounds in a 
    # more robust application.  Another possibly methodolgy for this function, which would be appropriate for large tournaments, would be splitting the players in half by the top ranked and bottom
    # ranked, then pairing them up.  The basics of this function would still be used, but called from within another function which splits the player list in half based on rankings.
    
    return pairings

 
