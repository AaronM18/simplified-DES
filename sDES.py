def getInput(lines = []):
  """ 
    Gets input from file input. Returns list of lines from input file
  """
  import fileinput
  return [ line.strip('\n') for line in fileinput.input() ]

class sDES:
  parseInt = lambda self, bit : int(bit)

  def subKeys(self, key: str) -> list:
    # Subkeys Permutations & extraction
    subkeyOne = [ key[0], key[6], key[8], key[3], key[7], key[2], key[9], key[5] ]
    subkeyTwo = [ key[7], key[2], key[5], key[4], key[9], key[1], key[8], key[0] ]
    
    return subkeyOne, subkeyTwo
    
  def mixingFunction(self, subKey: list, block: str) -> str:
    # Block Expansion
    expandBlock = lambda l : [ l[3], l[0], l[1], l[2], l[1], l[2], l[3], l[0] ]
    # S-boxes
    S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
    S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]
    # The 4-bit block expansion to 8-bits
    expandedBlock = expandBlock(block)
    # Parse str bits to int bits
    subKey, expandedBlock = map(self.parseInt, subKey), map(self.parseInt, expandedBlock)
    # XOR between subkey and expanded block
    xor = [ str(a ^ b) for a, b in zip(subKey, expandedBlock)]
    # Bits 0+3 and 1+2 are used as input to S0; bits 4+7 and 5+6 as input for S1
    row0, column0 = int( xor[0] + xor[3], 2), int( xor[1] + xor[2], 2)
    row1, column1 = int( xor[4] + xor[7], 2), int( xor[5] + xor[6], 2)
    # S-Box value  extraction
    sBoxValue = [ S0[row0][column0], S1[row1][column1]]
    # The outputs of S0 and S1 are converted to its binary value, concatenated and permuted
    sBoxValue = [ "%02d" % bit for bit in sBoxValue]
    sBoxValue = (lambda l: [ int(item) for sublist in l for item in sublist ])([binary for binary in sBoxValue])
    # Final permutation
    sBoxValue = [ sBoxValue[1], sBoxValue[3], sBoxValue[2], sBoxValue[0] ]

    return sBoxValue

  def rounds(self, key1: list, key2: list, block: str) -> str:
    # Initial Permutation
    initialPermutation = lambda b : [ b[1], b[5], b[2], b[0], b[3], b[7], b[4], b[6] ]
    # Inverse Initial Permutation 
    inversePermutation = lambda b : [ b[3], b[0], b[2], b[4], b[6], b[1], b[7], b[5] ]

    # Initial permutation
    permutedBlock = initialPermutation(block)
    # Block split
    left, right = permutedBlock[:4], permutedBlock[4:]
    print(left)
    mixinRes = self.mixingFunction(key1, left)
    xor = [ a ^ int(b)  for a, b in zip(mixinRes, left)]

    left, right = right, xor
    print(right)
    mixinRes = self.mixingFunction(key2, list(map( lambda i: str(i),right)))
    xor = [ a ^ int(b)  for a, b in zip(mixinRes, left)]
    print(mixinRes)
    
    pass

  def encrypt(self, key: str, message: str) -> str:
    key1, key2 = self.subKeys(key)
    return self.rounds(key1, key2, message)

  def decrypt(self, key: str, cypherText: str) -> str:
    key1, key2 = self.subKeys(key)
    return self.rounds(key2, key1, cypherText)


def main():
  sDes = sDES()
  lines = getInput()

  op = lines[0]
  key = lines[1]
  text = lines[2]

  if op == 'E':
    sDes.encrypt(key, text)
  elif op == 'D':
    sDes.decrypt(key, text)
  else:
    print('Wrong op')
  

main() if __name__ == "__main__" else None