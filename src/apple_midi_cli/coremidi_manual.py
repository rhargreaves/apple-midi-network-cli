from __future__ import annotations

import ctypes
import ctypes.util

OSStatus = ctypes.c_int32
UInt32 = ctypes.c_uint32
ByteCount = ctypes.c_uint64
MIDITimeStamp = ctypes.c_uint64

_lib: ctypes.CDLL | None = None


def _core_midi_path() -> str:
    path = ctypes.util.find_library("CoreMIDI")
    if not path:
        raise OSError("CoreMIDI framework not found")
    return path


def load() -> ctypes.CDLL:
    global _lib
    if _lib is not None:
        return _lib
    lib = ctypes.CDLL(_core_midi_path())
    lib.MIDIDeviceCreate.argtypes = [
        UInt32,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.POINTER(UInt32),
    ]
    lib.MIDIDeviceCreate.restype = OSStatus
    lib.MIDIDriverEnableMonitoring.argtypes = [UInt32, ctypes.c_uint8]
    lib.MIDIDriverEnableMonitoring.restype = OSStatus
    lib.MIDIEventListInit.argtypes = [ctypes.c_void_p, UInt32]
    lib.MIDIEventListInit.restype = ctypes.c_void_p
    lib.MIDIEventListAdd.argtypes = [
        ctypes.c_void_p,
        ByteCount,
        ctypes.c_void_p,
        MIDITimeStamp,
        ByteCount,
        ctypes.c_void_p,
    ]
    lib.MIDIEventListAdd.restype = ctypes.c_void_p
    lib.MIDIPacketListInit.argtypes = [ctypes.c_void_p]
    lib.MIDIPacketListInit.restype = ctypes.c_void_p
    lib.MIDIPacketListAdd.argtypes = [
        ctypes.c_void_p,
        ByteCount,
        ctypes.c_void_p,
        MIDITimeStamp,
        ByteCount,
        ctypes.c_void_p,
    ]
    lib.MIDIPacketListAdd.restype = ctypes.c_void_p
    lib.MIDIReceived.argtypes = [UInt32, ctypes.c_void_p]
    lib.MIDIReceived.restype = OSStatus
    lib.MIDIReceivedEventList.argtypes = [UInt32, ctypes.c_void_p]
    lib.MIDIReceivedEventList.restype = OSStatus
    lib.MIDISend.argtypes = [UInt32, UInt32, ctypes.c_void_p]
    lib.MIDISend.restype = OSStatus
    lib.MIDISendEventList.argtypes = [UInt32, UInt32, ctypes.c_void_p]
    lib.MIDISendEventList.restype = OSStatus
    lib.MIDISendSysex.argtypes = [ctypes.c_void_p]
    lib.MIDISendSysex.restype = OSStatus
    _lib = lib
    return lib
