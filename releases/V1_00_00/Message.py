# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 18:43:02 2026

@author: Tianrang Yang (github account: Tim16888)、Zhen Fang (github account: Fang-FuDaGuoNanCeYe)
"""

import enum

class bubbleState(enum.Enum):
    Stay = 0
    Flow = 1
    Out = 2
    Back = 3
    
def bubbleStateToText(state: bubbleState):
    f = {bubbleState.Stay: "stay",
         bubbleState.Flow: "flow",
         bubbleState.Out : "out",
         bubbleState.Back: "back"};
    return f[state];

class messageType(enum.Enum):
    PicturePredict = -1;      #This one will actually predict all pictures in a folder and its sub-folder.
    VideoPredict = -2;
    PicturePredictSingle = -3;
    LoadPickle = -4;
    DrawPlot    = -5;
    SavePlotData=-6;
    FrontAlive = -101;
    FrontIsDead = -102;
    SaveMono = -7
    Error = 0;#Error means the error is big so the process has to terminate
    
    TaskFailed = 301; #TaskFiled means the error disrupts the task, but the process is still alive.
    KidError = 302;
    KidDone = 303;
    FrontBlocked=304;
    FrontUnblocked=305;
    giveProcessed=306;
    TaskWarning=307;
    
    
    BackendAlive = 101;
    BackendIsDead = 102;
    
    PicturePredictProgress = 201;
    VideoPredictProgress   = 202;
    GaugeSetRunning = 203;#用于不方便显示具体进度的地方
    
    PicturePredictDone = 1;
    VideoPredictDone = 2;
    Fake = 99; #Fake message don't convey message between processes, but necessary because some functions require message typed args. 
    LoadPickleDone = 3;
    DrawPlotDone    = 4;
    SavePlotDataDone = 5;
    SaveMonoDone = 6;
class message:
    def __init__(self,
                 identification:int=0, messageType:messageType=messageType.Error,content:dict={}):
        self.id = identification;
        self.type = messageType;
        self.content = content;

"""
 processed:
     for every bubble:
         "startFrame":int
         "endFrame":int
         stayBool:whether flowing
         state:4 kinds
         shapely: 
        content : x , y , w , h , all absolute value
"""