# Changelog

English: [CHANGELOG.md](CHANGELOG.md)

Alle wichtigen Änderungen an `plugin.audio.audiobookshelf` werden in dieser Datei dokumentiert.

## Unveröffentlicht

## 0.1.41 - 2026-03-20

- Erkennung mehrteiliger Hörbücher für Server behoben, die die vollständige Track-Liste erst in der ABS-`/play`-Antwort statt schon in `item.media.tracks` liefern.
- Zusätzliche Debug-Ausgabe zur Track-Erkennung ergänzt, damit im Kodi-Log sichtbar ist, ob ein ausgewähltes Hörbuch als Mehrteiler erkannt wurde.

## 0.1.40 - 2026-03-20

- Fallback im Wiedergabe-Monitor für mehrteilige Hörbücher ergänzt, der nach einer beendeten Teil-Datei explizit die nächste ABS-Datei startet, wenn Kodi nicht selbst weiterschaltet.

## 0.1.39 - 2026-03-20

- Streaming-Wiedergabe für mehrteilige Hörbücher behoben, indem Kodi nun eine Playlist über alle ABS-Track-Dateien aufbaut, statt nach Ende der ersten Teil-Datei zu stoppen.
- Fortschrittssynchronisierung für playlistbasierte Hörbuch-Wiedergabe angepasst, damit Resume-Position und Fertig-Status weiterhin auf der gesamten Hörbuch-Zeitleiste basieren.

## 0.1.38 - 2026-03-19

- Fehlendes Cover während der aktiven Wiedergabe behoben, indem das Audiobookshelf-Artwork nun auch an das aufgelöste Kodi-Player-Item übergeben wird.
- Zusätzliche, wiedergabespezifische Musik-Artwork-Felder und reichhaltigere Metadaten für aufgelöste Player-Items ergänzt, damit Kodi das Hörbuch-Cover auch nach dem Start der Wiedergabe sichtbar hält.
