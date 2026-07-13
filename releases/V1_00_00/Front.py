# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 17:39:04 2026

@author: Tianrang Yang、Zhen Fang (Fang-FuDaGuoNanCeYe)
"""
import GlobalArguments as gl
import wx
import pathlib as pa
import FrontBase as fr
import multiprocessing as mu
import queue as qu
from Message import message
from Message import messageType
import pandas as pd
import time as ti
import os
class FrontMain(fr.MainFrame):
    def __init__(self,
                 parent):
        fr.MainFrame.__init__(self,parent);
        self.sender=mu.Queue();
        self.recver=mu.Queue();
        self.sendId = -1;
        self.backendAlive = 3000;
        self.alive = True;
        self.FrontAlivePulser.Start(1000);
        self.recverRenewTimer.Start(50);
        self.mainStatics = pd.DataFrame();
        self.frameDependentStatics = pd.DataFrame();
        self.backend = [];
        self.launchBackend();
        self.processedPath = "";
        self.processedFrameLen = 0;
        self.frameScaleVerifier();
    def gaugeZero(self):
        self.gauge.SetValue(0);
        self.gaugeText.SetLabel("StandBy");
        self.m_collapsiblePane3.Layout();
    def launchBackend(self):
        self.recverRenewTimer.Stop();
        if(len(self.backend) > 0):
            for bkend in self.backend:
                bkend.terminate();
        self.backend = [];
        self.backendAlive=3000;
        self.recver = mu.Queue();
        self.sender = mu.Queue();
        import Backend as ba;
        self.backend.append(ba.backend(recver=self.sender,sender=self.recver));    
        self.backend[-1].start();
        self.unlockTaskEntry();
        self.gaugeZero();
        self.recverRenewTimer.Start();
        
    def stopRunning(self,event):
        self.stopButton.Enable(False);
        self.launchBackend();
        
        self.stopButton.Enable(True);
        
    def send(self,
             messageType: messageType = messageType.Error , content:dict={} ):
        try:
            self.sender.put(message(self.sendId , messageType , content));
            self.sendId-=1;
        except (EOFError, BrokenPipeError, OSError):
            pass;
        
    def OnClose( self, event ):
        self.Alive=False;
        self.gaugeRenewTimer.Stop();
        self.FrontAlivePulser.Stop();
        self.recverRenewTimer.Stop();
        self.send(messageType.FrontIsDead,{});
        self.Destroy()
    
    def predictMessagePacking(self):
        content = {
            "model": self.modelPicker.Path,
            "target":self.targetPicker.Path,
            "device":self.devicePicker.GetValue(),
            "batchSize":self.batchSizePicker.GetValue(),
            "valve": self.valvePicker.GetValue(),
            "vidStride":self.vidStridePicker.GetValue(),
            "maxInstances":self.maxInstancesPicker.GetValue(),
            "width":self.widthPicker.GetValue(),
            "height":self.heightPicker.GetValue(),
            "saveVideo":self.saveVideoPicker.GetValue(),
            "saveVideoWithLabel":self.saveVideoWithLabelsPicker.GetValue(),
            "saveVideoWithConfidence":self.saveVideoWithConfidencePicker.GetValue(),
            "saveDir":self.SaveDirPicker.Path,
            "membraneZone":self.membraneZonePicker.Path,
            }
        try:
            
            if(content["target"] in [None,""]):
                raise OSError("target missing or illegal: {:s}".format(content["target"]));
            defaults = {
                "model": r"best.pt",
                "target":"",
                "device":"0",
                "batchSize":16,
                "valve": 0.9,
                "vidStride":1,
                "maxInstances":9999,
                "width": -1,
                "height":-1,
                "saveVideo":True,
                "saveVideoWithLabel":False,
                "saveVideoWithConfidence":False,
                "saveDir":os.path.join(os.path.dirname(content["target"]),"track_"+ti.strftime(r"%Y%m%d_%H%M%S",ti.localtime())),
                "membraneZone":"",
                }
            modelDir = pa.Path(content["model"]);
            if(modelDir.exists() == False or 
               modelDir.is_file() == False or
               modelDir.suffix not in [".pt"]):
                dlg = wx.MessageDialog(None,"Model path {:s} \n is unexpected, do you want to use the default YOLO model?".format(content["model"]),"Illegal Path",style=wx.YES_NO | wx.ICON_WARNING);
                self.send(messageType.FrontBlocked,{});
                sendBack = dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
                if(sendBack == wx.ID_YES):
                    content["model"] = defaults["model"];
                else:
                    self.unlockTaskEntry();
                    return None;
            membraneZoneDir = pa.Path(content["membraneZone"]);
            if(membraneZoneDir.exists() == False or 
               membraneZoneDir.is_file() == False or
               membraneZoneDir.suffix not in [".json"]):
                content["membraneZone"] = "";
        except Exception as e:
            dlg = wx.MessageDialog(None,"An error occured, task failed: \n\n {}".format(str(e)),"Task Failed",style=wx.OK | wx.ICON_ERROR);
            self.send(messageType.FrontBlocked,{});
            sendBack = dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            return None;
        
        for i in defaults.keys():
            if(content[i] in [None,""]):
                content[i] = defaults[i];
            
        if(type(content["batchSize"]) != type(0) or 
           content["batchSize"] < 1):
            content["batchSize"] = defaults["batchSize"];
        
        if(type(content["vidStride"] != type(0)) or
           content["vidStride"] < 1):
            content["vidStride"] = defaults["vidStride"];
        
        if(type(content["maxInstances"] != type(0)) or
           content["maxInstances"]<1):
            content["maxInstances"] = defaults["maxInstances"];
        
        if(type(content["valve"]) != type(0.1) or
           content["valve"]<=0 or content["valve"]>=1):
            content["valve"] = defaults["valve"];
        
        try:
            saveDir = pa.Path(content["saveDir"]);
            saveDir.resolve();
            if(saveDir.suffix):
                saveDir=saveDir.parent;
            if(saveDir.exists()==False):
                saveDir.mkdir(parents=True, exist_ok=True);
        except OSError as e:
            dlg = wx.MessageDialog(None,r"Save directory is illegal. Do you want to continue the task with the default directory?\n\n the default directory is: {:s}\n\nError is: {:s}".format(defaults["saveDir"],str(e)),"Illegal Path",style=wx.YES_NO | wx.ICON_WARNING);
            self.send(messageType.FrontBlocked,{});
            sendBack = dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            if(sendBack == wx.ID_YES):
                content["saveDir"] = defaults["saveDir"];
            else:
                self.unlockTaskEntry();
                return None;
        
        return content;
                
    def predict( self,
                event ):
        targetPath = self.targetPicker.Path;
        content = self.predictMessagePacking();
        if(content is None):
            return;
        if(targetPath.endswith(("png","jpg","jpeg"))):
            self.send(messageType.PicturePredictSingle,content);
        elif(targetPath.endswith(("mp4","avi"))):
            self.send(messageType.VideoPredict,content);
        else:
            targetPathPathlib = pa.Path(targetPath);
            dlg = wx.MessageDialog(None,"The suffix {} is not supported".format(targetPathPathlib.suffix),style=wx.OK | wx.ICON_WARNING);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            return;
        self.lockTaskEntry();
    def lockTaskEntry(self):
        self.predictButton.Enable(False);
        self.loadButton.Enable(False);
        self.saveSingle.Enable(False);
        self.saveSizeDistributionDataButton.Enable(False);
        self.saveSizeDistributionImageButton.Enable(False);
        self.showSizeDistributionButton.Enable(False);
    def unlockTaskEntry(self):
        self.predictButton.Enable(True);
        self.loadButton.Enable(True);
        self.saveSingle.Enable(True);
        self.saveSizeDistributionDataButton.Enable(True);
        self.saveSizeDistributionImageButton.Enable(True);
        self.showSizeDistributionButton.Enable(True);
    
    def saveMono( self,
                 event ):
        nowFrame = self.framePicker.GetValue();
        if(nowFrame < 0 or nowFrame > self.processedFrameLen):
            return;
        self.lockTaskEntry();
        with wx.FileDialog(self, 
            message="保存文件", 
            defaultDir="",           # 默认路径（空为当前路径）
            defaultFile="tmp.csv",          # 默认文件名
            wildcard="csv文件 (*.csv)|*.csv",  # 文件类型筛选
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.unlockTaskEntry();
                return;  # 用户取消，直接返回

            saveDir = fileDialog.GetPath();
            saveDirPath = pa.Path(saveDir);
        try:
            saveDirPath.resolve();
            if(saveDirPath.suffix not in [".csv"]):
                saveDir += ".csv";
            if(not saveDirPath.parent.exists()):
                saveDirPath.parent.mkdir(parents=True,exist_ok=True);
                
            self.send(messageType.SaveMono,
                      {"picklePath":self.processedPath,
                       "targetFrame":nowFrame,
                       "saveDir":saveDir,
                       });
        except IOError as e:
            dlg = wx.MessageDialog(None, "Something goes wrong,\n detail:{:s}".format(e.__str__()), "Error", style=wx.OK | wx.ICON_ERROR);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            self.unlockTaskEntry();
        return;

    def gaugeRenew( self,
                   event ):
        event.Skip()
    
    def gaugeRenewUnpack(self,msg):
        self.gauge.SetValue(int((
            (msg.content["now"]/msg.content["total"])  / msg.content["totalStep"] 
            + (msg.content["step"] / msg.content["totalStep"] )
            )* 1000));
        self.gaugeText.SetLabel("Step:{}/{},Now:{}/{}".format(int(msg.content["step"]+1),int(msg.content["totalStep"]),int(msg.content["now"]),int(msg.content["total"])));
        self.m_collapsiblePane3.Layout();
    def loadPickleMenu(self, event):
        self.loadPickle(event);
    def gaugeSetRunning(self,msg):
        self.gauge.SetValue(100);
        self.gaugeText.SetLabel(msg.content["content"]);
        self.m_collapsiblePane3.Layout();
    def backendRecover(self):
        self.recverRenewTimer.Stop();
        self.FrontAlivePulser.Stop();
        dlg = wx.MessageDialog(None, "Sorry, the backend has been terminated or corrupted, would you like to: \n Yes: restart the backend \n No: terminate this app", "Error", style=wx.YES_NO | wx.ICON_ERROR);
        self.send(messageType.FrontBlocked,{});
        sendBack = dlg.ShowModal();
        self.send(messageType.FrontUnblocked,{});
        dlg.Destroy();
        self.unlockTaskEntry();
        if(sendBack == wx.ID_YES):
            self.launchBackend();
        elif(sendBack == wx.ID_NO):
            self.Close(True);
        self.recverRenewTimer.Start();
        self.FrontAlivePulser.Start();
        
    
    def loadPickle(self, event):
        self.lockTaskEntry();
        try:
            with wx.FileDialog(self, "打开", wildcard="pickle文件 (*.pkl)|*.pkl",
                   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as file_dialog:
                if (file_dialog.ShowModal() == wx.ID_OK):
                    selectedPath = file_dialog.GetPath();
                    tmp = pa.Path(selectedPath).resolve();
                    if(tmp.is_dir() or (not tmp.exists()) or tmp.suffix not in [".pkl"]):
                        dlg = wx.MessageDialog(None, "The file you are trying to load: \n{:s}\n is probably not the Origin Data created by this app".format(selectedPath), "File open error", style=wx.OK | wx.ICON_ERROR);
                        self.send(messageType.FrontBlocked,{});
                        dlg.ShowModal();
                        self.send(messageType.FrontUnblocked,{});
                        dlg.Destroy();
                        return;
                    self.send(messageType.LoadPickle,
                      {"picklePath":selectedPath});
                else:
                    self.unlockTaskEntry();
                    return;
        
        except Exception as e:
            dlg = wx.MessageDialog(None, "Something is wrong: \n{:s}".format(e.__str__()), "Load Failed", style=wx.OK | wx.ICON_WARNING);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            self.unlockTaskEntry();
            self.gaugeZero();
    def resizeImage(self):
        scrolledWindow = self.m_scrolledWindow2;
        if (not scrolledWindow):
            return;
        clientWidth = scrolledWindow.GetClientSize().width;
        virtualH = scrolledWindow.GetVirtualSize().height;
        clientH = scrolledWindow.GetClientSize().height;
        if (virtualH > clientH):
            scrollbarWidth = wx.SystemSettings.GetMetric(wx.SYS_VSCROLL_X);
            clientWidth -= scrollbarWidth;
        if (clientWidth <= 0):
            return;
        if (not hasattr(self, 'originalImage_SizeDistribution') or self.originalImage_SizeDistribution is None):
            self.sizeDistributionImage.SetSize((clientWidth, 0));
            self.sizeDistributionImage.SetMinSize(wx.Size(clientWidth, 0));
            self.sizeDistributionImage.SetMaxSize(wx.Size(clientWidth, 0));
            self.sizeDistributionImage.SetBitmap(wx.NullBitmap);
            return;
        origW = self.originalImage_SizeDistribution.GetWidth();
        origH = self.originalImage_SizeDistribution.GetHeight();
        if (origW == 0 or origH == 0):
            return;
        newWidth = clientWidth;
        newHeight = int(origH * (newWidth / origW));
        scaledImage = self.originalImage_SizeDistribution.Scale(newWidth, newHeight, wx.IMAGE_QUALITY_HIGH);
        scaledBitmap = wx.Bitmap(scaledImage);
        self.sizeDistributionImage.SetBitmap(scaledBitmap);
        self.sizeDistributionImage.SetSize((newWidth, newHeight));
        self.sizeDistributionImage.SetMinSize(wx.Size(newWidth, newHeight));
        self.sizeDistributionImage.SetMaxSize(wx.Size(newWidth, newHeight));
    def setImage_SizeDistribution(self,imagePath):
        self.originalImage_SizeDistribution = wx.Image(imagePath,wx.BITMAP_TYPE_ANY);
        self.resizeImage();
    def rightSize3Change(self,event):
        event.Skip();
        self.resizeImage()
    def recverRenew( self,
                     event ):        
        try:
            msg = self.recver.get(block=False);
            
            if(msg.type == messageType.BackendAlive):
                self.backendAlive = 3000;
            
            if((self.backendAlive <= 0 and self.recver.empty()) or (msg.type == messageType.BackendIsDead and self.alive == False)):
                self.backendRecover();
            
            if(msg.type == messageType.VideoPredictDone):
                self.unlockTaskEntry();
                try:
                    self.frameDependentStatics = pd.read_csv(msg.content["outputFrameDependentStatics"]);
                    self.mainStatics = pd.read_csv(msg.content["outputMainStatics"]);
                    self.processedPath = msg.content["processed"];
                    self.setFrameIndicator();
                    self.renewMainStatics();
                    self.renewProcessed();
                    dlg = wx.MessageDialog(None, "Track task succeed \n statics are placed here: \n{:s}\n\n{:s}".format(msg.content["outputFrameDependentStatics"],msg.content["outputMainStatics"]), "Task Done", style=wx.OK | wx.ICON_INFORMATION);
                    self.send(messageType.FrontBlocked,{});
                    dlg.ShowModal();
                    self.send(messageType.FrontUnblocked,{});
                    dlg.Destroy();
                    self.gaugeZero();
                except Exception as e:
                    self.frameDependentStatics = pd.DataFrame();
                    self.mainStatics = pd.DataFrame();
                    dlg = wx.MessageDialog(None, "Reading \n {:s} or \n {:s} failed.\n\nDetailed Message: {}".format(msg.content["outputFrameDependentStatics"],msg.content["outputMainStatics"],e.__str__()), "Reading Failed", style=wx.OK | wx.ICON_ERROR);
                    self.send(messageType.FrontBlocked,{});
                    dlg.ShowModal();
                    self.send(messageType.FrontUnblocked,{});
                    dlg.Destroy();
                    self.gaugeZero();
                
            if(msg.type == messageType.TaskFailed):
                self.unlockTaskEntry();
                dlg = wx.MessageDialog(None, "Task failed due to:\n\n{:s}".format(msg.content["reason"]), "Task failed", style=wx.OK | wx.ICON_ERROR);
                
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                
                dlg.Destroy();
                self.gaugeZero();
            if(msg.type == messageType.LoadPickleDone):
                self.unlockTaskEntry();
                self.gaugeZero();
                dlg = wx.MessageDialog(None, "Data imported successfully", "Task Done", style=wx.OK | wx.ICON_INFORMATION);
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
                
                try:
                    self.frameDependentStatics = pd.DataFrame(msg.content["frameDependentStatics"]);
                    self.mainStatics = pd.DataFrame(msg.content["mainStatics"],index=[0]);
                    self.processedPath = msg.content["processed"];
                    self.setFrameIndicator();
                    self.renewMainStatics();
                    self.renewProcessed();
                    
                except Exception as e:
                    self.frameDependentStatics = pd.DataFrame();
                    self.mainStatics = pd.DataFrame();
                    dlg = wx.MessageDialog(None, "Reading failed.\n\nDetailed Message: {}".format(e.__str__()), "Reading failed", style=wx.OK | wx.ICON_ERROR);
                    self.send(messageType.FrontBlocked,{});
                    dlg.ShowModal();
                    self.send(messageType.FrontUnblocked,{});
                    dlg.Destroy();
            if(msg.type == messageType.TaskWarning):
                dlg = wx.MessageDialog(None, "{}".format(msg.content["content"]), "Warning", style=wx.OK | wx.ICON_WARNING);
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
            if(msg.type == messageType.DrawPlotDone):
                self.unlockTaskEntry();
                self.setImage_SizeDistribution(msg.content["imagePath"]);
                self.sizeDistributionImage.SetScaleMode(wx.StaticBitmap.ScaleMode.Scale_AspectFit);
                self.refreshRightLayout();
                self.gaugeZero();
            if(msg.type == messageType.PicturePredictDone):
                self.unlockTaskEntry();
                dlg = wx.MessageDialog(None, "Data saved here: \n{}".format(msg.content["saveDir"]), "Data Exported", style=wx.OK | wx.ICON_INFORMATION);
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
                self.gaugeZero();
            if(msg.type == messageType.SavePlotDataDone):
                self.unlockTaskEntry();
                dlg = wx.MessageDialog(None, "Data saved here: \n{}".format(msg.content["csvPath"]), "Data Exported", style=wx.OK | wx.ICON_INFORMATION);
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
                self.gaugeZero();
            if(msg.type == messageType.SaveMonoDone):
                self.unlockTaskEntry();
                dlg = wx.MessageDialog(None, "Data saved here: \n{}".format(msg.content["csvPath"]), "Data Exported", style=wx.OK | wx.ICON_INFORMATION);
                self.send(messageType.FrontBlocked,{});
                dlg.ShowModal();
                self.send(messageType.FrontUnblocked,{});
                dlg.Destroy();
                self.gaugeZero();
            if(msg.type == messageType.GaugeSetRunning):
                self.gaugeSetRunning(msg);
            if(msg.type in [messageType.PicturePredictProgress, messageType.VideoPredictProgress]):
                self.gaugeRenewUnpack(msg);
                return;
            
        except(qu.Empty):
            self.backendAlive -= 20;
            if( self.backendAlive <= 0 ):
                self.backendRecover();
            return ;
        except (EOFError, BlockingIOError, OSError, BrokenPipeError):
            return ;
    
    def frameScaleVerifier(self):
        [FROM,END] = [self.fromFramePicker_SizeDistribution.GetValue(),self.toFramePicker_SizeDistribution.GetValue()];
        if(END>=self.processedFrameLen):
            END = max(0,self.processedFrameLen-1);
            self.toFramePicker_SizeDistribution.SetValue(END);
        if(FROM>END):
            self.fromFramePicker_SizeDistribution.SetValue(END);
            self.toFramePicker_SizeDistribution.SetValue(FROM);
            [FROM,END]=[END,FROM];
        if(END>=self.processedFrameLen):
            END = max(0,self.processedFrameLen-1);
            self.toFramePicker_SizeDistribution.SetValue(END);
        self.fromFrameNum_SizeDistribution.SetLabel("/{:d}".format(END));
        self.totalFrame_SizeDistribution.SetLabel("The image/csv will contain data from {:d} frame(s).".format(END-FROM+1));
        self.refreshRightLayout();
    def fromFrameSet_SizeDistribution(self, event):
        self.frameScaleVerifier();
    def toFrameSet_SizeDistribution(self, event):
        self.frameScaleVerifier();

        
    def sizeDistributionVerifier(self):
        fromFrame = self.fromFramePicker_SizeDistribution.GetValue();
        toFrame = self.toFramePicker_SizeDistribution.GetValue()+1;
        lasting = toFrame - fromFrame;
        if(fromFrame < 0 or toFrame<=0 or
           fromFrame >= toFrame or 
           toFrame > self.processedFrameLen or
           lasting<1):
            dlg = wx.MessageDialog(None, "Frame scale illegal\nYou are trying to investigate frames from {} to {} ( {} frames), which is illegal.\n There are only {} frames here. ".format(fromFrame,toFrame-1,lasting,self.processedFrameLen), "Scale illegal", style=wx.OK | wx.ICON_WARNING);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            return [-100,-100,-100];
        bins = self.sizeDistributionImageBinsPicker.GetValue();
        if(bins < 1):
            dlg = wx.MessageDialog(None, "Bins illegal\nYou are trying put statistics in {}, which is not positive.".format(bins),"Bins illegal", style=wx.OK | wx.ICON_WARNING);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            return [-100,-100,-100];
        return [fromFrame,lasting,int(bins)];
   
    def showSizeDistribution(self,event):
        fromFrame,lasting,bins = self.sizeDistributionVerifier();
        if(fromFrame < 0):
            return;
        self.send(messageType.DrawPlot,
                  {"perspect":gl.sizeDistributionImagePerspect(self.sizeDistributionImagePerspectPicker.GetSelection()),
                   "type":    gl.sizeDistributionImageType(self.sizeDistributionImageTypePicker.GetSelection()),
                   "picklePath":self.processedPath,
                   "targetFrameStart":fromFrame,
                   "lasting":lasting,
                   "saveDir":gl.defaultImagePath,
                   "bins":bins,
                   });
        self.lockTaskEntry();
        return;
        
        
    def saveSizeDistributionImage(self, event):
        fromFrame,lasting,bins = self.sizeDistributionVerifier();
        if(fromFrame < 0):
            return;
        self.lockTaskEntry();
        with wx.FileDialog(self, 
            message="保存文件", 
            defaultDir="",           # 默认路径（空为当前路径）
            defaultFile="tmp.png",          # 默认文件名
            wildcard="png文件 (*.png)|*.png|bmp文件 (*.bmp)|*.bmp|jpg文件 (*.jpg)|*.jpg|jpeg文件 (*.jpeg)|*.jpeg|gif文件 (*.gif)|*.gif",  # 文件类型筛选
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.unlockTaskEntry();
                return;  # 用户取消，直接返回

            saveDir = fileDialog.GetPath();
            saveDirPath = pa.Path(saveDir);
        try:
            saveDirPath.resolve();
            if(saveDirPath.suffix not in [".bmp",".jpg",".jpeg",".gif",".png"]):
                saveDir += ".png";
            if(not saveDirPath.parent.exists()):
                saveDirPath.parent.mkdir(parents=True,exist_ok=True);
                
            self.send(messageType.DrawPlot,
                      {"perspect":gl.sizeDistributionImagePerspect(self.sizeDistributionImagePerspectPicker.GetSelection()),
                       "type":    gl.sizeDistributionImageType(self.sizeDistributionImageTypePicker.GetSelection()),
                       "picklePath":self.processedPath,
                       "targetFrameStart":fromFrame,
                       "lasting":lasting,
                       "saveDir":saveDir,
                       "bins":bins,
                       });
        except IOError as e:
            dlg = wx.MessageDialog(None, "Something goes wrong,\n detail:{:s}".format(e.__str__()), "Error", style=wx.OK | wx.ICON_ERROR);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            self.unlockTaskEntry();
        return;
    
    def saveSizeDistributionData(self, event):
        fromFrame,lasting = self.sizeDistributionVerifier();
        if(fromFrame < 0):
            return;
        self.lockTaskEntry();
        with wx.FileDialog(self, 
            message="保存文件", 
            defaultDir="",           # 默认路径（空为当前路径）
            defaultFile="tmp.csv",          # 默认文件名
            wildcard="csv文件 (*.csv)|*.csv",  # 文件类型筛选
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        ) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                self.unlockTaskEntry();
                return  # 用户取消，直接返回

            saveDir = fileDialog.GetPath();
            saveDirPath = pa.Path(saveDir);
        try:
            saveDirPath.resolve();
            if(saveDirPath.suffix not in [".csv"]):
                saveDir += ".csv";
            if(not saveDirPath.parent.exists()):
                saveDirPath.parent.mkdir(parents=True,exist_ok=True); 
            self.send(messageType.SavePlotData,
                      {"perspect":gl.sizeDistributionImagePerspect(self.sizeDistributionImagePerspectPicker.GetSelection()),
                       "type":    gl.sizeDistributionImageType(self.sizeDistributionImageTypePicker.GetSelection()),
                       "picklePath":self.processedPath,
                       "targetFrameStart":fromFrame,
                       "lasting":lasting,
                       "saveDir":saveDir,
                       });
        except IOError as e:
            dlg = wx.MessageDialog(None, "Something goes wrong,\n detail:{:s}".format(e.__str__()), "Error", style=wx.OK | wx.ICON_ERROR);
            self.send(messageType.FrontBlocked,{});
            dlg.ShowModal();
            self.send(messageType.FrontUnblocked,{});
            dlg.Destroy();
            self.unlockTaskEntry();
        return;
    def FrontAlivePulse( self, event ):
        try:
            self.send(messageType.FrontAlive,{});
        except(EOFError, BlockingIOError, OSError, BrokenPipeError):
            self.backendRecover();
    def m_splitter1OnIdle( self,
                          event ):
        event.Skip()
        #self.m_splitter1.SetSashPosition( 200 )
        #self.m_splitter1.Unbind( wx.EVT_IDLE )

    def m_splitter2OnIdle( self,
                          event ):
        event.Skip()
        #self.m_splitter2.SetSashPosition( 0 )
        #self.m_splitter2.Unbind( wx.EVT_IDLE )
    
    def refreshLeftLayout(self):
        self.m_scrolledWindow1.Layout();
        self.m_scrolledWindow1.FitInside()
    def collapseChanged1( self, event ):
        self.refreshLeftLayout();

    def collapseChanged2( self, event ):
        self.refreshLeftLayout();

    def collapseChanged3( self, event ):
        self.refreshLeftLayout();

    def collapseChanged4( self, event ):
        self.refreshLeftLayout();
        
    def collapseChanged5( self, event ):
        self.refreshLeftLayout();
        
    def refreshRightLayout(self):
        self.m_scrolledWindow2.Layout();
        self.m_scrolledWindow2.FitInside()
    def collapseChangedR1(self, event):
        self.refreshRightLayout();
    def collapseChangedR2(self, event):
        self.refreshRightLayout();
    
    def collapseChangedR3( self, event ):
        self.refreshRightLayout();
    def collapseChangedR4( self, event ):
        self.refreshRightLayout();

        
    def saveVideoPickerClicked( self, event ):
        if(self.saveVideoPicker.GetValue()):  #现在它变成了True
            self.saveVideoWithLabelsPicker.Enabled = True;
            self.saveVideoWithConfidencePicker.Enabled = True;
        else:                                #现在它变成了False  
            self.saveVideoWithLabelsPicker.Enabled = False;
            self.saveVideoWithConfidencePicker.Enabled = False;
            self.saveVideoWithLabelsPicker.Value = False;
            self.saveVideoWithConfidencePicker.Value = False;
    def renewMainStatics(self):
        if(len(self.mainStatics.index)<1):
            return;
        text = "";
        
        for column in self.mainStatics.columns:
            text += "{:<38s}:{:.2f}\n".format(column,float(self.mainStatics[column][0]));
        self.mainStaticsPicker.SetValue(text);
    def renewProcessed(self):
        self.processedFrameLen = len(self.frameDependentStatics);
        self.toFrameNum_SizeDistribution.SetLabel("/{:d}".format(max(self.processedFrameLen-1,1)));
        self.toFramePicker_SizeDistribution.SetRange(0, max(1,self.processedFrameLen-1));
        self.fromFramePicker_SizeDistribution.SetRange(0, max(1,self.processedFrameLen-1));
        self.frameScaleVerifier();
        self.refreshRightLayout();
        return;
    def renewFrameDependentStatics(self,frame:int):
        if(len(self.frameDependentStatics.index)<=frame):
            return;
        else:
            columnToText ={
                "stayNum" : self.stayNum,
                "flowNum" : self.flowNum,
                "outNum"  : self.outNum,
                "backNum" : self.backNum,
                "stayArea" : self.stayArea,
                "flowArea" : self.flowArea,
                "outArea"  : self.outArea,
                "backArea" : self.backArea
                }
            
            for index in columnToText:
                indexToHint={"m":"Num","a":"Area"};
                    
                columnToText[index].SetLabel(
                    "{:<4s}:{: >9.0f} ({:>.0%})".format(
                        indexToHint[index[-1]],
                        self.frameDependentStatics[index][frame],
                        self.frameDependentStatics[index+"Ratio"][frame])
                    );
            
            columnToGauge={
                "stayNumRatio": [self.stayNumGauge],
                "stayAreaRatio":[self.stayAreaGauge],
                "flowNumRatio": [self.flowNumGauge],
                "flowAreaRatio":[self.flowAreaGauge],
                "outNumRatio": [self.outNumGauge],
                "outAreaRatio":[self.outAreaGauge],
                "backNumRatio": [self.backNumGauge],
                "backAreaRatio":[self.backAreaGauge],
                }
            for index in columnToGauge.keys():
                columnToGauge[index][0].SetRange(100);
                columnToGauge[index][0].SetValue(int(self.frameDependentStatics[index][frame] * 100));
            self.m_collapsiblePane6.Layout();
    def frameSilde( self, event ):
        nowValue = int(self.frameSlider.GetValue());
        self.renewFrameDependentStatics(nowValue);
        if(self.framePicker.GetMin()<=nowValue and nowValue<=self.framePicker.GetMax()):
            self.framePicker.SetValue(nowValue);
    def frameSet( self, event ):
        nowValue = int(self.framePicker.GetValue());
        self.renewFrameDependentStatics(nowValue);
        if(self.frameSlider.GetMin()<= nowValue and nowValue <=self.frameSlider.GetMax()):
            self.frameSlider.SetValue(nowValue);
    def setFrameIndicator(self):
        self.frameSlider.SetValue(0);
        self.renewFrameDependentStatics(0);
        self.frameSlider.SetRange(0,max(1,int(len(self.frameDependentStatics)-1)));
        self.framePicker.SetRange(0,max(1,int(len(self.frameDependentStatics)-1)));
        self.frameNum.SetLabel(str(len(self.frameDependentStatics)-1));
        frame = self.framePicker.GetValue();
        self.frameSlider.SetValue(int(frame));
        self.renewFrameDependentStatics(int(frame));
        
    def predictMenuClick( self, event ):
        self.predict(event);
        
    def stopMenuClick( self, event ):
        self.stopRunning(event);

    def helpMenuClick( self, event ):
        dlg = wx.MessageDialog(None, r"We are still making the users' guide.", "Help", style=wx.OK | wx.ICON_INFORMATION);
        self.send(messageType.FrontBlocked,{});
        dlg.ShowModal();
        self.send(messageType.FrontUnblocked,{});
        dlg.Destroy();

    def aboutMenuClick( self, event ):
        dlg = wx.MessageDialog(None, "BubbleDAS:\nBubble Dynamics Analysis Software\n作者 Author：方桢\n指导教师 Mentor：杨天让", "About", style=wx.OK | wx.ICON_INFORMATION);
        self.send(messageType.FrontBlocked,{});
        dlg.ShowModal();
        self.send(messageType.FrontUnblocked,{});
        dlg.Destroy();