import os

folder1 = "/scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0/"
folder2 = "/scratchssd/sdonato/fileSkimFromNanoAOD/PROD_13_4/"
files1 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f)) and ".root" in f]
files2 = [f for f in os.listdir(folder1) if os.path.isfile(os.path.join(folder1, f)) and ".root" in f]

files = files1 + files2
#folders = ['DY105VBF_2016AMCPY','DY2J_2017AMCPY']

diffMap = {}
for fil in files:
    command1 = "ls -l -H %s "%(folder1+"/"+fil) #| grep Events | awk '{print $4}
    command2 = "ls -l -H %s "%(folder2+"/"+fil) #| grep Events | awk '{print $4}
    try:
        size1 = int(os.popen ( command1 ).read().split(" ")[4])
    except:
        size1 = 0
    try:
        size2 = int(os.popen ( command2 ).read().split(" ")[4])
    except:
        size2 = 0
    
    size1 = float(size1)
    size2 = float(size2)
    diff = (size2-size1)/size1 if size1>0 else 1000
    diffMap[diff] = fil
    print "%.2f"%(diff*100.), fil

for diff in sorted(diffMap.keys()):
    print ( diffMap[diff], diff)
