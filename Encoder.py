import random
class RSA:
    def __init__(self, word):
        self.word = word

    def encrypt(self):
        AlphaBet = ['a', 'b', 'c',
                    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x',
                    'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+']
        newword = ""
        e = int("""[5
             38""")
        N = int("""38
        """)
        for i in range(len(self.word)):
            newword += AlphaBet[(AlphaBet.index(self.word[i]) ** e) % N]

        return newword
    def decrypt(self):
        AlphaBet = ['a', 'b', 'c',
                    'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x',
                    'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+']
        newword = ""
        d = 11
        N = 38
        for i in range(len(self.word)):
            newword += AlphaBet[(AlphaBet.index(self.word[i]) ** d) % N]

        return newword


def GetPassword():
    AlphaBet = ['a', 'b', 'c',
                'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-', '+']
    word = ""
    for i in range(16):
        r = random.randint(0, len(AlphaBet) - 1)
        word += AlphaBet[r]
    RSAword = RSA(word)

    return RSAword



