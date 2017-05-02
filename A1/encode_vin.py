#!/usr/bin/env python

import sys

def compute_code(code):
    offset = [''] * len(code)
    for index,letter in enumerate(code):
        offset[index] = ord(letter) - ord('a')
    return offset

def read_from_file(filename):
    with open( filename, 'r' ) as chiffre_file:
        content = []
        for line in chiffre_file:
            content.append( line )
    return ''.join(content)

def write_to_file( filename, content ):
    with open(filename, 'w') as write_file:
        write_file.write(content)

def encode_letter(index,letter,code):
    index = index % len(code)
    new_char = ord(letter) + code[index]
    if new_char > 122:
        new_char -= 26
    if new_char < 97:
        new_char += 26
    return chr(new_char)

def main():
    filename = sys.argv[1]
    clear_text = read_from_file(filename).lower()
    code = sys.argv[2]
    code = compute_code( code )
    result = [''] * len(clear_text)
    for index,letter in enumerate(clear_text):
        result[index] = encode_letter(index,letter,code)
    result = ''.join(result)
    write_to_file( 'chiffre.txt', result )

if __name__ == '__main__':
    main()