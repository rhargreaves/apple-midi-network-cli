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


def test_create_local_e2e() -> None:
    env = os.environ.copy()
    env["APPLE_MIDI_CREATE_DRY_RUN"] = "1"
    result = subprocess.run(
        [sys.executable, "-m", "apple_midi_cli", "create-local"],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0
    assert (
        result.stdout.strip()
        == "Created Apple MIDI network connection to localhost:5006 (session port 5004)"
    )


def test_create_local_custom_args_e2e() -> None:
    env = os.environ.copy()
    env["APPLE_MIDI_CREATE_DRY_RUN"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "apple_midi_cli",
            "create-local",
            "--host",
            "127.0.0.1",
            "--connection-port",
            "6000",
        ],
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0
    assert (
        result.stdout.strip()
        == "Created Apple MIDI network connection to 127.0.0.1:6000 (session port 5004)"
    )
