from __future__ import annotations

import os
import subprocess
import sys


def test_list_sessions_e2e() -> None:
    env = os.environ.copy()
    env["APPLE_MIDI_SESSIONS_JSON"] = '["Session 1","Studio Network"]'
    result = subprocess.run(
        [sys.executable, "-m", "apple_midi_cli", "list"],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0
    assert result.stdout.splitlines() == ["Session 1", "Studio Network"]
