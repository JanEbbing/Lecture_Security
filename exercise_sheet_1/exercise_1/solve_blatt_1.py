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

# Languages the clear text is checked against
LANGUAGES = [ 'german', 'british', 'words' ] #, 'usa', 'spanish', 'french' ]
LANGUAGES_PREFIX = "/usr/share/dict/" # Where the dicts are stored
def find_best_solution( list_of_solutions ):
    ensure_dicts_exist( list_of_solutions )
    lang_dicts = {}
    solution_quality = {}
    for lang in LANGUAGES:
        lang_dicts[ lang ] = build_lang_dict( lang ) #FIXME: Currently uses a lot of memory if many languages are used. If many languages are possible it might be better to load a single language into memory, check all candidates, and iterate over the languages that way.
        solution_quality[ lang ] = {}
    for index, solution_candidate, language in [ ( index, solution_candidate, language ) for (index, solution_candidate) in enumerate( list_of_solutions ) for language in LANGUAGES ]:
        # Traverse the solution and find the number of words
        words_found = 0
        current_solution_index = 0
        current_lang_dict = lang_dicts[ language ]
        # find the shortest word at the index that's in the dictionary
        # If no such word exists, advance one letter. If it exists, advance to the end of the word
        while( True ):
            current_length = 1
            current_word_candidate = solution_candidate[ current_solution_index ]
            possible_words = current_lang_dict[ current_word_candidate ]
            while len( possible_words ) > 1 and current_word_candidate not in possible_words:
                current_word_candidate = solution_candidate[ current_solution_index:current_solution_index+current_length ]
                possible_words = current_lang_dict[ current_word_candidate ]
            #Either perfect match is found, or ambiguous match is found, or no match
            if not possile_words: #no match
                pass
                #FIXME: continue here


# Words below this length are not counted
IGNORE_LENGTH_BELOW = 3
def build_lang_dict( language ):
    import pygtrie
    lang_dict = pygtrie.StringTrie()
    with open( os.path.join( LANGUAGES_PREFIX, language ) ) as lang_file:
        for dict_entry in lang_file:
            if len( dict_entry ) >= IGNORE_LENGTH_BELOW:
                lang_dict[ dict_entry ] = dict_entry #Wastes a bit of memory, could be optimized with different Trie implementation

def ensure_dicts_exist( list_of_solutions ):
    basic_dict = os.path.join( LANGUAGES_PREFIX, "words" )
    if not os.path.exists(basic_dict) or not os.path.isfile(basic_dict):
        print "Please install the dictionary /usr/share/dict/words"
        print "Often this is done with the word utility program"
        print "I'm trying out the following languages, if they exist on your system %s" % LANGUAGES
        import time
        time.sleep(5)
        print "Here are the solution candidates: %s" % list_of_solutions
        exit(1)

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