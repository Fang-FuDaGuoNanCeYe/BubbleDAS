# -*- coding: utf-8 -*-
r"""
Created on Sun Mar 22 20:14:37 2026

@author: Tianrang Yang (github account: Tim16888)、Zhen Fang (github account: Fang-FuDaGuoNanCeYe)
"""

import Front as fr
import wx



if(__name__=="__main__"):
    #[q1,q2] = [mu.Queue(),mu.Queue()];
    app = wx.App(False)
    frame = fr.FrontMain(None);
    #backend = ba.backend(q1, q2);
    #backend.start();
    frame.Show();
    app.MainLoop();
    #backend.join();
    