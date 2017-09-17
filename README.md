# VirtualCPU
## Intro
I have built this Python program to simulate how memory (256 bytes) and register (16 bytes) interact while running machine code instructions with a GUI. The program displays changes in Memory, Register, Program Counter, and Instruction Register step-by-step. The program was written under Jupyter Notebook (which is why there are many "In[#]" throughout my code) with Python 3. The GUI package used is tkinter.

This program was developed for educational purpose for students in CSIM department at Soochow University in Taipei, Taiwan. 

## Features
The program supports the following features:
#### 1. User-defined machine code instruction (in certain format) stored in an external text file
#### 2. Two's complement for integer calculation (with "overflow" message if the result is overflowed)
#### 3. Options of "run" or "step" depending on if user wants to observe the process or just to see the result
#### 4. 14 types of machine code instructions including LOAD/ STORE/ ROTATE/ JUMP/ STOP (Please see Machine Code section for more info)

## Machine Code Instructions
#### 1RXY: 
LOAD the register R with the bit pattern found in the memory cell whose address is XY
#### 2RXY: 
LOAD the register R with the bit pattern XY
#### 3RXY: 
STORE the bit pattern found in register R in the memory cell whose address is XY
#### 40RX: 
MOVE the bit pattern found in register R to register S
#### 5RST: 
ADD the bit patterns in registers S and T as through they were two's complement representations and leave the result in register R
#### 6RST: 
ADD the bit patterns in registers S and T as through they represented values in floating-point notation and leave the floating-point result in register R
#### 7RST: 
OR the bit patterns in registers S and T and place the result in register R
#### 8RST: 
AND the bit patterns in registers S and T and place the result in register R
#### 9RST: 
EXCLUSIVE OR the bit patterns in registers S and T and place the result in register R
#### ARST: 
ROTATE the bit pattern in register R one bit to the right X times
#### BRXY: 
JUMP to the instruction located in the memory cell at address XY if the bit pattern in register R is equal to the bit pattern in register number 0. Otherwise, continue with the normal sequence of execution
#### C000: 
STOP
#### D0XY: 
INPUT value to memory location XY
#### E0XY: 
OUTPUT the value of memory location XY

## How to run the simulator
#### 1. Create an .txt file containing your machine code instruction. For the instruciton formate, Please refer to the file text.txt. That set of instructions will first LOAD the bit pattern found in memory 1A to register 2, and then STORE the bit pattern in register 23 to register. Lastly will tell the machine to stop.
#### 2. Load your .txt file through the "Browse" button
#### 3. Use "Step" button to observe the changes step by step or "Run" button to see the final result
