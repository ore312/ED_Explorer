from EDJConst import *
from EDJFile import *
import time
import threading

#ユーザーが設定できるデータ
uInterval = 10
uFuction = None

#中で使用するデータ
mThread = None
mThreadFlag = True
mBSize = None
mBPath = ""
mBRow = None


#非同期用のインターバル設定
def setInterval(pMs):
    global uInterval
    uInterval = pMs


#非同期用のファンクション設定
def setFnc(pFnc):
    global uFuction
    uFuction = pFnc


#差分を取得 そのうちバイトで取得できるようにする
def getDeffJournal(pFileName, pByte):
    aOut = getByteFile(pFileName, pByte)
    return aOut.split("\r\n")


#一番最後の一行のを取得
def getLatestJournal():
    pass


#非同期で最新のジャーナルを取得してイベントを発行する
def loggingJournal():
    global mInterval
    global uFuction
    global mThread
    global mThreadFlag
    global mBSize

    while mThreadFlag == True:
        aFByte = getFolderSize()
        if aFByte != mBSize:
            aRef = getJson(aFByte - mBSize)
            mBSize = aFByte
            #イベント送信
            uFuction(aRef)
            # functools.partial(uFuction, aRef)
        time.sleep(uInterval / 1000)


#自動取得開始
def startJournal():
    global mThread
    global mThreadFlag
    global mBSize

    mBSize = getFolderSize()
    mThreadFlag = True
    mThread = threading.Thread(target=loggingJournal)
    mThread.start()


#自動取得終了
def endJournal():
    global mThreadFlag
    mThreadFlag = False


#初期化
def init():
    global uInterval
    global uFuction

    global mThread
    global mThreadFlag
    global mBSize
    global mPath
    global mBRow

    uInterval = 10
    uFuction = None

    mThread = None
    mThreadFlag = True
    mBSize = getFolderSize()
    mBRow = None
