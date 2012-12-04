import profileLoader
import functionStat
import os
import json

startupData = {}
sequenceId = 0

def ComputeFunctionStats(startupData, id, profiles, functionName, lookFor):
  startupData[functionName] = { "sequence": id, "stats": functionStat.PrintStats(profiles, lookFor) }

profiles = profileLoader.GetProfiles();

ComputeFunctionStats(startupData, 0, profiles, "Total", "")
ComputeFunctionStats(startupData, 1, profiles, "XRE Main Init", "XREMain::XRE_mainInit")
ComputeFunctionStats(startupData, 2, profiles, "NS_InitXPCOM", "NS_InitXPCOM")
ComputeFunctionStats(startupData, 3, profiles, "nsAppStartupNotifier", "nsAppStartupNotifier::Observe(")
ComputeFunctionStats(startupData, 4, profiles, "CreateHiddenWindow", "nsAppStartup::CreateHiddenWindow")
ComputeFunctionStats(startupData, 5, profiles, "BG_observe", "BG_observe")
ComputeFunctionStats(startupData, 6, profiles, "nsXULDocument::StartLayout", "nsXULDocument::StartLayout")
ComputeFunctionStats(startupData, 7, profiles, "AMP_startup", "AMP_startup")
ComputeFunctionStats(startupData, 8, profiles, "SocialUI_init", "SocialUI_init")
ComputeFunctionStats(startupData, 9, profiles, "ssi_onLoad", "ssi_onLoad")
ComputeFunctionStats(startupData, 10, profiles, "BuildFontList", "gfxFontGroup::BuildFontList")
ComputeFunctionStats(startupData, 11, profiles, "layout::Flush", "layout::Flush")

#startupData["AMP_startup"] = functionStat.PrintStats(profiles, "AMP_startup (")
#startupData["ssi_onLoad"] = functionStat.PrintStats(profiles, "ssi_onLoad (")
#startupData["BuildFontList"] = functionStat.PrintStats(profiles, "gfxFontGroup::BuildFontList")
#startupData["MOZ_Z_inflate"] = functionStat.PrintStats(profiles, "MOZ_Z_inflate")
#startupData["MOZ_Z_deflate"] = functionStat.PrintStats(profiles, "MOZ_Z_deflate")

data = []
data.append( {"name": "Startup", "sequence": 0, "data": startupData} );

print "var jsonData = ",json.dumps(data),";"
