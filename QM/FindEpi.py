
from Dominance import removeUsed, colDominance, rowDominance
from Format import epiFormat

def findEpi(numOfVar, piDic):


    mCntDic = {}
    epiList = []
    nonEpiList = []

    # 각 minterm의 사용 횟수 count
    for pi in piDic:
        for minterm in pi[1]:
            if minterm not in mCntDic:
                mCntDic[minterm] = 1
            else:
                mCntDic[minterm] += 1
    
    # 각 minterm의 count를 비교하여 1이면 해당 minterm을 cover한 pi를 epi로
    for pi in piDic:
        isEpi = False
        for minterm in pi[1]:
            if (mCntDic[minterm] == 1):
                isEpi = True
                break
        if(isEpi):
            epiList.append(pi)
            for minterm in pi[1]:
                mCntDic[minterm] = -1
        else:
            nonEpiList.append(pi)

    # epi가 cover한 minterm을 nonEpi에서 지움
    for nonEpi in nonEpiList:
        removeList = []
        for num in nonEpi[1]:
            if (mCntDic[num] == -1):
                removeList.append(num)
        for num in removeList:
            nonEpi[1].remove(num)


    removeUsed(mCntDic)

    mCntDic = dict(sorted(mCntDic.items())) # mCntDic 한번 정렬해주기

    print("--After Find Epi--")
    # print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiFormat(numOfVar, epiList), epiFormat(numOfVar, nonEpiList)))
    print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiList, nonEpiList))

    if (len(mCntDic) == 0):
        return epiList
    
    while (True):
        dLen = len(mCntDic)
        if(dLen == 0):
            break

        changed = False # 두 dominance를 수행한 후에도 changed가 False라면, 더이상 epi를 찾을 없다는 뜻이다

        epiList += colDominance(nonEpiList, mCntDic)
        if (len(mCntDic) < dLen):
            dLen = len(mCntDic)
            changed = True
        print("--After Column Dominance--")
        # print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiFormat(numOfVar, epiList), epiFormat(numOfVar, nonEpiList)))
        print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiList, nonEpiList))

        epiList += rowDominance(nonEpiList, mCntDic)
        if (len(mCntDic) < dLen):
            dLen = len(mCntDic)
            changed = True
        
        print("--After Row Dominance--")
        # print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiFormat(numOfVar, epiList), epiFormat(numOfVar, nonEpiList)))
        print("mCntDic: {0}\nepiList: {1}\nnonEpiList: {2}\n".format(mCntDic, epiList, nonEpiList))
        
        if(not changed):
            break

    return epiList
