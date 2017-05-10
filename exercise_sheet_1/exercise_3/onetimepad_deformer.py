""" Implements a deformation attack against One-time-pads.

It receives the chiffre sent over the wire, the cleartext of this
chiffre and the desired new content of the message and puts out
the modified chiffre that can be sent to the victim.
"""

import sys

def hex_string_to_int(hex_string):
    strip_prefix = '0x'
    result=hex_string.lstrip(strip_prefix)
    result=int.from_bytes(bytes.fromhex(result),
                          byteorder=sys.byteorder)
    return result

def int_to_hex_string(integer):
    result = integer.to_bytes((integer.bit_length()+7)//8,
                              byteorder=sys.byteorder).hex()
    return result

def otp_deform_string(cur_chiffre, cur_cleartext, new_cleartext):
    """ Same as otp_deform, except all arguments have to be strings
    and will be converted. The return values will also be Strings.
    Note that the 0x prefix is not needed, it will be stripped.
    """
    args = [ cur_chiffre, cur_cleartext, new_cleartext ]
    args = [ hex_string_to_int(argument) for argument in args ]
    (byte_new_chiffre, byte_diff) = otp_deform( *args )
    results = [byte_new_chiffre, byte_diff]
    results = [int_to_hex_string(res) for res in results]
    return results

def otp_deform(cur_chiffre, cur_cleartext, new_cleartext):
    """ Returns the tuple (new_chiffre, diff) with diff being what you
    have to XOR to the current chiffre to get the new chiffre.
    All arguments have to be ints.
    """
    x = cur_cleartext ^ new_cleartext
    new_chiffre = cur_chiffre ^ x
    return (new_chiffre, x)

if __name__== "__main__":
    if len(sys.argv) != 4:
        print("USAGE: onetimepad_deformer.py chiffre cleartext new_cleartext")
        exit(1)
    else:
        (new_chiffre, diff)=otp_deform_string(*sys.argv[1:4])
        print("Here are my results:")
        print("The new chiffre that should be sent to the victim is %s" % new_chiffre)
        print("The difference vector X that has to be XOR'd to any chiffre text of this clear text is %s"%diff)
