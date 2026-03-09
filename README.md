# 🎵 Navidrome Smart Playlist Creator

A beautiful, interactive CLI tool for creating `.nsp` (Navidrome Smart Playlist) files — no manual JSON editing required.

![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Navidrome](https://img.shields.io/badge/Navidrome-Smart%20Playlists-blue?style=flat-square)

---

## Overview

[Navidrome](https://www.navidrome.org/) Smart Playlists are dynamic playlists defined as JSON objects stored in `.nsp` files. They automatically populate based on rules you define — things like "all songs I've loved from the 80s" or "high-quality tracks I haven't played recently."

This tool guides you through building those JSON rules via an interactive menu, handles all the formatting, and saves the finished `.nsp` file directly to your playlist directory.

---

## Features

- **Interactive menu-driven interface** — no JSON knowledge required
- **Full field support** — string, numeric, boolean, and date field types
- **Nested logic** — combine rules with `all` (AND) or `any` (OR)
- **Multi-field sorting** — sort by multiple fields with per-field direction control
- **Persistent config** — remembers your playlist directory between sessions
- **Example playlists** — built-in reference examples to get you started
- **Field & operator reference** — view available fields and operators at any prompt
- **Beautiful UI** — enhanced display via [`rich`](https://github.com/Textualize/rich) (optional, degrades gracefully)

---

## Requirements

- Python 3.7+
- [`rich`](https://pypi.org/project/rich/) *(optional, but recommended for the best experience)*

---

## Installation

1. **Clone or download** this repository:
   ```bash
   git clone https://github.com/your-username/Navidrome-SmartPlaylist-Generator-nsp.git
   cd Navidrome-SmartPlaylist-Generator-nsp
   ```

2. **Install the optional dependency** for enhanced UI:
   ```bash
   pip install rich
   ```

3. **Run the tool:**
   ```bash
   python navidrome_smart_playlist_creator.py
   ```

---

## Usage

On first run, you will be prompted to set your playlist directory — the folder where Navidrome scans for `.nsp` files (typically inside your `PlaylistsPath` or music library folder).

```
============================================================
  NAVIDROME SMART PLAYLIST CREATOR
============================================================

  [1] Set/Change Playlist Directory
  [2] Create New Smart Playlist
  [3] View Field Reference
  [4] View Operator Reference
  [5] Show Example Playlists
  [6] Exit
```

### Creating a Playlist

Select **[2]** and the tool will walk you through:

1. **Name & description** — give your playlist a title and optional comment
2. **Rules** — add one or more conditions (field + operator + value)
3. **Logic** — combine conditions with `all` (every rule must match) or `any` (at least one must match)
4. **Sorting** — choose a sort field and direction, including multi-field sorting
5. **Limit** — optionally cap the number of tracks
6. **Preview & save** — review the generated JSON before saving

The tool saves your playlist to the configured directory with a `.nsp` extension, ready to be picked up on the next Navidrome library scan.

---

## Fields Reference

| Category | Fields |
|---|---|
| **String** | `title`, `album`, `artist`, `albumartist`, `genre`, `composer`, `comment`, `lyrics`, `filepath`, `filetype`, `grouping`, `discsubtitle`, `albumtype`, `albumcomment`, `catalognumber` |
| **Numeric** | `year`, `tracknumber`, `discnumber`, `size`, `duration`, `bitrate`, `bitdepth`, `bpm`, `channels`, `playcount`, `rating`, `library_id` |
| **Boolean** | `loved`, `hascoverart`, `compilation` |
| **Date** | `date`, `originaldate`, `releasedate`, `dateadded`, `datemodified`, `dateloved`, `lastplayed`, `daterated` |

Additional fields from Navidrome's tag mappings are also supported, including MusicBrainz IDs (`mbz_album_id`, `mbz_artist_id`, `mbz_recording_id`, etc.) and any custom tags imported from your music files.

---

## Operators Reference

| Operator | Description | Applies To |
|---|---|---|
| `is` | Equal | String, Number, Boolean |
| `isNot` | Not equal | String, Number, Boolean |
| `gt` | Greater than | Number |
| `lt` | Less than | Number |
| `contains` | Contains substring | String |
| `notContains` | Does not contain | String |
| `startsWith` | Starts with | String |
| `endsWith` | Ends with | String |
| `inTheRange` | Inclusive range | Array of two numbers or dates |
| `before` | Before date | Date (`YYYY-MM-DD`) |
| `after` | After date | Date (`YYYY-MM-DD`) |
| `inTheLast` | Within the last N days | Number of days |
| `notInTheLast` | Not within the last N days | Number of days |
| `inPlaylist` | Track is in another playlist | Playlist ID |
| `notInPlaylist` | Track is not in another playlist | Playlist ID |

---

## Sorting

Sort by a single field:
```
"sort": "year", "order": "desc"
```

Sort by multiple fields using comma separation. Prefix with `+` (ascending, default) or `-` (descending):
```
"sort": "year,-rating,title"
```

Use `random` for a shuffled playlist:
```
"sort": "random"
```

---

## Example Playlists

### Recently Played
Tracks played in the last 30 days, most recent first:
```json
{
  "name": "Recently Played",
  "comment": "Tracks played in the last 30 days",
  "all": [{ "inTheLast": { "lastplayed": 30 } }],
  "sort": "lastplayed",
  "order": "desc",
  "limit": 100
}
```

### 80s Favorites
Loved or highly-rated songs from the 1980s:
```json
{
  "name": "80s Favorites",
  "all": [
    { "any": [{ "is": { "loved": true } }, { "gt": { "rating": 3 } }] },
    { "inTheRange": { "year": [1980, 1989] } }
  ],
  "sort": "year",
  "order": "desc",
  "limit": 50
}
```

### High Quality Tracks
Lossless FLAC files only:
```json
{
  "name": "High Quality",
  "comment": "Lossless tracks only",
  "all": [
    { "gt": { "bitrate": 900 } },
    { "is": { "filetype": "flac" } }
  ],
  "sort": "random",
  "limit": 200
}
```

### All Songs (Random)
Every track in your library, shuffled:
```json
{
  "all": [{ "gt": { "playcount": -1 } }],
  "sort": "random",
  "limit": 1000
}
```

### Multi-Library Filter
High-rated songs from a specific library:
```json
{
  "name": "High-Rated Songs from Library 2",
  "all": [
    { "gt": { "rating": 3 } },
    { "is": { "library_id": 2 } }
  ],
  "sort": "random",
  "limit": 100
}
```

---

## How Navidrome Imports Playlists

Place your `.nsp` files in:
- Any folder within your music library, **or**
- The path specified by the `PlaylistsPath` configuration option

Navidrome automatically detects and imports them during the next library scan. Smart Playlists refresh automatically when accessed, with a minimum delay configurable via `SmartPlaylistRefreshDelay` (default: `5s`).

> **Tip:** You can also use [Feishin](https://github.com/jeffvli/feishin/), a desktop/web Subsonic client, for graphical playlist editing that syncs back to Navidrome.

---

## Configuration

The tool saves your playlist directory to `~/.navidrome_playlist_config.json` so you don't have to re-enter it each session. To change it, select **[1] Set/Change Playlist Directory** from the main menu.

---

## Notes

- Dates must be in `YYYY-MM-DD` format
- Boolean values must not be quoted: `true` / `false`
- `filepath` is relative to your music library root (no leading `/music` prefix)
- To use `inPlaylist` / `notInPlaylist`, get the playlist ID from the Navidrome UI URL: `.../playlists/<ID>`
- The `_` character may be ignored in `contains` / `endsWith` conditions — adjust accordingly

---

## License

MIT — use freely, modify as needed.
