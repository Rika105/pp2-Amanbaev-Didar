import os

path = r'C:\Users\dasta\work\lab_6\lab6'

with open(path, 'r') as f:
    lines = f.readlines()
    print('Number of lines in {}: {}'.format(os.path.basename(path), len(lines)))