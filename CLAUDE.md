# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Idiom Solitaire (成语接龙) — a Flask web game where players chain Chinese idioms against an AI. Idioms are chained by matching the last pinyin syllable (tone-stripped) of one idiom to the first pinyin syllable of the next. The idiom dictionary (31,648 entries) lives in `data/idiom.json`.

## Running the App

**Entry point** — the Flask app with login and routing:
```
python game/play/login.py
```
This starts Flask on `0.0.0.0:5000` with debug mode. The app requires a running MySQL instance and Redis server.

**CLI-only version** (no web UI, terminal-based game):
```
python game/play/play.py
```

## Dependencies

No `requirements.txt` exists. Required packages (inferred from imports):
```
flask, pandas, numpy, mysql-connector-python, redis, requests, beautifulsoup4
```

## Infrastructure Requirements

- **MySQL**: database `communicate_sql` on `127.0.0.1`, configured in `sql/connect_mysql.py`. Tables: `auth_user`, `co_user_info`, `sys_ai_info`, `co_user_play_dtl`, `co_ai_play_dtl`, `co_user_play_record`.
- **Redis**: used for countdown timers in AI-first game mode. Server path and conf path are hardcoded in `redis_file/redis_countdown.py` — must match local Redis installation.

## Architecture

**Game flow**: Login → Start page → Choose AI opponent → Choose who goes first (user or AI) → Play idiom chain → View results/game records.

**Routing**: `game/play/login.py` is the main app. It registers additional routes from `game/play/routes.py` via `register_routes(app)`. Several modules (`AI_first_play.py`, `user_first_play.py`, `choose.py`, `battle_page.py`, `game_records.py`) each instantiate their own `Flask(__name__)` app objects for standalone testing, but are imported as route handlers by the main app.

**Idiom matching logic**: The DataFrame `idioms_df` is built at module import time from `data/idiom.json`. It computes `shoupin` (first pinyin syllable, no tone) and `weipin` (last pinyin syllable, no tone) columns. Chaining validates that the user's idiom `shoupin` matches the previous idiom's `weipin`. The AI responds by randomly selecting from idioms whose `shoupin` matches.

**Game state**: Stored in Flask `session` — `used_idioms`, `last_char`, `initial_ai_idiom`, `aiNo`, `Situation` (battle ID). Game records are persisted to MySQL on each turn.

**Redis countdown** (`redis_file/redis_countdown.py`): `RedisManager` auto-starts a Redis subprocess using hardcoded Windows paths, manages connection lifecycle, and registers an `atexit` cleanup handler. Used only in AI-first mode for 30-second turn timers.

## Data Scripts (`scripts/`)

Web scraping scripts for building the dictionary datasets:
- `chengyu.py` — scrapes idioms from zd9999.com → `chengyu.json`
- `addAbbreviation.py` — adds pinyin abbreviation field → produces `data/idiom.json`
- `ci.py`, `word.py`, `xiehouyu.py` — scrape words, characters, and two-part allegorical sayings

## Known Issues

- Hardcoded absolute Windows paths throughout (Flask template/static folders, Redis paths, data file paths)
- Each game module creates its own `Flask(__name__)` instance — only `login.py`'s instance is actually used at runtime; the others are vestigial
- `remove_tone()` and `insert_*_data()` functions are duplicated across `AI_first_play.py`, `user_first_play.py`, and `play.py`
- Database credentials are in plaintext in `sql/connect_mysql.py`