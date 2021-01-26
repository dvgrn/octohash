import golly as g
import hashlib

infile = "C:/Users/{username}/Desktop/buildconst/new-hash/collisions-for-fingerprints-12x12-455380.txt"
outfile = "C:/users/{username/Desktop/buildconst/new-hash/fingerprints.txt"

chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma

def get9char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr)
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:7]:
    i = i*256 + ord(char)
  s = ""
  while len(s)<9:
    d = i/90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) / 90   
  return s

g.setrule("B3/S23")

with open(infile,"r") as f:
  all_coll = f.readlines()
count = 0
g.note("Total collisions = " + str(len(all_coll)))

with open(outfile, "w") as f2:
  for item in all_coll:
    testpat = g.parse(item.strip())
    ptr = 0
    g.new("Octotest"+str(count))
    for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
      g.putcells(testpat,ptr*2048,0,*orientation)
      ptr += 1

    fingerprint = ""
    for i in range(256):
      for j in range(8):
        g.select([2048*j-1024,-1024,2048,2048])
        g.shrink()
        r = g.getselrect()
        if r == []: r = [0,0,1,1]
        pat = g.getcells(r)
        deltax, deltay = 0, 0
        if pat != []:
          deltax, deltay = -pat[0], -pat[1]
        if j==0:
          minstr = str(g.transform(pat, deltax, deltay))
        else:
          strpat = str(g.transform(pat, deltax, deltay))
          if  strpat < minstr:
            minstr = strpat
      hash = " " + get9char(minstr)
      fingerprint += hash
      if hash in fingerprint[:-10]:
        break  # only collect fingerprints until the first duplicate
               # (this won't work right if a hash collision shows up in the same run,
               #  or if an RRO shows up, but until then I think we'll be good.)
      g.run(1)
    f2.write(item.strip() + fingerprint + "\n")
    count +=1
    if count % 10 == 0:
      g.show(str(count) + " :: " + fingerprint[:100])
      g.update()
  