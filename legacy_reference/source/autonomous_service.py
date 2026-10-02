import threading
import time
import json

from genesis_core import genesis_core


class AutonomousService:

    def save_state(self):
        with open("autonomous_state.json","w") as f:
            json.dump({
                "cycles":self.cycles,
                "interval":self.interval,
                "last_error":self.last_error
            },f)

    def load_state(self):
        try:
            with open("autonomous_state.json") as f:
                d=json.load(f)
                self.cycles=d.get("cycles",0)
                self.interval=d.get("interval",1.0)
                self.last_error=d.get("last_error")
        except:
            pass


    def __init__(self, interval=1.0):
        self.interval = float(interval)
        self.cycles = 0
        self.thread = None
        self.last_error = None

        self._stop = threading.Event()
        self._lock = threading.RLock()
        self.load_state()


    @property
    def running(self):
        return (
            self.thread is not None
            and self.thread.is_alive()
            and not self._stop.is_set()
        )


    def loop(self):

        while not self._stop.is_set():

            started = time.monotonic()

            try:
                with self._lock:
                    genesis_core.tick()
                    self.cycles += 1
                    self.save_state()
                    self.last_error = None

            except Exception as exc:
                with self._lock:
                    self.last_error = (
                        f"{type(exc).__name__}: {exc}"
                    )

                self._stop.set()
                break

            elapsed = time.monotonic() - started
            wait = max(0.0, self.interval - elapsed)

            self._stop.wait(wait)


    def start(self, interval=None):

        with self._lock:

            if interval is not None:
                self.interval = max(
                    0.25,
                    float(interval)
                )

            if self.running:
                return self.status()

            self._stop.clear()

            self.thread = threading.Thread(
                target=self.loop,
                daemon=True,
                name="GenesisAutonomous"
            )

            self.thread.start()

        return self.status()


    def stop(self):

        self._stop.set()

        thread = self.thread

        if (
            thread
            and thread.is_alive()
            and thread is not threading.current_thread()
        ):
            thread.join(
                timeout=max(2.0, self.interval + 1.0)
            )

        return self.status()


    def status(self):

        with self._lock:

            return {
                "running": self.running,
                "cycles": self.cycles,
                "interval_seconds": self.interval,
                "core_cycle": genesis_core.status().get("cycle",0),
                "world": genesis_core.status().get("world",{}),
                "agents": genesis_core.status().get("agents",{}),
                "last_error": self.last_error
            }


autonomous_service = AutonomousService()
