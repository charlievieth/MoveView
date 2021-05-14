# MoveView

MoveView is a [Sublime Text 4](http://sublimetext.com/) plugin that adds two
[Window](https://www.sublimetext.com/docs/3/api_reference.html#sublime_plugin.WindowCommand)
commands (`move_view_next` and `move_view_prev`) that replicate the behavior of
the Sublime Text 3's `next_view` and `prev_view` which move the focus to the
next group (window pane) instead of wrapping the current group.

By default on OSX `"super+shift+["` and `"super+shift+]"` are remapped to use
`move_view_next` and `move_view_prev`.

### Usage

Add the following to your keymap:
```json
[
	{ "keys": ["super+shift+["], "command": "move_view_prev" },
	{ "keys": ["super+shift+]"], "command": "move_view_next" }
]
```
