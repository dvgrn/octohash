import golly as g
import hashlib

# test pattern is 2b2o$b2obo$ob3o$o2bo$2bo$bo!, one answer is 3o4$12b2o$11b2o$8b2o3bo$7bobo$7b2o! at T=36

fingerprintfile = "C:/users/greedd/Desktop/buildconst/new-hash/octohashes2obj2x12b.txt"

NUMLINES = 455380
chardict = {}
for i in range(37, 127):
  chardict[i-37] = chr(i)

chardict[92-37] = "!"  # backslash
chardict[39-37] = "#"  # apostrophe
chardict[44-37] = "$"  # comma
  
# Python function to convert a cell list to RLE
# Author: Nathaniel Johnston (nathaniel@nathanieljohnston.com), June 2009.
#           DMG: Refactored slightly so that the function input is a simple cell list.
#                No error checking added.
#                TBD:  check for multistate rule, show appropriate warning.
#           AJP: Replace g.evolve(clist,0) with Python sort
# --------------------------------------------------------------------
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

def giveRLE(clist):
    # clist_chunks = list (chunks (g.evolve(clist,0), 2))
    clist_chunks = list(chunks(clist, 2))
    clist_chunks.sort(key=lambda l:(l[1], l[0]))
    mcc = min(clist_chunks)
    rl_list = [[x[0]-mcc[0],x[1]-mcc[1]] for x in clist_chunks]
    rle_res = ""
    rle_len = 1
    rl_y = rl_list[0][1] - 1
    rl_x = 0
    for rl_i in rl_list:
        if rl_i[1] == rl_y:
            if rl_i[0] == rl_x + 1:
                rle_len += 1
            else:
                if rle_len == 1: rle_strA = ""
                else: rle_strA = str (rle_len)
                if rl_i[0] - rl_x - 1 == 1: rle_strB = ""
                else: rle_strB = str (rl_i[0] - rl_x - 1)
                
                rle_res = rle_res + rle_strA + "o" + rle_strB + "b"
                rle_len = 1
        else:
            if rle_len == 1: rle_strA = ""
            else: rle_strA = str (rle_len)
            if rl_i[1] - rl_y == 1: rle_strB = ""
            else: rle_strB = str (rl_i[1] - rl_y)
            if rl_i[0] == 1: rle_strC = "b"
            elif rl_i[0] == 0: rle_strC = ""
            else: rle_strC = str (rl_i[0]) + "b"
            
            rle_res = rle_res + rle_strA + "o" + rle_strB + "$" + rle_strC
            rle_len = 1
            
        rl_x = rl_i[0]
        rl_y = rl_i[1]
    
    if rle_len == 1: rle_strA = ""
    else: rle_strA = str (rle_len)
    rle_res = rle_res[2:] + rle_strA + "o"
    
    return rle_res+"!"
# --------------------------------------------------------------------

def get9char(inputstr):
  h = hashlib.sha1()
  h.update(inputstr.encode())
  i = 0  # convert first seven bytes of SHA1 digest to an integer
  for char in h.digest()[:7]:
    i = i*256 + ord(char)
  s = ""
  while len(s)<9:
    d = i//90
    r = i - d*90
    s = chardict[r] + s
    i = (i - r) // 90   
  return s

def getoctohash(clist):
  ptr = 0
  g.new("Octotest"+str(count))
  for orientation in [[1,0,0,1],[0,-1,1,0],[-1,0,0,-1],[0,1,-1,0],[-1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,-1,-1,0]]:
    g.putcells(clist,ptr*2048,0,*orientation)
    ptr += 1
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
  return " " + get9char(minstr)

g.fitsel()
r = g.getselrect()
if r == []:
  g.exit("No selection.  Select something to find by fingerprint.")

count = NUMLINES
outptr = 0
pat = g.getcells(r)

g.addlayer()  # do tests in a new layer, then put results there
hash = getoctohash(pat)
g.new("Output")
g.putcells(pat,-pat[0]-32,-pat[1])

with open(fingerprintfile, "r") as f:
  for line in f:
    count -= 1
    if hash in line:
      matchingpat = line[:line.index(" ")]
      g.putcells(g.parse(matchingpat),outptr*32,0)
      outptr+=1
      g.fit()
      g.update()
    if count % 1000 == 0:
      g.show("Searching.  Lines remaining: " + str(count/1000) + "K lines.")
plural = "" if outptr==1 else "s"
g.show("Found " + str(outptr) + " line" + plural + " matching" + hash + " in " + str(NUMLINES) + " lines of " + fingerprintfile + ".")
