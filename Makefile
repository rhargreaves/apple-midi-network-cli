CLI=apple-midi-cli

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

swift-demo:
	cd swift/MidiSessionDemo && swift build -c release && .build/release/MidiSessionDemo
.PHONY: swift-demo
