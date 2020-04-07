nprocesses = 16
version = "PROD_13_0"
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

#from datasetsAndreaV4_2017 import mc2017
from datasetsAndreaV8_DataSignal import mc2017
#from datasetsAndreaV8_ForMassScan import mc2017

selection = [
"vbfHmm_2017POWHERWIG7",
"vbfHmm_2017POWPY2",
#"DY2J_2017AMCPY",
#"EWKZ_2017MGPY2",
#"ZZ4l_2017POWPY",
#"STtbar_2017POWPY",
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
