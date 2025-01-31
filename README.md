# Pingelo

This is a personal project, that stems from my attempt to gather and represent data from the table tennis games of my group.
I gather data from games manually in .txt form. This data is processed by three different .py codes, from which the stats are gathered.
The data is updated into a Google Sheet, which updates most stats on the site.

---

## Table of Contents 📚

- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
- [How does it work?](#workings)

---

## Features 🌟

- Site for representing varied player and tournament stats.
- Site contains graphs, player cards and tournament cards with brackets.
- Code calculates elo rating, RD, average points, best/worst matchups etc.
---

## Usage

- Start by visiting the site! exksalted.github.io/pingelo/index.html
- I allow yall to copy the site format, if that is something you somehow want to do.
- Code is free for all to use as well.

## Contributing

- If you want to contribute, feel free to do so!
- For example finding/fixing bugs, making the code/site more efficient, adding automatisation for more stats etc.

## Workings

Steps on how I operate:
- Gather data on games manually into .txt files.
- Run the data through the three different .py files.
- One for calculating ratings, RD etc. This data I copy manually into a Google Sheet.
- Some values I need to check manually, while some the sheet automatically calculates. (Manual: Current/Peak/Wors Rank (read from a graph), Average points (Read from player_stats.txt), tournaments played/won (fully manual), RD & RD Change (read Elo.py output).
- The Sheet updates most values on the site, but several stats I update manually: (Best Victory/Worst Defeat, Best Tournament Performance, Matchup Stats)
- Tournament Cards and player won tournaments need to be added manually.


That's about it.
