nprocesses = 32
version = "PROD_12_0"
folder = "/home/users/sdonato/scratchssd/fileSkimFromNanoAOD"
server = "t2-xrdcms.lnl.infn.it:7070"
haddPath = "/home/users/sdonato/scratchssd/Skim/CMSSW_10_2_6/src/PhysicsTools/NanoAODTools/scripts/haddnano.py"
datasetsNames = ["data2018", "mc2018", "data2017", "mc2017", "data2016", "mc2016"]

import subprocess
import os

data2016, data2017, data2018, mc2016, mc2017, mc2018 = dict(), dict(), dict(), dict(), dict(), dict()
#from datasetsAndreaV8_DataSignal import data2016, data2017, data2018, mc2016, mc2017, mc2018
#from datasetsAndreaV8_ForMassScan import mc2016, mc2017, mc2018
#from datasetsNanoV6_2018 import mc2018
#from datasetsAndreaV4_2017 import mc2017
#from datasetsNanoV6_2016 import mc2016
#from datasetsNanoV6_ForJerStudy_2016 import mc2016

selection = [
    "SingleMuonRun2018D",
    "SingleMuonRun2018A",
    "SingleMuonRun2018B",
    "vbfHmm_2016AMCHERWIG",
    "SingleMuonRun2016",
    "ggHmm_2018POWPY",
    "SingleMuonRun2017",
    "ggHmm_2016POWPY",
    "DY_2016AMCPY",
    "DY_2016AMCHERWIG",
    "DY_2016MGPY",
    "STtbar_2018POWPY",
    "ZZ2l2n_2018POWPY",
    "TT_2018AMCPY",
    "W0J_2018AMCPY",
    "DY105_2018AMCPY",
    "ZZ4l_2018POWPY",
    "DY3J_2018MGPY",
    "ZZ2l2q_2018POWPY",
    "WWlnqq_2018POWPY",
    "DY1J_2018MGPY",
    "DY105_2018MGPY",
    "DY2J_2018AMCPY",
    "DY0J_2018AMCPY",
    "STt_2018POWPY",
    "TTsemi_2018POWPY",
    "DYM50_2018AMCPY",
    "TThad_2018POWPY",
    "DY2J_2016AMCPY",
    "TTsemi_2016POWPY",
    "DY105VBF_2016AMCPY",
    "TTlep_2016POWPY",
    "TT_2016POWPY",
    "TTlep_2016MGPY",
    "TThad_2016POWPY",
    "DYM50_2016AMCPY",
    "W2J_2016AMCPY",
    "DY105_2016AMCPY",
    "WZ2l2n_2016AMC_MADSPIN_PY",
    "DY1J_2016AMCPY",
    "DY0J_2016AMCPY",
    "DY105_2016MGPY",
    "W2J_2017AMCPY",
    "DY105_2017AMCPY",
    "W1J_2017AMCPY",
    "STt_2017POWPY",
    "W0J_2017AMCPY",
    "ZZ4l_2017POWPY",
    "DY2J_2017AMCPY",
    "DY105VBF_2016AMCPY"
]

from checker import checkDatasets
#checkDatasets(datasetsNames, globals())

#suffix = "_nano"+Y+".root"
#year = "_" + Y
#suffix = ".root"
#year = "

outputFolder = folder + "/" + version

os.system("mkdir -p %s"%outputFolder)

def haddSample((sample, datasets)):
    if (len(selection)>0) and not (sample in selection): return 
    print "Running %s"%sample
    script = 'python $CMSSW_BASE/src/PhysicsTools/NanoAODTools/scripts/haddnano.py %s/%s.root'%(folder,sample)
    folderSample = outputFolder + "/"+ sample
    os.popen("mkdir -p %s"%(folderSample))
    scriptPath = "%s/script.sh"%(folderSample)
    script = open(scriptPath,'w')
    print "Creating script.sh in %s"%(scriptPath)
    script.write("cd %s\n"%folderSample)
    for dataset in datasets:
        if not dataset: continue
        script.write("\n### DATASET: %s ###\n"%dataset)
        datasetPrimary = dataset.split("/")[1]
        datasetTag = dataset.split("/")[2]
        command = "xrdfs %s ls -u -R /store/user/sdonato/%s/%s/%s_%s | grep tree | grep -v failed "%(server, version,datasetPrimary,version,datasetTag)
        script.write("# %s \n"%command)
        try:
            xrootdFileNames = os.popen ( command ).read().split("\n")
#            xrootdFileNames = xrootdFileNames[:2]
        except:
            xrootdFileNames = []
        for i, xrootdFileName in enumerate(xrootdFileNames):
            if ".root" in xrootdFileName:
                outputFile = "%s_%s_%s.root"%(datasetPrimary, datasetTag, xrootdFileName.split(".root")[0].split("_")[-1])
                #print(outputFile) 
                #script.write("rm -f %s && xrdcp %s %s\n"%(outputFile, xrootdFileName, outputFile))
                script.write("xrdcp %s %s\n"%(xrootdFileName, outputFile))
    outputFile = "%s.root"%(sample)
    script.write('''
if [ `find -cmin -120 | grep root | wc -l` != '0' ]
    then rm -f %s && python %s %s *.root && mv %s ..
fi
'''%(outputFile, haddPath, outputFile, outputFile))
#        script.write('rm %s/%s/*root\n'%(outputFolder, sample))
    script.close()
    script = open(scriptPath,'r')
#    print script.read()
    script.close()
    command = "source %s/script.sh >& %s/logScript"%(folderSample,folderSample)
    print command
    try:
#            log = subprocess.Popen ( command , shell=True)
#            subprocess.communicate()
        log = os.popen ( command )
        log = log.read()
        print "DONE %s \n See  %s/logScript"%(sample, folderSample)
    except:
        print "ERROR in %s \n Please check %s/logScript"%(sample, folderSample)
    print

allSamples = []

for datasetsName in datasetsNames:
    datasets = globals()[datasetsName]
    samples = datasets.keys()
    for sample in samples:
#        if not sample in [
#    "EWKZ_2017MGHERWIG",
#    "WWJJlnln_2017MGPY",
#    "WWJJlnln_2016MGPY",]: continue
        if not sample in allSamples:
            allSamples.append((sample, datasets[sample]))
        else:
            raise Exception("Repeated sample in two set of datasets! %s %s"%(sample, datasetsName))


if nprocesses<=1:
    for (sample, datasets) in allSamples:
        haddSample((sample, datasets))
else:
    from multiprocessing import Pool
    p = Pool(nprocesses)
    outputs = p.map(haddSample, allSamples)
