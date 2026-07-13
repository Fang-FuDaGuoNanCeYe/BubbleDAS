# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 20:37:30 2026

@author: Tianrang Yang (github account: Tim16888)、Zhen Fang (github account: Fang-FuDaGuoNanCeYe)
"""
import enum;
class sizeDistributionImageType(enum.Enum):
    Stay=0;
    Flow=1;
    Out =2;
    Back=3;
    All =4;
    
class sizeDistributionImagePerspect(enum.Enum):
    Diamater=0;
    Area    =1;
    Width   =2;
    Height  =3;
    
appSignature = "BubbleDAS1_00_00";
noWarnSignature = [appSignature,"识别器20260419"] 
warnSignature = ["识别器20260418"]
defaultImagePath = r"tmp.png";