import profileLoader
import functionStat
import os
import json

startupData = {}
shutdownData = {}
sequenceId = 0

def ComputeFunctionStats(startupData, id, profiles, functionName, lookFor):
  startupData[functionName] = { "sequence": id, "stats": functionStat.PrintStats(profiles, lookFor) }

startupProfiles = profileLoader.GetProfiles("startup");
shutdownProfiles = profileLoader.GetProfiles("shutdown");

for profile in shutdownProfiles:
  profileLoader.TruncateBeforeMarker(profile, "Shutdown start")
  #profileLoader.SaveProfile(profile)


ComputeFunctionStats(startupData, 0, startupProfiles, "Total", "")
ComputeFunctionStats(startupData, 1, startupProfiles, "XRE Main Init", "XREMain::XRE_mainInit")
ComputeFunctionStats(startupData, 2, startupProfiles, "NS_InitXPCOM", "NS_InitXPCOM")
ComputeFunctionStats(startupData, 3, startupProfiles, "nsAppStartupNotifier", "nsAppStartupNotifier::Observe(")
ComputeFunctionStats(startupData, 4, startupProfiles, "CreateHiddenWindow", "nsAppStartup::CreateHiddenWindow")
ComputeFunctionStats(startupData, 5, startupProfiles, "BG_observe", "BG_observe")
ComputeFunctionStats(startupData, 6, startupProfiles, "nsXULDocument::StartLayout", "nsXULDocument::StartLayout")
ComputeFunctionStats(startupData, 7, startupProfiles, "AMP_startup", "AMP_startup")
ComputeFunctionStats(startupData, 8, startupProfiles, "SocialUI_init", "SocialUI_init")
ComputeFunctionStats(startupData, 9, startupProfiles, "ssi_onLoad", "ssi_onLoad")
ComputeFunctionStats(startupData, 10, startupProfiles, "BuildFontList", "gfxFontGroup::BuildFontList")
ComputeFunctionStats(startupData, 11, startupProfiles, "layout::Flush", "layout::Flush")

ComputeFunctionStats(shutdownData, 0, shutdownProfiles, "Total", "")
ComputeFunctionStats(shutdownData, 1, shutdownProfiles, "PluginInstanceParent::Destroy", "mozilla::plugins::PluginInstanceParent::Destroy")
ComputeFunctionStats(shutdownData, 2, shutdownProfiles, "IncrementalCollectSlice", "IncrementalCollectSlice")
ComputeFunctionStats(shutdownData, 3, shutdownProfiles, "nsCycleCollector::BeginCollection", "nsCycleCollector::BeginCollection")
ComputeFunctionStats(shutdownData, 4, shutdownProfiles, "nsCycleCollector::FinishCollection", "nsCycleCollector::FinishCollection")

#startupData["AMP_startup"] = functionStat.PrintStats(startupProfiles, "AMP_startup (")
#startupData["ssi_onLoad"] = functionStat.PrintStats(startupProfiles, "ssi_onLoad (")
#startupData["BuildFontList"] = functionStat.PrintStats(startupProfiles, "gfxFontGroup::BuildFontList")
#startupData["MOZ_Z_inflate"] = functionStat.PrintStats(startupProfiles, "MOZ_Z_inflate")
#startupData["MOZ_Z_deflate"] = functionStat.PrintStats(startupProfiles, "MOZ_Z_deflate")

data = []
data.append( {"name": "Startup", "sequence": 0, "data": startupData} );
data.append( {"name": "Shutdown", "sequence": 1, "data": shutdownData} );

print "var jsonData = ",json.dumps(data),";"
