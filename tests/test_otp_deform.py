import unittest
from exercise_sheet_1.exercise_3.onetimepad_deformer import otp_deform, \
    otp_deform_string, int_to_hex_string, hex_string_to_int

class TestOTPDeformer(unittest.TestCase):

    def test_exercise_from_lecture(self):
        old_cleartext=0x434F4D504C4558494659
        new_cleartext=0x444F4B544F524D455441
        old_chiffre  =0xDFC071428A90170E1412

        #Calculated by hand
        manual_solution=0x070006040317150C1218
        
        self.assertEquals(otp_deform(old_chiffre,old_cleartext,
                                     new_cleartext),
                          (old_chiffre ^ manual_solution,
                           manual_solution))

    def test_exercise_from_lecture_string(self):
        old_cleartext="434F4D504C4558494659"
        new_cleartext="444F4B544F524D455441"
        old_chiffre  ="DFC071428A90170E1412"

        #Calculated by hand
        manual_solution="070006040317150C1218"

        hex_prefix='0x'
        expected=[hex(0xDFC071428A90170E1412 ^ 0x070006040317150C1218).lstrip(hex_prefix),
                  hex(0x070006040317150C1218).lstrip(hex_prefix)]
        #Ugly hack to avoid python removing leading zero
        expected=[ "0"+x if len(x)%2==1 else x for x in expected]
        self.assertEquals(otp_deform_string(old_chiffre,old_cleartext,
                                     new_cleartext), expected)

if __name__ == '__main__':
    unittest.main()