import sys


class SymbolTable:
    def __init__(self):
        self.table = []
        self.variable = {
            'address': 0,
            'start': 0,
            'end': 0,
            'table': 0,
            'iterator': 0,
            'name': "",
            'only_value': 0,
            'value': -1,
            'is_in_memory' : 0
        }
        self.counter = 0

    def add_variable(self, name):
        find = list(filter(lambda variable: variable['name'] == name, self.table))
        if find:
            print("Zmienna ", name, " juz zadeklarowana")
            sys.exit()
        else:
            var = {'address': self.counter, 'start': 0, 'end': 0, 'table': 0, 'iterator': 0, 'name': name,
                   'only_value': 0, 'value': -1, 'is_in_memory' : 0}
            self.counter += 1
            self.table.append(var)

    def add_table(self, name, start, end):
        find = list(filter(lambda variable: variable['name'] == name, self.table))
        if find:
            print("Zmienna ", name, " juz zadeklarowana")
            sys.exit()
        else:
            if start > end:
                print("Zly zakres tablicy", name)
                sys.exit()
            var = {'address': self.counter, 'start': start, 'end': end, 'table': 1, 'iterator': 0, 'name': name,
                   'only_value': 0, 'value': -1, 'is_in_memory' : 0}
            l = end - start + 1
            self.counter += l
            self.table.append(var)

    def get_variable(self, name):
        find = list(filter(lambda variable: variable['name'] == name, self.table))
        if find:
            if find[0]['table'] == 1:
                print("Zle uzycie zmiennej ", name)
                sys.exit()
            else:
                return find
        else:
            print("Zmienna ", name, " nie zadeklarowana")
            sys.exit()

    def get_table_on_position_num(self, name, num):
        find = list(filter(lambda variable: variable['name'] == name, self.table))
        if find:
            if find[0]['table'] == 0:
                print("Zle uzycie tablicy ", name)
                sys.exit()
            elif find[0]['start'] > num or find[0]['end'] < num:
                print("W tablicy ", name, " nie ma pozycji ", num)
                sys.exit()
            else:
                new_name = name + "(" + str(num) + ")"
                address = find[0]['address'] + num - find[0]['start']
                var = {'address': address, 'start': 0, 'end': 0, 'table': 0, 'iterator': 0, 'name': new_name,
                       'only_value': 0, 'value': -1, 'is_in_memory' : 0}
                return var
        else:
            print("Tablica ", name, " nie zadeklarowana")
            sys.exit()

    def get_table_on_position_pidentifier(self, name, pid):
        find = list(filter(lambda variable: variable['name'] == name, self.table))
        if find:
            if find[0]['table'] == 0:
                print("Zle uzycie tablicy ", name)
                sys.exit()
            else:
                find2 = list(filter(lambda variable: variable['name'] == pid, self.table))
                if find:
                    if find2[0]['table'] == 1:
                        print("Tablica w tablicy")
                        sys.exit()
                    elif find2[0]['value'] == -1:
                        print("Zmienna ", pid, " nie zainicjalizowana")
                        sys.exit()
                    elif find2[0]['value'] < find[0]['start'] or find2[0]['value'] > find[0]['end']:
                        print("Tablica ", name, " nie ma pozycji ", find2[0]['value'])
                        sys.exit()
                    else:
                        address = find[0]['address'] + find2[0]['value']
                        var = {'address': address, 'start': 0, 'end': 0, 'table': 0, 'iterator': 0, 'name': "",
                               'only_value': 0, 'value': -1, 'is_in_memory' : 0}
                        return var
                else:
                    print("Zmienna ", pid, " nie zadeklarowana")

        else:
            print("Tablica ", name, " nie zadeklarowana")
            sys.exit()

    def get_num(self, num):
        # jak taka liczba jest juz w tabeli to nie dodawac nastepnej tylko zwracac ta co juz jest
        for numb in self.table:
            if numb['name'] == str(num):
                return numb
        var = {'address': self.counter, 'start': 0, 'end': 0, 'table': 0, 'iterator': 0, 'name': str(num),
               'only_value': 1, 'value': num, 'is_in_memory' : 0}
        self.counter += 1
        self.table.append(var)
        return var

