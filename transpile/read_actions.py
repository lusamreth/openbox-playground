with open("Note.txt") as f:
    print(f)
    lines = f.readlines()
    trim_list = list(map(lambda line: line.strip(), lines))

    sig = "-- HERE --"
    sig_indx = trim_list.index(sig)

    pure_inst = trim_list[sig_indx:]
    print(pure_inst)
    res = []
    for p in pure_inst:
        split = p.split(" ", 1)
        if split[0].isdigit():
            res.append(split[1])
    print(res)

Validation = {
    "context": [
        "Frame",
        "Client",
        "Desktop",
        "Root",
        "Titlebar",
        # "Top, Bottom, Left, Right",
        # "TLCorner, TRCorner, BLCorner, BRCorner",
        "Icon",
        "Iconify",
        "Maximize",
        "Close",
        "AllDesktops",
        "Shade",
        "MoveResize",
    ],
    "actions": [
        "Execute",
        "ShowMenu",
        "NextWindow",
        "PreviousWindow",
        "DirectionalCycleWindows",
        "DirectionalTargetWindow",
        "GoToDesktop",
        "AddDesktop",
        "RemoveDesktop",
        "ToggleShowDesktop",
        "ToggleDockAutohide",
        "Reconfigure",
        "Restart",
        "Exit",
        "SessionLogout",
        "Debug",
        "Focus",
        "Raise",
        "Lower",
        "RaiseLower",
        "Unfocus",
        "FocusToBottom",
        "Iconify",
        "Close",
        "ToggleShade",
        "Shade",
        "Unshade",
        "ToggleOmnipresent",
        "ToggleMaximize",
        "Maximize",
        "Unmaximize",
        "ToggleFullscreen",
        "ToggleDecorations",
        "Decorate",
        "Undecorate",
        "SendToDesktop",
        "Move",
        "Resize",
        "MoveResizeTo",
        "MoveRelative",
        "ResizeRelative",
        "MoveToEdge",
        "GrowToEdge",
        "GrowToFill",
        "ShrinkToEdge",
        "If",
        "ForEach",
        "Stop",
        "ToggleAlwaysOnTop",
        "ToggleAlwaysOnBottom",
        "SendToLayer",
    ],
}
