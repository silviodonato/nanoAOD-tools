import ROOT
import math, os,re, tarfile, tempfile
import numpy as np
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.JetPuId17 import JetPuId17

class jetPuId17Producer(Module):
    def __init__(self, jetBranchName):
        self.jetBranchName = jetBranchName
        self.lenVar = "n" + self.jetBranchName

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("%s_puId17" % self.jetBranchName, "I", lenVar=self.lenVar)

                        
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        jets = Collection(event, self.jetBranchName )
        jets_puId17 = []
        
        for jet in jets:
            jets_puId17.append(JetPuId17(jet.pt, jet.eta, jet.puIdDisc)) 
        
        self.out.fillBranch("%s_puId17" % self.jetBranchName, jets_puId17)

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
jetPuId17 = lambda : jetPuId17Producer("Jet")

