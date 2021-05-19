import sublime
import sublime_plugin


PLUGIN_ENABLED = True


class MoveViewNext(sublime_plugin.WindowCommand):
    def run(self) -> None:
        if not PLUGIN_ENABLED:
            # match the default behavior when not enabled
            self.window.run_command("next_view")
            return

        sheet = self.window.active_sheet()
        if sheet is None:
            return

        # CEV: idx == -1 if there are no sheets in the group
        # for example an empy pane after a split
        group, idx = self.window.get_sheet_index(sheet)
        if group == -1:
            return

        num_groups = self.window.num_groups()
        sheets = self.window.sheets_in_group(group)

        if idx >= 0 and idx < len(sheets) - 1:
            self.window.focus_sheet(sheets[idx + 1])
        elif num_groups == 1:
            if idx > 0:
                self.window.focus_sheet(sheets[0])
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
                sheets = self.window.sheets_in_group(group)
                if len(sheets) > 0:
                    self.window.focus_sheet(sheets[0])
                    return


class MoveViewPrev(sublime_plugin.WindowCommand):
    def run(self) -> None:
        if not PLUGIN_ENABLED:
            # match the default behavior when not enabled
            self.window.run_command("prev_view")
            return

        sheet: sublime.Sheet = self.window.active_sheet()
        if sheet is None:
            return

        group, idx = self.window.get_sheet_index(sheet)
        if group == -1:
            return

        num_groups = self.window.num_groups()
        sheets = self.window.sheets_in_group(group)

        if idx > 0:
            self.window.focus_sheet(sheets[idx - 1])
        elif num_groups == 1:
            idx = len(sheets) - 1
            if idx > 0:
                self.window.focus_sheet(sheets[idx])
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
                sheets = self.window.sheets_in_group(group)
                if len(sheets) > 0:
                    self.window.focus_sheet(sheets[len(sheets) - 1])
                    return


def on_settings_update() -> None:
    global PLUGIN_ENABLED
    enabled = True
    try:
        settings = sublime.load_settings("MoveView.sublime-settings")
        if settings:
            settings.clear_on_change("MoveView")
            settings.add_on_change("MoveView", on_settings_update)
            enabled = settings.get("move_view_enabled") is not False
    except Exception as e:
        raise e
    finally:
        PLUGIN_ENABLED = enabled


def plugin_loaded() -> None:
    on_settings_update()
