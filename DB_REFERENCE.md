# superbowl.db — Reference

Quick reference for the SQLite database created in this project.

File
- `superbowl.db` — SQLite database file at the repository root.

Main table
- `superbowl_champions` — the single table containing the scraped Super Bowl data.

Columns (DB name -> original CSV header)
- `game` -> `Game`  — Super Bowl identifier (Roman numeral)
- `date_season` -> `Date ( Season)`  — date and season information (contains years)
- `winning_team` -> `Winning team`  — winning team (may include parenthetical record)
- `score` -> `Score`  — final score string (e.g. `35–10`)
- `losing_team` -> `Losing team`  — losing team (may include parenthetical record)
- `venue` -> `Venue`  — stadium name
- `city` -> `City`  — city (may contain parenthetical numbering)
- `attendance` -> `Attendance`  — attendance string (commas retained)
- `referee` -> `Referee`  — referee name
- `ref` -> `Ref.`  — footnote reference (if present)

Notes
- All columns are stored as TEXT.
- Team names often include parenthetical records (e.g. `New England Patriots A (5, 3–2 )`). If you want to query just the team name, strip parentheses with SQL string functions or post-process in your application.

Example SQL queries

- Show table names
```sql
-- run in the sqlite3 CLI
.tables
```

- Show schema for the `superbowl_champions` table
```sql
PRAGMA table_info('superbowl_champions');
```

- Count rows
```sql
SELECT COUNT(*) FROM superbowl_champions;
```

- Select basic columns
```sql
SELECT game, date_season, winning_team, score, losing_team
FROM superbowl_champions
LIMIT 20;
```

- Find rows containing a specific year (matches any occurrence of the year string in `date_season`)
```sql
SELECT * FROM superbowl_champions
WHERE date_season LIKE '%1999%';
```

- Find by Super Bowl (game) roman numeral
```sql
SELECT * FROM superbowl_champions WHERE game = 'XXXIV';
```

- Example: show the most recent game (by searching for a year and ordering, or inspect rows)
```sql
-- if you want the game with the latest year present in `date_season`, you'll need to parse the year out
-- a simple approach: find rows matching the latest 4-digit year you care about
SELECT * FROM superbowl_champions WHERE date_season LIKE '%2020%';
```

Tips
- If you want typed columns (e.g. `attendance` as INTEGER or separate `year` column), I can add a small migration script to parse and convert fields and rewrite the database with typed columns.
- To use from Python, open with `sqlite3.connect('superbowl.db')` and query normally.

If you want, I can also add ready-to-use example scripts (Python or SQL) that demonstrate filtering by year, extracting clean team names, or normalizing attendance as integers.
