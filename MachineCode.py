from SymbolTable import *
from Expression import *


class MachineCode:

    def __init__(self):
        self.code = []
        self.command = {'com': "", 'arg1': "", 'arg2': ""}
        # registers:
        self.r1 = {'name': 'a', 'value': -1}
        self.r2 = {'name': 'b', 'value': -1}
        self.r3 = {'name': 'c', 'value': -1}
        self.r4 = {'name': 'd', 'value': -1}
        self.r5 = {'name': 'e', 'value': -1}
        self.r6 = {'name': 'f', 'value': -1}

    def get_register_by_value(self, value):
        if self.r1['value'] == value:
            return self.r1
        elif self.r2['value'] == value:
            return self.r2
        elif self.r3['value'] == value:
            return self.r3
        elif self.r4['value'] == value:
            return self.r4
        elif self.r5['value'] == value:
            return self.r5
        elif self.r6['value'] == value:
            return self.r6
        else:
            return self.r1

    def get_2_registers(self, value1):
        if self.r1['value'] == value1:
            return self.r1, self.r2
        elif self.r2['value'] == value1:
            return self.r2, self.r3
        elif self.r3['value'] == value1:
            return self.r3, self.r4
        elif self.r4['value'] == value1:
            return self.r4, self.r5
        elif self.r5['value'] == value1:
            return self.r5, self.r6
        elif self.r6['value'] == value1:
            return self.r6, self.r1
        else:
            return self.r1, self.r2

    def get_3_registers(self, value1):
        if self.r1['value'] == value1:
            return self.r1, self.r2, self.r3
        elif self.r2['value'] == value1:
            return self.r2, self.r3, self.r4
        elif self.r3['value'] == value1:
            return self.r3, self.r4, self.r5
        elif self.r4['value'] == value1:
            return self.r4, self.r5, self.r6
        elif self.r5['value'] == value1:
            return self.r5, self.r6, self.r1
        elif self.r6['value'] == value1:
            return self.r6, self.r1, self.r2
        else:
            return self.r1, self.r2, self.r3

    def get_register_diff(self, reg):
        if self.r1['name'] != reg:
            return self.r1
        elif self.r2['name'] != reg:
            return self.r2
        elif self.r3['name'] != reg:
            return self.r3
        elif self.r4['name'] != reg:
            return self.r4
        elif self.r5['name'] != reg:
            return self.r5
        else:
            return self.r6

    def set_value_to_register(self, r_name, r_value, value):
        if r_value == -1:
            r_value = 0
            command = {'com': "RESET", 'arg1': r_name, 'arg2': ""}
            self.code.append(command)

        if r_value == value:
            return
        if r_value == 0:
            r_value += 1
            command = {'com': "INC", 'arg1': r_name, 'arg2': ""}
            self.code.append(command)

        if r_value < value:
            while r_value * 2 <= value:
                r_value *= 2
                command = {'com': "SHL", 'arg1': r_name, 'arg2': ""}
                self.code.append(command)
                if r_value == value:
                    return
            while r_value + 1 <= value:
                r_value += 1
                command = {'com': "INC", 'arg1': r_name, 'arg2': ""}
                self.code.append(command)
                if r_value == value:
                    return
        elif r_value > value:
            while r_value // 2 >= value:
                r_value //= 2
                command = {'com': "SHR", 'arg1': r_name, 'arg2': ""}
                self.code.append(command)
                if r_value == value:
                    return
            while r_value - 1 >= value:
                r_value -= 1
                command = {'com': "DEC", 'arg1': r_name, 'arg2': ""}
                self.code.append(command)
                if r_value == value:
                    return

    def actualize_register_value(self, name, new_value):
        if name == 'a':
            self.r1['value'] = new_value
        elif name == 'b':
            self.r2['value'] = new_value
        elif name == 'c':
            self.r3['value'] = new_value
        elif name == 'd':
            self.r4['value'] = new_value
        elif name == 'e':
            self.r5['value'] = new_value
        elif name == 'f':
            self.r6['value'] = new_value


    def read(self, variable):
        address = variable[0]['address']
        reg = self.get_register_by_value(address)
        self.set_value_to_register(reg['name'], reg['value'], address)
        command = {'com': "GET", 'arg1': reg['name'], 'arg2': ""}
        self.code.append(command)
        self.actualize_register_value(reg['name'], address)

    def write(self, variable):
        if isinstance(variable, list):
            variable = variable[0]
        if variable['value'] == -1:
            print("Zmienna nie zainicjalizowana")
            sys.exit()
        if variable['is_in_memory'] == 0:
            reg1, reg2 = self.get_2_registers(variable['value'])
            self.set_value_to_register(reg1['name'], reg1['value'], variable['value'])
            self.set_value_to_register(reg2['name'], reg2['value'], variable['address'])
            command = {'com': "STORE", 'arg1': reg1['name'], 'arg2': reg2['name']}
            self.code.append(command)
            command = {'com': "PUT", 'arg1': reg2['name'], 'arg2': ""}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], variable['value'])
            self.actualize_register_value(reg2['name'], variable['address'])
        else:
            reg = self.get_register_by_value(variable['address'])
            self.set_value_to_register(reg['name'], reg['value'], variable['address'])
            command = {'com': "PUT", 'arg1': reg['name'], 'arg2': ""}
            self.code.append(command)
            self.actualize_register_value(reg['name'], variable['address'])

    def expression_1(self, variable):
        if isinstance(variable, list):
            variable = variable[0]
        if variable['only_value'] == 1:
            value = variable['value']
            reg = self.get_register_by_value(value)
            self.set_value_to_register(reg['name'], reg['value'], value)
            self.actualize_register_value(reg['name'], value)
            return reg
        else:
            if variable['value'] == -1:
                print("Zmienna ", variable['name'], " nie zainicjalizowana")
                sys.exit()
            else:
                address = variable['address']
                reg = self.get_register_by_value(address)
                self.set_value_to_register(reg['name'], reg['value'], address)
                self.actualize_register_value(reg['name'], address)
                command = {'com': "LOAD", 'arg1': reg['name'], 'arg2': reg['name']}
                self.code.append(command)
                self.actualize_register_value(reg['name'], -1)
                return reg

    def expression_plus_minus(self, var1, var2, sign):
        if isinstance(var1, list):
            var1 = var1[0]
        if isinstance(var2, list):
            var2 = var2[0]

        if var1['only_value'] == 1 and var2['only_value'] == 1:
            if sign == '+':
                result = var1['value'] + var2['value']
            elif sign == '-':
                result = max(var1['value']-var2['value'], 0)
            reg = self.get_register_by_value(result)
            self.set_value_to_register(reg['name'], reg['value'], result)
            self.actualize_register_value(reg['name'], result)
            return reg
        elif var1['only_value'] == 1 and var2['only_value'] == 0:
            value1 = var1['value']
            reg1, reg2 = self.get_2_registers(value1)
            self.set_value_to_register(reg1['name'], reg1['value'], value1)
            self.actualize_register_value(reg1['name'], value1)

            address2 = var2['address']
            self.set_value_to_register(reg2['name'], reg2['value'], address2)
            self.actualize_register_value(reg2['name'], address2)
            command = {'com': "LOAD", 'arg1': reg2['name'], 'arg2': reg2['name']}
            self.code.append(command)
            self.actualize_register_value(reg2['name'], -1)

            if sign == '+':
                command = {'com': "ADD", 'arg1': reg1['name'], 'arg2': reg2['name']}
            elif sign == '-':
                command = {'com': "SUB", 'arg1': reg1['name'], 'arg2': reg2['name']}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], -1)
            return reg1
        elif var1['only_value'] == 0 and var2['only_value'] == 1:
            value2 = var2['value']
            reg2, reg1 = self.get_2_registers(value2)
            self.set_value_to_register(reg2['name'], reg2['value'], value2)
            self.actualize_register_value(reg2['name'], value2)

            address1 = var1['address']
            self.set_value_to_register(reg1['name'], reg1['value'], address1)
            self.actualize_register_value(reg1['name'], address1)
            command = {'com': "LOAD", 'arg1': reg1['name'], 'arg2': reg1['name']}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], -1)

            if sign == '+':
                command = {'com': "ADD", 'arg1': reg2['name'], 'arg2': reg1['name']}
            elif sign == '-':
                command = {'com': "SUB", 'arg1': reg2['name'], 'arg2': reg1['name']}
            self.code.append(command)
            self.actualize_register_value(reg2['name'], -1)
            return reg2
        else:
            address1 = var1['address']
            reg1, reg2 = self.get_2_registers(address1)

            self.set_value_to_register(reg1['name'], reg1['value'], address1)
            self.actualize_register_value(reg1['name'], address1)
            command = {'com': "LOAD", 'arg1': reg1['name'], 'arg2': reg1['name']}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], -1)

            address2 = var2['address']
            self.set_value_to_register(reg2['name'], reg2['value'], address2)
            self.actualize_register_value(reg2['name'], address2)
            command = {'com': "LOAD", 'arg1': reg2['name'], 'arg2': reg2['name']}
            self.code.append(command)
            self.actualize_register_value(reg2['name'], -1)

            if sign == '+':
                command = {'com': "ADD", 'arg1': reg1['name'], 'arg2': reg2['name']}
            elif sign == '-':
                command = {'com': "SUB", 'arg1': reg1['name'], 'arg2': reg2['name']}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], -1)
            return reg1

    def expression_times(self, var1, var2):
        if isinstance(var1, list):
            var1 = var1[0]
        if isinstance(var2, list):
            var2 = var2[0]
        if var1['only_value'] == 1 and var2['only_value'] == 1:
            result = var1['value'] * var2['value']
            reg = self.get_register_by_value(result)
            self.set_value_to_register(reg['name'], reg['value'], result)
            self.actualize_register_value(reg['name'], result)
            return reg
        elif var1['only_value'] == 1 and var2['only_value'] == 0:
            value1 = var1['value']
            if value1 == 0:
                reg = self.get_register_by_value(0)
                self.set_value_to_register(reg['name'], reg['value'], 0)
                self.actualize_register_value(reg['name'], 0)
                return reg
            else:
                address2 = var2['address']
                reg2, reg1 = self.get_2_registers(address2)
                self.set_value_to_register(reg2['name'], reg2['value'], address2)
                self.actualize_register_value(reg2['name'], address2)
                command = {'com': "LOAD", 'arg1': reg2['name'], 'arg2': reg2['name']}
                self.code.append(command)
                self.actualize_register_value(reg2['name'], -1)
                # w reg2 jest zapisana wartosc zmiennej 2
                command = {'com': "RESET", 'arg1': reg1['name'], 'arg2': ""}
                self.code.append(command)
                self.actualize_register_value(reg1['name'], -1)
                # w reg1 jest 0

                for i in range(0, value1):
                    command = {'com': "ADD", 'arg1': reg1['name'], 'arg2': reg2['name']}
                    self.code.append(command)

                return reg1
        elif var1['only_value'] == 0 and var2['only_value'] == 1:
            value2 = var2['value']
            if value2 == 0:
                reg = self.get_register_by_value(0)
                self.set_value_to_register(reg['name'], reg['value'], 0)
                self.actualize_register_value(reg['name'], 0)
                return reg
            else:
                address1 = var1['address']
                reg1, reg2 = self.get_2_registers(address1)
                self.set_value_to_register(reg1['name'], reg1['value'], address1)
                self.actualize_register_value(reg1['name'], address1)
                command = {'com': "LOAD", 'arg1': reg1['name'], 'arg2': reg1['name']}
                self.code.append(command)
                self.actualize_register_value(reg1['name'], -1)
                # w reg1 jest zapisana wartosc zmiennej 1
                command = {'com': "RESET", 'arg1': reg2['name'], 'arg2': ""}
                self.code.append(command)
                self.actualize_register_value(reg2['name'], -1)
                # w reg2 jest 0

                for i in range(0, value2):
                    command = {'com': "ADD", 'arg1': reg2['name'], 'arg2': reg1['name']}
                    self.code.append(command)

                return reg2
        else:
            address1 = var1['address']
            address2 = var2['address']
            reg1, reg2, reg3 = self.get_3_registers(address1)

            self.set_value_to_register(reg1['name'], reg1['value'], address1)
            self.actualize_register_value(reg1['name'], address1)
            command = {'com': "LOAD", 'arg1': reg1['name'], 'arg2': reg1['name']}
            self.code.append(command)
            self.actualize_register_value(reg1['name'], -1)

            self.set_value_to_register(reg2['name'], reg2['value'], address2)
            self.actualize_register_value(reg2['name'], address2)
            command = {'com': "LOAD", 'arg1': reg2['name'], 'arg2': reg2['name']}
            self.code.append(command)
            self.actualize_register_value(reg2['name'], -1)

            self.set_value_to_register(reg3['name'], reg3['value'], 0)
            self.actualize_register_value(reg3['name'], 0)

            command = {'com': "JZERO", 'arg1': reg2['name'], 'arg2': str(3)}
            self.code.append(command)
            command = {'com': "ADD", 'arg1': reg3['name'], 'arg2': reg1['name']}
            self.code.append(command)
            command = {'com': "DEC", 'arg1': reg2['name'], 'arg2': ""}
            self.code.append(command)
            command = {'com': "JZERO", 'arg1': reg2['name'], 'arg2': str(2)}
            self.code.append(command)
            command = {'com': "JUMP", 'arg1': str(-3), 'arg2': ""}
            self.code.append(command)

            return reg3

    def assign(self, reg, var):
        if isinstance(var, list):
            var = var[0]
        if isinstance(reg, list):
            reg = reg[0]
        address = var['address']
        address_reg = self.get_register_diff(reg['name'])
        self.set_value_to_register(address_reg['name'], address_reg['value'], address)
        self.actualize_register_value(address_reg['name'], address)
        command = {'com': "STORE", 'arg1': reg['name'], 'arg2': address_reg['name']}
        self.code.append(command)