# -*- coding: utf-8 -*-
import time

import xbmc

from resources.lib import utils


class AbsPlayerMonitor(xbmc.Monitor):
    def __init__(self, api, item_id, episode_id=None, resume_time=0.0, track_context=None, total_duration=0.0):
        super().__init__()
        self.api = api
        self.item_id = item_id
        self.episode_id = episode_id
        self.resume_time = float(max(0.0, resume_time or 0.0))
        self.player = xbmc.Player()
        self.interval = max(5, int(utils.ADDON.getSetting("progress_sync_interval") or "30"))
        self.finished_threshold = max(50, min(100, int(utils.ADDON.getSetting("mark_finished_threshold") or "97")))
        self._resume_applied = False
        self._last_current_time = self.resume_time
        self._last_total_time = float(max(0.0, total_duration or 0.0))
        self._track_context = track_context or []
        self._current_track = self._find_track_by_time(self.resume_time)

    @staticmethod
    def _normalize_path(path):
        return (path or "").strip()

    def _find_track_by_time(self, current_time):
        if not self._track_context:
            return None
        current_time = float(max(0.0, current_time or 0.0))
        fallback = self._track_context[0]
        for track in self._track_context:
            start = float(track.get("start", 0.0) or 0.0)
            duration = float(track.get("duration", 0.0) or 0.0)
            end = start + duration if duration > 0 else start
            if current_time >= start:
                fallback = track
            if duration > 0 and start <= current_time < end:
                return track
        return fallback

    def _find_current_track(self):
        if not self._track_context:
            return None
        playing_file = self._normalize_path(getattr(self.player, "getPlayingFile", lambda: "")())
        for track in self._track_context:
            if self._normalize_path(track.get("path")) == playing_file:
                return track
        return self._current_track or self._find_track_by_time(self._last_current_time)

    def _combined_position(self):
        current_time = float(self.player.getTime() or 0.0)
        total_time = float(self.player.getTotalTime() or 0.0)
        track = self._find_current_track()
        if not track:
            return current_time, total_time

        self._current_track = track
        start = float(track.get("start", 0.0) or 0.0)
        track_duration = float(track.get("duration", 0.0) or 0.0)
        combined_current = max(0.0, start + current_time)
        combined_total = self._last_total_time
        if combined_total <= 0:
            combined_total = float(track.get("total", 0.0) or 0.0)
        if combined_total <= 0:
            combined_total = start + max(track_duration, total_time)
        return combined_current, combined_total

    def run(self):
        utils.debug("Player monitor started for item_id=%s episode_id=%s" % (self.item_id, self.episode_id or ""))
        started = time.time()
        # Wait up to 15s for playback to start.
        while not self.abortRequested() and (time.time() - started) < 15:
            if self.player.isPlayingAudio():
                break
            self.waitForAbort(0.2)

        last_sync = 0
        last_playing = time.time()
        while not self.abortRequested():
            playing = self.player.isPlayingAudio()
            if playing:
                last_playing = time.time()
            elif (time.time() - last_playing) > 3.0:
                break
            if not self._resume_applied and self.resume_time > 0:
                try:
                    seek_target = self.resume_time
                    if self._track_context:
                        track = self._find_track_by_time(self.resume_time)
                        if track:
                            self._current_track = track
                            seek_target = max(0.0, self.resume_time - float(track.get("start", 0.0) or 0.0))
                    if float(self.player.getTime() or 0.0) < max(1.0, seek_target - 2.0):
                        self.player.seekTime(seek_target)
                    self._resume_applied = True
                except Exception as exc:
                    utils.log("Initial resume seek failed: %s" % exc, xbmc.LOGWARNING)
            now = time.time()
            if playing and now - last_sync >= self.interval:
                self.sync_progress(False)
                last_sync = now
            self.waitForAbort(0.5)

        # Final sync when playback stops.
        self.sync_progress(True)
        utils.debug("Player monitor stopped for item_id=%s" % self.item_id)

    def sync_progress(self, final):
        try:
            if not self.player.isPlayingAudio() and not final:
                return
            if final and not self.player.isPlayingAudio():
                current_time = float(self._last_current_time or 0.0)
                total_time = float(self._last_total_time or 0.0)
            else:
                current_time, total_time = self._combined_position()
                self._last_current_time = max(self._last_current_time, current_time)
                self._last_total_time = max(self._last_total_time, total_time)
            is_finished = False
            if total_time > 0:
                is_finished = (current_time / total_time) * 100.0 >= self.finished_threshold
            self.api.patch_progress(
                item_id=self.item_id,
                episode_id=self.episode_id,
                current_time=current_time,
                duration=total_time,
                is_finished=is_finished,
            )
            utils.debug(
                "Progress synced item_id=%s episode_id=%s current=%.2f duration=%.2f finished=%s final=%s"
                % (self.item_id, self.episode_id or "", current_time, total_time, is_finished, final)
            )
        except RuntimeError as exc:
            if final:
                utils.debug("Skipping final progress sync after playback stop: %s" % exc)
                return
            utils.log("Progress sync failed: %s" % exc, xbmc.LOGWARNING)
        except Exception as exc:
            utils.log("Progress sync failed: %s" % exc, xbmc.LOGWARNING)
