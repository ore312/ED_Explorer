from EDJConst import *
import os

#ジャーナルフォルダを取得
def getFolderList(pSortFlag = False):
    aFiles = os.listdir(FOLDER_JRL)

    #使わないファイルを取り除く
    aList = []
    for i in range(len(aFiles)):
        if(aFiles[i].find(".log") != -1):
            if pSortFlag == True:
                aList.append({"Name":aFiles[i], "Date":os.path.getmtime(FOLDER_JRL + aFiles[i])})
            else:
                aList.append(aFiles[i])
    if pSortFlag != True:
        return aList

    #ソートする
    aList = sorted(aList, key=lambda x:x['Date'])
    aOut = []
    for i in range(len(aList)):
        aOut.append(aList[i].get("Name"))
    aOut.reverse()
    return aOut


#すべてのジャーナルの総容量を取得
def getFolderSize():
    aOut = 0
    aFiles = getFolderList()
    for aF in aFiles:
        if(aF.find(".log") != -1):
            aOut += os.path.getsize(FOLDER_JRL + aF)
    return aOut


#指定されたバイト数逆読みして出力
def getByteFile(pPath, pByte = None):
    aOut = None
    with open(pPath, "rb") as f:
        if pByte != None:
            f.seek(os.path.getsize(pPath) - pByte)
        aOut = f.read()

    return aOut.decode()


#指定したバイト数のジャーナルを取得する
def getJson(pByte):
    aOut = ""

    #元の値を変化させてしまうので変数に置き換える
    aBCnt = pByte

    #ソートされたフォルダリストを取得
    aFiles = getFolderList(True)

    #いくつファイルを読み込めば目的のバイト数に到達するか
    aFCnt = 0
    aACnt = 0
    for aFCnt in range(len(aFiles)):
        if aACnt >= pByte:
            break
        aACnt += os.path.getsize(FOLDER_JRL + aFiles[aFCnt])

    #もしaFCnt=2が来た場合は2つファイルがある
    #n番目は最後から数バイトを読み込む
    #0~n-1番目はすべて読み込み

    # print("B_FCnt :" + str(aFCnt))
    # print("B_BCnt :" + str(aBCnt))

    #ファイルが1つで完結している場合
    if aFCnt == 1:
        aOut += getByteFile(FOLDER_JRL + aFiles[0], aBCnt)
    else:
        #リストカウントに変換0からスタートなので-1
        aFCnt -= 1
        #ファイルをまたいでいる場合
        #一番古いファイルを途中から最後まで読み込む
        # print("fast:" + str((aBCnt - aACnt) + os.path.getsize(FOLDER_JRL + aFiles[aFCnt])))
        aFByte = (aBCnt - aACnt) + os.path.getsize(FOLDER_JRL + aFiles[aFCnt])
        aOut += getByteFile(FOLDER_JRL + aFiles[aFCnt], aFByte)

        #残ったファイルを古い順ですべて読み込む
        for i in reversed(range(aFCnt)):
            aOut += getByteFile(FOLDER_JRL + aFiles[i])

    # print("A_FCnt :" + str(aFCnt))
    # print("A_BCnt :" + str(aBCnt))

    #リスト形式にする
    return aOut.split("\r\n")

