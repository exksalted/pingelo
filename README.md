# Pingelo

This is a personal project, that stems from my attempt to gather and represent data from the table tennis games of my group.
I gather data from games manually in .txt form. This data is processed with Python, from which the stats are gathered.
The data is updated into a Google Sheet, which the site pings for most stats on the site.

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
- Run the data through a .py file
- The data is exported to 4 .csv files, which I manually copy into a Google Sheet.
- The site checks the Sheet for data, and populates tables and player cards with the data.
- Still manual: Creating new players in the sheet, player.htmls, tournament card.htmls, setting the stat of "tournaments won" in the sheet.
- Also updating the graphs is still manual, some I might change into automatically updating.


That's about it.
