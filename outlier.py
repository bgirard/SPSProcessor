import profileLoader

def PrintStats(profiles, symbolName):
  symbolDurations = [];
  durationTotal = 0;
  durationCount = 0;
  for profile in profiles:
    symbolId = profileLoader.FindSymbolID(profile, symbolName)
    symbolDuration = profileLoader.CalculateCost(profile, symbolId)
    symbolDurations.append([symbolDuration, profile['file']])
    durationTotal = durationTotal + symbolDuration;
    durationCount = durationCount + 1

  print symbolName, "Min: " + str(min(symbolDurations)), "Average: " + str(durationTotal / durationCount), "Max: " + str(max(symbolDurations))



