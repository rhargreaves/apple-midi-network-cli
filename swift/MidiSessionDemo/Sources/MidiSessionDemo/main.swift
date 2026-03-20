import AppKit
import ApplicationServices
import Foundation

NSApplication.shared.setActivationPolicy(.accessory)

let amsBundleId = "com.apple.audio.AudioMIDISetup"
let amsPath = "/System/Applications/Utilities/Audio MIDI Setup.app"

let listSessionsId = "_NS:467"
let listSessionsAndDirectoriesId = "_NS:150"
let connectButtonId = "_NS:33"
let disconnectId = "_NS:58"
let listParticipantsId = "_NS:387"

func axString(_ element: AXUIElement, _ attr: String) -> String {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, attr as CFString, &ref) == .success else { return "" }
    if let s = ref as? String { return s }
    if let a = ref as? NSAttributedString { return a.string }
    if let n = ref as? NSNumber { return n.stringValue }
    return ""
}

func axChildren(_ element: AXUIElement) -> [AXUIElement] {
    var ref: CFTypeRef?
    guard AXUIElementCopyAttributeValue(element, kAXChildrenAttribute as CFString, &ref) == .success else { return [] }
    guard let arr = ref as? [AXUIElement] else { return [] }
    return arr
}

func axRole(_ element: AXUIElement) -> String {
    axString(element, kAXRoleAttribute as String)
}

func axTitle(_ element: AXUIElement) -> String {
    axString(element, kAXTitleAttribute as String)
}

func axValue(_ element: AXUIElement) -> String {
    axString(element, kAXValueAttribute as String)
}

func axIdentifier(_ element: AXUIElement) -> String {
    axString(element, kAXIdentifierAttribute as String)
}

func findByIdentifier(_ root: AXUIElement, identifier: String) -> AXUIElement? {
    if axIdentifier(root) == identifier {
        return root
    }
    for c in axChildren(root) {
        if let f = findByIdentifier(c, identifier: identifier) {
            return f
        }
    }
    return nil
}

func rowTextParts(_ element: AXUIElement) -> [String] {
    var out: [String] = []
    let role = axRole(element)
    if role == "AXStaticText" || role == "AXTextField" {
        let v = axValue(element)
        let t = axTitle(element)
        let s = v.isEmpty ? t : v
        if !s.isEmpty {
            out.append(s)
        }
    } else if role == "AXCheckBox" {
        let v = axValue(element)
        if !v.isEmpty {
            out.append("checkbox=\(v)")
        }
    }
    for c in axChildren(element) {
        out.append(contentsOf: rowTextParts(c))
    }
    return out
}

func rowsInTable(_ table: AXUIElement) -> [AXUIElement] {
    var rows: [AXUIElement] = []
    for c in axChildren(table) {
        if axRole(c) == "AXRow" {
            rows.append(c)
        }
    }
    if rows.isEmpty {
        for c in axChildren(table) {
            for cc in axChildren(c) {
                if axRole(cc) == "AXRow" {
                    rows.append(cc)
                }
            }
        }
    }
    return rows
}

func printTableTextLines(_ table: AXUIElement, heading: String) {
    print(heading)
    let rows = rowsInTable(table)
    if rows.isEmpty {
        print("  (no rows)")
        return
    }
    for row in rows {
        let parts = rowTextParts(row)
        if parts.isEmpty {
            print("  (row without text)")
        } else {
            print("  \(parts.joined(separator: " | "))")
        }
    }
}

func printButtonText(_ button: AXUIElement, heading: String) {
    print(heading)
    let t = axTitle(button)
    let v = axValue(button)
    let s = t.isEmpty ? v : t
    if s.isEmpty {
        print("  (no title)")
    } else {
        print("  \(s)")
    }
}

print("=== launch Audio MIDI Setup ===")
if let url = NSWorkspace.shared.urlForApplication(withBundleIdentifier: amsBundleId) {
    NSWorkspace.shared.open(url)
} else {
    NSWorkspace.shared.open(URL(fileURLWithPath: amsPath, isDirectory: true))
}

var pid: pid_t = 0
for _ in 0 ..< 50 {
    if let app = NSRunningApplication.runningApplications(withBundleIdentifier: amsBundleId).first {
        pid = app.processIdentifier
        break
    }
    Thread.sleep(forTimeInterval: 0.1)
}

guard pid != 0 else {
    print("error could not find running app bundle=\(amsBundleId)")
    exit(1)
}

print("Audio MIDI Setup pid=\(pid)")
Thread.sleep(forTimeInterval: 1.5)

let appAX = AXUIElementCreateApplication(pid)
var windowsRef: CFTypeRef?
guard AXUIElementCopyAttributeValue(appAX, kAXWindowsAttribute as CFString, &windowsRef) == .success,
    let windows = windowsRef as? [AXUIElement],
    !windows.isEmpty
else {
    print("error no AX windows (grant Accessibility to Terminal/Cursor/your runner)")
    exit(1)
}

print("")
print("=== AMS text (windows=\(windows.count)) ===")
print("")
if let el = findByIdentifier(appAX, identifier: listSessionsId) {
    printTableTextLines(el, heading: "sessions (\(listSessionsId))")
} else {
    print("sessions (\(listSessionsId))")
    print("  (not found)")
}
print("")
if let el = findByIdentifier(appAX, identifier: listSessionsAndDirectoriesId) {
    printTableTextLines(el, heading: "sessions & directories (\(listSessionsAndDirectoriesId))")
} else {
    print("sessions & directories (\(listSessionsAndDirectoriesId))")
    print("  (not found)")
}
print("")
if let el = findByIdentifier(appAX, identifier: connectButtonId) {
    printButtonText(el, heading: "connect (\(connectButtonId))")
} else {
    print("connect (\(connectButtonId))")
    print("  (not found)")
}
print("")
if let el = findByIdentifier(appAX, identifier: disconnectId) {
    printButtonText(el, heading: "disconnect (\(disconnectId))")
} else {
    print("disconnect (\(disconnectId))")
    print("  (not found)")
}
print("")
if let el = findByIdentifier(appAX, identifier: listParticipantsId) {
    printTableTextLines(el, heading: "participants (\(listParticipantsId))")
} else {
    print("participants (\(listParticipantsId))")
    print("  (not found)")
}
