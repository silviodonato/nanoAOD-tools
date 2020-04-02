import os

prodFolder = "/scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0/"
folders = [f for f in os.listdir(prodFolder) if not os.path.isfile(os.path.join(prodFolder, f))]

#folders = ['DY105VBF_2016AMCPY','DY2J_2017AMCPY']

tobeUpdated = set()
for folder in folders:
    tbd = set()
    print ("#FOLDER %s"%folder)
    fullPath = prodFolder+"/"+folder+"/"
    files = [f for f in os.listdir(fullPath) if os.path.isfile(os.path.join(fullPath, f))]
    sizes = {}
    for f_ in files:
        size = os.path.getsize(fullPath+"/"+f_)
        if size in sizes:
            command = "edmEventSize -v %s "%(fullPath+"/"+sizes[size]) #| grep Events | awk '{print $4}
            ev1 = os.popen ( command ).read()
            command = "edmEventSize -v %s "%(fullPath+"/"+f_) #| grep Events | awk '{print $4}
            ev2 = os.popen ( command ).read()
            if ev1==ev2:
                print("Same size of files %s %s"%(sizes[size], f_))
                print("Events of files %s %s"%(ev1, ev2))
                tbd.add(fullPath+"/"+sizes[size])
                tbd.add(fullPath+"/"+f_)
        else:
            sizes[size] = f_
#    for f in tbd:
#        print ("rm %s # %d"%(f, os.path.getsize(f)))
    if len(tbd)>0:
#        print ("cd %s && source script.sh >& logScript && cd .. # %d"%(fullPath, os.path.getsize(f)))
#        print ("rm %s/*"%(fullPath))
        pass




#    print (sizes)
#print ()
#print ()
#cd /scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0//DY105VBF_2016AMCPY/ && source script.sh >& logScript && cd .. # 936003997
#cd /scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0//DY2J_2017AMCPY/ && source script.sh >& logScript && cd .. # 32857451

