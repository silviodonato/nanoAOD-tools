import sys
from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB


config = Configuration()

version = "PROD_13_0"

datasetToTest = [ ## if empty, run on all datasets
    #"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/arizzi-RunIISummer16MiniAODv3_FSRmyNanoProdMc2017_NANOV4a_017_realistic_v14-v1-35a58109e00c38928fe6fe04f08bafb3/USER"] ## if empty, run on all datasets
]

requestsToSkip = [ ## if empty, run on all datasets
]

requestsToTest = [ ## if empty, run on all datasets
"PROD_13_0_vbfHmm_2017POWHERWIG7",
"PROD_13_0_vbfHmm_2017POWPY2",
] 

def getModuleSettingsFromSampleName(sample):
    if   "_2018" in sample: return 'mc2018'
    elif "_2017" in sample: return 'mc2017'
    elif "_2016" in sample: return 'mc2016'
    elif "Run2016" in sample: return 'data2016'
    elif "Run2017" in sample: return 'data2017'
    elif "Run2018A" in sample: return 'data2018A'
    elif "Run2018B" in sample: return 'data2018B'
    elif "Run2018C" in sample: return 'data2018C'
    elif "Run2018D" in sample: return 'data2018D'
    else: raise Exception("Unable to find module settings for %s"%dataset)

config.section_("General")
config.General.transferLogs=True
config.General.workArea = '/scratchssd/sdonato/crab'#+version
#config.General.workArea = '/afs/cern.ch/work/g/gimandor/public/testNANOAOD'#+version

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
#config.JobType.psetName = 'PSet1.py'
#config.JobType.maxMemoryMB=2500

config.JobType.inputFiles = ['crab_script_all.py','checker.py','../scripts/haddnano.py']

print "inputFiles ", config.JobType.inputFiles
config.JobType.sendPythonFolder         = True
config.section_("Data")
#config.Data.inputDataset = '/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'
#config.Data.inputDBS = 'global'
config.Data.inputDBS = 'phys03'
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset=True
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'EventAwareLumiBased'
#config.Data.unitsPerJob = 10
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1 ## for testing


config.Data.outLFNDirBase = '/store/user/sdonato/'+version+'/'
#config.Data.outLFNDirBase = '/store/user/gimandor/'+version+'/'
config.Data.publication = True
config.section_("Site")
config.Site.ignoreGlobalBlacklist = True
#config.Data.ignoreLocality = True
#config.Site.storageSite = "T2_IT_Bari"
config.Site.storageSite = "T2_IT_Legnaro"
#config.Site.storageSite = "T2_IT_Pisa"

#config.Data.ignoreLocality = True
#config.Site.whitelist = ['T2_US_*']

config.JobType.allowUndistributedCMSSW = True

data2016, data2017, data2018, mc2016, mc2017, mc2018 = dict(), dict(), dict(), dict(), dict(), dict()
datasetsNames = ["mc2016","mc2017","mc2018","data2016","data2017","data2018"]

#from datasetsAndreaV8_DataSignal import data2016, data2017, data2018, mc2016, mc2017, mc2018
#from datasetsAndreaV4_2017 import mc2017
#from datasetsAndreaV8_ForMassScan import mc2016, mc2017, mc2018
#from datasetsNanoV6_2016 import mc2016
#from datasetsNanoV6_2018 import mc2018
#from datasetsNanoV6_ForJerStudy_2016 import mc2016

from datasetsAndreaV10_DataSignal_2018 import mc2018
#from datasetsAndreaV8_DataSignal import mc2017
#from datasetsAndreaV4_2017 import mc2017
#from datasetsAndreaV8_ForMassScan import mc2017

from checker import checkDatasets
#checkDatasets(datasetsNames, globals())

from CRABAPI.RawCommand import crabCommand

requestNames = set()
if __name__ == '__main__':
    for datasetsName in datasetsNames:
        datasets = globals()[datasetsName]
        samples = datasets.keys()
        for sample in samples:
            for dataset in datasets[sample]:
                if type(dataset) != str: continue
#                print "New job"
                if datasetToTest and not dataset in datasetToTest: continue ## run only datasetToTest, if filled 
                config.Data.inputDataset = dataset
                config.Data.lumiMask = None
                if dataset == data2016 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'
                if dataset == data2017 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
                if dataset == data2018 : 
                    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'
                ext = ''
                if "_ext" in dataset: 
                    ext = '_ext' + dataset.split("_ext")[1][0]
                requestName = version + "_" + sample +  ext
                while requestName in requestNames:
                    requestName = requestName+"_"        
                requestNames.add(requestName)
		print requestName
                if requestName in requestsToSkip: continue
                #print "requestName and requestsToTest 1 ", requestName, requestsToTest
                if requestsToTest and not requestName in requestsToTest: continue ## run only requestsToTest, if filled 
                #print "requestName and requestsToTest 2 ", requestName, requestsToTest
                config.General.requestName = requestName
                config.Data.outputDatasetTag = version+"_"+dataset.split("/")[-2]
#                config.JobType.scriptExe = 'crab_script_%s.sh'%getModuleSettingsFromDataset(dataset)
                print "AAA ", sample
                config.JobType.scriptExe = 'crab_script_%s.sh'%getModuleSettingsFromSampleName(sample)
                print
                print config
                print
                try:
#                if True:
                    crabCommand('submit', config = config, dryrun = False) ## dryrun = True for local test
                    print "DONE"
                except:
                    print('crab submission failed. Move the the next job. %s'%requestName)
