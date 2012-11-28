import profileLoader
import outlier
import os

profiles = profileLoader.GetProfiles();
for profile in profiles:
  #print fname + " -> " + str(profileLoader.GetProfileDuration(profile)) + " ms"

  symbolId = profileLoader.FindSymbolID(profile, "ss_init");
  #print "  ss_init -> " + str(profileLoader.ExecutionTime(profile, symbolId)) + " ms"
  #profileLoader.FindInflectionPoints(profile)

outlier.PrintStats(profiles, "glTexSubImage2D_Exec (in GLEngine)")
outlier.PrintStats(profiles, "LayerManagerOGL::Render")
outlier.PrintStats(profiles, "ssi_restoreWindow (")
outlier.PrintStats(profiles, "ssi_onLoad (")
