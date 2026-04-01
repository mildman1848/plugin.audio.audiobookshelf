# Changelog

English: [CHANGELOG.md](CHANGELOG.md)

Alle wichtigen Änderungen an `plugin.audio.audiobookshelf` werden in dieser Datei dokumentiert.

## Unveröffentlicht

## 0.1.47 - 2026-04-01

- Resume-Zuverlässigkeit bei der Hörbuchwiedergabe behoben, indem Fortschrittspositionen aus personalisierten/Weiterhören-Listen erhalten und an die Play-Route weitergereicht werden.
- Fortschrittsauswertung robuster gemacht: Der Fallback für Resume-Positionen unterstützt jetzt mehrere Audiobookshelf-Antwortformate (inklusive verschachtelter Progress-Objekte und Millisekunden-Felder).

## 0.1.45 - 2026-03-28

- Einzeldatei-Hörbücher im `.m4b`-Format korrigiert: Das Addon bevorzugt jetzt die ABS-`/play`-Streamdaten und die echte Single-Track-`ino` statt der nicht abspielbaren Library-Root-`ino`, die in Kodi zu `404` führte.
- Start mehrteiliger Hörbücher überarbeitet: Kodi bekommt jetzt ein korrekt aufgelöstes Abspiel-Item für den gewählten Track statt einer direkten Playlist-Übergabe aus der Plugin-Route, wodurch die wiederholten `GetDirectory`-Fehler und die hängenbleibende Ladeanimation beim Start entfallen.
- Die Fortschrittsüberwachung in einen Hintergrund-Service verschoben, damit Kodi nicht mehr auf einen aus der Plugin-Route gestarteten Monitor-Thread wartet und doppelte Monitor-Instanzen mit fehlerhafter Mehrtrack-Synchronisierung ausbleiben.

## 0.1.44 - 2026-03-28

- `Podcasts -> Weiterhören` und `Hörbücher -> Weiterhören` korrigiert: Beide Routen behalten jetzt ihren Bibliotheks- und Medientyp-Filter, statt auf die globale gemischte Continue-Liste zurückzufallen.
- HTTP-Retries für ABS-API-Aufrufe ergänzt, damit das Addon temporäre DNS- oder Verbindungsfehler in Kodi-/Flatpak-Umgebungen besser übersteht.
- Den Start von Mehrdateien-Hörbüchern korrigiert: Der initiale Resume-Seek läuft jetzt erst, wenn Kodi tatsächlich Audio wiedergibt, wodurch die wiederholten Warnungen `Kodi is not playing any media file` beim Start entfallen.
- Audiobookshelf-Netzwerk- und DNS-Fehler in `AbsApiError` gekapselt, damit temporäre Verbindungsprobleme als kontrollierte Addon-Fehler statt als rohe unhandled exceptions im Kodi-Log erscheinen.

## 0.1.43 - 2026-03-24

- Bibliotheksfilterung behoben, damit Podcast-Einträge nicht mehr in Hörbuch-Ansichten oder gefilterten "Weiterhören"-Listen auftauchen.
- Unnötige ABS-`/play`-Aufrufe bei direkter Einzeldatei-Wiedergabe vermieden, wodurch serverseitige Direct-Play-/MIME-Fehler bei manchen FLAC-Titeln ausbleiben.
- Resume-Wiedergabe für mehrteilige Hörbücher robuster gemacht, indem fehlerhafte Track-Offsets normalisiert und der Wiedergabe-Monitor asynchron gestartet wird, um hängenbleibende Ladeanzeige und absturzanfällige Fortsetzungen zu vermeiden.

## 0.1.42 - 2026-03-20

- Erkennung mehrteiliger Hörbücher für ABS-Antworten behoben, bei denen die echten Teil-Dateien unter `libraryItem.media.tracks` und `media.audioFiles` liegen, währen die oberste `/play`-Antwort nur einen einzelnen zusammengeführten HLS-Stream ausweist.
- Direkten Fallback für dateibasierte Wiedergabe-URLs aus Track-/Datei-Inodes ergänzt, wenn ABS auf der Item-Seite kein `contentUrl` pro Teil-Datei mitliefert.

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
