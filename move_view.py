import sublime
import sublime_plugin


class MoveViewNext(sublime_plugin.WindowCommand):
    def run(self) -> None:
        sheet = self.window.active_sheet()
        if sheet is None:
            return

        group, idx = self.window.get_sheet_index(sheet)
        if group == -1 or idx == -1:
            return

        num_groups = self.window.num_groups()
        sheets = self.window.sheets_in_group(group)

        if idx < len(sheets) - 1:
            self.window.focus_sheet(sheets[idx + 1])
        elif num_groups == 1:
            if idx != 0:
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
        sheet: sublime.Sheet = self.window.active_sheet()
        if sheet is None:
            return

        group, idx = self.window.get_sheet_index(sheet)
        if group == -1 or idx == -1:
            return

        num_groups = self.window.num_groups()
        sheets = self.window.sheets_in_group(group)

        if idx > 0:
            self.window.focus_sheet(sheets[idx - 1])
        elif num_groups == 1:
            idx = len(sheets) - 1
            if idx != 0:
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
