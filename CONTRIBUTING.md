# Contributing to plugin.audio.audiobookshelf

Deutsch: [CONTRIBUTING.DE.md](CONTRIBUTING.DE.md)

## Before opening a pull request

- Keep changes focused on the Audiobookshelf addon or its release automation.
- Follow the PR template.
- Link the related issue when applicable with `closes #<number>`.
- Update `README.md`, `CHANGELOG.md` or docs/localization when behavior changes.
- If you touch publishing logic, verify both this source repo and the `mildman1848.github.io` publish flow.

## Files of interest

| File                                     | Purpose                                           |
| ---------------------------------------- | ------------------------------------------------- |
| `plugin.audio.audiobookshelf/`           | Kodi plugin addon payload                         |
| `plugin.audio.audiobookshelf/main.py`    | Entry point for routing, menus and playback       |
| `plugin.audio.audiobookshelf/resources/` | API, player, i18n and settings files              |
| `scripts/build_release.py`               | Builds the addon ZIP                              |
| `scripts/publish_to_repo.py`             | Publishes the addon into the Kodi repository repo |
| `.github/workflows/release-publish.yml`  | Cross-repo release publishing                     |

## Local validation

- `python3 -m py_compile $(find . -path './.git' -prune -o -path './node_modules' -prune -o -path './dist' -prune -o -path '*/__pycache__/*' -prune -o -name '*.py' -print)`
- `xmllint --noout plugin.audio.audiobookshelf/addon.xml plugin.audio.audiobookshelf/resources/settings.xml`
- `python3 scripts/build_release.py`
- `python3 scripts/publish_to_repo.py --publish-repo /path/to/mildman1848.github.io`
