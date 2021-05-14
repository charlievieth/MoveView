import sublime
import sublime_plugin

PLUGIN_ENABLED = True


def view_next(window: sublime.Window) -> None:
    sheet = window.active_sheet()
    if sheet is None:
        return

    group, idx = window.get_sheet_index(sheet)
    if group == -1 or idx == -1:
        return

    num_groups = window.num_groups()
    sheets = window.sheets_in_group(group)

    if idx < len(sheets) - 1:
        window.focus_sheet(sheets[idx + 1])
    elif num_groups == 1:
        if idx != 0:
            window.focus_sheet(sheets[0])
    else:
        # search through the groups to the right then end
        # on our original group
        #
        # num_groups = 5
        # active_group = 2
        #  => [3, 4, 0, 1, 2]
        #
        groups = list(range(group + 1, num_groups))
        groups += list(range(0, group + 1))
        for group in groups:
            sheets = window.sheets_in_group(group)
            if len(sheets) > 0:
                window.focus_sheet(sheets[0])


def view_prev(window: sublime.Window) -> None:
    sheet: sublime.Sheet = window.active_sheet()
    if sheet is None:
        return

    group, idx = window.get_sheet_index(sheet)
    if group == -1 or idx == -1:
        return

    num_groups = window.num_groups()
    sheets = window.sheets_in_group(group)

    if idx > 0:
        window.focus_sheet(sheets[idx - 1])
    elif num_groups == 1:
        idx = len(sheets) - 1
        if idx != 0:
            window.focus_sheet(sheets[idx])
    else:
        # search through the groups to the left then end
        # on our original group
        #
        # num_groups = 5
        # active_group = 2
        #  => [1, 0, 4, 3, 2]
        #
        groups = list(range(group - 1, -1, -1))
        groups += list(range(num_groups - 1, group - 1, -1))
        for group in groups:
            sheets = window.sheets_in_group(group)
            if len(sheets) > 0:
                window.focus_sheet(sheets[len(sheets) - 1])


class MoveViewNext(sublime_plugin.WindowCommand):
    __slots__ = "window"

    def run(self) -> None:
        if PLUGIN_ENABLED:
            view_next(self.window)
        else:
            self.window.run_command("next_view")


class MoveViewPrev(sublime_plugin.WindowCommand):
    __slots__ = "window"

    def run(self) -> None:
        if PLUGIN_ENABLED:
            view_prev(self.window)
        else:
            self.window.run_command("prev_view")


def on_settings_update() -> None:
    global PLUGIN_ENABLED
    settings = sublime.load_settings("MoveView.sublime-settings")
    if settings:
        PLUGIN_ENABLED = settings.get("move_view_enabled") is not False


def init_settings() -> None:
    settings = sublime.load_settings("MoveView.sublime-settings")
    settings.add_on_change("MoveView", on_settings_update)


def plugin_loaded() -> None:
    init_settings()
    on_settings_update()
