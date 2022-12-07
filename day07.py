import sys
from collections import defaultdict

folder_sizes = defaultdict(int)
pwd_list = []
with open(sys.argv[1], 'r') as f:
    for line in f:
        tokens = line.strip().split()
        if tokens[0] == '$':  # commands
            cmd = tokens[1]
            if cmd == 'cd':
                param = tokens[2]
                if param == '..':
                    del pwd_list[-1]
                else:
                    new_folder = param.split('/')
                    if param == '/':
                        pwd_list = []
                    else:
                        pwd_list.extend(new_folder)
        else:  # output
            if tokens[0].isnumeric():
                file_size = int(tokens[0])
                parent_folder = '/'
                folder_sizes[parent_folder] += file_size
                for folder in pwd_list:
                    parent_folder += folder + '/'
                    folder_sizes[parent_folder] += file_size

# part1
MAX_FOLDER_SIZE = 100000
print(sum(s for s in folder_sizes.values() if s <= MAX_FOLDER_SIZE))

# part2
TOTAL_DISK_SPACE = 70000000
SIZE_NEEDED = 30000000

free_space = TOTAL_DISK_SPACE - folder_sizes['/']
min_remove_size = SIZE_NEEDED - free_space
print(min(s for s in folder_sizes.values() if s >= min_remove_size))
