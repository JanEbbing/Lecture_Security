from asymmetric.rsa import RSA

import random
import os
import unittest

random.seed()

SECURITY_PARAMETER=128
class BasicScenario(object):
    def __init__(self, gen, enc, dec):
        self.gen = gen
        self.enc = enc
        self.dec = dec

    def generate_keys(self, k):
        """ To be implemented by the subclasses """
        pass

    def alice_send_to_bob(self, assertobject, message=0):
        """ To be implemented by the subclasses """
        pass

    def bob_send_to_alice(self, assertobject, message=0):
        """ To be implemented by the subclasses """
        pass

class Symmetric_Case(BasicScenario):
    def generate_keys(self, k):
        self.shared_secret = random.getrandbits(k)

    def alice_send_to_bob(self, assertobject, message=0):
        if not message:
            message = 4892571
        chiffrat = self.enc(self.shared_secret, message)
        cleartext = self.dec(self.shared_secret, chiffrat)
        assertobject.assertEquals(cleartext, message, "Decryption failed")
        return (chiffrat, cleartext)

    def bob_send_to_alice(self, assertobject, message=0):
        if not message:
            message = 1938595181312
        chiffrat = self.enc(self.shared_secret, message)
        cleartext = self.dec(self.shared_secret, chiffrat)
        assertobject.assertEquals(cleartext, message, "Decryption failed")
        return (chiffrat, cleartext)

class Asymmetric_Case(BasicScenario):
    def generate_keys(self, k):
        (pk_al, sk_al) = self.gen(k)
        (pk_bob, sk_bob) = self.gen(k)
        self.pk_alice = pk_al
        self.sk_alice = sk_al
        self.pk_bob = pk_bob
        self.sk_bob = sk_bob

    def alice_send_to_bob(self, assertobject, message=0):
        if not message:
            message = 4892571
        chiffrat = self.enc(self.pk_bob, message)
        cleartext = self.dec(self.sk_bob, chiffrat)
        assertobject.assertEquals(cleartext, message, "Decryption failed")
        return (chiffrat, cleartext)

    def bob_send_to_alice(self, assertobject, message=0):
        if not message:
            message = 1938595181312
        chiffrat = self.enc(self.pk_alice, message)
        cleartext = self.dec(self.sk_alice, chiffrat)
        assertobject.assertEquals(cleartext, message, "Decryption failed")
        return (chiffrat, cleartext)

class EncryptionTests(unittest.TestCase):
    def setUp(self):
        self.scenario_rsa = Asymmetric_Case(RSA.generation, RSA.encryption, RSA.decryption)
        self.scenario_rsa.generate_keys(SECURITY_PARAMETER)
        #self.scenario_des = Symmetric_Case(des_gen, des_enc, des_dec)
        #self.scenario_des.generate_keys(SECURITY_PARAMETER)

    def test_keygen_rsa(self):
        scenario = Asymmetric_Case(RSA.generation, RSA.encryption, RSA.decryption)
        scenario.generate_keys(SECURITY_PARAMETER)
        for (N, key) in [scenario.pk_alice, scenario.sk_alice, scenario.pk_bob, scenario.sk_bob]:
            assert isinstance(key, (int, float, complex))
            assert isinstance(N, (int, float, complex))

    @unittest.skip("not implemented")
    def test_keygen_des(self):
        scenario = Symmetric_Case(des_gen, des_enc, des_dec)
        scenario.generate_keys(SECURITY_PARAMETER)
        assert isinstance(scenario.shared_secret, (int, float, complex))

    def send_messages(self, scenario):
        (chiffre_al, cleartext_al) = scenario.alice_send_to_bob(self)
        (chiffre_bob, cleartext_bob) = scenario.bob_send_to_alice(self)
        self.assertNotEquals(chiffre_al, cleartext_al, "Sending cleartext")
        self.assertNotEquals(chiffre_bob, cleartext_bob, "Sending cleartext")
        string_length = 1024
        (chiffre_al, cleartext_al) = scenario.alice_send_to_bob(self, random.randint(10000000, 1000000000))
        (chiffre_bob, cleartext_bob) = scenario.bob_send_to_alice(self, random.randint(10000000, 1000000000))

    def test_send_messages_rsa(self):
        self.send_messages(self.scenario_rsa)

    @unittest.skip("not implemented")
    def test_send_messages_des(self):
        self.send_messages(self.scenario_des)