from copy import deepcopy


class Database:
    def __init__(self, copy_from=None):
        self.storage = deepcopy(copy_from.storage) if copy_from else {}

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value):
        self.storage[key] = value

    def unset(self, key):
        del self.storage[key]

    def counts(self, value):
        return list(self.storage.values()).count(value)

    def find(self, value):
        return [k for k, v in self.storage.items() if value == v]


db = Database()


def prepare_value(value: str):
    if value.isdigit():
        value = int(value)
    return value


def exec_db_commands(cmd):
    if len(cmd) == 0:
        print()
    elif cmd[0] == 'GET':
        res = db.get(key=cmd[1])
        print(res)
    elif cmd[0] == 'SET':
        db.set(key=cmd[1], value=prepare_value(cmd[2]))
        print()
    elif cmd[0] == 'UNSET':
        db.unset(key=cmd[1])
        print()
    elif cmd[0] == 'COUNTS':
        value_counts = db.counts(value=prepare_value(cmd[1]))
        print(value_counts)
    elif cmd[0] == 'FIND':
        value_keys = db.find(value=prepare_value(cmd[1]))
        print(value_keys)
    else:
        print('ERROR: [WRONG COMMAND]')


def transaction():
    global db
    db_snapshot = deepcopy(db)
    while True:
        row = input('>>: ').strip()
        split_row = row.split()
        if len(split_row) == 0:
            print()
        elif split_row[0] == 'BEGIN':
            transaction()
        elif split_row[0] == 'COMMIT':
            break
        elif split_row[0] == 'ROLLBACK':
            db = db_snapshot
            break
        else:
            exec_db_commands(split_row)


def main():
    while True:
        row = input('>>: ').strip()
        split_row = row.split()

        if len(split_row) == 0:
            print()
        elif split_row[0] == 'END':
            break
        elif split_row[0] == 'BEGIN':
            transaction()
        else:
            exec_db_commands(split_row)


if __name__ == '__main__':
    main()
