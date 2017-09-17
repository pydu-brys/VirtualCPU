
# coding: utf-8

# In[1]:

#RAM: dict (key:int)
#Program counter: vector (int 2 bits)
#IR: vector (str 4 bits)
#hexacimal decoder
MMR = dict.fromkeys(list(range(0,256)), "00000000")
REG = dict.fromkeys(list(range(0,16)),"00000000")
PC = '--'
IR = '----'
msg = ''
opt = ""
ipt = ""
from random import randint

#for i in range(0,16):
#    REG[i] = str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1))

#for i in range(0,256):
#    MMR[i] = str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1))


# In[2]:

def bin2Hex(inputBinStr):
    if len(inputBinStr) == 8:
        output = hex(int(inputBinStr, 2))[2:]
        if len(output) == 1:
            output = '0' + output
    else:
        output = inputBinStr
    return(output)


# In[3]:

def hex2Bin(inputHexStr):
    if len(inputHexStr) == 2:
        output = bin(int(inputHexStr, 16))[-8:]
    else: output = inputHexStr
    return(output)


# In[4]:

def bin2Int(inputBinStr):
    num = len(inputBinStr)
    if inputBinStr == '1' * num:
        outputInt = -1
    elif inputBinStr[0] == '0':
        outputInt = int(inputBinStr, 2)
    elif inputBinStr[0] == '1':
        #incr = pow(2, num) - 1 - int(inputBinStr, 2)
        #outputInt = -1 * pow(2, num - 1) + incr
        outputInt = int(inputBinStr, 2) - pow(2, num)
    return (outputInt)


# In[5]:

def int2Bin(inputInt, num):
    if inputInt <= (pow(2, (num - 1)) - 1) and inputInt >= 0:
        outputString = str('{0:0' + str(num) + 'b}').format(inputInt)
    elif inputInt < 0 and inputInt >= -1 * pow(2, num - 1):
        incr = inputInt + pow(2, num - 1)
        outputString = str('{0:0' + str(num - 1) + 'b}').format(pow(2, num - 1) + incr)
    else: outputString = 'error'
    return (outputString)


# In[184]:

def iptValue():
    import tkinter.simpledialog
    global ipt
    ipt = tkinter.simpledialog.askinteger("Input Value", "Enter a integer between -128 and 127")


# In[185]:

def incrtInst():
    import tkinter.messagebox
    tkinter.messagebox.showerror("Incorrect Instruction", "Instruction format incorrect")


# In[7]:

class code:
    def code1(self, R, XY): #LOAD the register R with the bit pattern found in the memory cell whose address is XY
        R = int(str(R), 16) #tranform the hexadecimal number into decimal
        XY = int(str(XY), 16)
        REG[R] = MMR[XY]

    def code2(self, R, XY): #LOAD the register R with the bit pattern XY
        R = int(str(R), 16)
        XY = int(str(XY), 16)
        REG[R] = str('{0:08b}'.format(XY))

    def code3(self, R, XY): #STORE the bit pattern found in register R in the memory cell whose address is XY
        R = int(str(R), 16)
        XY = int(str(XY), 16)
        MMR[XY] = REG[R]

    def code4(self, R, S): #MOVE the bit pattern found in register R to register S
        R = int(str(R), 16)
        S = int(str(S), 16)
        REG[S] = REG[R]

    def code5(self, R, S, T): #ADD the bit patterns in registers S and T as through they were two's complement representations and leave the result in register R
        global msg
        R = int(str(R), 16)
        S = int(str(S), 16)
        T = int(str(T), 16)
        try:
            if bin2Int(REG[S]) + bin2Int(REG[T]) <= 127 and bin2Int(REG[S]) + bin2Int(REG[T]) >= -128:
                REG[R] = int2Bin((bin2Int(REG[S]) + bin2Int(REG[T])),8)
            else:
                print("overflow")
                msg = "overflow"
        except:
            print ("overflow")
            msg = "overflow"

    #*****
    def code6(self, R, S, T): #ADD the bit patterns in registers S and T as through they represented values in floating-point notation and leave the floating-point result in register R
        R = int(str(R), 16)
        S = int(str(S), 16)
        T = int(str(T), 16)
        exp1 = int(REG[S][1:4], 2) - 4
        exp2 = int(REG[T][1:4], 2) - 4

        neg = '0'
        bin1 = '0' * (3-exp1) + REG[S][-4:] + '0' * (exp1 + 4)
        bin2 = '0' * (3-exp2) + REG[T][-4:] + '0' * (exp2 + 4)

        int1 = int(bin1, 2) * pow(-1, int(REG[S][0]))
        int2 = int(bin2, 2) * pow(-1, int(REG[T][0]))

        result = int1 + int2
        if result < 0:
            result = result * -1
            neg = '1'
        output = result
        #int1 = bin2Int(bin1) * pow(-1, int(REG[S][0]))
        #int2 = bin2Int(bin2) * pow(-1, int(REG[T][0]))
        output11 = int2Bin(result, 11)

        for i in range(0,len(output11)):
            if output11[i] == '1':
                expOutput = 3 - i + 4
                if expOutput >= 0:
                    output = output11[i:i+4]
                else:
                    output = output11[-4:]
                    expOutput = 0
                REG[R] = neg + '{0:03b}'.format(expOutput) + output
                break
            else:
                REG[R] = '00000000'




    #*****

    def code7(self, R, S, T): #OR the bit patterns in registers S and T and place the result in register R
        R = int(str(R), 16)
        S = int(str(S), 16)
        T = int(str(T), 16)
        bp = bin2Int(REG[S]) | bin2Int(REG[T])
        if bp < 0:
            bp = bin(bp)[3:]
        else: bp = bin(bp)[2:]
        REG[R] = '0' * (8-len(bp)) + bp

    def code8(self, R, S, T): #AND the bit patterns in registers S and T and place the result in register R
        R = int(str(R), 16)
        S = int(str(S), 16)
        T = int(str(T), 16)
        bp = bin2Int(REG[S]) & bin2Int(REG[T])
        if bp < 0:
            bp = bin(bp)[3:]
        else: bp = bin(bp)[2:]
        REG[R] = '0' * (8-len(bp)) + bp

    def code9(self, R, S, T): #EXCLUSIVE OR the bit patterns in registers S and T and place the result in register R
        R = int(str(R), 16)
        S = int(str(S), 16)
        T = int(str(T), 16)
        bp = bin2Int(REG[S]) ^ bin2Int(REG[T])
        if bp < 0:
            bp = bin(bp)[3:]
        else: bp = bin(bp)[2:]
        REG[R] = '0' * (8-len(bp)) + bp

    def codeA(self, R, X): #ROTATE the bit pattern in register R one bit to the right X times
        R = int(str(R), 16)
        X = int(str(X), 16)
        lowerPart = REG[R][:(8-X)]
        upperPart = REG[R][(-X):]
        REG[R] = upperPart + lowerPart

    def codeD(self, XY):
        global ipt, MMR
        XY = int(str(XY), 16)
        iptValue()
        MMR[XY] = int2Bin(ipt, 8)

    def codeE(self, XY):
        global opt
        XY = int(str(XY), 16)
        opt = opt + " " + bin2Hex(MMR[XY])



# In[8]:

def read(start):
    global r, PC
    if r == True:
        PC = start
    return(PC)


# In[186]:

def step(start):
    global PC, IR, REG, msg
    run = True
    msg = ""

    if IR in ('c000', 'C000'): run = False
    function = code()

    start = int(str(start), 16)

    if len(hex(list(MMR.keys())[start])[2:]) == 1:
        PC = '0' + hex(list(MMR.keys())[start])[2:]
    else: PC = hex(list(MMR.keys())[start])[2:]

    #print(PC)
    #input("----------------Press the <ENTER> key to continue...----------------")

    while run == True:


        if len(hex(list(MMR.keys())[start + 2])[2:]) == 1:
            PC = '0' + hex(list(MMR.keys())[start + 2])[2:]
        else: PC = hex(list(MMR.keys())[start + 2])[2:]
        #####
        inst = bin2Hex(MMR[start]) + bin2Hex(MMR[start+1])
        #print (inst)
        #####
        IR = inst
        #print("Program Counter: " + PC)
        #print('Instruction Register: ' + IR)
        #input("\n----------------Press the <ENTER> key to continue...----------------")

        #C000
        if inst in ('C000', 'c000'):
            run = False
            msg = "Program closed"
            print ("program closed")

        #BRXY: #JUMP to the instruction located in the memory cell at address XY if the bit pattern in register R
               #is equal to the bit pattern in register number 0. Otherwise,
               #continue with the normal sequence of execution
        elif inst[0] in ('B', 'b'):
            R = int(inst[1], 16)
            if REG[R] == REG[0]:
                start = int(inst[-2:], 16)

                if len(hex(list(MMR.keys())[start])[2:]) == 1:
                    PC = '0' + hex(list(MMR.keys())[start])[2:]
                else: PC = hex(list(MMR.keys())[start])[2:]

                start = start - 2

        elif inst[0] == '1':
            function.code1(inst[1], inst[2:])

        elif inst[0] == '2':
            function.code2(inst[1], inst[2:])

        elif inst[0] == '3':
            function.code3(inst[1], inst[2:])

        elif inst[0] == '4':
            function.code4(inst[2], inst[3])

        elif inst[0] == '5':
            function.code5(inst[1], inst[2], inst[3])

        elif inst[0] == '6':
            function.code6(inst[1], inst[2], inst[3])

        elif inst[0] == '7':
            function.code7(inst[1], inst[2], inst[3])

        elif inst[0] == '8':
            function.code8(inst[1], inst[2], inst[3])

        elif inst[0] == '9':
            function.code9(inst[1], inst[2], inst[3])

        elif inst[0] in ('a', 'A'):
            function.codeA(inst[1], inst[3])

        elif inst[0] in ('e', 'E'):
            function.codeE(inst[2:])

        elif inst[0] in ('d', 'D'):
            function.codeD(inst[2:])

        else: incrtInst()

        start = start + 2

        run = False
    return(PC,IR)


# In[187]:

def run(start):
    global REG, msg, IR
    function = code()
    PC = start
    start = int(str(start), 16)

    #if len(hex(list(MMR.keys())[start])[2:]) == 1:
    #    PC = '0' + hex(list(MMR.keys())[start])[2:]
    #else: PC = hex(list(MMR.keys())[start])[2:]

    run = True
    #print(PC)
    #input("----------------Press the <ENTER> key to continue...----------------")
    if IR in ('c000', 'C000'): run = False

    while run == True:
        if len(hex(list(MMR.keys())[start + 2])[2:]) == 1:
            PC = '0' + hex(list(MMR.keys())[start + 2])[2:]
        else: PC = hex(list(MMR.keys())[start + 2])[2:]
        #print (PC)
        inst = bin2Hex(MMR[start]) + bin2Hex(MMR[start+1])
        IR = inst
        #print("Program Counter: " + PC)
        #print('Instruction Register: ' + IR)
        #input("\n----------------Press the <ENTER> key to continue...----------------")

        #C000
        if inst in ('C000', 'c000'):
            run = False
            msg = "Program closed"
            #print ("program closed")

        #BRXY: #JUMP to the instruction located in the memory cell at address XY if the bit pattern in register R
               #is equal to the bit pattern in register number 0. Otherwise,
               #continue with the normal sequence of execution
        elif inst[0] in ('B', 'b'):
            R = int(inst[1], 16)
            if REG[R] == REG[0]:
                start = int(inst[-2:], 16)

                if len(hex(list(MMR.keys())[start])[2:]) == 1:
                    PC = '0' + hex(list(MMR.keys())[start])[2:]
                else: PC = hex(list(MMR.keys())[start])[2:]
                start = start - 2

        elif inst[0] == '1':
            function.code1(inst[1], inst[2:])

        elif inst[0] == '2':
            function.code2(inst[1], inst[2:])

        elif inst[0] == '3':
            function.code3(inst[1], inst[2:])

        elif inst[0] == '4':
            function.code4(inst[2], inst[3])

        elif inst[0] == '5':
            function.code5(inst[1], inst[2], inst[3])

        elif inst[0] == '6':
            function.code6(inst[1], inst[2], inst[3])

        elif inst[0] == '7':
            function.code7(inst[1], inst[2], inst[3])

        elif inst[0] == '8':
            function.code8(inst[1], inst[2], inst[3])

        elif inst[0] == '9':
            function.code9(inst[1], inst[2], inst[3])

        elif inst[0] in ('a', 'A'):
            function.codeA(inst[1], inst[3])

        elif inst[0] in ('e', 'E'):
            function.codeE(inst[2:])

        elif inst[0] in ('d', 'D'):
            function.codeD(inst[2:])

        else: incrtInst()

        start = start + 2

        #print(PC)
    return(PC,IR)


# In[188]:

def instInput(dirct, orgStart):
    #global msg

    crtInst = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    #print("Assign the instructions")
    #inst = input()
    #print("Assign the start of storing location")
    #orgStart = input()
    with open (dirct, 'r') as f:
        inst = f.read()
        inst = inst.replace("\n", "")

        if all(el.lower() in crtInst for el in inst):

            if len(inst) % 4 == 0:
                startLoc = int(orgStart,16)
                for i in range(0,len(inst)):
                    if i%2 == 0:
                        MMR[startLoc] = inst[i:i+2]
                        startLoc = startLoc + 1

            else:
                msg = 'Instruction format incorrect'
                incrtInst()


        else:
            msg = 'Instruction format incorrect'
            incrtInst()
            #print("\nInstruction " + inst + "\n starts at " + orgStart)


# In[182]:

from tkinter import *
from tkinter import filedialog
import tkinter.simpledialog


# In[189]:

class virtualCPU:
    def __init__(self):

        window = Tk()
        window.title("Virtual CPU")

        global r, opt, ipt, msg, MMR, REG
        opt = "Output: "
        ipt = ""
        r = True
        #frame1 = Frame(window)
        #frame1.pack()
        self.inst = StringVar()
        label1 = Label(window, text = "Instruction directory")
        label1.grid(row = 2, column = 20)
        browseBut = Button(window, text='Browse', command = self.askopenfile).grid(row = 2, column = 21)
        #instEnt = Entry(frame1, textvariable = self.inst)

        #frame2 = Frame(window)
        #frame2.pack()


        label2 = Label(window, text = "Starting location").grid(row = 1, column = 20, padx = 10)

        self.startLoc = StringVar(value = '00')
        #self.startLoc = '00'

        #self.dirLabel = Label(window, text = "")
        #self.dirLabel.grid(row = 3, column = 20, columnspan = 2)

        sLocEnt = Entry(window, textvariable = self.startLoc).grid(row = 1, column = 21, padx = 15)

        #btCon = Button(window, text = "Confirm", command = self.processConfirm).grid(row = 4, column = 20)

        self.msg = Label(window, text = "                                                  ")
        self.msg.grid(row = 5, column = 20, columnspan = 2)


        #frame3 = Frame(window)
        #frame3.pack()
        #for i in range(0,16):

        lbPC = Label(window, text = "Program Counter:").grid(row = 7, column = 20)
        lbIR = Label(window, text = "Instruction Register").grid(row = 8, column = 20)

        self.etyPC = Label(window, text = PC)
        self.etyPC.grid(row = 7, column = 21)
        self.etyIR = Label(window, text = IR)
        self.etyIR.grid(row = 8, column = 21)

        #btRead = Button(window, text = "Read instruction", command = self.read).grid(row = 8, column = 20)
        btClear = Button(window, text = "Reset", command = self.processClear).grid(row = 5, column = 20)
        btStep = Button(window, text = 'Step', command = self.step).grid(row = 4, column = 20)
        btRun = Button(window, text = "Run", command = self.run).grid(row = 4, column = 21, padx = 5)


        self.outputMsg = Label(window, text = opt)
        self.outputMsg.grid(row = 10, column = 20, columnspan = 2)
        #btIpt = Button(window, text = 'input', command = self.inputValue).grid(row = 10, column = 20, columnspan = 2)
        #btRandom = Button(window, text = "Generate Random Data", command = self.random)
        #btRandom.grid(row = 0, column = 20, columnspan = 2)

        self.msgLine = Label(window, text = "")
        self.msgLine["text"] = msg
        self.msgLine.grid(row = 12, column = 20, columnspan = 2)
        for i in range(0,16):

            globals()['labelRow%s' % i] = Label(window, text = hex(i)[-1])
            globals()['labelCol%s' % i] = Label(window, text = hex(i)[-1])
            exec("labelRow%s.grid(row = 1+i, column = 0, padx = 15)" % i)
            exec("labelCol%s.grid(row = 0, column = 1+i, pady = 15)" % i)

            globals()['btREG%s' % i] = Button(window, text = bin2Hex(REG[i]))
            exec("btREG%s.grid(row = 20, column = i+1, pady = 15)" % i)
            for j in range(0,16):
                globals()['button%s_%s' % (i, j)] = Button(window, text = bin2Hex(MMR[16 * i + j]))
                exec("button%s_%s.grid(row = i+1, column = j+1, sticky = E)" % (i, j))
                #exec("label%s%s.pack()" % (i, j))

        #browseBut.pack()

        #frame2.pack()
        #label1.pack()
        #label2.pack()
        #instEnt.pack()
        #sLocEnt.pack()
        #btCon.pack()
        #self.msg.pack()

        window.mainloop()
    def update(self):
        global MMR, REG, IR, PC, opt, msg
        msg = ""
        for i in range(0,16):
            exec('btREG%s["text"] = bin2Hex(REG[' % i + str(i) + '])')
            for j in range(0,16):
                value = bin2Hex(MMR[16 * i + j])
                exec('button%s_%s["text"] = value' % (i, j))
        self.etyPC["text"] = PC
        self.etyIR["text"] = IR
        self.outputMsg["text"] = opt
        self.msgLine["text"] = msg

    def processConfirm(self):
        global MMR, REG, IR, PC
        instInput(str(self.inst), str(self.startLoc.get()))
        with open(self.inst, 'r') as file:
            inst = file.read()
        #self.msg["text"] = inst + " starts at "  + self.startLoc.get()
        self.update()

    def read(self):
        global PC, r
        PC = read(self.startLoc.get())
        #self.etyPC["text"] = "" + pc
        self.update()

    def askopenfile(self):
        self.inst = filedialog.askopenfilename()
        #self.dirLabel["text"] = self.inst
        self.processConfirm()
        self.read()
        self.update()

    def processClear(self):
        global MMR, REG, IR, PC, r, opt, ipt
        #MMR = dict.fromkeys(list(range(0,256)), "00")
        #REG = dict.fromkeys(list(range(0,16)),"00")
        PC = '--'
        IR = '----'
        r = True
        opt = "Output: "
        ipt = ""
        self.update()


    def run(self):
        global PC, IR, r

        PC, IR = run(self.startLoc.get())
        self.update()
        r = False

    def step(self):
        global PC, IR, r, msg
        PC, IR = step(PC)
        self.msgLine["text"] = msg
        self.update()


    #def inputValue(self):
    #    global MMR, ipt
    #    ipt = simpledialog.askinteger("Input integer", "Enter a integer between -128 and 127")
    #    loc = simpledialog.askstring("Input location", "Enter a memroy location in hexadecimal")
    #    loc = int(loc, 16)
    #
    #    MMR[loc] = int2Bin(ipt, 8)
    #    self.update()

    #def random(self):
    #    global MMR, REG
    #    from random import randint
    #
    #    #for i in range(0,16):
    #    #    REG[i] = str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1))
    #
    #    for i in range(0,256):
    #        MMR[i] = hex(randint(0,16))[-1] + hex(randint(0,16))[-1]
    #        #MMR[i] = str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1)) + str(randint(0,1))
    #    self.update()


virtualCPU()



virtualCPU()
