import json
import cPickle
import os
import sys

def GetProfiles(subfolder="startup"):
  dirList = os.listdir("../profiles/" + subfolder)
  profiles = [];
  for fname in dirList:
    if fname.endswith(".prof"):
      profile = LoadProfile(os.path.join("../profiles/" + subfolder, fname))

      if profile["format"] != "profileJSONWithSymbolicationTable,1":
        raise BaseException("Format not supported") 

      profiles.append(profile)

  return profiles

def LoadProfile(path_str):

  cache_path_str = path_str + ".cache"
  if not os.path.exists(cache_path_str):
    # Load a json file is slow (about x10 times vs cPickle)
    # so lets create a cache
    json_data=open(path_str).read()
    data = json.loads(json_data)

    FILE = open(cache_path_str, 'w')
    cPickle.dump(data, FILE)

  FILE = open(cache_path_str, 'r')
  data = cPickle.load(FILE)

  data["file"] = path_str

  return data

def SaveProfile(profile):
  path_str = profile["file"]
  cache_path_str = path_str + ".cache"

  with io.open(path_str, 'w') as outfile:
    data = json.dump(profile, outfile)

  FILE = open(cache_path_str, 'w')
  cPickle.dump(data, FILE)


def TruncateBeforeMarker(profile, markerName):
  c = 0
  samples = profile["profileJSON"]
  for sample in samples:
    if sample['extraInfo'] and "marker" in sample['extraInfo']:
      for markerInSample in sample['extraInfo']['marker']:
        if markerInSample == markerName and c > 0:
          del samples[:c]
          TruncateBeforeMarker(profile, markerName)
          return
    c = c + 1

def ProfileLength(profile):
  return len(profile["profileJSON"])

def CalculateCost(profile, symbol_ids):
  c = 0
  samples = profile["profileJSON"]
  for sample in samples:
    for frame in sample["frames"]:
      foundSample = False
      for symbol_id in symbol_ids:
        if frame == symbol_id:
          c = c + 1
          foundSample = True
          break;
      if foundSample:
        break;

  return c

def GetProfileDuration(profile):
  return profile["meta"]["interval"] * len(profile["profileJSON"])

def FindSymbolID(profile, symbol_name):
  symbolTable = profile['symbolicationTable'];
  for k, v in symbolTable.iteritems():
    if v.startswith(symbol_name):
      #sys.stderr.write(v + "\n")
      return int(k)
  #print symbol_name + " not found."
  return None

def FindSymbolIDs(profile, symbol_name):
  symbolTable = profile['symbolicationTable'];
  symbolIDs = []
  for k, v in symbolTable.iteritems():
    if v.startswith(symbol_name):
      symbolIDs.append(int(k))
      #sys.stderr.write(v + "\n")
  return symbolIDs

def SymbolName(profile, symbol_id):
  return profile['symbolicationTable'][str(symbol_id)].split(" + ")[0]

# Inflection points are defined as points in the profile tree that
# describe a non trivial number of samples that branch into 2 or more
# non trivial sub tree
#
#  100 func_a()
#  100  func_b() <-- Inflection point
#  85    func_c()
#  15    func_d()

def FindInflectionPoints(profile):

  inflectionPoints = []

  # Sort each element based on their symbol_id
  # comparing against an empty position is always greater
  def sampleCompare(a, b):
    a = a["frames"]
    b = b["frames"]
    for i in range(0, min(len(a), len(b))):
      diff = a[i] - b[i]
      if diff != 0: 
        return diff

    return len(a) - len(b) 

  samples = profile["profileJSON"]
  sortedSamples = sorted(samples, cmp=sampleCompare)

  currentState = []; # each entry is a tripple [symbol_id, counter, expensive_subtree]
  for i in range(0, len(sortedSamples)):
    frames = sortedSamples[i]["frames"]
    # Compare the sample vs the current state
    for j in range(0, len(frames)):
      frame = frames[j]
      if j >= len(currentState) or currentState[j][0] != frames[j]:
        if j > 0 and j < len(currentState) and currentState[j][1] > 5:
          # We have an expensive subtree
          #print SymbolName(profile, currentState[j][0]) 
          currentState[j-1][2] = currentState[j-1][2] + 1
          if currentState[j-1][2] > 0:
            #print ("\\" * j) + SymbolName(profile, currentState[j-1][0])
            inflectionPoints.append([currentState[j][0], frames[j]])
            print SymbolName(profile, currentState[j-1][0]) + " -> " + SymbolName(profile, currentState[j][0])
            print SymbolName(profile, currentState[j-1][0]) + " -> " + SymbolName(profile, frames[j])
        currentState = currentState[0:j]
        for k in range(j, len(frames)):
          currentState.append([frames[k], 1, 0])
        break;
      else:
        currentState[j][1] = currentState[j][1] + 1

def ExecutionTime(profile, symbol_id):
  samples = profile["profileJSON"]
  c = 0;
  for sample in samples:
    frames = sample["frames"]
    for frame in frames:
      if frame == symbol_id:
        c = c + 1;

  return c;
