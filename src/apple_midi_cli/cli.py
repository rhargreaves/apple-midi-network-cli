from __future__ import annotations

from enum import StrEnum
import importlib
import json
import os

import typer

app = typer.Typer(help="Control Apple MIDI network sessions.")


class SessionDirection(StrEnum):
    IN = "in"
    OUT = "out"
    BOTH = "both"


@app.command("list")
def list_sessions() -> None:
    sessions = discover_apple_midi_sessions()
    if not sessions:
        typer.echo("No Apple MIDI sessions found.")
        raise typer.Exit(code=1)
    for session in sessions:
        typer.echo(session)


@app.command()
def create(
    name: str = typer.Argument(..., help="Session name."),
    host: str = typer.Option(..., "--host", "-h", help="Remote host."),
    port: int = typer.Option(5004, "--port", "-p", min=1, max=65535, help="UDP port."),
    direction: SessionDirection = typer.Option(
        SessionDirection.BOTH, "--direction", "-d"
    ),
) -> None:
    typer.echo(
        f"create name={name} host={host} port={port} direction={direction.value}"
    )


@app.command()
def start(name: str = typer.Argument(..., help="Session name.")) -> None:
    typer.echo(f"start name={name}")


@app.command()
def stop(name: str = typer.Argument(..., help="Session name.")) -> None:
    typer.echo(f"stop name={name}")


def main() -> None:
    app()


def discover_apple_midi_sessions() -> list[str]:
    env_payload = os.getenv("APPLE_MIDI_SESSIONS_JSON")
    if env_payload:
        parsed = json.loads(env_payload)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
        raise ValueError("APPLE_MIDI_SESSIONS_JSON must be a JSON array.")

    try:
        mido = importlib.import_module("mido")
    except ModuleNotFoundError:
        return []

    port_names = set(mido.get_input_names()) | set(mido.get_output_names())
    candidates = []
    for port_name in sorted(port_names):
        lowered = port_name.lower()
        if "session" in lowered or "network" in lowered:
            candidates.append(port_name)
    return candidates
