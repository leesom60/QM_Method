def piFormat(numOfVar, piResult):
    piList = []
    for i in range(len(piResult)):
        piList.append(int(piResult[i][0]))

    piList.sort()

    for i in range(len(piResult)):
        piList[i] = str(piList[i]).zfill(numOfVar).replace("2", "-")
    
    return piList
    
def epiFormat(numOfVar, epiResult):
    epiList = []
    for epi in epiResult:
        epiList.append(int(epi[0]))

    epiList.sort()

    for i in range(len(epiList)):
        epiList[i] = str(epiList[i]).zfill(numOfVar).replace("2", "-")
    
    return epiList