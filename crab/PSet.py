#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
#"root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv5/ZJJtoMuMu_EWK_SM_5f_NLO_TuneCUETP8M1_13TeV_powheg-pythia8/NANOAODSIM/PUMoriond17_Nano1June2019_102X_mcRun2_asymptotic_v7-v1/20000/02B352FE-ABF6-494C-9AA7-09BC7EF3A704.root"
#"root://cms-xrd-global.cern.ch//store/user/arizzi/FSRNANO2016MCV7a/VBFHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnlo_pythia8/RunIISummer16MiniAODv3_FSRNANO2016MCV7a_un2_asymptotic_v3-v1/191212_092143/0000/myNanoProdMc2016_NANO_1.root"
#"vbfHmm_2016POWPY.root"
#"file:///scratchssd/sdonato/Delphes/VBFHToMuMu_M125_14TeV_powheg_pythia8_11.root"
#"file:///scratchssd/sdonato/fileSkimFromNanoAOD/SingleMuon_Run2016C_NANOAOD_02Apr2020_25DB115F-B447-8447-BE02-48F35AC42163.root" #"root://cms-xrd-global.cern.ch//store/data/Run2016C/SingleMuon/NANOAOD/02Apr2020-v1/20000/25DB115F-B447-8447-BE02-48F35AC42163.root", ## Run2016C/SingleMuon, NanoAODv7
"file:///scratchssd/sdonato/fileSkimFromNanoAOD/VBFHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnlo_pythia8_mc2018_RunIIAutumn18NanoAODv7_NANOAODSIM_Nano02Apr2020_102X_upgrade2018_realistic_v21-v1_FF8D5716-D133-4F40-A5FF-51D4BC30949A.root" ## Taken from /store/mc/RunIIAutumn18NanoAODv7/VBFHToMuMu_M125_TuneCP5_PSweights_13TeV_amcatnlo_pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/130000/FF8D5716-D133-4F40-A5FF-51D4BC30949A.root, ### MC2018, NanoAODv7
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)








