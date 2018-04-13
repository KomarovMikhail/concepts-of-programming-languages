class FonNeyman:
    def __init__(self):
        self._mem = [0] * 1024 * 1024
        self._mem[0] = 4
        self._cust_progs = {}
        self._labels = {}

    def _running_mode(self, ptr, args):
        self._mem[3] = ptr
        for arg in args:
            self._mem[3] += 4
            self._mem[self._mem[3] + 3] = int(arg)
            self._mem[self._mem[3] + 2] = int(arg)
        self._mem[3] += 4
        while True:
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
            elif self._mem[self._mem[3]] == 254:
                self._mem[ptr+3] = self._mem[self._mem[self._mem[3]+3]+3]
                break
            elif self._mem[self._mem[3]] == 0:
                if self._mem[self._mem[3]+1] == 0:
                    if self._mem[self._mem[3]+2] is not None:
                        self._mem[self._mem[3]+3] = self._mem[self._mem[3]+2]
                    else:
                        self._mem[self._mem[3] + 2] = self._mem[self._mem[self._mem[3]+3]+3]
                        self._mem[self._mem[3] + 3] = self._mem[self._mem[3] + 2]
                else:
                    curr_prt = self._mem[3]
                    self._running_mode(self._mem[self._mem[3]+1], {})
                    self._mem[3] = curr_prt
                    self._mem[self._mem[3] + 3] = self._mem[self._mem[self._mem[3]+1]+3]
            elif self._mem[self._mem[3]] == 8:
                pass
            elif self._mem[self._mem[3]] == 9:
                self._mem[3] = self._mem[self._mem[3]+3]
            elif self._mem[self._mem[3]] == 10:
                if self._mem[self._mem[self._mem[3]+2]+3] != self._mem[self._mem[self._mem[3]+3]+3]:
                    self._mem[3] = self._mem[self._mem[3]+1]

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

        buf = [0, 0, None, 0]
        count = 4

        args = self._cust_progs.get(file)[1]
        for arg in args.keys():
            args[arg] = ptr + count
            count += 4
            buf.extend([0, 0, None, 0])
        jumps = {}
        ifs = []
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
            elif len(str) > 2 and str[1] == "=":
                if self._cust_progs.get(str[2]) is None:
                    buf.extend([0, 0, int(str[2]), int(str[2])])
                else:
                    func_ptr = self._cust_progs.get(str[2])[0]
                    for i in range(len(str)):
                        if i == 0 or i == 1 or i == 2:
                            continue
                        if self._cust_progs.get(file)[1].get(str[i]) is None:
                            self._mem[func_ptr + (i * 4) - 5] = int(str[i])
                            self._mem[func_ptr + (i * 4) - 6] = int(str[i])
                        else:
                            self._mem[func_ptr + (i * 4) - 5] = \
                                self._cust_progs.get(file)[1].get(str[i])
                    buf.extend([0, func_ptr, 0, 0])
                self._cust_progs.get(file)[1][str[0]] = ptr + count
            elif str[0] == "stop":
                buf.extend([255, 0, 0, 0])
            elif str[0][len(str[0])-1] == ":" and len(str) == 1:
                buf.extend([8, 0, 0, 0])
                if str[0] == "else:":
                    if_ptr = ifs.pop()
                    buf[if_ptr+1] = ptr + count
                else:
                    self._labels[str[0][0:len(str[0])-1]] = ptr + count
            elif str[0] == "jmp" and len(str) == 2:
                buf.extend([9, 0, 0, 0])
                if jumps.get(str[1]) is None:
                    jumps[str[1]] = [ptr + count]
                else:
                    jumps[str[1]].append(ptr + count)
            elif str[0] == "if" and len(str) == 3:
                buf.extend([10, 0, self._cust_progs.get(file)[1].get(str[1]),
                            self._cust_progs.get(file)[1].get(str[2])])
                ifs.append(count)
            elif str[0] == "return" and len(str) == 2:
                buf.extend([254, 0, 0, self._cust_progs.get(file)[1].get(str[1])])
            count += 4
        if ptr + count > 1024 * 1024:
            print("Memory exhausted")
        else:
            self._mem[ptr:ptr + count] = buf

            # расставляем джампы
            for label, pointers in jumps.items():
                for pointer in pointers:
                    self._mem[pointer+3] = self._labels.get(label)
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
                    if len(com) != 2 + ptr[2]:
                        print("Wrong number of arguments, expected:", ptr[2])
                    else:
                        print("Program " + com[1] + " is running...")
                        self._running_mode(ptr[0], com[2:len(com)])
                        print("Program " + com[1] + " completed")
            elif com[0] == "read":
                args = {}
                if len(com) > 2:
                    for i in range(len(com)):
                        if i == 0 or i == 1:
                            continue
                        args[com[i]] = 0
                self._cust_progs[com[1]] = [self._mem[0], args, len(com)-2]
                self._read_from_file(com[1], self._mem[0])
            else:
                print("Unknown command")
        print("Goodbye, see you.")
