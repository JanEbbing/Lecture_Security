from fractions import gcd
import random

def extended_euclidean(b, a):
    """ Computes the inverse to b in the multiplicative group Z_a.
    This means result*b = 1 mod a"""
    s = [1, 0]
    t = [0, 1]
    R = [a, b]
    A = [-1, -1, a]
    B = [-1, -1, b]
    R.append(A[-1]%B[-1])
    while R[-1] > 0:
        f = A[-1]//B[-1]
        A.append(B[-1])
        B.append(R[-1])
        s.append(s[-2]-f*s[-1])
        t.append(t[-2]-f*t[-1])
        R.append(A[-1]%B[-1])
    t = t[-1]
    while t < 0:
        t += a
    while t >= a:
        t -= a
    return t

def isPrime(n, k=5): # miller-rabin
    from random import randint
    if n < 2: return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0: return n == p
        s, d = 0, n-1
    while d % 2 == 0:
        s, d = s+1, d//2
    for i in range(k):
        x = pow(randint(2, n-1), d, n)
        if x == 1 or x == n-1: continue
        for r in range(1, s):
            x = (x * x) % n
            if x == 1: return False
            if x == n-1: break
        else: return False
    return True

def get_odd_random(k):
    result = random.randint(pow(2, k-2), pow(2,k-1))
    result << 1
    result += 1
    return result

def _random_prime_of_length(k):
    candidate = get_odd_random(k)
    while not isPrime(candidate):
        candidate = get_odd_random(k)
    return candidate
    
class RSA(object):
    """implements the RSA encryption algorithm. Please do not use this to encrypt anything remotely serious."""
    @classmethod
    def generation(cls, k):
        P = _random_prime_of_length(k)
        Q = _random_prime_of_length(k)
        while Q == P:
            Q = _random_prime_of_length(k)
        phi = (P-1)*(Q-1)
        e = random.randint(3, phi-1)
        while gcd(e, phi) != 1:
            e = random.randint(3, phi-1)
        d = extended_euclidean(e, phi)
        N = P * Q
        public_key = (N, e)
        secret_key = (N, d)
        return (public_key, secret_key)

    @classmethod
    def encryption(cls, public_key, message):
        (N, e) = public_key
        chiffre = pow(message, e, N)
        return chiffre

    @classmethod
    def decryption(cls, secret_key, chiffre):
        (N, d) = secret_key
        clear_text = pow(chiffre, d, N)
        return clear_text
