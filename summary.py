import profileLoader
import os

dirList = os.listdir("../profiles/")
for fname in dirList:
  if fname.endswith(".prof"):
    profile = profileLoader.LoadProfile(os.path.join("../profiles/", fname))

    if profile["format"] != "profileJSONWithSymbolicationTable,1":
      raise BaseException("Format not supported")

    #print fname + " -> " + str(profileLoader.GetProfileDuration(profile)) + " ms"

    symbolId = profileLoader.FindSymbolID(profile, "ss_init");
    #print "  ss_init -> " + str(profileLoader.ExecutionTime(profile, symbolId)) + " ms"
    profileLoader.FindInflectionPoints(profile)

