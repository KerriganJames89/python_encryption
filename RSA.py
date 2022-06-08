#The program in this file is the individual work of JAMES KERRIGAN
import random
from datetime import datetime
random.seed(datetime.now())

 #Write a class called RSA that will contain all of the functions in the program. 
 #In the constructor for RSA initialize an empty list and set variables e and d to 0.
class RSA:

  def __init__(self):
    self.messages = []
    self.e = 0 
    self.d = 0

  #Write a function called inputFunc that reads in the number of entries from the user. Then, read in
  #those many values and add them to the list.
  def inputFunc(self):
    print ("Enter the amount of messages:")
    x = int(input())

    print ("Enter the messages:")
    for i in range(x):
      self.messages.append(int(input()))
    
    print ("Enter the minimum value for the prime numbers:")
    return int(input())

  #Write a function called printFunc that takes in a number and prints “message is ” followed by the number.
  def printFunc(func):
    def innerFunc(self, *arg, **kw):
      func(self, *arg)
      print("message is", *arg)

    return innerFunc

  #Write a generator function called primeGen that will take a minimum value as a parameter and then
  #yield the next prime numbers. Please note that this input parameter will be quite large and you
  #might want to use long if you’re using Python 2. 
  def primeGen(self, minimum):
    #big O(sqrt(N))
    #I made it just select the next two primes after the minimum instead of random to prevent
    #very, very large primes. I assume that's what's intended otherwise the assignment should have mentioned a range.
    x = 0
    while x != 2: 
      minimum += 1
      i = 2
      prime = True
      while i * i <= (minimum):
        if (minimum) % i == 0:
            prime = False
        i += 1
      if prime == True:
        x += 1
        #print ("prime is", minimum)
        yield minimum

  #Write a function called keyGen. This function will read in a minimum value from the user. 
  #Then, it will use the primeGen generator to get the next 2 prime numbers and generate the value N and the
  #keys e and d. Print e and N but not the other values. 
  def keyGen(self, minimum):
    x = self.primeGen(minimum)
    p = next(x)
    q = next(x)

    N = p * q
    phi_N = (p - 1)*(q - 1)

    #The public key value could range from anywhere from 1 to PHI N.
    while True:

      self.e = random.randint(1, (phi_N))

      if self.GCD(self.e, phi_N) == 1:
        break

    #Choosing the private key value is based greatly off the primes; larger primes can take longer to decrypt.
    self.d = self.modInverse(self.e, phi_N)

    
    #print ("Phi N is", phi_N)
    print ("N is", N)
    print ("e is", self.e)
    #print ("d is", self.d)
    return N


  #You would probably also need to write helper functions for the Lowest Common Multiple (LCM),
  #Greatest Common Divisor (GCD) and the Totient function.
  def GCD(self, num1, num2):
    if(num2 == 0): 
        return num1 
    else: 
        return self.GCD(num2,num1%num2)

  def LCM(self, num1, num2):
    return num1 * num2 / self.GCD(num1, num2)

  #EGCD and modInverse snippets from S/O
  def EGCD(self, num1, num2):
    if num1 == 0:
        return (num2, 0, 1)
    else:
        GCD, y, x = self.EGCD(num2 % num1, num1)
        return (GCD, x - (num2 // num1) * y, y)

  def modInverse(self, num, mod):
      g, x, y = self.EGCD(num, mod)
      if g != 1:
          return 0
      else:
          return x % mod
  
  #Returns the max bit value; used to set a range and prevent overflow (was used as a range for primes, but assignment reads as if the primes should be next to the minimum)
  def getMax(self, numBits, signed):
    if signed:
      numBits -= 1
    return 2**numBits - 1

  #Square and multiply function from asecuritysite.com that helps with calculating large exponents (I use the pow function instead)
  def expFunc(self, x, y):
    exp = bin(y)
    value = x
    for i in range(3, len(exp)):
      value = value * value
      if(exp[i:i+1]=='1'):
        value = value*x
    return value

  #Write a function called encrypt that takes in a number as a parameter and returns the RSA encrypted
  #value of the number.
  def encrypt(self, num, N):
    return int(pow(num, self.e, N))
    #return (self.expFunc(num, self.e) % N)
    #return num**self.e % N

  #Write a function called decrypt that takes in an encrypted number as a parameter and returns the
  #RSA decrypted value
  def decrypt(self, num, N):
    return int(pow(num, self.d, N))
    #return (self.expFunc(num, self.d) % N)
    #print (num**self.d % N)

  #Write a decorator function for printFunc that will print ”The encrypted ” before the printed message.
  @printFunc
  def deco1(self, num):
    print("The encrypted ", end="")

  #Write another decorator function for printFunc that will print “The decrypted ” before the printed message
  @printFunc
  def deco2(self, num):
    print("The decrypted ", end="")

  #Write a function called messages that calls inputFunc and keyGen and then, uses an iterator to
  #iterate through the list and encrypts each of the numbers using the encrypt function. Store the
  #results in another list. Then, go through the second list and print each encrypted number using the
  #decorator for the encrypted message.
  def messagesFunc(self):
    tempList = []
    N = self.keyGen(self.inputFunc())
    for i, m in enumerate(self.messages):
      tempList.append(self.encrypt(m, N))
      self.deco1(tempList[i])
    
    print("------------------------------------")
    for i, m in enumerate(tempList):
      self.deco2(self.decrypt(tempList[i], N))


if __name__ == '__main__':

  RSA = RSA()
  RSA.messagesFunc()


