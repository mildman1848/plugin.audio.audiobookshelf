# -*- coding: utf-8 -*-
import json

import xbmc

from resources.lib.api import AbsClient
from resources.lib.player import AbsPlayerMonitor
from resources.lib import utils


class PlaybackMonitorService(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        self._last_request = ""

    def run(self):
        utils.debug("Playback monitor service started")
        while not self.abortRequested():
            payload = utils.window_property(utils.MONITOR_REQUEST_PROP, "")
            if payload and payload != self._last_request:
                self._last_request = payload
                self._run_monitor(payload)
            self.waitForAbort(0.5)
        utils.debug("Playback monitor service stopped")

    def _run_monitor(self, payload):
        try:
            data = json.loads(payload)
        except Exception as exc:
            utils.log("Invalid playback monitor payload: %s" % exc, xbmc.LOGWARNING)
            return

        item_id = (data.get("item_id") or "").strip()
        if not item_id:
            return

        try:
            monitor = AbsPlayerMonitor(
                AbsClient(),
                item_id=item_id,
                episode_id=data.get("episode_id") or None,
                resume_time=float(data.get("resume_time") or 0.0),
                track_context=data.get("track_context") or [],
                total_duration=float(data.get("total_duration") or 0.0),
            )
            monitor.run()
        except Exception as exc:
            utils.log("Playback monitor service failed: %s" % exc, xbmc.LOGWARNING)


if __name__ == "__main__":
    PlaybackMonitorService().run()
