import sys

with open(sys.argv[1], 'r') as f:
    print(sum(sorted(sum(map(int, elf_string.split('\n'))) for elf_string in f.read().split('\n\n'))[-3:]))
