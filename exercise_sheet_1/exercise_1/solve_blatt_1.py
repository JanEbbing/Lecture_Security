#! /usr/bin/env python

import collections
import sys

def read_from_file( filename ):
    with open( filename, 'r' ) as chiffre_file:
        content = []
        for line in chiffre_file:
            content.append( line )
    return ''.join(content)

def find_max_occurence(string_to_search):
    return collections.Counter(string_to_search).most_common(1)[0][0]
#flag = True
#def find_max_occurence(string):
#    global flag
#    if flag:
#        flag = False
#        return 'f'
#    else:
#        return 'g'

def main():
    read_file = 'Sicherheit_UE01_A1_Chiffre.txt'
    if len( sys.argv ) > 1:
        read_file = sys.argv[1]
    chiffre = read_from_file(read_file).lower()
    for k in range( 2, 20 ):
        # Assume codeword of length k
        clear_text = [ '' ] * len(chiffre)
        for i in range(0,k):
            cur_chiffre = chiffre[i::k]
            max_char = find_max_occurence(cur_chiffre) #guess this is e
            #print('max_char is %s' % max_char)
            offset = ord( 'e' ) - ord( max_char )
            #print("offset is %s" % offset)
            for index, letter in enumerate(cur_chiffre):
                new_char = ord(letter) + offset
                if new_char > 122:
                    new_char -= 26
                if new_char < 97:
                    new_char += 26
                clear_text[index*k + i] = chr( new_char )
        print( 'I believe the cleartext, assuming codeword length %s, is:' % k )
        print( ''.join(clear_text) )

if __name__ == "__main__":
    main()