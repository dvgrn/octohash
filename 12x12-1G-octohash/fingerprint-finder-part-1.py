# fingerprint-finder-part-1.py
import golly as g

# this script doesn't add a new layer, so it will overwrite whatever's in the current Golly universe

WIDTH = 12
HEIGHT = 12
LONG_ENOUGH = 32768
g.setrule("B3/S23")

# the next three lines are just a standard Python trick to figure out where the script is saved
import os
import sys
defaultfolder = os.path.abspath(os.path.dirname(sys.argv[0]))

# Change the next line to a hard-coded path if you don't want to have to
#   choose the constellations.txt file every time you run the script
constellation_fname = "C:/users/{username}/Desktop/buildconst/sorted12x12b/datapile.txt"

output_fname = "C:/users/{username}/Desktop/buildconst/sorted12x12b/collisions-for-fingerprints-12x12-blinkers-1G.txt"
  
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
glider = g.parse("3o$o$bo!")

# backup way for the script to work:  have user choose a text file containing constellations
if constellation_fname == "C:/users/{USERNAME}/Desktop/constellations.txt":  # don't edit the path in this line
   constellation_fname = g.opendialog("Open constellation list", "Text files (*.txt)|*.txt", \
                                      defaultfolder, "constellations.txt", False)
   if constellation_fname == "": g.exit("No constellation list found.  Script has exited.")

if output_fname == "C:/users/{USERNAME}/Desktop/output-collisions.rle":  # don't edit the path in this line
   output_fname = g.savedialog("Pick a place for the output file", "RLE files (*.rle)|*.rle", \
                                      defaultfolder, "output-collisions.rle", False)
   if output_fname == "": g.exit("No output filename provided.  Script has exited.")

# create an empty output file to append results to
with open(output_fname, "w") as outf:
  outf.write("x = 0, y = 0, rule = B3/S23\n")

x, y, count, match = 0, 0, 0, 0
s = ""
rlecount = 0
g.setrule("Interaction-prep")
with open (constellation_fname,"r") as f:
  rledata = f.readlines()
for rlestr in rledata:
  rlecount += 1
  if rlestr.startswith("#"):
    continue
  pat = g.parse(rlestr.replace("\n",""))
  mindiag, maxdiag = 99999,-99999
  for i in range(0,len(pat),2):
     diag = pat[i]-pat[i+1]
     if diag<mindiag: mindiag = diag
     if diag>maxdiag: maxdiag = diag
  s += str(rlecount) + "," + str(maxdiag + 5 + HEIGHT + 2 - (mindiag - 5 + HEIGHT + 2)) + "\n"
  for lane in range(mindiag - 5 + HEIGHT + 2, maxdiag + 5 + HEIGHT + 2):
    count += 1
    if count % 1000 == 0:  g.show(str(count))
g.setclipstr(s)
g.note(str(count))
"""
    g.new("Test")
    g.putcells(pat, x, y)
    g.run(1)
    g.setrule("Interaction-test")
    g.putcells(glider, lane, HEIGHT + 2)
#    g.fit()
#    g.update()
#    c = g.getevent()
#    while c != "key c none":
#      c = g.getevent()
#    c = ""

    refpop = g.getpop()
    curpop = refpop
    while curpop == refpop:
      pat = g.getcells(g.getrect())
      g.run(1)
      curpop = g.getpop()  # I know it's a string. The comparison will still work.
    g.new("Closest approach")
    g.putcells(pat)
    g.run(LONG_ENOUGH)
    g.setrule("Interaction-trim")
    g.run(1)
    if g.getrect() != []:
      g.new("Exclude this one")
      g.putcells(pat)
      g.setrule("Interaction-test")
    else:
      g.new("Run time")
      g.putcells(pat)
      g.setrule("Interaction-test")
      g.run(LONG_ENOUGH)
      p = g.getpop()
      g.run(12)
      if p != g.getpop():
        g.note("Found one...")
        g.exit()
        
    rle = giveRLE(g.getcells(g.getrect())).replace("\n","")

    
    # Make Golly update the screen every now and then
    if count % 1000 == 0:
      g.show("Matches so far: " + str([match,count]))
    #  g.fit()
    #  g.update()
      
    # TODO: replace the test in this next if statement with the tests from the pseudocode for clean OTTs and splitters
    # g.run(4096)
    # remainder = g.getcells([-120,-120,256,256])
    # if len(remainder) == 0:
    #   pop = int(g.getpop())
    #   if pop !=0:
    #     justgliders=1
    #     if pop % 5 == 0:
    #       for test in range(8):
    #         g.run(1)
    #         pop = int(g.getpop())
    #         if pop % 5 != 0:
    #           justgliders = 0
    #       # population only remains a multiple of 10 for 3 ticks at most if it's not a glider
    #     else:
    #       justgliders = 0
    #     if justgliders == 0:
    #       # These next three lines write a pattern to the chosen output file,
    #       #   so they should only be executed if a pattern passes the test
    #       with open(output_fname, "a") as outf:
    #         outf.write(rle + "$$$$$$$$$$$$$$$$$$$$$$$$$\n")
    #         match += 1
  
# just for the record, make the output file into valid RLE
# with open(output_fname, "a") as outf:
#   outf.write("!")
# g.open(output_fname)
g.show(str(count))
"""