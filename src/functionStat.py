import profileLoader

def PrintStats(profiles, symbolName):
  symbolStats = [];
  for profile in profiles:
    symbolId = profileLoader.FindSymbolID(profile, symbolName)
    symbolDuration = profileLoader.CalculateCost(profile, symbolId)
    funcStat = {};
    funcStat['file'] = profile['file']
    funcStat['duration'] = symbolDuration
    symbolStats.append(funcStat)

  return symbolStats


