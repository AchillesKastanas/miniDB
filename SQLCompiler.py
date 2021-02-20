from database import Database
import re
from table import Table

db = Database('SQL', load=False)

db.create_table('classroom', ['building', 'room_number', 'capacity'], [str, str, int], primary_key='room_number')
db.insert('classroom', ['Packard', '101', '500'])
db.insert('classroom', ['Painter', '514', '10'])
db.insert('classroom', ['Taylor', '3128', '70'])
db.insert('classroom', ['Watson', '100', '30'])
db.insert('classroom', ['Watson', '120', '50'])
print('If you want to exit the program type "exit"')
while True:
    userInput = input('Enter your SQL Statement : ')
    list = userInput.split()
    if (userInput == 'exit'):
        break

    if (list[0] == 'select' and 'from' in list and 'where' in list and list.index('where') > 3):
        columns = ''.join(list[i] for i in range(1, list.index('from'))).split(',')
        if ('*' in columns):
            db.select(list[3], '*', list[-1])
        else:
            db.select(list[3], columns, list[-1])
    elif (list[0] == 'update' and list[2] == 'set' and 'where' in list and list.index('where') > 3):
        conditions = re.split(',|=', ''.join(list[i] for i in range(3, list.index('where'))))
        j = 0
        while j < len(conditions):
            db.update(list[1], conditions[j + 1], conditions[j], list[-1])
            j += 2
        db.show_table(list[1])
    elif (list[0] == 'insert' and list[1] == 'into' and list[3] == 'values'):
        values = re.split(',|\(|\)', ''.join(list[i] for i in range(4, len(list))))
        while (i < len(values)):
            if (values[i] == ''):
                values.pop(i)
            else:
                i += 1
        print(values)
        db.insert(list[2], values)
        db.show_table(list[2])
    elif (list[0] == 'delete' and list[1] == 'from' and list[3] == 'where'):
        db.delete(list[2], list[4])
        db.show_table(list[2])
    elif (list[0] == 'create' and list[1] == 'table'):
        columns = re.split(',|\(|\)| ', ' '.join(list[i] for i in range(3, len(list))))
        column_names = []
        column_types = []
        i = 0
        while (i < len(columns)):
            if (columns[i] == ''):
                columns.pop(i)
            else:
                i += 1
        pk_index = 0
        if ('pk' in columns):
            pk_index = columns.index('pk')
            columns.remove('pk')
        for i in range(len(columns)):
            if (i % 2 == 0):
                column_names.append(columns[i])
            else:
                column_types.append(columns[i])
        print(column_names)
        print(column_types)
        for i in column_types:
            if i == 'str':
                column_types.remove(i)
                column_types.insert(column_types.index(i), str)
            elif i == 'int':
                column_types.remove(i)
                column_types.insert(column_types.index(i), int)
            else:
                pass
        print(column_types)
        if (pk_index == 0):
            db.create_table(list[2], column_names, column_types)
        else:
            db.create_table(list[2], column_names, column_types, columns[pk_index - 2])
    elif list[0] == 'create' and list[1] == 'database':
        if not Database(list[2]):
            db1 = Database(list[2], load=False)
        else:
            print('Database already exists')
    elif (list[0] == 'select' and 'from' in list and 'join' in list and 'on' in list):
        if ('inner' in list):
            table1 = list[list.index('from') + 1]
            table2 = list[list.index('join') + 1]
            condition = list[-1]
            db.inner_join(table1, table2, condition, 'innertable1', True)
            columns = ''.join(list[i] for i in range(1, list.index('from'))).split(',')
            if ('*' in columns):
                db.select('innertable1', '*')
            else:
                db.select('innertable1', columns)
        # Η λειτουργία δεν ειναι πλήρως σωστή διότι για να γίνει το select πρέπει να αποθηκευθεί ο πίνακας στην βάση,
        # με αποτέλεσμα να πετάει error την δεύτερη φορά που θα τρέξει.
        # Για την επίλυση αυτου του error χρείαζεται να διαγραφεί ο πίνακας απο την βάση κάτι που δεν μπορεί να
        # πραγματοποιηθεί με την εντολή delete καθώς δεν γνωρίζουμε την συνθήκη που ειναι απαραίτητη
    elif (list[0] == 'create' and list[1] == 'index' and list[3] == 'on'):
        db.create_index(list[4], list[2])
