from pkg_resources import UnknownExtra


def findPi(numOfVar, mDic, unchecked):
        
        nullDic = 0
        for dic in mDic:
            if not mDic[dic]:
                nullDic += 1
                
        if(len(mDic) - nullDic < 2): # 만약 비어있지 않은 dic의 개수가 2 미만이면
            for dic in mDic.values():
                for key in dic:
                    unchecked.append([key,dic[key]["Minterms"]]) # mDic의 minterm을 모두 unchecked에 저장 후 return
            return unchecked

        newDic = {} # 새로운 dic에 기존 dic의 key값을 모두 복사하기(value는 빈 dic으로 init)
        keyList = [k for k in mDic]
        for k in keyList:
            newDic[k] = {} 
        # newdic = {0:{}, 1:{}}
        
        
        for kIdx in range(len(keyList)-1): # keyList[kIdx] = mDic's key
            thisDic = mDic[keyList[kIdx]] # thisDic = {Binary Minterm : {MintermNum:?, Combined:0}, 1000 : {MintermNum:8, Combined:0},....}

            nextDic = mDic[keyList[kIdx+1]]
            nextKeyList = [k for k in nextDic] # 나중에 minterm merge할 때 사전의 key값은 변경할 수 없으므로 미리 list에 str형태로 저장해놓고 
                                               # merge할 때 이 list의 값을 사용하여 newdic에 변경된 minterm을 저장

            for thisKey in thisDic:
                mIdx = -1 # kIdx: mDic의 keyList의 idx / mIdx: thisDic의 thisKeyList의 idx
                for nextKey in nextDic: # thisDic과 nextDic의 minterm을 비교
                    mIdx += 1

                    hd = 0 # Hamming Distance
                    diffIdx = -1 # bit가 차이나는 곳의 idx
                    for i in range(numOfVar):
                        if (thisKey[i] != nextKey[i]):
                            hd += 1
                            diffIdx = i

                    if(hd == 1): # HD가 1이면 병합하고 check
                        mergedMinterm = list(nextKeyList[mIdx]) # 해당 minterm을 list로 변환하여 쪼갬

                        mergedMinterm[diffIdx] = "2" # 2 = '-'  ex) 0120 = 01-0
                        mergedMinterm = "".join(mergedMinterm) # 다시 String으로 변환
                        
                        # merge한 minterm의 number를 Minterms key에 저장
                        newDic[keyList[kIdx]][mergedMinterm] = {"Minterms":[], "Combined":0}
               

                        for thisNum in thisDic[thisKey]["Minterms"]:
                            newDic[keyList[kIdx]][mergedMinterm]["Minterms"].append(thisNum)
                        for nextNum in nextDic[nextKey]["Minterms"]:
                            newDic[keyList[kIdx]][mergedMinterm]["Minterms"].append(nextNum)

                        thisDic[thisKey]["Combined"] = 1
                        nextDic[nextKey]["Combined"] = 1
        

        for dic in mDic.values():
            for key in dic: # [00-0, 0001, 0010....]
                if (dic[key]["Combined"] == 0): # unchecked된 것이 있으면 pi
                    unchecked.append([key,dic[key]["Minterms"]]) # [ [00-0, [0,2]] , [0001, [1]] ...]

        return findPi(numOfVar, newDic, unchecked)