import profileLoader
import functionStat
import os
import json

profiles = profileLoader.GetProfiles();

data = {}
data["ssi_onLoad"] = functionStat.PrintStats(profiles, "ssi_onLoad (")
data["LayerManagerOGL::Render"] = functionStat.PrintStats(profiles, "LayerManagerOGL::Render")

print "var jsonData = ",json.dumps(data),";"
