#!/usr/bin/env python3

import argparse

def gen_num_sys(n, m, prefix = None):
    prefix = prefix or []
    if m == 0:
        print(prefix)
        return
    for i in range(n):
        prefix.append(i)
        gen_num_sys(n, m - 1, prefix)
        prefix.pop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="help args")
    parser.add_argument("-n", type=int, help="numeral system")
    parser.add_argument("-m", type=int, help="number of characters")
    args = parser.parse_args()

    try:
        n = args.n or int(input("numeral system: "))
        m = args.m or int(input("number of characters: "))
        gen_num_sys(n, m)
    except ValueError as no_int:
        print("wrong input", no_int)
        

    


    
