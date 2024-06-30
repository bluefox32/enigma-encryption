import random
from sympy import primerange

class EnigmaMachine:
    def __init__(self, rotors, reflector, plugboard):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

    def encrypt(self, char):
        char = self.plugboard.swap(char)
        for rotor in self.rotors:
            char = rotor.forward(char)
        char = self.reflector.reflect(char)
        for rotor in reversed(self.rotors):
            char = rotor.backward(char)
        char = self.plugboard.swap(char)
        self.advance_rotors()
        return char

    def advance_rotors(self):
        # ローターの進行ロジック
        for i in range(len(self.rotors)):
            if not self.rotors[i].advance():
                break

class Rotor:
    def __init__(self, wiring, notch, position=0):
        self.wiring = wiring
        self.notch = notch
        self.position = position

    def forward(self, char):
        index = (ord(char) - ord('A') + self.position) % 26
        return chr((ord(self.wiring[index]) - ord('A') - self.position) % 26 + ord('A'))

    def backward(self, char):
        index = (self.wiring.index(char) - self.position) % 26
        return chr((index + ord('A')) % 26)

    def advance(self):
        self.position = (self.position + 1) % 26
        return self.position == ord(self.notch) - ord('A')

class Reflector:
    def __init__(self, wiring):
        self.wiring = wiring

    def reflect(self, char):
        return self.wiring[ord(char) - ord('A')]

class Plugboard:
    def __init__(self, wiring):
        self.wiring = wiring

    def swap(self, char):
        return self.wiring.get(char, char)

# 素数のリストを生成
prime_list = list(primerange(2, 1000))

# 素数ローターの数をランダムに選択
num_rotors = random.choice(prime_list)

# ローター設定例
rotor_wirings = [
    "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "BDFHJLCPRTXVZNYEIWGAKMUSQO"
]

notches = ["Q", "E", "V"]

# 素数個のローターを作成
rotors = [Rotor(rotor_wirings[i % 3], notches[i % 3]) for i in range(num_rotors)]

reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT")
plugboard = Plugboard({"A": "B", "B": "A"})

# エニグマ暗号機の作成
enigma = EnigmaMachine(rotors, reflector, plugboard)

# メッセージの暗号化例
message = "HELLOWORLD"
encrypted_message = ''.join([enigma.encrypt(c) for c in message])
print(f"Number of Rotors (Prime): {num_rotors}")
print(f"Encrypted Message: {encrypted_message}")