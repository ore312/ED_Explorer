#ore312_作

# { "timestamp":"2021-05-10T10:14:35Z", "event":"FSDTarget", "Name":"Screakiae VS-B d1852", "SystemAddress":63643052036483, "StarClass":"F" }

#my module
from EDJournalLib import *
from modConst import *
from modWeb import *

import json

#debug
import sys
import os

def getSystem(pSysName):
    aJson = getApi(API_EDSM_BODIES + pSysName)
    if aJson == None:
        print("取得に失敗しました")
        return

    #未登録の星系
    if aJson == {}:
        print("登録されていない星系です")
        return

    #ファーストディスカバリーされていない星系を出力
    print("星系内の情報")
    aName = []
    aDist = []
    aFast = []
    aNameCnt = 0
    aDistCnt = 0
    aFastCnt = 0
    aCnt = 0
    for aB in aJson.get(TAG_BODIES):
        aN = aB.get(TAG_STARNAME)
        aD = aB.get(TAG_DISTANCE)
        aF = ""
        if aB.get(TAG_DISCOVERY) != None:
            if aB.get(TAG_DISCOVERY).get(TAG_COMMANDER) != None:
                aF = aB.get(TAG_DISCOVERY).get(TAG_COMMANDER)
        #エラー対策
        if aN == None:
            aN = ""
        if aD == None:
            aD = 0
        if aF == None:
            aF = ""
        if not(aN == "" and aD == 0 and aF == ""):
            aName.append(aN)
            aDist.append(aD)
            aFast.append(aF)

            if len(aN) > aNameCnt:
                aNameCnt = len(aN)
            if len(str(aD)) > aDistCnt:
                aDistCnt = len(str(aD))
            if len(aF) > aFastCnt:
                aFastCnt = len(aF)
            aCnt += 1

    #距離でソート
    for i in range(aCnt):
        for j in range(i + 1, aCnt):
            if aDist[i] > aDist[j]:
                aWork = aName[i]
                aName[i] = aName[j]
                aName[j] = aWork

                aWork = aDist[i]
                aDist[i] = aDist[j]
                aDist[j] = aWork

                aWork = aFast[i]
                aFast[i] = aFast[j]
                aFast[j] = aWork

    print("bodies count:" + "{:,}".format(aCnt))

    #出力
    for i in range(aCnt):
        aOut = ""
        aD = "{:,}".format(aDist[i]) + "ls"
        aOut += aD + (" " * ((aDistCnt + 2 + 4) - len(aD))) + (" " * 3)
        aOut += aName[i] + (" " * (aNameCnt - len(aName[i]))) + (" " * 3)
        aOut += aFast[i] + (" " * (aFastCnt - len(aFast[i]))) + (" " * 3)
        print(aOut)

def fncJrl(pJrl):
    for i in range(len(pJrl) - 1):
        aJson = None
        try:
            aJson = json.loads(pJrl[i])
        except Exception:
            continue
        if aJson == None:
            continue

        if aJson.get(TAG_EVENT) == EVENT_FSD:
            if aJson.get(TAG_STAR) != None:
                print("StarClass : ", end="")
                print(aJson.get(TAG_STARCLASS))
                print("System    : ", end="")
                print(aJson.get(TAG_STAR))
                print("↓" * 20)
                getSystem(aJson.get(TAG_STAR))
                print("\n" * 2)
            else:
                print("星系名の取得に失敗しました\n")

def main():
    print("Ver:" + VERSION + "\n")

    #debug
    if len(sys.argv) > 1:
        print("debug\n")
        for aP in sys.argv:
            if os.path.exists(aP) != True:
                continue
            aStr = None
            with open(aP, "rb") as f:
                aByte = f.read()
                aStr = aByte.decode()
            fncJrl(aStr.split("\r\n"))
        return

    init()
    setInterval(200)
    setFnc(fncJrl)
    startJournal()

if __name__ == "__main__":
    main()
