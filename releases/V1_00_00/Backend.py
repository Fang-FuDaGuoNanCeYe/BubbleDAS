# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 19:15:52 2026

@author: Tianrang Yang (github account: Tim16888)、Zhen Fang (github account: Fang-FuDaGuoNanCeYe)
"""

import traceback as tr
import multiprocessing as mu
import multiprocessing.shared_memory as sh
import time as ti
import threading as th
import queue as qu
from Message import message
from Message import messageType
from Message import bubbleState
import Message as me
import GlobalArguments as gl
import pathlib as pa
import pandas as pd
import os
import io
import pickle
import concurrent.futures as fu
cpuNum = int(max(1,mu.cpu_count()));
mainLoopRenewInternals = 50;
totalStepVideoProcessing = 7;
def isEmpty(obj):
    if obj is None:
        return True
    if hasattr(obj, '__len__'):
        return len(obj) == 0
    return False

class bPredict(mu.Process):
    def __init__(self,
                  senderToBackend: mu.Queue, senderToFront: mu.Queue, content: dict = {},kidId : int = 0):
        mu.Process.__init__(self,daemon=True);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.content = content;
        self.kidId = kidId;
    def saveLabels(self,imgPath, result, saveDir=None):
        
        if saveDir is None:
            saveDir = os.path.dirname(imgPath)
        imgName = os.path.splitext(os.path.basename(imgPath))[0]
        labelPath = os.path.join(saveDir, f"{imgName}.txt")
        
        labelLines = []
        boxes = result.boxes
        boxesForNext = [];
        bubbleData = [];
        if boxes is not None and len(boxes) > 0:
            classIds = boxes.cls.cpu().numpy().astype(int)
            xywhn = boxes.xywhn.cpu().numpy();
            for classId, (x, y, w, h) in zip(classIds, xywhn):
                line = f"{classId} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                labelLines.append(line)
            boxesForNext=boxes.xywh.cpu().numpy();
            for i in range(len(boxesForNext)):
                bubbleData.append([boxesForNext[i,0], boxesForNext[i,1], boxesForNext[i,2], boxesForNext[i,3]]);
            
        with open(labelPath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(labelLines))
        return bubbleData
    
    def run(self):
        try:
            modelPath = pa.Path(self.content["model"]).resolve();
            from ultralytics import YOLO
            if(modelPath.exists()):
                if(modelPath.suffix in [".pt"]):
                    model = YOLO(modelPath);
            target = pa.Path(self.content["target"]).resolve();
            targetImages = [];
            if(target.exists()):
                targetImages = list(target.rglob("*.png")) + list(target.rglob("*.jpg")) + list(target.rglob("*.jpeg")) + list(target.rglob("*.gif"));
            
            numImages = len(targetImages);
            batchSize = 1;
            from PIL import Image;
            membraneZone = self.content["membraneZone"];
            statics = {"bubbleNum":0,"bubbleArea":0,"bubbleAreaRatio":0,
                       "membraneZoneArea":0,"membraneZoneAreaRatio":0,
                       "totalArea":0};
            if(membraneZone != ""):
                membraneZone = formMembraneZone(self.content["membraneZone"]);
            else:
                membraneZone = None;
            for i in range(0, numImages, batchSize):
                start = i
                end = min(i + batchSize, numImages)
                
                currentBatch = targetImages[start:end]
                
                sizes = Image.open(targetImages[i]).size;
                
                batchResults = model(currentBatch, stream=True, imgsz=[sizes[1],sizes[0]],max_det=99999)
                
                # Save results for current batch
                for imgPath, result in zip(currentBatch, batchResults):
                    bubbleData=self.saveLabels(imgPath, result,self.content["saveDir"]);
                    bubbleShapely = [];
                    for i in range(len(bubbleData)):
                        [x,y,w,h] = i[0:4];
                        circle = Point(x, y).buffer(1)
                        scaled = affinity.scale(circle, xfact=w/2, yfact=h/2);
                        bubbleShapely.append(scaled);
                    bubbleShapely = unary_union(bubbleShapely);
                    bubbleShapelyArea = bubbleShapely.area;
                    membraneZoneArea = 0 
                    if (membraneZone!=None):
                        membraneZoneArea=bubbleShapely.intersection(membraneZone).area;
                    
                    statics = {
                        "bubbleNum":len(bubbleData),
                        "bubbleArea":bubbleShapelyArea,
                        "bubbleAreaRatio":bubbleShapelyArea/sizes[0]/sizes[1],
                        "membraneZoneArea":membraneZoneArea,
                        "membraneZoneAreaRatio":membraneZoneArea/sizes[0]/sizes[1],
                        "totalArea":sizes[0]*sizes[1]};
                    bubbleDataFrame=pd.DataFrame(statics,index=[0]);
                    print(os.path.join(self.content["saveDir"],str(imgPath.stem)+"_result.csv"));
                    bubbleDataFrame.to_csv(os.path.join(self.content["saveDir"],str(imgPath.stem)+"_result.csv"),index=False);
                self.senderToFront.put(message(-1,messageType.PicturePredictDone,{"saveDir":self.content["saveDir"]}));
                self.senderToBackend.put(message(self.messageID,messageType.KidDone,{"From":"kid","Id":self.kidId}));
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();

class bPredictSinglePicture(mu.Process):
    def __init__(self,
                  senderToBackend: mu.Queue, senderToFront: mu.Queue, content: dict = {},kidId : int = 0):
        mu.Process.__init__(self,daemon=True);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.content = content;
        self.kidId = kidId;
        self.messageID = 0;
    def saveLabels(self,imgPath, result, saveDir=None):
        
        if saveDir is None:
            saveDir = os.path.dirname(imgPath)
        imgName = os.path.splitext(os.path.basename(imgPath))[0]
        labelPath = os.path.join(saveDir, f"{imgName}.txt")
        
        labelLines = []
        boxes = result.boxes
        boxesForNext = [];
        bubbleData = [];
        if boxes is not None and len(boxes) > 0:
            classIds = boxes.cls.cpu().numpy().astype(int)
            xywhn = boxes.xywhn.cpu().numpy();
            for classId, (x, y, w, h) in zip(classIds, xywhn):
                line = f"{classId} {x:.6f} {y:.6f} {w:.6f} {h:.6f}"
                labelLines.append(line)
            boxesForNext=boxes.xywh.cpu().numpy();
            for i in range(len(boxesForNext)):
                bubbleData.append([boxesForNext[i,0], boxesForNext[i,1], boxesForNext[i,2], boxesForNext[i,3]]);
            
        with open(labelPath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(labelLines))
        return bubbleData
    
    def run(self):
        try:
            modelPath = pa.Path(self.content["model"]).resolve();
            from ultralytics import YOLO
            if(modelPath.exists()):
                if(modelPath.suffix in [".pt"]):
                    model = YOLO(modelPath);
                
            targetImage = [pa.Path(self.content["target"]).resolve()];
            numImages = len(targetImage);
            batchSize = 1;
            from PIL import Image;
            
            membraneZone = self.content["membraneZone"];
            try:
                if(membraneZone != ""):
                    membraneZone = formMembraneZone(self.content["membraneZone"]);
                else:
                    membraneZone = None;
            except Exception as e:
                membraneZone = None;
                self.sendToFront(messageType.TaskWarning, {"content":f"membrane Zone generate failed because: \n{e}\nthe statics are made without using the given membrane zone"});
            statics = {"bubbleNum":0,"bubbleArea":0,"bubbleAreaRatio":0,
                       "membraneZoneArea":0,"membraneZoneAreaRatio":0,
                       "bubbleOnMembraneArea":0,"bubbleOnMembraneAreaRatio":0,
                       "bubbleElsewhereArea":0,"bubbleElsewhereAreaRatio":0,
                       "totalArea":0};
            
            for i in range(0, numImages, batchSize):
                self.senderToFront.put(message(-1,messageType.PicturePredictProgress,
                                               {"now":i,"total":numImages,"step":0,"totalStep":1}));
                
                start = i
                end = min(i + batchSize, numImages)
                
                currentBatch = targetImage[start:end]
                
                sizes = Image.open(targetImage[i]).size;
                if(self.content["width"] not in ["",-1,0,"-1",0,None]):
                    sizes[0] = self.content["width"];
                if(self.content["height"] not in ["",-1,0,"-1",0,None]):
                    sizes[1] = self.content["height"];
                batchResults = model(currentBatch, stream=True, imgsz=[sizes[1],sizes[0]],max_det=99999)
                
                # Save results for current batch
                for imgPath, result in zip(currentBatch, batchResults):
                    bubbleData=self.saveLabels(imgPath, result,self.content["saveDir"]);
                    bubbleShapely = [];
                    for i in range(len(bubbleData)):
                        [x,y,w,h] = bubbleData[i][0:4];
                        circle = Point(x, y).buffer(1)
                        scaled = affinity.scale(circle, xfact=w/2, yfact=h/2);
                        bubbleShapely.append(scaled);
                    bubbleShapely = unary_union(bubbleShapely);
                    bubbleShapelyArea = bubbleShapely.area;
                    
                    membraneZoneArea = 0;
                    bubbleOnMembraneArea = 0;
                    bubbleElsewhereArea = 0;
                    if (membraneZone!=None):
                        membraneZoneArea=membraneZone.area;
                        bubbleOnMembraneArea=bubbleShapely.intersection(membraneZone).area;
                        bubbleElsewhereArea = bubbleShapelyArea - bubbleOnMembraneArea
                    statics = {
                        "bubbleNum":len(bubbleData),
                        "bubbleArea":bubbleShapelyArea,
                        "bubbleAreaRatio":bubbleShapelyArea/sizes[0]/sizes[1],
                        "membraneZoneArea":membraneZoneArea,
                        "membraneZoneAreaRatio":membraneZoneArea/sizes[0]/sizes[1],
                        "bubbleOnMembraneArea":bubbleOnMembraneArea,
                        "bubbleOnMembraneAreaRatio":bubbleOnMembraneArea/sizes[0]/sizes[1],
                        "bubbleElsewhereArea":bubbleElsewhereArea,
                        "bubbleElsewhereAreaRatio":bubbleElsewhereArea/sizes[0]/sizes[1],
                        "totalArea":sizes[0]*sizes[1]};
                    bubbleDataFrame=pd.DataFrame(statics,index=[0]);
                    print(os.path.join(self.content["saveDir"],str(imgPath.stem)+"_result.csv"))
                    bubbleDataFrame.to_csv(os.path.join(self.content["saveDir"],str(imgPath.stem)+"_result.csv"),index=False);
                self.senderToFront.put(message(-1,messageType.PicturePredictDone,{"saveDir":self.content["saveDir"]}));
                self.senderToBackend.put(message(self.messageID,messageType.KidDone,{"From":"kid","Id":self.kidId}));
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();

from shapely.geometry import Point
from shapely import affinity
from shapely.ops import unary_union
from shapely.ops import Polygon

def identifyer(task: dict, valve: float=0.9):
    task["stayBool"] = []
    task["state"] = []
    task["shapely"] = []
    for state in bubbleState:
        task[me.bubbleStateToText(state)] = 0;
    for i in range(len(task["content"])):
        
        x, y, w, h = task["content"][i][0:4];
        if w <= 0 or h <= 0:
            w, h = max(w, 1e-6), max(h, 1e-6)
        circle = Point(x, y).buffer(1)
        scaled = affinity.scale(circle, xfact=w/2, yfact=h/2)
        task["shapely"].append(scaled)

    n = len(task["shapely"])
    if n > 1:
        for i in range(n - 1):
            area_i = task["shapely"][i].area
            if area_i == 0:
                common = 0.0
            else:
                inter = task["shapely"][i].intersection(task["shapely"][i+1]).area
                common = inter / area_i
            task["stayBool"].append(common > valve)
        task["stayBool"].append(task["stayBool"][-1])
    else:
        task["stayBool"] = [False] if n == 1 else []

    for i in range(len(task["stayBool"])):
        if i == 0:
            if(task["stayBool"][i]==True):
                task["state"].append(bubbleState.Stay);
            else:
                task["state"].append(bubbleState.Flow);
        else:
            [curr, prev] = task["stayBool"][i], task["stayBool"][i-1];
            if curr and prev:
                task["state"].append(bubbleState.Stay);
            elif curr and not prev:
                task["state"].append(bubbleState.Back);
            elif not curr and prev:
                task["state"].append(bubbleState.Out);
            else:
                task["state"].append(bubbleState.Flow);
        task[me.bubbleStateToText(task["state"][-1])]+=1;

    while len(task["state"]) < len(task["content"]): #正常情况这段代码只运行一次。
        last_state = task["state"][-1] if task["state"] else bubbleState.Stay
        if last_state in (bubbleState.Stay, bubbleState.Back):
            task["state"].append(bubbleState.Stay)
        else:
            task["state"].append(bubbleState.Flow)
        task[me.bubbleStateToText(task["state"][-1])]+=1;

    return task;

def formMembraneZone(json_file):
    import json;
    with open(json_file, 'r',encoding="utf-8") as f:
        data = json.load(f)
    
    membranePolygons = [];
    for shape in data["shapes"]:
        points = shape["points"];
        if len(points) >= 3:
            membranePolygons.append(Polygon(points));
    
    if membranePolygons:
        membranePolygon = unary_union(membranePolygons)
        return membranePolygon;
    else:
        return Polygon();
"""
def staticMaker(bigList,bigListSize, beginEnd: list):
    staticsLocal = {
        "out": [], "back": [], "flow": [], "stay": [],
        "coverage": [], "outArea": [], "backArea": [],
        "flowArea": [], "stayArea": []
    };
    bigListLocal = sh.SharedMemory(name=bigList);
    processed = pickle.loads(bigListLocal.buf[:bigListSize]);
    bigListLocal.close()
    for i in range(beginEnd[0],beginEnd[1],1):
        plate = {
            bubbleState.Stay: [],
            bubbleState.Flow: [],
            bubbleState.Out: [],
            bubbleState.Back: []
        }
        for instance in processed:
            if instance["startFrame"] <= i < instance["endFrame"]:
                nowi = i - instance["startFrame"]
                if nowi < len(instance["state"]) and nowi < len(instance["shapely"]):
                    plate[instance["state"][nowi]].append(instance["shapely"][nowi])

        staticsLocal["out"].append(len(plate[bubbleState.Out]))
        staticsLocal["back"].append(len(plate[bubbleState.Back]))
        staticsLocal["flow"].append(len(plate[bubbleState.Flow]))
        staticsLocal["stay"].append(len(plate[bubbleState.Stay]))
        
        totalArea = {}
        for state in bubbleState:
            union = unary_union(plate[state])
            totalArea[state] = union

        staticsLocal["outArea"].append(totalArea[bubbleState.Out].area)
        staticsLocal["backArea"].append(totalArea[bubbleState.Back].area)
        staticsLocal["flowArea"].append(totalArea[bubbleState.Flow].area)
        staticsLocal["stayArea"].append(totalArea[bubbleState.Stay].area)

        coverage_union = unary_union([totalArea[bubbleState.Out], totalArea[bubbleState.Stay]])
        staticsLocal["coverage"].append(coverage_union.area);
    
    return staticsLocal;
"""
class processSingleVideoStatics:
    def __init__(self, bubbles, senderToFront: mu.Queue,mediaWidth,mediaHeight,valve,membraneZone):
        self.senderToFront = senderToFront;
        self.bubbles = [];
        self.messageID = 0;
        self.mediaSize = [mediaWidth,mediaHeight];
        self.valve=valve;
        self.membraneZone = membraneZone;
        for instance in bubbles:
            if isEmpty(instance):
                continue;
            self.bubbles.append({
                "startFrame": instance[0][-1],
                "content": list(map( lambda x : [*x[0:4]] , instance)),
                "endFrame": instance[-1][-1] + 1
                });
    def sendToFront(self,messagetype,messageContent):
        if(self.senderToFront is not None):
            self.messageID+=1;
            self.senderToFront.put(message(self.messageID,messagetype,messageContent));
            return True;
        else:
            return False;
        
    def run(self):
        bubbleList = self.bubbles;
        total = len(bubbleList);
        if total == 0:
            return {
                "out": [], "back": [], "flow": [], "stay": [],
                "coverage": [], "outArea": [], "backArea": [],
                "flowArea": [], "stayArea": []
            }
        if(self.sendToFront(messageType.VideoPredictProgress,
                            {"now":1,"total":2,"step":1,"totalStep":totalStepVideoProcessing})
           ==False):
            return;
        valves=[self.valve] * total;
        with mu.Pool(processes=max(1,min(total,cpuNum))) as pool:
            processed = pool.starmap(identifyer, tuple(zip(bubbleList,valves)));
        
        if(self.sendToFront(messageType.VideoPredictProgress,
                            {"now":0,"total":1,"step":2,"totalStep":totalStepVideoProcessing})
           ==False):
            return;
        
        frameDependentStatics = {
            "totalInstanceInSight":[],
            "coverageArea": [],"coverageAreaRatio":[],
            "coverageMembraneArea": [],"coverageMembraneAreaRatio":[],"membraneCoveredRatio":[],
            "coverageElsewhereArea": [],"coverageElsewhereAreaRatio":[],"elsewhereCoveredRatio":[],
            "stayElsewhereArea":[],"backElsewhereArea":[]
        };
        for state in bubbleState:
            for suffix in ["Num","NumRatio","Area","AreaRatio"]:
                frameDependentStatics[me.bubbleStateToText(state) + suffix] = [];
        
        end = max(lst["endFrame"] for lst in processed);
        
        """
        staticsRaw = [];
        batchSize = int(max(12,min(48,end/2/16)));
        beginEnd = [];
        
        
        buffer = io.BytesIO();
        pickle.dump(processed,buffer);
        dataBytes=buffer.getvalue();
        
        processedInSharedMemory = sh.SharedMemory(create=True,size=len(dataBytes));
        processedInSharedMemory.buf[:len(dataBytes)] = dataBytes;
        processedInSharedMemoryKey = processedInSharedMemory.name;
        processedInSharedMemorySize = len(dataBytes);
        
        for i in range(0,end,batchSize):
            beginEnd.append([min(i,end),min(i+batchSize,end)]);
        
        with mu.Pool(processes=max(1,min(total,16))) as pool:
            args = [(processedInSharedMemoryKey,processedInSharedMemorySize,bE) for bE in beginEnd];
            staticsRaw = list(pool.starmap(staticMaker,args));
        if(self.sendToFront(messageType.VideoPredictProgress,
                                       {"now":0,"total":len(staticsRaw),"step":3,"totalStep":totalStepVideoProcessing})
           ==False):
            return;
        processedInSharedMemory.close();
        processedInSharedMemory.unlink();
        
        
        for i in range(0,len(staticsRaw)):
            for key in staticsRaw[i].keys():
                frameDependentStatics[key] += staticsRaw[i][key];
            if(self.sendToFront(messageType.VideoPredictProgress,
                                           {"now":i+1,"total":len(staticsRaw),"step":3,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
        """
        """
        for i in range(end):
            plate = {
                bubbleState.Stay: [],
                bubbleState.Flow: [],
                bubbleState.Out: [],
                bubbleState.Back: []
            }
            for instance in processed:
                if instance["startFrame"] <= i < instance["endFrame"]:
                    nowi = i - instance["startFrame"]
                    if nowi < len(instance["state"]) and nowi < len(instance["shapely"]):
                        plate[instance["state"][nowi]].append(instance["shapely"][nowi])

            frameDependentStatics["out"].append(len(plate[bubbleState.Out]))
            frameDependentStatics["back"].append(len(plate[bubbleState.Back]))
            frameDependentStatics["flow"].append(len(plate[bubbleState.Flow]))
            frameDependentStatics["stay"].append(len(plate[bubbleState.Stay]))

            totalArea = {}
            for state in bubbleState:
                union = unary_union(plate[state])
                totalArea[state] = union

            frameDependentStatics["outArea"].append(totalArea[bubbleState.Out].area)
            frameDependentStatics["backArea"].append(totalArea[bubbleState.Back].area)
            frameDependentStatics["flowArea"].append(totalArea[bubbleState.Flow].area)
            frameDependentStatics["stayArea"].append(totalArea[bubbleState.Stay].area)

            coverage_union = unary_union([totalArea[bubbleState.Out], totalArea[bubbleState.Stay]])
            frameDependentStatics["coverage"].append(coverage_union.area)
            if(self.sendToFront(messageType.VideoPredictProgress,
                                           {"now":i+1,"total":end,"step":3,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
        """
        
        n = len(processed)
        instanceID = 0                     # 指向下一个待添加的 instance
        active = []                        # 当前活跃的 instance 列表（直接存储对象引用）
        
        for i in range(end):
            # ----- 1. 加入新开始的 instance -----
            while instanceID < n and processed[instanceID]["startFrame"] == i:
                active.append(processed[instanceID])
                instanceID += 1
            
            # ----- 2. 构建当前帧的 plate -----
            plate = {
                bubbleState.Stay: [],
                bubbleState.Flow: [],
                bubbleState.Out: [],
                bubbleState.Back: []
            }
            for inst in active:
                if inst["startFrame"] <= i < inst["endFrame"]:
                    nowi = i - inst["startFrame"]
                    if nowi < len(inst["state"]) and nowi < len(inst["shapely"]):
                        plate[inst["state"][nowi]].append(inst["shapely"][nowi])
            
            # ----- 3. 统计数量 -----
            totalNum = 0;
            for state in bubbleState:
                totalNum += len(plate[state]);
                frameDependentStatics[me.bubbleStateToText(state)+"Num"].append(len(plate[state]))
            frameDependentStatics["totalInstanceInSight"].append( totalNum );
            for state in bubbleState:
                frameDependentStatics[me.bubbleStateToText(state) + "NumRatio"].append(len(plate[state])/totalNum)
            
            # ----- 4. 计算并集与面积 -----
            totalArea = {}
            totalAreaList = [];
            
            with fu.ThreadPoolExecutor(max_workers=16) as executor:
                totalAreaList = list(executor.map(
                    lambda state : unary_union(plate[state]) if (plate[state]) else None ,bubbleState));
            
            for (state,totalAreaListI) in zip(bubbleState,range(0,len(bubbleState))):
                totalArea[state] = totalAreaList[totalAreaListI];
                
                
            for state in bubbleState:
                frameDependentStatics[me.bubbleStateToText(state)+"Area"].append(totalArea[state].area if totalArea[state] else 0.0);
                frameDependentStatics[me.bubbleStateToText(state)+"AreaRatio"].append( (totalArea[state].area if totalArea[state] else 0.0) / self.mediaSize[0]/self.mediaSize[1] );
            
            # coverage = Back ∪ stay
            
            stay_geoms = []
            back_geoms = []
            coverageArea = 0.0;
            coverageMembraneArea = 0.0;
            coverageElsewhereArea = 0.0;
            membraneArea = 0.0;
            if totalArea[bubbleState.Back]:
                back_geoms.append(totalArea[bubbleState.Back])
            if totalArea[bubbleState.Stay]:
                stay_geoms.append(totalArea[bubbleState.Stay])
            if (stay_geoms+back_geoms!=[]):
                coverageGeoms = unary_union(stay_geoms+back_geoms);
                coverageArea = coverageGeoms.area;
                if(self.membraneZone == None):
                    coverageMembraneArea = 0.0;
                    coverageElsewhereArea = 0.0;
                    stayElsewhereUnionArea=0.0
                    backElsewhereUnionArea=0.0
                else:
                    coverageMembraneArea = coverageGeoms.intersection(self.membraneZone).area;
                    coverageElsewhereArea= coverageArea - coverageMembraneArea;
                    membraneArea = self.membraneZone.area;
                    
                    stayElsewhereUnionArea=unary_union(stay_geoms).intersection(self.membraneZone).area
                    backElsewhereUnionArea=unary_union(back_geoms).intersection(self.membraneZone).area
                    
                    
            else:
                coverageArea = 0.0;
                coverageMembraneArea = 0.0;
                coverageElsewhereArea = 0.0;
            frameDependentStatics["coverageArea"].append(coverageArea)
            frameDependentStatics["coverageAreaRatio"].append(coverageArea / self.mediaSize[0] /self.mediaSize[1]);
            frameDependentStatics["coverageMembraneArea"].append(coverageMembraneArea);
            frameDependentStatics["coverageElsewhereArea"].append(coverageElsewhereArea);
            
            frameDependentStatics["coverageMembraneAreaRatio"].append(coverageMembraneArea / self.mediaSize[0] /self.mediaSize[1]);
            frameDependentStatics["coverageElsewhereAreaRatio"].append(coverageElsewhereArea / self.mediaSize[0] /self.mediaSize[1]);
            frameDependentStatics["membraneCoveredRatio"].append(coverageMembraneArea / membraneArea if(membraneArea>0) else 0);
            frameDependentStatics["elsewhereCoveredRatio"].append(coverageElsewhereArea / (self.mediaSize[0] * self.mediaSize[1] - membraneArea) if(self.mediaSize[0] * self.mediaSize[1] - membraneArea>0) else 0);
            frameDependentStatics["stayElsewhereArea"].append(stayElsewhereUnionArea);
            frameDependentStatics["backElsewhereArea"].append(backElsewhereUnionArea);
            
            if(i%(max(50,end//100))==0):
                if( self.sendToFront(messageType.VideoPredictProgress,
                                     {"now": i+1, "total": end, "step": 3, "totalStep": totalStepVideoProcessing}) == False):
                    
                    return;
            
            # ----- 6. 移除已结束的 instance（下一帧不再活跃）-----
            # 注意：当前帧 i 处理完后，下一帧是 i+1，需要保留 endFrame > i+1 的 instance
            active = [inst for inst in active if inst["endFrame"] > i+1]
        membraneArea = 0;
        
        if(self.membraneZone != None):
            membraneArea = self.membraneZone.area;
        mainStatics = {
            "totalInstanceInSightFrameAveraged":0, #在依时循环中求得
            "coverageAreaFrameAveraged":0,         #在依时循环中求得
            "coverageAreaRatioFrameAveraged":0,    #在依时循环中求得
            "averageFramesInstanceInSight":0,      #在依物循环中求得
            "totalInstance":len(processed),
            "membraneArea": membraneArea,
            "membraneAreaRatio":membraneArea/self.mediaSize[0]/self.mediaSize[1]
            }
        
        
        for state in bubbleState:
            for suffix in ["NumFrameAveraged","NumRatioFrameAveraged",        #在依时循环中求得
                           "AreaFrameAveraged","AreaRatioFrameAveraged",      #在依时循环中求得
                           "NumInstanceAveraged","NumRatioInstanceAveraged"]: #在依物循环中求得
                mainStatics[me.bubbleStateToText(state)+suffix]=0;
        
        #依时循环
        import numpy as npy;
        for (keyNow,processingNow) in zip(frameDependentStatics.keys(),range(0,len(frameDependentStatics))):
            frameAveragedKey = keyNow + "FrameAveraged";
            mainStatics[frameAveragedKey] = sum(frameDependentStatics[keyNow])/len(frameDependentStatics[keyNow]);
            print("this is nothing just for test:"+str(len(frameDependentStatics[keyNow])))
            frameVarKey = keyNow + "FrameVariance";
            mainStatics[frameVarKey] = npy.var(frameDependentStatics[keyNow],ddof=0);
            if self.sendToFront(messageType.VideoPredictProgress,
                                {"now": processingNow+1, "total": len(frameDependentStatics), "step": 4, "totalStep": totalStepVideoProcessing}) == False:
                return;
        
        #依物循环
        for (instance,instanceID) in zip(processed,range(0,len(processed))):
            lifeSpan = len(instance["state"]);
            
            mainStatics["averageFramesInstanceInSight"]+= lifeSpan;
            for state in bubbleState:
                mainStatics[me.bubbleStateToText(state)+"NumInstanceAveraged"]+= instance[me.bubbleStateToText(state)];
                mainStatics[me.bubbleStateToText(state)+"NumRatioInstanceAveraged"]+= instance[me.bubbleStateToText(state)]/lifeSpan;
            if(instanceID % max(100,len(processed)//100) == 0):
                if self.sendToFront(messageType.VideoPredictProgress,
                                    {"now": instanceID+1, "total": len(processed), "step": 5, "totalStep": totalStepVideoProcessing}) == False:
                    return;
                
        for key in ["averageFramesInstanceInSight"]:
            mainStatics[key]/=mainStatics["totalInstance"];
            
        for state in bubbleState:
            for key in ["NumInstanceAveraged","NumRatioInstanceAveraged"]:
                mainStatics[me.bubbleStateToText(state)+key]/=mainStatics["totalInstance"];
        
        return [frameDependentStatics,mainStatics,processed]

def interpolateTrajectory(instance):
    """对单个轨迹进行线性插值，补全缺失帧"""
    if not instance:
        return instance

    # 提取已知帧的信息
    frames = [item[-1] for item in instance]
    bboxes = [item[:4] for item in instance]   # [x,y,w,h]
    confs = [item[4] for item in instance]

    startFrame = frames[0]
    endFrame = frames[-1]
    totalLen = endFrame - startFrame + 1

    # 初始化连续帧数组（None 表示缺失）
    contFrames = [None] * totalLen
    contConfs = [0.0] * totalLen

    # 填入已知帧
    for i, (f, bbox, conf) in enumerate(zip(frames, bboxes, confs)):
        idx = f - startFrame
        contFrames[idx] = bbox
        contConfs[idx] = conf

    # 线性插值缺失帧
    for i in range(totalLen):
        if contFrames[i] is not None:
            continue
        # 找左边最近已知帧
        leftIdx = i - 1
        while leftIdx >= 0 and contFrames[leftIdx] is None:
            leftIdx -= 1
        # 找右边最近已知帧
        rightIdx = i + 1
        while rightIdx < totalLen and contFrames[rightIdx] is None:
            rightIdx += 1

        # 左右都存在（首尾已知保证一定存在）
        if leftIdx >= 0 and rightIdx < totalLen:
            leftBbox = contFrames[leftIdx]
            rightBbox = contFrames[rightIdx]
            ratio = (i - leftIdx) / (rightIdx - leftIdx)
            newBbox = [
                leftBbox[0] + (rightBbox[0] - leftBbox[0]) * ratio,
                leftBbox[1] + (rightBbox[1] - leftBbox[1]) * ratio,
                leftBbox[2] + (rightBbox[2] - leftBbox[2]) * ratio,
                leftBbox[3] + (rightBbox[3] - leftBbox[3]) * ratio,
            ]
            contFrames[i] = newBbox
            # conf 保持 0.0（插值置信度无意义）

    # 重新组装为 [x,y,w,h,conf,frameIdx] 格式
    result = []
    for i in range(totalLen):
        if contFrames[i] is not None:   # 理论上全部非 None
            result.append([
                contFrames[i][0], contFrames[i][1],
                contFrames[i][2], contFrames[i][3],
                contConfs[i], startFrame + i
            ])
    return result

class bPredictSingleVideo(mu.Process):
    def __init__(self,
                  senderToBackend: mu.Queue, senderToFront: mu.Queue, recver:mu.Queue, content: dict = {},kidId : int = 0):
        mu.Process.__init__(self,daemon=False);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.recver = recver;
        self.content = content;
        self.messageID = 0;
        self.kidId = 0;
    def sendToFront(self,messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToFront is not None):
            self.messageID += 1;
            self.senderToFront.put(message(self.messageID,messageType,messageContent));
            
            return True;
        else:
            return False;
    
    def run(self):
        try:
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":0,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
            from ultralytics import YOLO
            model = YOLO(self.content["model"]);
            videoPath = self.content["target"];
            outputDir = self.content["saveDir"];
            outputOriginData = os.path.join(outputDir, "originData.pkl");
            outputFrameDependentStatics = os.path.join(outputDir, "frameDependentStatics.csv")
            outputMainStatics = os.path.join(outputDir, "mainStatics.csv")
            import cv2
            
            
            if(self.content["width"] in [-1,"-1",0,"0",None,""] or self.content["width"]<=0):
                self.content["width"] = cv2.VideoCapture(videoPath).get(cv2.CAP_PROP_FRAME_WIDTH);
            if(self.content["height"] in [-1,"-1",0,"0",None,""] or self.content["height"]<=0):
                self.content["height"] = cv2.VideoCapture(videoPath).get(cv2.CAP_PROP_FRAME_HEIGHT);
            
            results = model.track(
                videoPath,
                stream=True,
                device=self.content["device"],
                #conf=0.05,
                #iou=0.2,
                vid_stride=self.content["vidStride"],
                imgsz=(self.content["height"], self.content["width"]),
                max_det=self.content["maxInstances"],
                show_conf=self.content["saveVideoWithConfidence"],
                show_labels=self.content["saveVideoWithLabel"],
                line_width=1,
                batch=self.content["batchSize"],
                save=self.content["saveVideo"],
                persist=True,
                save_dir= outputDir,
                verbose=False
                )
            del model;
            from collections import defaultdict
            trackData = defaultdict(list)
            
            
            totalFrames = cv2.VideoCapture(videoPath).get(cv2.CAP_PROP_FRAME_COUNT);
            
            frameIdx = 0
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xywh.cpu().numpy();
                    confs = result.boxes.conf.cpu().numpy();
                    track_ids = result.boxes.id.cpu().numpy() if result.boxes.id is not None else None
    
                    if track_ids is None:
                        frameIdx += 1
                        continue
    
                    for i in range(len(boxes)):
                        track_id = int(track_ids[i])
                        info = [boxes[i,0], boxes[i,1], boxes[i,2], boxes[i,3], confs[i], frameIdx]
                        trackData[track_id].append(info)
    
                frameIdx += 1;
                if((frameIdx*2)%self.content["batchSize"]==0):
                    if(self.sendToFront(messageType.VideoPredictProgress,
                                     {"now":frameIdx,"total":totalFrames,"step":0,"totalStep":totalStepVideoProcessing})
                       ==False):
                        return;
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":2,"step":1,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
            trackDict = dict(trackData);
            trackDictValue = trackDict.values();
            with mu.Pool(processes=cpuNum) as pool:
                interpolatedResults = pool.map(interpolateTrajectory, trackDictValue);
            newTrackDict = {tid: interpolatedResults[i] for i, tid in enumerate(trackDict.keys())};
            trackData = defaultdict(list, newTrackDict);
            del newTrackDict,interpolatedResults,trackDict;
            try:
                if(self.content["membraneZone"] == "" ):
                    membraneZone = None;
                else:
                    membraneZone = formMembraneZone(self.content["membraneZone"]);
            except Exception as e:
                membraneZone=None;
                self.sendToFront(messageType.TaskWarning, {"content":f"membrane Zone generate failed because: \n{e}\nthe statics are made without using the given membrane zone"});
            cover = processSingleVideoStatics(trackData.values(),self.senderToFront,self.content["width"],self.content["height"],self.content["valve"],membraneZone);
            
            [frameDependentStatics,mainStatics,processed] = cover.run()
            if(self.sendToFront(messageType.VideoPredictProgress,
                             {"now":0,"total":1,"step":6,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
            originData = {"appSignature":gl.appSignature,"frameDependentStatics":frameDependentStatics,"mainStatics":mainStatics,
                          "processed":processed};
            #bubbleDataFrame=pd.DataFrame(trackData,index=range(len(trackData)));
            #bubbleDataFrame["WidthHeight"][0:2] = [self.content["width"],self.content["height"]];
            #bubbleDataFrame.to_parquet(outputOriginData,index=False);
            #del bubbleDataFrame;
            
            
            pd.DataFrame(frameDependentStatics).to_csv(outputFrameDependentStatics, index=True);
            pd.DataFrame(mainStatics,index=[0]).to_csv(outputMainStatics, index=False);
            
            import pgzip;
            with pgzip.open(outputOriginData, 'wb',thread=cpuNum) as f:
                pickle.dump(originData, f, protocol=pickle.HIGHEST_PROTOCOL);
            
            if(self.sendToFront(messageType.VideoPredictProgress,
                             {"now":1,"total":1,"step":6,"totalStep":totalStepVideoProcessing})
               ==False):
                return;
            if(self.sendToFront(messageType.VideoPredictDone,
                             {"outputFrameDependentStatics":outputFrameDependentStatics,"outputMainStatics":outputMainStatics,"processed":outputOriginData})
               ==False):
                return;
            
            self.senderToBackend.put(message(self.messageID,messageType.KidDone,{"From":"kid","Id":self.kidId}));
            
            return;
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();

class bReadProcessedData(mu.Process):
    def __init__(self,senderToBackend:mu.Queue, senderToFront: mu.Queue  , content:dict , kidId:int = 0):
        mu.Process.__init__(self,daemon=True);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.content = content;
        self.recver = mu.Queue();
        self.messageID = 0;
        self.kidId = 0;
        
    def LoadPickle(self):
        
        import pgzip;
        loaded = [];
        with pgzip.open(self.content["picklePath"],"rb",thread=cpuNum) as f:
            loaded = pickle.load(f);
        
        if(not isinstance(loaded, dict) or 
           loaded.get("appSignature") not in gl.noWarnSignature):
            if(loaded.get("appSignature" not in gl.warnSignature)):
                self.sendToFront(messageType.TaskWarning, {"content":f"the .pkl file comes from an older version of this app.\n\nOpening that file may not be safe.\n\nThis code will tey to open it."});
            else:
                raise ValueError("This file was not created by this app (signature mismatch)")
        return [loaded["frameDependentStatics"],
                loaded["mainStatics"],
                loaded["processed"]];
    
    def sendToFront(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToFront is not None):
            self.messageID +=1;
            self.senderToFront.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;
    
    def sendToBackend(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToBackend is not None):
            self.messageID +=1;
            self.senderToBackend.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;
    
    def run(self):
        try:
            if(self.sendToFront(messageType.GaugeSetRunning,
                                {"content":"Loading..."})
               ==False):
                return;
            [frameDependentStatics,mainStatics,processed] = self.LoadPickle();
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":1,"total":1,"step":0,"totalStep":1})
               ==False):
                return;
            
            self.sendToFront(
                messageType.LoadPickleDone,
                {"frameDependentStatics":frameDependentStatics,
                 "mainStatics":mainStatics,
                 "processed":self.content["picklePath"]});
            
            self.sendToBackend(messageType.KidDone,{"From":"kid","Id":self.kidId});
            
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();
import math as ma

totalStepDrawPlot = 3;
class drawPlot(bReadProcessedData):
    def __init__(self,senderToBackend:mu.Queue, senderToFront: mu.Queue , content:dict , kidId:int = 0):
        bReadProcessedData.__init__(self, senderToBackend, senderToFront, content);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.content = content;
        self.recver = mu.Queue();
        self.messageID = 0;
        self.kidId = 0;
        
    def sendToFront(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToFront is not None):
            self.messageID +=1;
            self.senderToFront.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;
    
    def sendToBackend(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToBackend is not None):
            self.messageID +=1;
            self.senderToBackend.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;
    
    def getDiamater(self,shapelyClass):
        s = shapelyClass.area;      #this is the area
        return ma.sqrt(4*s/ma.pi);  #circleArea =  pi * d^2 / 4 => 4 * circleArea / pi = d^2
    def getArea(self,shapelyClass):
        return shapelyClass.area;
    def getWidth(self,content):
        return content[2];
    def getHeight(self,content):
        return content[3];
    def get(self,shapelyClass,content):
        if(self.content["perspect"]==gl.sizeDistributionImagePerspect.Diamater):
            return self.getDiamater(shapelyClass);
        elif(self.content["perspect"]==gl.sizeDistributionImagePerspect.Area):
            return self.getArea(shapelyClass);
        elif(self.content["perspect"]==gl.sizeDistributionImagePerspect.Width):
            return self.getWidth(content);
        elif(self.content["perspect"]==gl.sizeDistributionImagePerspect.Height):
            return self.getHeight(content);
        
    def isTheRightState(self,state:bubbleState):
        if(self.content["type"]==gl.sizeDistributionImageType.All):
            return True;
        elif(self.content["type"]==gl.sizeDistributionImageType.Stay):
            return state == bubbleState.Stay;
        elif(self.content["type"]==gl.sizeDistributionImageType.Flow):
            return state == bubbleState.Flow;
        elif(self.content["type"]==gl.sizeDistributionImageType.Out):
            return state == bubbleState.Out;
        elif(self.content["type"]==gl.sizeDistributionImageType.Back):
            return state == bubbleState.Back;
    
    def choose(self):
        
        plate = [];
        for (instance,instanceID) in zip(self.content["processed"],range(0,len(self.content["processed"]))):
            if(instance["startFrame"]<= self.content["targetFrameStart"] <instance["endFrame"]):
                startID = self.content["targetFrameStart"] - instance["startFrame"];
                for i in range(startID,min(len(instance["content"]),startID+self.content["lasting"])):
                    if(self.isTheRightState(instance["state"][i])):
                        plate.append(self.get(instance["shapely"][i],instance["content"][i]));
            if(instanceID % max(10000,int(len(self.content["processed"])//10)) == 0):
                if(self.sendToFront(messageType.VideoPredictProgress,
                                    {"now":instanceID,"total":len(self.content["processed"]),"step":1,"totalStep":totalStepDrawPlot})
                   ==False):
                    return;
        return plate;
    def run(self):
        try:
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":0,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            [a,b,self.content["processed"]]=self.LoadPickle();
            del a,b;
            
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":1,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            plate = self.choose();
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":2,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            if(plate == None):
                return;
            if(plate == []):
                self.sendToBackend(messageType.KidError, {"From":"kid","Id":self.kidId,"reason":"There is no datum to draw a plot."});
                return;
            import matplotlib.pyplot as plt;
            [fig, ax] = plt.subplots();
            fig.subplots_adjust(left=0.25)
            ax.hist(plate,bins=self.content["bins"]);
            ylabels = {
                gl.sizeDistributionImageType.Stay:"Staying",
                gl.sizeDistributionImageType.Flow:"Flowing",
                gl.sizeDistributionImageType.Out: "Detaching",
                gl.sizeDistributionImageType.Back:"Re-attaching",
                gl.sizeDistributionImageType.All:"All"
                }
            xlabels = {
                gl.sizeDistributionImagePerspect.Diamater:"Diamater(pixel)",
                gl.sizeDistributionImagePerspect.Area    :"Area(pixel)",
                gl.sizeDistributionImagePerspect.Height  :"Height(pixel)",
                gl.sizeDistributionImagePerspect.Width   :"Width(pixel)"
                }
            ax.set_xlabel('{:s}'.format(xlabels[self.content["perspect"]]));
            ax.set_ylabel('Number of {:s} Bubbles\nin Frame {:d} to {:d}'.format(ylabels[self.content["type"]],self.content["targetFrameStart"],self.content["targetFrameStart"]+self.content["lasting"]-1));
            plt.savefig(self.content["saveDir"]);
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":1,"total":1,"step":2,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            
            self.sendToFront(messageType.DrawPlotDone,{"imagePath":self.content["saveDir"]});
            self.sendToBackend(messageType.KidDone,{"From":"kid","Id":self.kidId});
            return ;
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();
            
class savePlotData(drawPlot):
    def __init__(self,senderToBackend:mu.Queue, senderToFront: mu.Queue , content:dict , kidId:int = 0):
        drawPlot.__init__(self,senderToBackend,senderToFront,content,kidId);
    def run(self):
        try:
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":0,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            [a,b,self.content["processed"]]=self.LoadPickle();
            del a,b;
            plate = self.choose();
            if(plate == None):
                return;
            if(plate == []):
                plate = [0];
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":1,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            
            ylabels = {
                gl.sizeDistributionImageType.Stay:"Staying",
                gl.sizeDistributionImageType.Flow:"Flowing",
                gl.sizeDistributionImageType.Out: "Detaching",
                gl.sizeDistributionImageType.Back:"Re-attaching",
                gl.sizeDistributionImageType.All:"All"
                }
            xlabels = {
                gl.sizeDistributionImagePerspect.Diamater:"Diamater(pixel)",
                gl.sizeDistributionImagePerspect.Area    :"Area(pixel)",
                gl.sizeDistributionImagePerspect.Height  :"Height(pixel)",
                gl.sizeDistributionImagePerspect.Width   :"Width(pixel)"
                }
            plateDataFrame = pd.DataFrame(
                {"bubbleType":[ylabels[self.content["type"]]]+ [""]*max(0,len(plate)-1),
                 "staticFromFrame":[self.content["targetFrameStart"]] + [""]*max(0,len(plate)-1),
                 "staticEndFrame" :[self.content["lasting"]+self.content["targetFrameStart"]-1]+ [""]*max(0,len(plate)-1),
                 "frameNum"       :[self.content["lasting"]]+ [""]*max(0,len(plate)-1),
                 xlabels[self.content["perspect"]]:plate,
                 }, index=list(range(0,len(plate))));
            
            plateDataFrame.to_csv(self.content["saveDir"],index=False);
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":1,"total":1,"step":1,"totalStep":totalStepDrawPlot})
               ==False):
                return;
            
            self.sendToFront(messageType.SavePlotDataDone,{"csvPath":self.content["saveDir"]});
            self.sendToBackend(messageType.KidDone,{"From":"kid","Id":self.kidId});
            return ;
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();

class saveMono(bReadProcessedData):
    def __init__(self,senderToBackend:mu.Queue, senderToFront: mu.Queue , content:dict , kidId:int = 0):
        bReadProcessedData.__init__(self, senderToBackend, senderToFront, content);
        self.senderToBackend = senderToBackend;
        self.senderToFront = senderToFront;
        self.content = content;
        self.recver = mu.Queue();
        self.messageID = 0;
        self.kidId = 0;
        
    def sendToFront(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToFront is not None):
            self.messageID +=1;
            self.senderToFront.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;
    
    def sendToBackend(self,messageType:messageType,messageContent:dict):
        try:
            while(True):
                tmpMessage = self.recver.get_nowait();
                if(tmpMessage.type == messageType.BackendIsDead):
                    return False;
        except(qu.Empty):
            pass;
        if(self.senderToBackend is not None):
            self.messageID +=1;
            self.senderToBackend.put(message(self.messageID,messageType,messageContent));
            return True;
        else:
            return False;

    def choose(self):
        
        plate = {"Summary":{"frameNo":self.content["targetFrame"]}};
        for i in bubbleState:
            plate[me.bubbleStateToText(i)]=[];
        for i in self.content["frameDependentStatics"].keys():
            plate["Summary"][i] = self.content["frameDependentStatics"][i][self.content["targetFrame"]];
        for (instance,instanceID) in zip(self.content["processed"],range(0,len(self.content["processed"]))):
            if(instance["startFrame"]<= self.content["targetFrame"] <instance["endFrame"]):
                frameID = self.content["targetFrame"]-instance["startFrame"];
                try:
                    state = instance["state"][frameID];
                except Exception as e:
                    with open('debug_log.txt', 'w', encoding='utf-8') as log:
                        log.write(f"frameID: {frameID}\n")
                        log.write("start: {}\n".format(instance["startFrame"]))
                        log.write("end:{}\n".format(instance["endFrame"]))
                        log.write("len:{}\n".format(len(instance["state"])))
                        log.write("d:{}\n".format(instanceID))
                    raise e;
                bubbleData = {
                              "x(pixel)":instance["content"][frameID][0],
                              "y(pixel)":instance["content"][frameID][1],
                              "w(pixel)":instance["content"][frameID][2],
                              "h(pixel)":instance["content"][frameID][3],
                              "bubbleState"   :me.bubbleStateToText(state)
                             }
                plate[me.bubbleStateToText(state)].append(bubbleData);
            if(instanceID % max(1000,int(len(self.content["processed"])//100)) == 0):
                if(self.sendToFront(messageType.VideoPredictProgress,
                                    {"now":instanceID,"total":len(self.content["processed"]),"step":1,"totalStep":3})
                   ==False):
                    return;
        return plate;
    def run(self):
        try:
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":0,"totalStep":3})
               ==False):
                return;
            [self.content["frameDependentStatics"],b,self.content["processed"]]=self.LoadPickle();
            del b;
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":0,"total":1,"step":1,"totalStep":3})
               ==False):
                return;
            plate = self.choose();
            if(plate == None):
                return;
            if(plate == {}):
                self.sendToBackend(messageType.KidError, {"From":"kid","Id":self.kidId,"reason":"There is no datum to save."});
                return;
            plateDataFrameBubble = pd.DataFrame();
            for i in plate.keys():
                if(i != "Summary"):
                    plate[i] = pd.DataFrame(plate[i],index=range(0,len(plate[i])));
                    plateDataFrameBubble = pd.concat([plateDataFrameBubble,plate[i]]);
                else:
                    plate[i] = pd.DataFrame(plate[i],index=range(0,1));
            with open(self.content["saveDir"], 'w',newline="") as f:
                plate["Summary"].to_csv(f, index=True);
                f.write('\n')  # 可选空行分隔
                plateDataFrameBubble.to_csv(f, index=True);
            if(self.sendToFront(messageType.VideoPredictProgress,
                                {"now":1,"total":1,"step":2,"totalStep":3})
               ==False):
                return;
            
            self.sendToFront(messageType.SaveMonoDone,{"csvPath":self.content["saveDir"]});
            self.sendToBackend(messageType.KidDone,{"From":"kid","Id":self.kidId});
            return ;
        except Exception as e:
            self.senderToBackend.put(message(0,messageType.KidError,{"From":"kid","Id":self.kidId,"reason":str(e)}));
            tr.print_exc();
            

class backend(mu.Process):
    def __init__(self,
                 recver: mu.Queue , sender: mu.Queue):
        mu.Process.__init__(self,daemon=False);
        self.recver = recver;
        self.sender = sender;
        self.senderToKids = [];
        self.kids = [];
        self.sendId = 1;
        self.frontAlive = 3000;
        self.kidIdBook = [];
        self.kidIdUse = 0;
        self.frontBlock = False;
    def setKidId(self):
        self.kidIdUse += 1;
        self.kidIdBook.append(self.kidIdUse);
        return self.kidIdUse;
    def sendToAllKids(self,
             messageType: messageType = messageType.Error , content:dict={"From":"backend"} ):
        try:
            for i in self.senderToKids:
                i.put(message(self.sendId , messageType , content));
        except (EOFError, BrokenPipeError, OSError):
            pass
        
    def send(self,
             messageType: messageType = messageType.Error , content:dict={"From":"backend"} ):
        try:
            self.sender.put(message(self.sendId , messageType , content));
            self.sendId+=1;
        except (EOFError, BrokenPipeError, OSError):
            pass;
    
    def recverRenew(self):
        try:
            message = self.recver.get(block=False);
            
            if(message.type == messageType.FrontIsDead):
                #Terminate this app
                self.sendToAllKids(messageType.BackendIsDead,{"From":"backend"});
                return False;
            
            
            if(message.type == messageType.KidError):
                if(message.content["From"] == "kid"):
                    if(message.content["Id"] in self.kidIdBook):
                        self.kidIdBook.remove(message.content["Id"]);
                        for i in range(0,len(self.kids)):
                            if(self.kids[i].kidId == message.content["Id"]):
                                self.kids[i].terminate();
                                self.kids.pop(i);
                                break;
                    self.send(messageType.TaskFailed,{"From":"backend","reason":message.content["reason"]});
            
            if(message.type == messageType.KidDone):
                if(message.content["Id"] in self.kidIdBook):
                    self.kidIdBook.remove(message.content["Id"]);
                    for i in range(0,len(self.kids)):
                        if(self.kids[i].kidId == message.content["Id"]):
                            self.kids[i].terminate();
                            self.kids.pop(i);
                            break;
            
            if(message.type == messageType.FrontAlive):
                self.frontAlive = 5000;
            if(message.type == messageType.FrontBlocked):
                self.frontBlock = True;
            elif(message.type == messageType.FrontUnblocked):
                self.frontBlock = False;
            if(self.frontAlive <= 0 and self.recver.empty()):
                #terminate this app.
                return False;
            
            
            
            
            if(message.type == messageType.PicturePredictSingle):
                proc = bPredictSinglePicture(self.recver,self.sender,message.content,self.setKidId());
                proc.start();
            if(message.type == messageType.VideoPredict):
                self.senderToKids.append(mu.Queue());
                proc = bPredictSingleVideo(self.recver,self.sender,self.senderToKids[-1],message.content,self.setKidId());
                proc.start();
                self.kids.append(proc);
            if(message.type == messageType.PicturePredict):
                proc = bPredict(self.recver,self.sender,message.content,self.setKidId());
                proc.start();
                self.kids.append(proc);
            if(message.type == messageType.LoadPickle):
                proc = bReadProcessedData(self.recver, self.sender, message.content ,self.setKidId() )
                proc.start();
                self.kids.append(proc);
            if(message.type == messageType.DrawPlot):
                proc = drawPlot(self.recver, self.sender, message.content,self.setKidId());
                proc.start();
                self.kids.append(proc);
            if(message.type == messageType.SavePlotData):
                proc = savePlotData(self.recver, self.sender, message.content,self.setKidId());
                proc.start();
                self.kids.append(proc);
            if(message.type == messageType.SaveMono):
                proc = saveMono(self.recver, self.sender, message.content,self.setKidId());
                proc.start();
                self.kids.append(proc);
            return True;
        except(qu.Empty):
            self.frontAlive -= 20;
            if(self.frontAlive <= 0 and self.recver.empty() and self.frontBlock==True):
                #terminate this app.
                return False;
            return True;
        except (EOFError, BlockingIOError, OSError, BrokenPipeError):
            return False;
    
    def run(self):
        try:
            loopNum = 0;
            while(True):
                loopNum += 1;
                if(loopNum >= 1000/mainLoopRenewInternals):
                    loopNum = 0;
                    self.send(messageType.BackendAlive,{});
                
                msg = self.recverRenew();
                if(msg == False):
                    self.ends();
                    break;
                ti.sleep(mainLoopRenewInternals/1000.0);
        except Exception as e:
            print(e);
            tr.print_exc();
            self.terminate();
    def ends(self):
        self.sendToAllKids(messageType.BackendIsDead,{});
        self.send(messageType.BackendIsDead,{});