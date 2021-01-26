# needs definition of 'fingerprintfile', the output of 'fingerprint-Python3.py'

count = 0
ptr = 0
with open(fingerprintfile + ".txt","r") as f:
  f2 = open(fingerprintfile + "_0.txt", "w")
  for line in f:
    f2.write(line)
    count +=1
    if count == 45538:
      count = 0
      f2.close()
      ptr += 1
      f2 = open(fingerprintfile + "_" + str(ptr) + ".txt", "w")
f2.close()       
g.exit()