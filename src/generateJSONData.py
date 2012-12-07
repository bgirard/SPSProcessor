import profileLoader
import functionStat
import os
import json

startupData = {}
shutdownData = {}
sequenceId = 0

def ComputeFunctionStats(startupData, id, profiles, functionName, lookFor, bugs=None):
  startupData[functionName] = { "sequence": id, "stats": functionStat.PrintStats(profiles, lookFor), "bugs": bugs }

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
ComputeFunctionStats(shutdownData, 1, shutdownProfiles, "PluginInstanceParent::Destroy", "mozilla::plugins::PluginInstanceParent::Destroy",
                     [["Bug 818265 - [Shutdown] Plug-in shutdown takes ~90ms on shutdown" ,"https://bugzilla.mozilla.org/show_bug.cgi?id=818265"]])
ComputeFunctionStats(shutdownData, 1, shutdownProfiles, "TelemetryPing.js", "TelemetryPing.js",
                     [["Bug 818274 - [Shutdown] Telemetry takes ~10ms on shutdown" ,"https://bugzilla.mozilla.org/show_bug.cgi?id=818274"]])
ComputeFunctionStats(shutdownData, 1, shutdownProfiles, "js::NukeCrossCompartmentWrappers", "js::NukeCrossCompartmentWrappers",
                     [["Bug 818296 - [Shutdown] js::NukeCrossCompartmentWrappers takes up 300ms on shutdown" ,"https://bugzilla.mozilla.org/show_bug.cgi?id=818296"]])
ComputeFunctionStats(shutdownData, 2, shutdownProfiles, "IncrementalCollectSlice", "IncrementalCollectSlice")
ComputeFunctionStats(shutdownData, 3, shutdownProfiles, "nsCycleCollector::BeginCollection", "nsCycleCollector::BeginCollection")
ComputeFunctionStats(shutdownData, 4, shutdownProfiles, "nsCycleCollector::FinishCollection", "nsCycleCollector::FinishCollection")
ComputeFunctionStats(shutdownData, 5, shutdownProfiles, "PresShell::Destroy", "PresShell::Destroy")
ComputeFunctionStats(shutdownData, 6, shutdownProfiles, "nsSHistory::EvictAllContentViewers", "nsSHistory::EvictAllContentViewers")
ComputeFunctionStats(shutdownData, 7, shutdownProfiles, "nsCSSStyleSheet::~nsCSSStyleSheet", "nsCSSStyleSheet::~nsCSSStyleSheet")

#startupData["AMP_startup"] = functionStat.PrintStats(startupProfiles, "AMP_startup (")
#startupData["ssi_onLoad"] = functionStat.PrintStats(startupProfiles, "ssi_onLoad (")
#startupData["BuildFontList"] = functionStat.PrintStats(startupProfiles, "gfxFontGroup::BuildFontList")
#startupData["MOZ_Z_inflate"] = functionStat.PrintStats(startupProfiles, "MOZ_Z_inflate")
#startupData["MOZ_Z_deflate"] = functionStat.PrintStats(startupProfiles, "MOZ_Z_deflate")

data = []
data.append( {"name": "Startup", "sequence": 0, "data": startupData} );
data.append( {"name": "Shutdown", "sequence": 1, "data": shutdownData} );

print "var jsonData = ",json.dumps(data),";"
