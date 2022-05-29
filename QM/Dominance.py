import copy

def removeUsed(mCntDic):
    for key in mCntDic.copy().keys():
        if (mCntDic[key] == -1):
            del mCntDic[key]

def rowDominance(nonEpiList, mCntDic):

    secondEpi = [] # 지배하는 pi
    interchange = []

    # nonEpi들을 비교해서 dominance 관계인지 확인 
    for i in range(len(nonEpiList)-1): 
        for j in range(i+1, len(nonEpiList)):

            # pi 1 < pi 2 인지 판별
            isDom = True
            for nonE in nonEpiList[i][1]:
                if (nonE not in nonEpiList[j][1]): # 첫번째 pi의 mintermNum이 두번째 pi에 없으면 break
                    isDom = False
                    break
            
            if (isDom): # dominance 관계이면 list에 추가
                # 만약 이전 비교에서 첫 번째 pi가 지배했지만, 현재 비교에서는 지배당하는 경우
                # (더 큰 pi가 나타난 경우) secondEpi에서 첫 번째 pi를 삭제

                # interchange한 케이스일 때는 일단 interchange에 저장만 해둠
                if(nonEpiList[i][1] == nonEpiList[j][1]):
                    interchange.append(nonEpiList[i][1])
                    for minterm in nonEpiList[i][1]:
                        mCntDic[minterm] = -1
                    continue

                if(nonEpiList[i] in secondEpi):
                    secondEpi.remove(nonEpiList[i])
                secondEpi.append(nonEpiList[j])
                for num in nonEpiList[j][1]:
                    mCntDic[num] = -1
                
                continue # continue함으로써 interchange한 경우도 자동으로 해결
            
            # pi 1 > pi 2 인지 판별
            for nonE in nonEpiList[j][1]:
                if (nonE not in nonEpiList[i][1]): # 두번째 pi의 mintermNum이 첫번째 pi에 없으면 break
                    isDom = False
                    break
            
            if (isDom): # 지배관계가 반대로 형성되어 있을 때도 마찬가지
                if(nonEpiList[j] in secondEpi):
                    secondEpi.remove(nonEpiList[j])
                secondEpi.append(nonEpiList[i])
                for num in nonEpiList[i][1]:
                    mCntDic[num] = -1
    
    for epi in secondEpi:
        if(epi in nonEpiList):
            nonEpiList.remove(epi)
    
    # findInterchange가 true로 변하는 시점의 pi만 epi로 쓰고 나머지는 버림
    findInterchange = False
    if interchange: #interchange한 pi들이 nonEpiList에 남아있으면
        for i in interchange:
            for nonEpi in nonEpiList:
                if(i == nonEpi[1]):
                    if(findInterchange):
                        nonEpiList.remove(nonEpi)
                    else:
                        secondEpi.append(nonEpi) 
                        findInterchange = True

    removeUsed(mCntDic)

    return secondEpi


def colDominance(nonEpiList, mCntDic):
    secondEpi = []


    # minterm들을 비교해서 dominance 관계인지 확인
    for m1 in mCntDic:
        for m2 in mCntDic:
            if (m1 >= m2):
                continue
            if (mCntDic[m1] == -1):
                break
            if (mCntDic[m2] == -1):
                continue

            pi_1 = set() # 첫 번째 minterm이 포함된 pi
            pi_2 = set() # 두 번째 minterm이 포함된 pi

            for nonEpi in nonEpiList:
                for m in nonEpi[1]:
                    # nonEpi가 minterm 1 또는 2를 포함하고 있으면 각각의 set에 넣어줌
                    if (m == m1):
                        pi_1.add(nonEpiList.index(nonEpi))
                    elif (m == m2):
                        pi_2.add(nonEpiList.index(nonEpi))

            # dominance 관계인지 확인 pi_1 > pi_2
            isDom = True
            for pi in pi_2:
                if (pi not in pi_1):
                    isDom = False
                    break
            
            if (isDom):
                
                for idx in pi_2:
                    # nonEpi 하나 고르기
                    if (nonEpiList[idx] not in secondEpi): #secondEpi에 없는 pi를 선택
                        # 그 nonEpi를 secondEpi에 넣기
                        secondEpi.append(nonEpiList[idx])
                        
                        for m in nonEpiList[idx][1]:
                            # epi가 포함하는 minterm들의 cnt를 -1로 변경
                            mCntDic[m] = -1

                            # nonEpi가 만약 없어질 minterm을 cover하고 있다면 제거해줌
                            for nonEpi in nonEpiList:
                                if (nonEpi == nonEpiList[idx]):
                                    continue
                                if (m in nonEpi[1]):
                                    nonEpi[1].remove(m)
                        

                        del nonEpiList[idx] # nonEpiList에서 pi 지우기
                        
                        # 만약 모두 체크되지 않은 빈 pi가 추가적으로 생기면 제거
                        for nonEpi in nonEpiList:
                            if(nonEpi[1] == []):
                                nonEpiList.remove(nonEpi)
                        break
                
            
            # dominance 관계인지 확인 pi_1 < pi_2
            for pi in pi_1:
                if (pi not in pi_2):
                    isDom = False
                    break
            
            if (isDom):

                for idx in pi_1:
                    if (nonEpiList[idx] not in secondEpi):
                        secondEpi.append(nonEpiList[idx])
                        
                        
                        for m in nonEpiList[idx][1]:

                            mCntDic[m] = -1

                            for nonEpi in nonEpiList:
                                if (m in nonEpi[1]):
                                    nonEpi[1].remove(m)

                        del nonEpiList[idx] 
                        for nonEpi in nonEpiList:
                            if(nonEpi[1] == []):
                                nonEpiList.remove(nonEpi)
                        break
    
    removeUsed(mCntDic)

    return secondEpi