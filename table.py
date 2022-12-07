from terminaltables import DoubleTable

def table(title, data):

    # DoubleTable.
    table_instance = DoubleTable(data, title)
    table_instance.justify_columns[1] = 'center'
    table_instance.justify_columns[2] = 'center'
    table_instance.justify_columns[3] = 'center'
    table_instance.justify_columns[4] = 'center'


    return table_instance.table

