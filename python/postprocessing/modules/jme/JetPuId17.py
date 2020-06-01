#Taken from https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID#Working_points (01/06/2020). The cut value on the discriminator is pT (0-10, 10-20, 20-30, 30-50, no cut above) and eta (0-2.5 2.5-2.75 2.75-3.0 3.0-5.0) dependent. This is the full table of cuts for 3 working points corresponding to 80(80), 90(90) and 99(95)% efficiency for eta<2.5(>2.5) for quark jets: 
wps={
"tight":
    {
    "Pt010":  [0.69, -0.35, -0.26, -0.21],
    "Pt1020": [0.69, -0.35, -0.26, -0.21],
    "Pt2030": [0.69, -0.35, -0.26, -0.21],
    "Pt3050": [0.86, -0.10, -0.05, -0.01],
    },
"medium":
    {
    "Pt010":  [0.18, -0.55, -0.42, -0.36],
    "Pt1020": [0.18, -0.55, -0.42, -0.36],
    "Pt2030": [0.18, -0.55, -0.42, -0.36],
    "Pt3050": [0.61, -0.35, -0.23, -0.17],
    },
"loose":
    {
    "Pt010":  [-0.97, -0.68, -0.53, -0.47],
    "Pt1020": [-0.97, -0.68, -0.53, -0.47],
    "Pt2030": [-0.97, -0.68, -0.53, -0.47],
    "Pt3050": [-0.89, -0.52, -0.38, -0.30],
    },
}

etaEdges = [2.5, 2.75, 3.0, 5.0]

def JetPuId17(pt, eta, discr):
    etaBin = -1
    for i, etaEdge in enumerate(reversed(etaEdges)):
        if eta<etaEdge: etaBin = i

    if pt<10:   ptBin = "Pt010"
    elif pt<20: ptBin = "Pt1020"
    elif pt<30: ptBin = "Pt2030"
    elif pt<50: ptBin = "Pt3050"
    else:       ptBin = "Pt50"

    if ptBin == "Pt50": return 8
    if etaBin == -1: return 9

    if   discr > wps["tight"][ptBin][etaBin]: return 7
    elif discr > wps["medium"][ptBin][etaBin]: return 6
    elif discr > wps["loose"][ptBin][etaBin]: return 4
    else: return 0

