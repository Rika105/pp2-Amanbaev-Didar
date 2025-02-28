import os

path = r'C:\Users\dasta\work\lab_6\lab6\dir-and-files\ex06_A-Z_files'

if not os.path.exists(path):
   os.makedirs(path)

A = ord('A')
base = 'ex06_A-Z_files\\{}.txt'
for i in range(A, A+26):
    f = open(base.format(chr(i)), 'w')