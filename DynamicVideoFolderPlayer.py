import psutil
import os
import time
import queue
import sys
from subprocess import Popen

kDropboxFolderPath = "C:\\Users\\siddhaja\\Dropbox\\Public\\publish\\"
kVLCOpenCommand = "\"C:\\Program Files (x86)\\VideoLan\\VLC\\vlc.exe\""
kTriggerIntervalSeconds = 15
DETACHED_PROCESS = 0x00000008

global NewVideosQueue
global AllVideosDict
global isNewVideoMode



def playVideoInVLC(item):
    print("playVideoInVLC")
    if item is 'desktop.ini':
        return
    completeFilePath = kDropboxFolderPath + item + "\\video.mp4"
    completeCommand = kVLCOpenCommand + " --fullscreen " + completeFilePath
    print(completeCommand)
    p = Popen(completeCommand,shell=False,stdin=None,stdout=None,stderr=None,close_fds=True,creationflags=DETACHED_PROCESS)


    
def flushNewVideosQueue():
    global NewVideosQueue
    global AllVideosDict
    print("flushNewVideosQueue")
    while(1):
        print("inside flush new video while")
        if len(NewVideosQueue) > 0:
            item = NewVideosQueue.pop(0)
        else:
            return
        print("after break point")

        playVideoInVLC(item)
        #siddhant: handle case when two videos have same name
        AllVideosDict[str(item)] = None

def getVLCProcessID():
    print("getVLCProcessID")
    processIDList =  psutil.pids()
    returnPID = -1;
    #TBD: Handle exception being thrown if after getting the
    # pids, one of the process is closed and we are trying to access
    # it
    for each in processIDList:
        try:
            process = psutil.Process(each)
            if process is not None:
                if process.name() == 'vlc.exe':
                    return each
        except:
            continue
        

    return returnPID
    
def killVLCIfRunning():
    print("killVLCIfRunning")
    vlcProcessID = getVLCProcessID()
    if vlcProcessID!=-1:
        vlcProcess = psutil.Process(vlcProcessID)
        vlcProcess.terminate()


def checkForNewVideosInFolder():
    print("checkForNewVideosInFolder")
    areNewVideosAdded = False
    global AllVideosDict
    global NewVideosQueue
    
    currentFilesDict = dict ([(f, None) for f in os.listdir (kDropboxFolderPath)])
    addedFilesDict = [f for f in currentFilesDict if not f in AllVideosDict]
    print (currentFilesDict)
    print (addedFilesDict)
    print (AllVideosDict)
    AllVideosDict = currentFilesDict

    for each in addedFilesDict:
        NewVideosQueue.append(each)

    numItemsInList = len(addedFilesDict)
    if numItemsInList > 0:
        areNewVideosAdded = True
        
    return areNewVideosAdded


def playAllVideosDict():
    print(" playAllVideosDict" )
    global AllVideosDict
    for each in AllVideosDict.keys():
        playVideoInVLC(each)
        
    
def startScript():
    print("startScript")
    global isNewVideoMode
    while(1):
        print("newWhileLoop")
        if checkForNewVideosInFolder():
            print(isNewVideoMode)
            if isNewVideoMode:
                flushNewVideosQueue()
            else:
                killVLCIfRunning()
                flushNewVideosQueue()
                isNewVideoMode = True
        else:
            vlcProcessID = getVLCProcessID()
            print("VLC process ID ")
            print(vlcProcessID)
            if vlcProcessID==-1:
                isNewVideoMode = False
                playAllVideosDict()

        time.sleep(kTriggerIntervalSeconds)
            
    
if __name__ == '__main__':
    print ('Welcome to the amazing dynamic folder player')
    print ('This script will be playing the following folder:')
    print(kDropboxFolderPath)

    print ('Starting the timer...')
    AllVideosDict = dict()
    NewVideosQueue = list()
    isNewVideoMode = bool()
    isNewVideoMode = False
    startScript()
