CLI=apple-midi-network-cli

setup:
	uv sync
.PHONY: setup

sync:
	uv sync
.PHONY: sync

run:
	uv run $(CLI) --help
.PHONY: run

lock:
	uv lock
.PHONY: lock
