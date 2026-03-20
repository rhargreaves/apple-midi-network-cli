from __future__ import annotations

from enum import StrEnum
import importlib
import json
import os

import typer

from . import coremidi_manual

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


@app.command("create-local")
def create_local(
    host: str = typer.Option("localhost", "--host", "-h", help="Remote host."),
    session_port: int = typer.Option(
        5004,
        "--session-port",
        "-s",
        min=1,
        max=65535,
        help="UDP port for the local RTP-MIDI network session.",
    ),
    connection_port: int = typer.Option(
        5006,
        "--connection-port",
        "-p",
        min=1,
        max=65535,
        help="UDP port used for the outbound connection to the remote MIDI host.",
    ),
) -> None:
    create_localhost_session(
        host=host,
        session_port=session_port,
        connection_port=connection_port,
    )
    typer.echo(
        f"Created Apple MIDI network connection to {host}:{connection_port} (session port {session_port})"
    )


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


def create_localhost_session(
    host: str,
    session_port: int,
    connection_port: int,
) -> None:
    if os.getenv("APPLE_MIDI_CREATE_DRY_RUN") == "1":
        return

    coremidi_manual.load()
    core_midi = importlib.import_module("CoreMIDI")
    session = core_midi.MIDINetworkSession.defaultSession()
    if session is None:
        raise RuntimeError("MIDINetworkSession.defaultSession() returned nil")

    session.setEnabled_(True)
    set_network_port = getattr(session, "setNetworkPort_", None)
    if callable(set_network_port):
        set_network_port(session_port)
    midi_host = core_midi.MIDINetworkHost.hostWithName_address_port_(
        f"{host}:{connection_port}", host, connection_port
    )
    connection = core_midi.MIDINetworkConnection.connectionWithHost_(midi_host)
    if not session.addConnection_(connection):
        raise RuntimeError(
            f"Failed to add {host}:{connection_port} MIDI network connection"
        )
