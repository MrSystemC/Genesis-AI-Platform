from __future__ import annotations

import threading
import time
from sqlalchemy import select

from .config import settings
from .database import SessionLocal, World
from .engine import tick_world


class SimulationSupervisor:
    def __init__(self) -> None:
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self.last_error: str | None = None

    @property
    def running(self) -> bool:
        return bool(self._thread and self._thread.is_alive() and not self._stop.is_set())

    def start(self) -> None:
        if not settings.autorun or self.running:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="GenesisSimulationSupervisor", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=3)

    def _loop(self) -> None:
        while not self._stop.wait(max(0.5, settings.tick_interval_seconds)):
            try:
                with SessionLocal() as session:
                    worlds = session.scalars(select(World).where(World.status == "running")).all()
                    for world in worlds:
                        tick_world(session, world, max(1, min(world.speed, 20)))
                self.last_error = None
            except Exception as exc:
                self.last_error = f"{type(exc).__name__}: {exc}"
                time.sleep(1)


supervisor = SimulationSupervisor()
