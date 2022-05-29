
from Dominance import removeUsed, colDominance, rowDominance
from FindEpi import findEpi
from FindPi import findPi  
from Format import piFormat, epiFormat


def solution(minterm):
    # minterm: [numOfVar, numOfMin, Minterms...]
    # mDic = {numOf1:{Binary Minterm : Combined}, 0:{0000:0}, 1:{0100:0, 1000:0}...}
    # 새로운 mDic = {{numOf1:{Binary Minterm : {MintermNum:?, Combined:0}}}

    # 0의 갯수로 minterm들 사전(mDic)에 저장
    mDic = {}
    numOfVar = minterm[0]
    numOfMin = minterm[1]
    for i in range(numOfVar+1):
        mDic[i] = {}
    
    # 초기에 입력받은 minterm의 data를image.png mDic에 저장
    for i in range(2, numOfMin+2):
        MintermNum = minterm[i]
        minterm[i] = str(bin(minterm[i]))[2:].zfill(numOfVar) # minterm을 2진수로 변환
        
        # 1의 갯수 count
        zeroCnt = 0
        for bit in minterm[i]:
            if(bit == "1"):
                zeroCnt+=1
        
        mDic[zeroCnt][minterm[i]] = {"Minterms":[MintermNum], "Combined":0} # 0: unchecked / 1: checked
    

    
    # 최적화 진행
    piResult = findPi(numOfVar, mDic, []) # answer = [ [0220, [1,2,4]] , [1020, [5,6]], .....]
    epiResult = findEpi(numOfVar,piResult)

    # pi 정렬
    piList = piFormat(numOfVar, piResult)
    
    # epi 정렬
    epiList = epiFormat(numOfVar, epiResult)

    # 합병
    result = piList + ["EPI"] + epiList

    print(result)

    
# a= solution([4, 8, 0, 4, 8, 10, 11, 12, 13, 15])
b = solution([4, 13, 0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
