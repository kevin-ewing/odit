#!/usr/bin/env python
import os
import pygit2

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import SearchToolbar, TextArea
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.layout.containers import (
    HorizontalAlign,
    HSplit,
    VerticalAlign,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter, merge_completers
from prompt_toolkit.contrib.completers.system import SystemCompleter

from table import table
import commands


GIT_ADDED = {
            pygit2.GIT_STATUS_INDEX_NEW, 
            pygit2.GIT_STATUS_INDEX_MODIFIED,
            pygit2.GIT_STATUS_INDEX_DELETED,
            pygit2.GIT_STATUS_INDEX_RENAMED,
            pygit2.GIT_STATUS_INDEX_TYPECHANGE
            }


COMMAND_COMPLETER = WordCompleter(
    [
        "help",
        "add",
        "commit",
        "quit",
        "log",
        "push",
        "pull",
        "refresh",
        "summarize",
        "summary"
        
    ],
    ignore_case=True,
)

help_text = """Type your odit command followed by enter to execute. 
Press Control-C or run quit to exit.
"""


def get_table_data():
    status_dict = commands.get_git_repo().status()
    table_data = [('File Name', 'New', 'Deleted', 'Changed', 'Added')]

    for file_name, status in status_dict.items():
        if status in GIT_ADDED:
            if status == pygit2.GIT_STATUS_INDEX_NEW:
                table_data.append((file_name, "X", "", "", "X"))
            elif status == pygit2.GIT_STATUS_INDEX_DELETED:
                table_data.append((file_name, "", "X", "", "X"))
            else:
                table_data.append((file_name, "", "", "", "X"))
        else:
            if status & pygit2.GIT_STATUS_WT_NEW:
                table_data.append((file_name, "X", "", "X", ""))
            elif status & pygit2.GIT_STATUS_INDEX_DELETED:
                table_data.append((file_name, "", "X", "X", ""))
            else:
                table_data.append((file_name, "", "", "X", ""))

    return table("File Status", table_data)


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(style="class:output-field", text=help_text)
    tabl = TextArea(style="class:current-status-field", text=get_table_data())
    input_field = TextArea(
        completer= merge_completers([SystemCompleter(), COMMAND_COMPLETER]),
        complete_while_typing=True,
        auto_suggest=AutoSuggestFromHistory(),
        height=1,
        prompt="odit -> ",
        style="class:input-field",
        multiline=False,
        wrap_lines=False,
        search_field=search_field,
    )

    container = HSplit(
        [
            Window(height=1, char="=", style="class:line"),
            Window(FormattedTextControl(HTML("<u>the open dialogue for git</u>")),
                    ignore_content_width=True,
                    align=WindowAlign.CENTER,
                    height=1),
            Window(height=1, char="=", style="class:line"),
            output_field,
            tabl,
            Window(height=1, char="=", style="class:line"),
            input_field,
            search_field,
        ]
    )

    def accept(buff):
        # Evaluate "calculator" expression.
        command = input_field.text.split()[0]

        try:
            if command == 'add':
                output = commands.add(input_field.text)
            elif command == 'commit':
                output = commands.commit(input_field.text)
            elif command == 'log':
                output = commands.log()
            elif command == 'help':
                output = commands.help()
            elif command == 'refresh':
                output = "Force refreshed commits\n"
            elif command in ('summary', 'summarize'):
                output = commands.summarize()
            elif command == 'clear':
                output = ""
            elif command == 'push':
                output = commands.push(input_field.text)
            elif command == 'pull':
                output = commands.pull(input_field.text)
            elif command in ('q', 'quit', 'exit'):
                output = "quit"
                get_app().exit()
            else:
                output = "Not a valid odit command, type help for more information"
        except BaseException as e:
            output = f"{e}"
            
        
        # Add text to output buffer.
        output_field.buffer.document = Document(
            text=output, cursor_position=len(output)
        )

        tabl.buffer.document = Document(
            text=get_table_data(), cursor_position=len(output)
        )


    input_field.accept_handler = accept

    # The key bindings.
    kb = KeyBindings()

    @kb.add("c-c")
    @kb.add("c-q")
    def _(event):
        "Pressing Ctrl-Q or Ctrl-C will exit the user interface."
        event.app.exit()

    # Style.
    style = Style(
        [
            ("output-field", "bg:#30363d #f85149"),
            ("input-field", "bg:#000000 #ffffff"),
            ("current-status-field", "bg:#30363d #ffffff"),
            ("line", "#fa7a18"),
        ]
    )
    
    # Run application.
    application = Application(
        layout=Layout(container, focused_element=input_field),
        key_bindings=kb,
        style=style,
        mouse_support=True,
        full_screen=True,
    )

    application.run()
    


if __name__ == "__main__":
    dir = commands.get_project_root_dir()
    os.chdir(dir)
    main()