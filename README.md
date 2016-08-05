# Tournament Swiss Pairings
This program was produced as a project submission for Udacity's FSND Tournament Project.

##Requirements:
- a computer running PostgreSql and Python
- The following files included in this repository:
  - **tournament.sql** - this file creates the database tables used to store tournament players, points and results
  - **tournament.py** - this file contains python fuctions that interact with the database for registering players, matching pairs, etc.
  - **tournament_test.py** - this file was provided by Udacity and is used to check the correct function of tournament.py

##Usage:
1.  create a blank database called 'tournament'
2.  import tournament.sql, which will create necessary tables and populate the points table.
3.  run tournament_test.py which will attempt to register players, delete players and report matches.
