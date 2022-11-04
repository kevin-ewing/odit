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
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import PathCompleter, merge_completers
from prompt_toolkit.contrib.completers.system import SystemCompleter

from table import table


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
    ],
    ignore_case=True,
)

help_text = """Type your odit command followed by enter to execute. 
Press Control-C or run quit to exit.
"""

def get_git_repo():
    curr_dir = os.getcwd()
    repo = pygit2.Repository(curr_dir)
    return repo 

def get_project_root_dir():
    curr_dir = os.getcwd()
    repo = pygit2.discover_repository(curr_dir)
    return repo[:-5]

def add(text):
    files = text.split()[1:]
    repo = get_git_repo()

    if "." in files:
        repo.index.add_all()
        repo.index.write()
        return "Added all files to to be committed.\n"
    else:
        for temp_file in files:
            repo.index.add(temp_file)
            repo.index.write()

        if len(files) < 3:
            return "Added " + " and ".join(files) + " to to be committed.\n"
        else:
            return "Added " + ", ".join(files[:-1]) + ", and " + files[-1] + " to be committed.\n"
    
def git_current_status():
    status_dict = get_git_repo().status()
    staged = []
    new = []
    deleted = []
    modified = []

    #DEBUGGING
    return_string = ""#str(status_dict) + "\n\n\n"


    #TODO Fix whatever bug this is... changes aren't showing up how we would expect them to
    for file_name, status in status_dict.items():
        if status & 1:
            staged.append(file_name)
        if status & pygit2.GIT_STATUS_WT_DELETED:
            deleted.append(file_name)
        if status & pygit2.GIT_STATUS_WT_MODIFIED:
            modified.append(file_name)
        if status & pygit2.GIT_STATUS_WT_NEW:
            new.append(file_name)

    # return_string = ""
    if len(staged) != 0:
        return_string = return_string + "Staged:\n"
        for i in staged:
            return_string = return_string + "    " + i + "\n"
    if len(new) != 0:
        return_string = return_string + "New:\n"
        for i in new:
            return_string = return_string + "    " + i + "\n"
    if len(modified) != 0:
        return_string = return_string + "Modified:\n"
        for i in modified:
            return_string = return_string + "    " + i + "\n"
    if len(deleted) != 0:
        return_string = return_string + "Deleted:\n"
        for i in deleted:
            return_string = return_string + "    " + i + "\n"
    return return_string


def get_table_data():
    status_dict = get_git_repo().status()
    table_data = [('File Name', 'Changed', 'Added')]

    for file_name, status in status_dict.items():
        if status in GIT_ADDED:
            table_data.append((file_name, "", "X"))
        else:
            table_data.append((file_name, "X", ""))

    return table("File Status", table_data)


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(style="class:output-field", text=help_text)
    tabl = TextArea(style="class:current-status-field", text=get_table_data())
    current_status_field_field = TextArea(style="class:current-status-field", text=git_current_status())
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
            current_status_field_field,
            Window(height=1, char="=", style="class:line"),
            input_field,
            search_field,
        ]
    )

    # Attach accept handler to the input field. We do this by assigning the
    # handler to the `TextArea` that we created earlier. it is also possible to
    # pass it to the constructor of `TextArea`.
    # NOTE: It's better to assign an `accept_handler`, rather then adding a
    #       custom ENTER key binding. This will automatically reset the input
    #       field and add the strings to the history.
    def accept(buff):
        # Evaluate "calculator" expression.
        command = input_field.text.split()[0]

        try:
            if command == 'add':
                output = add(input_field.text)
            elif command == 'commit':
                output = "This will do the committing\n"
            elif command == 'log':
                output = "tThis will pretty print the log for you\n"
            elif command == 'help':
                output = "This will help you\n"
            elif command == 'refresh':
                output = "This force refreshes the commits and stuff\n"
            elif command in ('q', 'quit'):
                output = "quit"
                get_app().exit()
            else:
                output = "Not a valid odit command, type help for more information\n"
        except BaseException as e:
            output = f"{e}"
            
        
        # Add text to output buffer.
        output_field.buffer.document = Document(
            text=output, cursor_position=len(output)
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
    dir = get_project_root_dir()
    os.chdir(dir)
    main()