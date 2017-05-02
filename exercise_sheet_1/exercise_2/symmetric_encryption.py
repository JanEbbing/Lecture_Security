""" The exercise defines this function as the encryption function for a (constant) given key K_0.
"""
class given_encryption_function(object):

    FUNCTION_TABLE = { "0000" : "0000",
                       "0001" : "0001",
                       "0010" : "1001",
                       "0011" : "1110",
                       "0100" : "1111",
                       "0101" : "1011",
                       "0110" : "0111",
                       "0111" : "0110",
                       "1000" : "1101",
                       "1001" : "1100",
                       "1010" : "1100",
                       "1011" : "0101",
                       "1100" : "1010",
                       "1101" : "0100",
                       "1110" : "0011",
                       "1111" : "1000"
                   }
    
    def encrypt(self, message):
        """ Encrypts the given message with the encryption function.
        """
        return self.FUNCTION_TABLE[message]

class symmetric_encryption(object):
    """ Implements three different symmetric encryption modes.
    """

    @classmethod
    def ecb_mode( cls, encryption_function, message ):
        """ ECB mode simply applies the function to the message and returns the value.
        """
        if len(message) % 4 != 0:
            raise ValueError( "illegal message length, must be multiple of 4: %s" % message)
        message_chunks = [ message[i:i+4] for i in range(0, len(message), 4)]
        chiffre = ""
        for chunk in message_chunks:
            chiffre += encryption_function(chunk)
        return chiffre

    @classmethod
    def cbc_mode( cls, encryption_function, message, initialization_vector ):
        """ CBC Mode XORs the IV and the message, then encrypts it with the function, then XORS that chiffre
        to the next part of the message, encrypts it, uses that new chiffre to XOR again, etc.
        """
        if len(message) % 4 != 0:
            raise ValueError( "illegal message length, must be multiple of 4: %s" % message)
        message_chunks = [ message[i:i+4] for i in range(0, len(message), 4)]
        old_chiffre = initialization_vector
        complete_chiffre = ""
        for chunk in message_chunks:
            xor_result = xor_implementation(chunk,old_chiffre)
            old_chiffre = encryption_function(xor_result)
            complete_chiffre += old_chiffre
        return complete_chiffre

    @classmethod
    def ctr_mode( cls, encryption_function, message, initialization_vector ):
        """ CTR Mode in the i-th step takes the IV + i, encrypts it with the encryption function, and XORs
        that onto the message to get the chiffre
        """
        if len(message) % 4 != 0:
            raise ValueError( "illegal message length, must be multiple of 4: %s" % message)
        number_chunks = int(len(message)/4)
        chiffre = ""
        for i in range(0, number_chunks):
            secret = encryption_function( initialization_vector )
            initialization_vector = binary_add_one(initialization_vector)
            chiffre += xor_implementation( secret, message[4*i:4*i+4] )
        return chiffre

XOR_TABLE = { '0' : { '0' : '0', '1' : '1' }, '1' : { '0' : '1', '1' : '0' } }
def xor_implementation( number1, number2 ):
    """ Helper function to compute XOR of two "numbers"
    """
    if len(number1) != len(number2):
        raise ValueError("shouldnt happen, different length")
    result = ""
    for bit1,bit2 in zip(number1,number2):
        if bit1 != '0' and bit1 != '1':
            raise ValueError("bit1 is illegal: %c" % bit1)
        if bit2 != '0' and bit2 != '1':
            raise ValueError("bit2 is illegal: %c" % bit2)
        result += XOR_TABLE[bit1][bit2]
    return result

def binary_add_one( number ):
    """ Helper function to add 1 to a binary number (mod 16) """
    if len(number) != 4:
        raise ValueError("illegal length of number")
    if number[3] == '0':
        result = number[0:3]
        result += '1'
        return result
    if number[2] == '0':
        result = number[0:2]
        result += "10"
        return result
    if number[1] == '0':
        result = "" + number[0]
        result += "100"
        return result
    if number[0] == '1':
        return "0000"
    else:
        return "1000"

def main():
    """ Runs the exercise. IVs were chosen randomly beforehand. """
    enc_class = given_encryption_function()
    encryption_function = enc_class.encrypt

    message1 = "0100011101000001"
    message2 = "0100110101000001"
    print( "Using ECB mode for encryption........." )
    print( "Chiffre of message 1: %s" % symmetric_encryption.ecb_mode(encryption_function, message1) )
    print( "Chiffre of message 2: %s" % symmetric_encryption.ecb_mode(encryption_function, message2) )
    print( "Using CBC mode for encryption........." )
    iv = "0110"
    print( "Chiffre of message 1: %s" % symmetric_encryption.cbc_mode(encryption_function, message1, iv) )
    iv = "1010"
    print( "Chiffre of message 2: %s" % symmetric_encryption.cbc_mode(encryption_function, message2, iv) )
    print( "Using CTR mode for encryption........." )
    iv = "0001"
    print( "Chiffre of message 1: %s" % symmetric_encryption.ctr_mode(encryption_function, message1, iv) )
    iv = "1111"
    print( "Chiffre of message 2: %s" % symmetric_encryption.ctr_mode(encryption_function, message2, iv) )

if __name__ == "__main__":
    main()