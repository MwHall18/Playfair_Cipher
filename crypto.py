import argparse

class RailFence:
    """ Encrypts / Decrypts using the RailFence Method """

    def __init__(self):
        """ Self Description """
        return

    def encrypt(self,plaintext):
        """ Encrypt RailFence message """
        msgLength = len(plaintext)
    
        evenChars = ""
        oddChars = ""
        for i in range(msgLength):
            if i % 2 == 0:
                evenChars = evenChars + plaintext[i]
            else:
                oddChars = oddChars + plaintext[i]
        ciphertext = oddChars + evenChars
        return ciphertext
    
    def decrypt(self,ciphertext):
        """ Decrypt Railfence message """
        halfLength = len(ciphertext) // 2
        oddText = ciphertext[:halfLength]  # from the beginning, up to the halfway point
        evenText = ciphertext[halfLength:]

        plaintext = ''
        for i in range(halfLength):
            plaintext = plaintext + evenText[i]
            plaintext = plaintext + oddText[i]

        if len(evenText) > len(oddText):
            plaintext = plaintext + evenText[-1]

        return plaintext

class Substitution:
    """ Encrypts / Decrypts using substitution """

    def __init__(self, key):
        """ Self Description """
        self.key = key

    def removePasswordDupes(password):
        """ Removes duplicate characters in password """
        newPassword = ''
        for ch in password:
            if ch not in newPassword:
                newPassword = newPassword + ch
        return newPassword

    def removeAlphabetDupes(alphabet, password):
        """ Removes duplicate characters in the alphabet we create """
        newAlphabet = ''
        for ch in alphabet:
            if ch not in password:
                newAlphabet = newAlphabet + ch
        return newAlphabet

    def create_playfair_grid(self, password):
        """ Creates the Playfair Grid """
        alphabet = "abcdefghiklmnopqrstuvwxyz "
        password = password.lower()
        password = password.replace('j', 'i')
        password = self.removePasswordDupes(password)
        splitChr = password[-1]
        splitIdx = alphabet.find(splitChr)
        afterStr = self.removeAlphabetDupes(alphabet[splitIdx+1:], password)
        beforeStr = self.removeAlphabetDupes(alphabet[:splitIdx], password)
        
        return password + afterStr + beforeStr 
    
    def encrypt(self, plaintext):
        """ Encrypt Playfair message """
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        ciphertext = ""
        for ch in plaintext:
            idx = alphabet.find(ch)
            ciphertext = ciphertext + self.key[idx]
        return ciphertext
    
    def decrypt(self, ciphertext):
        """ Decrypt Playfair message"""
        alphabet = "abcdefghijklmnopqrstuvwxyz "
        plaintext = ""
        for ch in ciphertext:
            idx = self.key.find(ch)
            plaintext += alphabet[idx]
        return plaintext

class Playfair:
    """ Encrypts / Decrypts using the WW2 Playfair Method """

    def removePasswordDupes(password):
        """ Remove any duplicate characters in password"""
        newPassword = ''
        for ch in password:
            if ch not in newPassword:
                newPassword = newPassword + ch
        return newPassword
    
    def xDupes(plaintext):
        """ Puts an x between two of the same chars in a row"""
        final = []
        prev = ''

        for i in plaintext:
            if i == prev:
                final.appent('x')
            final.append(i)
            prev = i

        return ''.join(final)

    def removeAlphabetDupes(alphabet, password):
        """ Remove any duplicate characters in alphabet """
        newAlphabet = ''
        for ch in alphabet:
            if ch not in password:
                newAlphabet = newAlphabet + ch
        return newAlphabet
    
    # I got a little lost making this project and in the help I found it was recommended to use like a grid search with the list I have made from the key
    def findPOS(keyList, character):
            for i in range(5):
                for j in range(5):
                    if keyList[i][j] == character:
                        return i, j

    def create_playfair_grid(self, password):
        """ Create the playfair grid"""
        alphabet = "abcdefghiklmnopqrstuvwxyz"
        password = password.lower()
        password = self.removeSpace(password)
        password = password.replace('j', 'i')
        password = self.removePasswordDupes(password)
        splitChr = password[-1]
        splitIdx = alphabet.find(splitChr)
        afterStr = self.removeAlphabetDupes(alphabet[splitIdx+1:], password)
        beforeStr = self.removeAlphabetDupes(alphabet[:splitIdx], password)
        
        return password + afterStr + beforeStr 

    def encrypt(self, plaintext, key):
        """ Encrypt Playfair message """

        # Key preperation
        key = key.replace(" ", "").lower()
        key = self.create_playfair_grid(key)
        keyList = []
        for i in key:
            keyList.append(i)
        
        # Encryption
        plaintext = plaintext.replace(" ", "").lower()
        plaintext = plaintext.replace("j", "i")

        plaintext = self.xDupes(plaintext)
        if (len(plaintext) % 2 != 0):
            plaintext = plaintext + 'x'

        # Creating pairs
        pairs = []
        for i in range(0, len(plaintext), 2):
            x = plaintext[i:i+2]
            pairs.append(x)

        # Translation
        cipher = ""
        for pair in pairs:
            #Found help on stackoverflow about the rows and columns to create the translation
            row1, col1 = self.findPOS(keyList, pairs[0])
            row2, col2 = self.findPOS(keyList, pairs[1])

            if row1 == row2:
                cipher += keyList[row1][(col1 + 1) % 5] + keyList[row2][(col2 + 1) % 5]
            elif col1 == col2:
                cipher += keyList[(row1 + 1) % 5][col1] + keyList[(row2 + 1) % 5][col2]
            else:
                ciphertext += keyList[row1][col2] + keyList[row2][col1]

        return cipher       
    
    def decrypt(self, ciphertext, key):
        """ Decrypt Playfair message"""

        # Key preperation
        key = key.replace(" ", "").lower()
        key = self.create_playfair_grid(key)
        keyList = []
        for i in key:
            keyList.append(i)

        # Traslation (Once I figured out the translation part, the opposite was easy)
        plaintext = ""
        for pair in [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]:
            row1, col1 = self.findPOS(keyList, pair[0])
            row2, col2 = self.findPOS(keyList, pair[1])
            
        if row1 == row2:
            plaintext += keyList[row1][(col1 - 1) % 5] + keyList[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += keyList[(row1 - 1) % 5][col1] + keyList[(row2 - 1) % 5][col2]
        else:
            plaintext += keyList[row1][col2] + keyList[row2][col1]
    
        return plaintext

def main():
    """ Main Program """

    pf = Playfair()

    parser = argparse.ArgumentParser(description="Playfair Cipher Encoder and Decoder")
    parser.add_argument("--algorithm", choices=["playfair"], required=True, help="Select the algorithm(only playfair)")
    parser.add_argument("--mode", choices=["encrypt", "decrypt"], required=True, help="Select the mode: encrypt or decrypt")
    parser.add_argument("--key", required=True, help="Enter the key for the Playfair cipher")
    parser.add_argument("--text", required=True, help="Enter the text to process")
    
    args = parser.parse_args() # My computer keeps erroring out on this line but I looked up tutorials on it / stackoverflow / chatGPT and they all say to do my main like this

    if args.algorithm == "playfair":
        key = args.key
        text = args.text
        
        if args.mode == "encrypt":
            result = pf.encrypt(text, key)
            print(result)
        elif args.mode == "decrypt":
            result = pf.decrypt(text, key)
            print(result)
    else:
        print("ERROR: Unsupported algorithm please select 'playfair'")


if __name__ == "__main__":
    main()
# The only part I had to get outside source of help on was the rows and columns part of the encryption