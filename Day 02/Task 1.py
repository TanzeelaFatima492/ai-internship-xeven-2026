"""
==============================================
Script Purpose:
    This script demonstrates Python's basic
    data types: int, float, bool, and str.
    It shows how to declare variables, check
    their types using type(), and perform
    type conversions between them.
Author  : Tanzeela
==============================================
"""

# DECLARE & INITIALIZE VARIABLES 

name   = "Tanzeela"  # str  — text value (use quotes)
age    = 22          # int  — whole number (no quotes)
blood  = 'A'         # str  — single char is still a str in Python
point  = 3.90        # float — decimal number
value  = True        # bool — True or False

# PRINT VALUES 

print("=" * 45)
print("        VARIABLE VALUES")
print("=" * 45)
print("Name  :", name)
print("Age   :", age)
print("Blood :", blood)
print("Point :", point)
print("Value :", value)

# PRINT TYPES

print("type(name)  :", type(name))
print("type(age)   :", type(age))
print("type(blood) :", type(blood))
print("type(point) :", type(point))
print("type(value) :", type(value))

# TYPE CONVERSION

print("TYPE CONVERSION")

# int → str
age_str = str(age)
print(type(age_str))

# str → float
point_str = "9.5"                  # string containing a number
point_flt = float(point_str)       # convert to float
print(type(point_flt))

# float → int 
point_int = int(point)
print(type(point_int))

# bool → int
val_int = int(value)               
print(type(val_int))


# MEMORY MODEL
x = 22         
y = x           
print(id(x) == id(y))   # True

x = 99         
print(id(x) == id(y))  

# MUTABLE
a = [1, 2, 3]
b = a           
b.append(4)
print(a)        # [1, 2, 3, 4]  
b = a.copy()    # real copy
b.append(99)
print(a)     
