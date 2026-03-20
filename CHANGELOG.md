# Changelog

Deutsch: [CHANGELOG.DE.md](CHANGELOG.DE.md)

All notable changes to this project will be documented in this file.

## Unreleased

## 0.1.41 - 2026-03-20

- Fixed multi-part audiobook detection for servers that only expose the full track list in the ABS `/play` response instead of `item.media.tracks`.
- Added debug logging for item/play track detection so Kodi logs now show whether multi-track playback was recognized for a selected audiobook.

## 0.1.40 - 2026-03-20

- Added a playback-monitor fallback for multi-part audiobooks that explicitly starts the next ABS part file when Kodi stops after a finished part instead of advancing on its own.

## 0.1.39 - 2026-03-20

- Fixed streaming playback for multi-part audiobooks by building a Kodi playlist across all ABS track files instead of stopping after the first part file ends.
- Updated playback progress sync for playlist-based audiobook playback so resume and finished-state calculations still use the full audiobook timeline.

## 0.1.38 - 2026-03-19

- Fixed missing cover art during active playback by carrying the Audiobookshelf item artwork into the resolved Kodi player item.
- Added playback-specific music artwork fields and richer resolved item metadata so Kodi keeps showing the audiobook cover after playback starts.

## 0.1.37 - 2026-03-16

- Fixed playback selection for multi-track audiobooks so Kodi no longer opens a short single-track ABS file instead of the proper book stream.
- Hardened progress sync against empty or non-JSON ABS PATCH responses and against final sync attempts after playback has already stopped.
- Removed forced music visualisation window activation to avoid repeated `MusicVisualisation` and `fullscreenmusic` errors on incompatible Kodi skins.

## 0.1.36 - 2026-03-15

- Restricted exported audiobook NFO artist fields to the primary author only, so multi-author Audible books no longer reintroduce extra Kodi interpreters during STRM sync.
- Kept narrators in exported NFO `credits` only; they are no longer duplicated into album artist fields.

## 0.1.35 - 2026-03-15

- Fixed UI language resolution for the `Use Kodi language` setting so German and English Kodi locale variants use a consistent translated menu set.

## 0.1.34 - 2026-03-15

- Fixed playback URL signing so external podcast/feed URLs no longer receive an ABS token that breaks playback.
- Restricted playback source selection to ABS-hosted URLs only, preferring local/server-provided ABS files instead of falling back to external feed links.

## 0.1.33 - 2026-03-12

- Fixed FLAC playback on Audiobookshelf servers that expose fragile HLS transcodes by preferring direct audio file streams when available.

## 0.1.32 - 2026-03-10

- Fixed podcast playback on Kodi systems that fail direct-play checks when no audio MIME type is exposed for an episode stream.

## 0.1.31 - 2026-02-21

- Added path-based deduplication during STRM sync to prevent repeated writes of identical STRM, NFO, CUE and M3U targets in a single sync run.

## 0.1.30 - 2026-02-21

- Removed duplicate playlist writes during STRM sync so per-item M3U export happens only once.

## 0.1.29 - 2026-02-21

- Adjusted STRM sidecar naming to scanner-friendly track patterns like `NN - Title` and `NNN - Title` for improved Kodi `musicfilenamefilters` matching.

## 0.1.28 - 2026-02-21

- Added extra Kodi library compatibility metadata, including richer NFO sort and artist fields, extended CUE hints and optional per-book M3U playlist export.

## 0.1.27 - 2026-02-21

- Hardened STRM sync metadata escaping by sanitizing invalid XML control characters for NFO output and normalizing CUE text fields.

## 0.1.26 - 2026-02-21

- Improved STRM proxy compatibility by generating metadata-rich `.cue` files even without explicit chapters, increasing Kodi music-library discoverability for stream-based audiobooks.

## 0.1.25 - 2026-02-21

- Added chapter export from ABS metadata during STRM sync via `.cue` sidecar files and chapter blocks in NFO output.

## 0.1.24 - 2026-02-21

- Removed ASIN tokens from STRM and NFO filenames while keeping the ASIN inside exported NFO metadata, so library naming stays clean.

## 0.1.23 - 2026-02-21

- Added optional NFO and cover export during STRM sync for audiobooks and podcasts, including richer ABS metadata dumps for Kodi library integration.

## 0.1.22 - 2026-02-21

- Appended Audible ASIN tokens like `[ASIN-XXXXXXXXXX]` to exported audiobook `.strm` filenames for deterministic scraper matching.

## 0.1.21 - 2026-02-21

- Moved debug logging into its own settings category.

## 0.1.20 - 2026-02-21

- Added strict library filtering for continue menus and a background STRM sync progress indicator in the top-right corner.

## 0.1.19 - 2026-02-21

- Added filtered continue menus for audiobooks and podcasts.
- Shortened audiobook labels.
- Added STRM stale-file cleanup with author subfolders.
- Added automatic STRM sync settings.
- Added optional English debug logging.

## 0.1.18 - 2026-02-21

- Completed localization for the new menu model in German and English and removed mixed hardcoded labels.

## 0.1.17 - 2026-02-21

- Added a new API-driven navigation model with audiobook and podcast hubs, personalized home sections, per-library search and stats views.

## 0.1.16 - 2026-02-21

- Improved `Weiterhören` and `Serien fortsetzen` by merging `items-in-progress` with a paged `listening-sessions` fallback and deduplicating unfinished entries.

## 0.1.15 - 2026-02-21

- Fixed series click-through on ABS instances where item references exist only in the entity list payload (`/series`) but not in `/series/{id}`.

## 0.1.14 - 2026-02-21

- Fixed empty series item views by resolving entity detail IDs first and only then using local metadata fallback.

## 0.1.13 - 2026-02-21

- Fixed `Weiterhören` for ABS payloads that only provide `itemId` or `libraryItemId` by resolving item details lazily.

## 0.1.12 - 2026-02-21

- Fixed empty entity menus by adding ABS metadata fallbacks like `seriesName` and `authorName` plus a more robust library-id filter for `Series fortsetzen`.

## 0.1.11 - 2026-02-21

- Rebased on the `0.1.6` functional baseline.
- Added a dedicated server reachability test.
- Added a new addon language setting for Kodi, Deutsch and English.

## 0.1.10 - 2026-02-21

- Added a 502-focused API fallback with GET retry via `?token=` and an auth-test fallback from `/api/authorize` to `/api/me`.

## 0.1.9 - 2026-02-21

- Rolled back to the stable pre-menu-split codebase based on `0.1.2` behavior.

## 0.1.8 - 2026-02-21

- Added a proxy-friendly GET token-query fallback and an `/api/me` auth-test fallback for 502 environments.

## 0.1.7 - 2026-02-21

- Hardened API retry and error handling.
- Made directory failure behavior safer.

## 0.1.6 - 2026-02-21

- Added fully local paginated entity menus for series, authors, narrators and collections.
- Added Kodi 21 compatible music info keys.

## 0.1.5 - 2026-02-21

- Improved entity submenu loading across ABS API variants and paginated fallback matching.

## 0.1.4 - 2026-02-21

- Fixed entity submenu opening fallback.
- Forced the Kodi music player into the foreground on playback start.
- Cache-busted the addon icon path via `abs_icon.png`.

## 0.1.3 - 2026-02-21

- Added ABS-oriented audiobook menus with home sections, series, collections, authors and narrators.

## 0.1.2 - 2026-02-21

- Fixed resume-from-ABS playback start.
- Improved metadata and cover display.

## 0.1.1 - 2026-02-21

- Fixed auth mode parsing for username and password login.

## 0.1.0 - 2026-02-21

- Added the first installable Audiobookshelf addon with login, playback, progress sync and STRM export.
- Replaced the addon icon with the official Audiobookshelf icon.
- Added German and English localization plus a community translation interface.
