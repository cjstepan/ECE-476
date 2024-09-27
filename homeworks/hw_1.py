# --------------- Problem 1 ---------------
# Variable Declarations
R1 = 200
R2 = 300
R3 = 450
R4 = 75
R5 = 250
R6 = 50

# Calculations
R7 = R1 + R2
R8 = (1/R7 + 1/R3)**-1
R9 = R8 + R4
R10 = (1/R9 + 1/R5)**-1
R11 = R10 + R6
print(f'1) Rab = {R11:.3f} Ohms')

# --------------- Problem 2 ---------------
# Variable Declarations
R1 = 200
R1_1 = 50
R2 = 300
R2_1 = 75
R3 = 400
R3_1 = 125
I0 = 10 #Amps

I1 = ((1/R1) / (1/(R1 + R1_1) + 1/(R2 + R2_1) + 1/(R3 + R3_1))) * I0
I2 = ((1/R2) / (1/(R1 + R1_1) + 1/(R2 + R2_1) + 1/(R3 + R3_1))) * I0
I3 = I0 - I1 - I2

print(f'\n2) I1 = {I1:.3f}A')
print(f'   I2 = {I2:.3f}A')
print(f'   I3 = {I3:.3f}A')

# --------------- Problem 3 ---------------
# Variable Declarations
R1 = 50
R2 = 200
R3 = 75
R4 = 300
R5 = 125
R6 = 400
V0 = 10 #Volts

# Calculations
R_1 = (R4 * (R5 + R6)) / (R4 + (R5 + R6))
R_2 = (R2 * (R_1 + R3)) / (R2 + (R_1 + R3))
V1 = (R_2 / (R_2 + R1)) * V0
V2 = (R_1 / (R_1 + R3)) * V1
V3 = ((R6) / (R5 + R6)) * V2
print(f'\n3) R_1 = {R_1:.3f} Ohms') #makes visualising things easier
print(f'   R_2 = {R_2:.3f} Ohms')   #makes visualising things easier
print(f'   V1 = {V1:.3f}V')
print(f'   V2 = {V2:.3f}V')
print(f'   V3 = {V3:.3f}V')

# --------------- Problem 4 ---------------
# Variable Declarations
j = (-1) ** 0.5
R1 = 20
R2 = 30
R3 = 40
R4 = 100
L1 = j * 100
L2 = j * 200
C1 = j * -150

# Calculations
Z1 = ((R4 * L2) / (R4 + L2)) + R3
Z2 = ((C1 * Z1) / (C1 + Z1)) + R2
Zab = ((L1 * Z2) / (L1 + Z2)) + R1
print(f'\n4) Zab = {Zab} Ohms')
