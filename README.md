# Tournament Swiss Pairings
This program was produced as a project submission for Udacity's FSND Tournament Project.

## Requirements:
- a computer running PostgreSql and Python
- The following files included in this repository:
  - **tournament.sql** - this file creates the database tables used to store tournament players, points and results
  - **tournament.py** - this file contains python fuctions that interact with the database for registering players, matching pairs, etc.
  - **tournament_test.py** - this file was provided by Udacity and is used to check the correct function of tournament.py.  It has been modified to add an additional test for recording tied matches, which was beyond the basic scope of the project

## Usage:
1.  create a blank database called 'tournament':
  1.  at the command prompt, enter `psql`
  2.  at the psql prompt, enter `create database tournament;`
2.  import tournament.sql, which will create necessary tables and populate the points table.
  1.  at the prompt, enter `\i tournament.sql`
  2.  to exit psql, enter `\q`
3.  run tournament_test.py which will attempt to register players, delete players and report matches.
  1.  at the server command prompt, enter `python tournament_test.py`
