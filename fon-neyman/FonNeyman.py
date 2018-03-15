import time


class FonNeyman:
    def __init__(self):
        self._mem = [0] * 1024 * 1024
        self._mem[0] = 4
        self._cust_progs = {}

    def _coding_mode(self, prog, ptr):
        buf = []
        count = 0
        print("Type your code")
        while True:
            str = input(": ").split()
            if str[0] == "mov" and len(str) == 3:
                buf.extend([1, self._cust_progs.get(prog)[1].get(str[1]), 0,
                            self._cust_progs.get(prog)[1].get(str[2])])
            elif str[0] == "add" and len(str) == 3:
                buf.extend([2, self._cust_progs.get(prog)[1].get(str[1]), 0,
                            self._cust_progs.get(prog)[1].get(str[2])])
            elif str[0] == "inp" and len(str) == 2:
                buf.extend([3, 0, 0, self._cust_progs.get(prog)[1].get(str[1])])
            elif str[0] == "out" and len(str) == 2:
                buf.extend([4, 0, 0, self._cust_progs.get(prog)[1].get(str[1])])
            elif len(str) == 3 and str[1] == "=":
                buf.extend([0, 0, 0, int(str[2])])
                self._cust_progs.get(prog)[1][str[0]] = ptr + count
            elif str[0] == "stop":
                buf.extend([255, 0, 0, 0])
                break
            elif str[0] == "cx" and len(str) == 2:
                buf.extend([5, 0, 0, self._cust_progs.get(prog)[1].get(str[1])])
            elif str[0] == "mrk" and len(str) == 1:
                buf.extend([6, 0, 0, ptr+count])
            elif str[0] == "loop" and len(str) == 1:
                buf.extend([7, 0, 0, 0])
            count += 4
        if ptr + count > 1024 * 1024:
            print("Memory exhausted")
        else:
            self._mem[ptr:ptr+count] = buf
            self._mem[0] += count

    def _running_mode(self, ptr):
        self._mem[3] = ptr
        while self._mem[self._mem[3]] != 255:
            if self._mem[self._mem[3]] == 1:
                self._mov(self._mem[self._mem[3]+1], self._mem[self._mem[3]+3])
            elif self._mem[self._mem[3]] == 2:
                self._add(self._mem[self._mem[3]+1], self._mem[self._mem[3]+3])
            elif self._mem[self._mem[3]] == 3:
                self._inp(self._mem[self._mem[3]+3])
            elif self._mem[self._mem[3]] == 4:
                self._out(self._mem[self._mem[3]+3])
            elif self._mem[self._mem[3]] == 255:
                break
            elif self._mem[self._mem[3]] == 5:
                self._mem[1] = self._mem[self._mem[self._mem[3]+3] + 3]
            elif self._mem[self._mem[3]] == 6:
                self._mem[2] = self._mem[self._mem[3] + 3]
            elif self._mem[self._mem[3]] == 7:
                self._mem[1] -= 1
                if self._mem[1] > 0:
                    self._mem[3] = self._mem[2]
            self._mem[3] += 4

    def _mov(self, dest, src):
        """Command code: 1"""
        self._mem[dest:dest+4] = self._mem[src:src+4]

    def _add(self, dest, src):
        """Command code: 2"""
        self._mem[dest+3] += self._mem[src+3]

    def _inp(self, dest):
        """Command code: 3"""
        buf = input("Type your value: ")
        self._mem[dest+3] = int(buf)

    def _out(self, src):
        """Command code: 4"""
        print(self._mem[src+3])

    def _read_from_file(self, file, ptr):
        with open(file) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        buf = []
        count = 0
        for line in content:
            str = line.split()
            if str[0] == "mov" and len(str) == 3:
                buf.extend([1, self._cust_progs.get(file)[1].get(str[1]), 0,
                            self._cust_progs.get(file)[1].get(str[2])])
            elif str[0] == "add" and len(str) == 3:
                buf.extend([2, self._cust_progs.get(file)[1].get(str[1]), 0,
                            self._cust_progs.get(file)[1].get(str[2])])
            elif str[0] == "inp" and len(str) == 2:
                buf.extend([3, 0, 0, self._cust_progs.get(file)[1].get(str[1])])
            elif str[0] == "out" and len(str) == 2:
                buf.extend([4, 0, 0, self._cust_progs.get(file)[1].get(str[1])])
            elif len(str) == 3 and str[1] == "=":
                buf.extend([0, 0, 0, int(str[2])])
                self._cust_progs.get(file)[1][str[0]] = ptr + count
            elif str[0] == "stop":
                buf.extend([255, 0, 0, 0])
                break
            elif str[0] == "cx" and len(str) == 2:
                buf.extend([5, 0, 0, self._cust_progs.get(file)[1].get(str[1])])
            elif str[0] == "mrk" and len(str) == 1:
                buf.extend([6, 0, 0, ptr + count])
            elif str[0] == "loop" and len(str) == 1:
                buf.extend([7, 0, 0, 0])
            count += 4
        if ptr + count > 1024 * 1024:
            print("Memory exhausted")
        else:
            self._mem[ptr:ptr + count] = buf
            self._mem[0] += count

    def run(self):
        print("Welcome to Fon Neyman Virtual Machine"
              "\nType \"help\" to get commands info")

        while True:
            com = input("> ").split()
            if com[0] == "help":
                print("You can use following commands to manage the machine:\n"
                      "\"help\" - print commands info\n"
                      "\"shutdown\" - shutdown machine\n"
                      "\"prog [prog_name]\" - turn on coding mode\n"
                      "\"run [prog_name]\" - run custom program\n"
                      "\"read [file_name]\" - read program from file")
            elif com[0] == "shutdown":
                break
            elif com[0] == "prog":
                self._cust_progs[com[1]] = [self._mem[0], {}]
                self._coding_mode(com[1], self._mem[0])
                print("Created program " + com[1])
            elif com[0] == "run":
                ptr = self._cust_progs.get(com[1])
                if ptr is None:
                    print("Program not found")
                else:
                    print("Program " + com[1] + " is running...")
                    self._running_mode(ptr[0])
                    print("Program " + com[1] + " completed")
            elif com[0] == "read":
                self._cust_progs[com[1]] = [self._mem[0], {}]
                self._read_from_file(com[1], self._mem[0])
            else:
                print("Unknown command")

        print("Goodbay, see you.")
