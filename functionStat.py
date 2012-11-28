import profileLoader

def PrintStats(profiles, symbolName):
  symbolStats = {};
  for profile in profiles:
    symbolId = profileLoader.FindSymbolID(profile, symbolName)
    symbolDuration = profileLoader.CalculateCost(profile, symbolId)
    symbolStats[profile['file']] = {}
    symbolStats[profile['file']]["duration"] = symbolDuration

  return symbolStats


