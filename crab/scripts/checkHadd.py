import os

prodFolder = "/scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0/"
folders = [f for f in os.listdir(prodFolder) if not os.path.isfile(os.path.join(prodFolder, f))]

#folders = ['DY105VBF_2016AMCPY','DY2J_2017AMCPY']

tobeUpdated = set()
for folder in folders:
    command = "ls -l %s "%(prodFolder+"/"+folder+".root") #| grep Events | awk '{print $4}
    try:
        sizeFile = int(os.popen ( command ).read().split(" ")[4])
    except:
        sizeFile = 0
    command = "du -l %s "%(prodFolder+"/"+folder) #| grep Events | awk '{print $4}
    sizeFolder = int(os.popen ( command ).read().split("\t")[0])
    sizeFolder = sizeFolder*1024
    
    diff = (sizeFile*1.-sizeFolder)/sizeFolder
    if sizeFile>0 and abs(diff)>0.02:
        command = 'root -l %s  -e "Runs->Draw(\\"\\",\\"\\")" -q'%(prodFolder+"/"+folder+".root")
#        print command
        nFilesHadd, nFilesFolder = 0, 0
        if not "SingleMuonRun" in folder:
            nFilesHadd   = int(os.popen ( command ).read().split("(long long) ")[1])
            command = 'ls %s | grep "\.root" | wc -l'%(prodFolder+"/"+folder)
            nFilesFolder = int(os.popen ( command ).read())
            print ("%s : %.2f %d %d" %(folder, diff*100, nFilesHadd, nFilesFolder))

#    print (sizes)
#print ()
#print ()
#cd /scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0//DY105VBF_2016AMCPY/ && source script.sh >& logScript && cd .. # 936003997
#cd /scratchssd/sdonato/fileSkimFromNanoAOD/PROD_12_0//DY2J_2017AMCPY/ && source script.sh >& logScript && cd .. # 32857451


'''
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2018B/*root");c.Draw("","")' >& SingleMuonRun2018B.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2018C/*root");c.Draw("","")' >& SingleMuonRun2018C.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2018D/*root");c.Draw("","")' >& SingleMuonRun2018D.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2018E/*root");c.Draw("","")' >& SingleMuonRun2018E.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2018A/*root");c.Draw("","")' >& SingleMuonRun2018A.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2017/*root");c.Draw("","")' >& SingleMuonRun2017.events.txt &
root -l -q -e 'TChain c("Events");c.Add("SingleMuonRun2016/*root");c.Draw("","")' >& SingleMuonRun2016.events.txt &
'''
