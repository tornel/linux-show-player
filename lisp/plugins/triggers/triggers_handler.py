##########################################
# Copyright 2012-2014 Ceruti Francesco & contributors
#
# This file is part of LiSP (Linux Show Player).
##########################################

from lisp.application import Application
from lisp.core.media_time import MediaTime


class TriggersHandler:

    def __init__(self, media):
        self._media = media
        self._media.on_play.connect(self._on_play)
        self._media.stopped.connect(self._stopped)

        self._media_time = MediaTime(media)
        self._media_time.notify.connect(self._on_notify)

        self._triggers = {}

    def load_triggers(self, conf):
        for position in conf:
            for cue_id in conf[position]:
                cue = Application().layout.get_cue_by_id(cue_id)
                if position in self._triggers:
                    self._triggers[position].append((cue, cue_id))
                else:
                    self._triggers[position] = [(cue, cue_id)]

    def reset_triggers(self):
        self._triggers.clear()

    def finalize(self):
        self._media_time.notify.disconnect(self._on_notify)
        self.reset_triggers()

    def _on_play(self):
        self._execute('Play')

    def _on_notify(self, time):
        self._execute(str(time // 100))

    def _stopped(self):
        self._execute('Stopped')

    def _execute(self, action):
        for n, trigger in enumerate(self._triggers.get(action, [])):
            cue, cue_id = trigger
            if cue is None or cue.is_finalized():
                cue = Application().layout.get_cue_by_id(cue_id)
                self._triggers[action][n] = (cue, cue_id)

            if cue is not None:
                cue.execute()
