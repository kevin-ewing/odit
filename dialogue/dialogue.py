#!/usr/bin/env python
from prompt_toolkit.application import Application
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
def add():
    return "This is doing the adding per usual\n"


def main():
    # The layout.
    search_field = SearchToolbar()  # For reverse search.

    output_field = TextArea(style="class:output-field", text=help_text)
    input_field = TextArea(
        completer=COMMAND_COMPLETER, complete_while_typing=True,
        height=3,
        prompt="odit -> ",
        style="class:input-field",
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
        try:
            if input_field.text == 'add':
                output = add()
            elif input_field.text == 'commit':
                output = "This will do the committing\n"
            elif input_field.text == 'log':
                output = "tThis will pretty print the log for you\n"
            elif input_field.text == 'help':
                output = "This will help you\n"
            elif input_field.text == 'refresh':
                output = "This force refreshes the commits and stuff\n"
            elif input_field.text in ('q', 'quit'):
                output = "quit"
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
    main()