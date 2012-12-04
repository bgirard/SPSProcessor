import profileLoader

def PrintStats(profiles, symbolName):
  symbolStats = [];
  for profile in profiles:
    if symbolName == "":
      symbolDuration = profileLoader.ProfileLength(profile)
    else:
      symbolIds = profileLoader.FindSymbolIDs(profile, symbolName)
      if symbolIds:
        symbolDuration = profileLoader.CalculateCost(profile, symbolIds)
      else:
        symbolDuration = 0
    funcStat = {};
    funcStat['file'] = profile['file']
    funcStat['duration'] = symbolDuration
    funcStat['symbolName'] = symbolName
    symbolStats.append(funcStat)

  return symbolStats


