from terminaltables import AsciiTable, DoubleTable, SingleTable

TABLE_DATA = (
    ('Files', 'Changed', 'Added'),
    ('file1','', 'X'),
    ('file2', 'X', ''),
)

title = 'Files'

def table(self, title, data):

    # AsciiTable.
    table_instance = AsciiTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()

    # SingleTable.
    table_instance = SingleTable(TABLE_DATA, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()

    # DoubleTable.
    table_instance = DoubleTable(TABLE_DATA, title)
    table_instance.justify_columns[1,2] = 'center'
    print(table_instance.table)
    print()

"""Simple example usage of terminaltables without any other dependencies.
Just prints sample text and exits.
"""

#gitpython to parse and see what changed
#repo.untracked files or something
#git add function
