# P04_ChessCheckCheckmate

## Table of contents
- [Table of content](#table-of-content)
- [Foreword](#foreword)
- [Installation](#installation)
- [How to use](#how-to-use)
- [Possible improvements](#possible-improvements)

## Foreword

The aim of the program is the to manage chest tournaments.

Tournaments are playing weekly. So they can be created one at a time.

About the rules, there are :
- 8 players by tournament.
- 4 rounds.
- 3 choices of time comtrol (blitz, bullet or rapid).
- colors are choosen randomly.

The format is a Swiss-sytsem tournament
## Installation
### Clone the code source (using ssh)

    mkdir foo
    git clone git@github.com:jjbochard/ChessCheckCheckmate.git foo
    cd foo

### Create your virtual environnement

First, install [Python 3.6+](https://www.python.org/downloads/).

Then, create your virtual environnement :

    python3 -m venv <your_venv_name>

Activate it :

- with bash command prompt

        source <your_venv_name>/bin/activate

- or with Windows PowerShell

        .\venv\Scripts\activate

Finally, install required modules

    pip3 install -r requirements.txt

To deactivate your venv :

    deactivate

### Optionnal : configure your git repository with pre-commit (if you want to fork this project)

You can install the configured pre commit hook with

    pre-commit install

## How to use

+ Run the program

To start the program, use :

    python ucm.py

+ Create HTML file generate by flake8-html

To create this file, use :

    flake8 --format=html --htmldir=flake8_rapport --exclude=env/

In this programm you can :

* Manage tournament
  + Create a tournament
    - enter the informations of the tournament
    - add 8 players (already in base or create new players)

  + Create round
    - incoming matchs are displayed
    - end the round or go to the main menu

  + Write scores

  + When the tournament is finished, an overview table and the winner are displayed

* Display informations
  + About tournaments
  + About rounds
  + About matchs

## Possible improvements

* before starting coding, think about packages to use. Here I could use one which is better for display menu and taking user input.

* sometimes, the last match of the last round has already been played. I try to respect as much as possible the Swiss System and favorise the last player by creating 2 other matchs with the last 4 players of the tournament. If all the potential matchs have already been played, I create 3 other matchs with the last 6 players.

* divise the controllers file in other smaller files for better readness.
