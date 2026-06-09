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

