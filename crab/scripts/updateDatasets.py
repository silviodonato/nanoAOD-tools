from allNanoAODV7 import allNanoAODv7
import pprint


def makeData (allDatasets, name="data2016"):
    data = {}
    for dataset in allDatasets[name]:
        Run201XY = "Run201"+dataset.split("Run201")[1][:2]
        sample = "SingleMuon%s"%Run201XY
        if sample in data: data[sample].append(dataset)
        else: data[sample] = [dataset]
    return data


def updateDatasets(mc):
    allPrimaryDatasets=set()

    ## take only primary dataset
    mc_pd = {}
    for sample in mc:
        mc_pd[sample] = set()
        for dataset in mc[sample]:
            if dataset:
                primaryDataset = dataset.split("/")[1]
                if "ext1" in dataset: primaryDataset += "ext1"
                if "ext2" in dataset: primaryDataset += "ext2"
                if "ext3" in dataset: primaryDataset += "ext3"
                if "v2" in dataset: primaryDataset += "v2"
                if not primaryDataset in allPrimaryDatasets:
                    allPrimaryDatasets.add(primaryDataset)
                    mc_pd[sample].add(primaryDataset)
                else:
                    print "## WARNING: %s %s"%(sample, primaryDataset)

    ##init mc new
    mc_new = {}
    for sample in mc:
        for primaryDataset in mc_pd[sample]:
            primaryDataset.replace("ext1","")
            primaryDataset.replace("ext2","")
            primaryDataset.replace("ext3","")
            primaryDataset.replace("v2","")
        mc_new[sample] = [dataset for dataset in allNanoAODv7 if primaryDataset in dataset]
    
    return mc_new

allDatasets={
    "mc2016":set(),
    "mc2017":set(),
    "mc2018":set(),
    "data2016":set(),
    "data2017":set(),
    "data2018":set(),
}

for dataset in allNanoAODv7:
    if   "RunIISummer15" in dataset: allDatasets["mc2016"  ].add(dataset)
    elif "RunIIFall17"   in dataset: allDatasets["mc2017"  ].add(dataset)
    elif "RunIIAutumn18" in dataset: allDatasets["mc2018"  ].add(dataset)
    elif "SingleMuon" in dataset and "Run2016" in dataset: allDatasets["data2016"].add(dataset)
    elif "SingleMuon" in dataset and "Run2017" in dataset: allDatasets["data2017"].add(dataset)
    elif "SingleMuon" in dataset and "Run2018" in dataset: allDatasets["data2018"].add(dataset)

data2016 = makeData (allDatasets, name="data2016")
data2017 = makeData (allDatasets, name="data2017")
data2018 = makeData (allDatasets, name="data2018")

mc2016 = {}
mc2017 = {}
mc2018 = {}

import datasetsAndreaV8_DataSignal
mc2016.update(datasetsAndreaV8_DataSignal.mc2016)
mc2017.update(datasetsAndreaV8_DataSignal.mc2017)
mc2018.update(datasetsAndreaV8_DataSignal.mc2018)

import datasetsAndreaV8_ForMassScan 
mc2016.update(datasetsAndreaV8_ForMassScan.mc2016)
mc2017.update(datasetsAndreaV8_ForMassScan.mc2017)
mc2018.update(datasetsAndreaV8_ForMassScan.mc2018)

import datasetsAndreaV10_DataSignal_2018
mc2018.update(datasetsAndreaV10_DataSignal_2018.mc2018)

import datasetsAndreaV4_2017 
mc2017.update(datasetsAndreaV4_2017.mc2017)

import datasetsNanoV6_2016 
mc2016.update(datasetsNanoV6_2016.mc2016)

import datasetsNanoV6_2018 
mc2018.update(datasetsNanoV6_2018.mc2018)

import datasetsNanoV6_ForJerStudy_2016 
mc2016.update(datasetsNanoV6_ForJerStudy_2016.mc2016)

print
print "data2016 = ",
pprint.pprint(data2016)
print
print "data2017 = ",
pprint.pprint(updateDatasets(mc2017))
print
print "data2018 = ",
pprint.pprint(data2018)
print
print "mc2016 = ",
pprint.pprint(data2017)
print
print "mc2017 = ",
pprint.pprint(updateDatasets(mc2016))
print
print "mc2018 = ",
pprint.pprint(updateDatasets(mc2018))
print


