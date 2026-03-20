# Apple MIDI CLI

CLI for automating the setup of Apple MIDI Network Sessions

## Audio MIDI Setup (AX)

Observed `kAXIdentifier` values (macOS build may change private `_NS:` ids):

| UI | Identifier |
| --- | --- |
| List of sessions | `_NS:467` |
| List of session & directories | `_NS:150` |
| Connect button | `_NS:33` |
| Disconnect | `_NS:58` |
| List of participants | `_NS:387` |

## Getting Started

1. Install dependencies:

```bash
make setup
```

## Release

Tag a version (for example `v0.1.0`) and push the tag.