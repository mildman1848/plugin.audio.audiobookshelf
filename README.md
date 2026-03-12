# plugin.audio.audiobookshelf

Kodi-Addon für Audiobookshelf mit Login, Wiedergabe, Fortschritts-Sync und STRM-Export für Hörbücher und Podcasts.

## Struktur

- `plugin.audio.audiobookshelf/`: installierbares Kodi-Addon
- `plugin.audio.audiobookshelf/resources/lib/`: API-, Player- und Hilfslogik
- `scripts/build_release.py`: erzeugt das Release-ZIP unter `dist/`
- `scripts/publish_to_repo.py`: publiziert das Addon nach `mildman1848.github.io`
- `.github/workflows/release-publish.yml`: veröffentlicht nach einem GitHub-Release automatisch in die Kodi-Repo

## Repository-Hygiene

Das Repo enthält dieselbe Grundausstattung wie die anderen eigenständigen Addon-Repos:

- `CHANGELOG.md`, `SECURITY.md`, `CONTRIBUTING.md`
- Issue- und PR-Templates unter `.github/`
- `Dependabot`, `CI`, `CodeQL`, `Security`, `Greetings` und `Stale` Workflows
- Prettier-, Git- und Editor-Konfiguration für konsistente Änderungen
