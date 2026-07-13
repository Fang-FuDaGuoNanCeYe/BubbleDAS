# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"BubbleDAS"), pos = wx.DefaultPosition, size = wx.Size( 646,452 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D|wx.SP_3DBORDER|wx.SP_LIVE_UPDATE )
        self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

        self.m_scrolledWindow1 = wx.ScrolledWindow( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        self.m_scrolledWindow1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_scrolledWindow1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )

        leftSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_collapsiblePane1 = wx.CollapsiblePane( self.m_scrolledWindow1, wx.ID_ANY, _(u"YOLO model"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane1.Collapse( False )

        self.m_collapsiblePane1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_collapsiblePane1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        self.m_collapsiblePane1.SetMinSize( wx.Size( 60,-1 ) )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        self.modelPicker = wx.FilePickerCtrl( self.m_collapsiblePane1.GetPane(), wx.ID_ANY, wx.EmptyString, _(u"Select a YOLO model"), _(u"*.*"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN )
        self.modelPicker.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        bSizer8.Add( self.modelPicker, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_collapsiblePane1.GetPane().SetSizer( bSizer8 )
        self.m_collapsiblePane1.GetPane().Layout()
        bSizer8.Fit( self.m_collapsiblePane1.GetPane() )
        leftSizer.Add( self.m_collapsiblePane1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_collapsiblePane2 = wx.CollapsiblePane( self.m_scrolledWindow1, wx.ID_ANY, _(u"Files to be predicted"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane2.Collapse( False )

        self.m_collapsiblePane2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_collapsiblePane2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
        self.m_collapsiblePane2.SetMinSize( wx.Size( 60,-1 ) )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.text2 = wx.StaticText( self.m_collapsiblePane2.GetPane(), wx.ID_ANY, _(u"Image/video File:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text2.Wrap( -1 )

        bSizer9.Add( self.text2, 0, wx.ALL, 5 )

        self.targetPicker = wx.FilePickerCtrl( self.m_collapsiblePane2.GetPane(), wx.ID_ANY, wx.EmptyString, _(u"Select a file"), _(u"*.png;*.jpeg;*.jpg;*mp4;*avi"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer9.Add( self.targetPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText34 = wx.StaticText( self.m_collapsiblePane2.GetPane(), wx.ID_ANY, _(u"Membrane zone:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText34.Wrap( -1 )

        bSizer9.Add( self.m_staticText34, 0, wx.ALL, 5 )

        self.membraneZonePicker = wx.FilePickerCtrl( self.m_collapsiblePane2.GetPane(), wx.ID_ANY, wx.EmptyString, _(u"Select a file"), _(u"*.json"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer9.Add( self.membraneZonePicker, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_collapsiblePane2.GetPane().SetSizer( bSizer9 )
        self.m_collapsiblePane2.GetPane().Layout()
        bSizer9.Fit( self.m_collapsiblePane2.GetPane() )
        leftSizer.Add( self.m_collapsiblePane2, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_collapsiblePane5 = wx.CollapsiblePane( self.m_scrolledWindow1, wx.ID_ANY, _(u"Arguments"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane5.Collapse( False )

        self.m_collapsiblePane5.SetMinSize( wx.Size( 60,-1 ) )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.SetFlexibleDirection( wx.HORIZONTAL )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText3 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Device"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )

        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.devicePicker = wx.TextCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"0"), wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
        self.devicePicker.SetHelpText( _(u"default: 0") )
        self.devicePicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.devicePicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText10 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Batch size"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )

        fgSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )

        self.batchSizePicker = wx.SpinCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 1048576, 16 )
        self.batchSizePicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.batchSizePicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText5 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Vid_stride"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )

        fgSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

        self.vidStridePicker = wx.SpinCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 1048576, 1 )
        self.vidStridePicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.vidStridePicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText4 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Valve"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        fgSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

        self.valvePicker = wx.SpinCtrlDouble( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 1, 0.900000, 1e-05 )
        self.valvePicker.SetDigits( 5 )
        self.valvePicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.valvePicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText6 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Max instances"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        fgSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.maxInstancesPicker = wx.SpinCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 10, 1048576, 9999 )
        self.maxInstancesPicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.maxInstancesPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText8 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Media width"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )

        fgSizer1.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.widthPicker = wx.SpinCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, -1, 1048576, -1 )
        self.widthPicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.widthPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Media height"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )

        fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.heightPicker = wx.SpinCtrl( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, -1, 1048576, -1 )
        self.heightPicker.SetMinSize( wx.Size( 20,-1 ) )

        fgSizer1.Add( self.heightPicker, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( fgSizer1, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.VERTICAL )

        self.saveVideoPicker = wx.CheckBox( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Save video with track boxes"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.saveVideoPicker.SetValue(True)
        bSizer15.Add( self.saveVideoPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.saveVideoWithLabelsPicker = wx.CheckBox( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Show labels in the saved video"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.saveVideoWithLabelsPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.saveVideoWithConfidencePicker = wx.CheckBox( self.m_collapsiblePane5.GetPane(), wx.ID_ANY, _(u"Show confidence in the saved video"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer15.Add( self.saveVideoWithConfidencePicker, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer13.Add( bSizer15, 0, wx.EXPAND, 5 )


        self.m_collapsiblePane5.GetPane().SetSizer( bSizer13 )
        self.m_collapsiblePane5.GetPane().Layout()
        bSizer13.Fit( self.m_collapsiblePane5.GetPane() )
        leftSizer.Add( self.m_collapsiblePane5, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_collapsiblePane4 = wx.CollapsiblePane( self.m_scrolledWindow1, wx.ID_ANY, _(u"Control"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane4.Collapse( False )

        self.m_collapsiblePane4.SetMinSize( wx.Size( 60,-1 ) )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )

        self.loadButton = wx.Button( self.m_collapsiblePane4.GetPane(), wx.ID_ANY, _(u"Load data from"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.loadButton, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText35 = wx.StaticText( self.m_collapsiblePane4.GetPane(), wx.ID_ANY, _(u"results will be placed here:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText35.Wrap( -1 )

        self.m_staticText35.SetHelpText( _(u"default: track_time") )

        bSizer10.Add( self.m_staticText35, 0, wx.ALL, 5 )

        self.SaveDirPicker = wx.DirPickerCtrl( self.m_collapsiblePane4.GetPane(), wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer10.Add( self.SaveDirPicker, 0, wx.ALL|wx.EXPAND, 5 )

        self.predictButton = wx.Button( self.m_collapsiblePane4.GetPane(), wx.ID_ANY, _(u"Predict and save results"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.predictButton, 0, wx.ALL|wx.EXPAND, 5 )

        self.stopButton = wx.Button( self.m_collapsiblePane4.GetPane(), wx.ID_ANY, _(u"Stop running (ESC)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stopButton.SetBackgroundColour( wx.Colour( 252, 203, 203 ) )

        bSizer10.Add( self.stopButton, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_collapsiblePane4.GetPane().SetSizer( bSizer10 )
        self.m_collapsiblePane4.GetPane().Layout()
        bSizer10.Fit( self.m_collapsiblePane4.GetPane() )
        leftSizer.Add( self.m_collapsiblePane4, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_collapsiblePane3 = wx.CollapsiblePane( self.m_scrolledWindow1, wx.ID_ANY, _(u"ProgressBar"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane3.Collapse( False )

        self.m_collapsiblePane3.SetMinSize( wx.Size( 60,-1 ) )

        bSizer16 = wx.BoxSizer( wx.HORIZONTAL )

        self.gauge = wx.Gauge( self.m_collapsiblePane3.GetPane(), wx.ID_ANY, 1000, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.gauge.SetValue( 0 )
        bSizer16.Add( self.gauge, 1, wx.ALL, 5 )

        self.gaugeText = wx.StaticText( self.m_collapsiblePane3.GetPane(), wx.ID_ANY, _(u"0/0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.gaugeText.Wrap( -1 )

        bSizer16.Add( self.gaugeText, 0, wx.ALL, 5 )


        self.m_collapsiblePane3.GetPane().SetSizer( bSizer16 )
        self.m_collapsiblePane3.GetPane().Layout()
        bSizer16.Fit( self.m_collapsiblePane3.GetPane() )
        leftSizer.Add( self.m_collapsiblePane3, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_scrolledWindow1.SetSizer( leftSizer )
        self.m_scrolledWindow1.Layout()
        leftSizer.Fit( self.m_scrolledWindow1 )
        self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow2.SetScrollRate( 5, 5 )
        self.m_scrolledWindow2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        rightSizer = wx.BoxSizer( wx.VERTICAL )

        self.m_collapsiblePane7 = wx.CollapsiblePane( self.m_scrolledWindow2, wx.ID_ANY, _(u"Main data"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane7.Collapse( False )

        self.m_collapsiblePane7.SetMinSize( wx.Size( 60,-1 ) )

        bSizer19 = wx.BoxSizer( wx.VERTICAL )

        self.mainStaticsPicker = wx.TextCtrl( self.m_collapsiblePane7.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        self.mainStaticsPicker.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.mainStaticsPicker.SetMinSize( wx.Size( -1,80 ) )

        bSizer19.Add( self.mainStaticsPicker, 1, wx.ALL|wx.EXPAND, 5 )


        self.m_collapsiblePane7.GetPane().SetSizer( bSizer19 )
        self.m_collapsiblePane7.GetPane().Layout()
        bSizer19.Fit( self.m_collapsiblePane7.GetPane() )
        rightSizer.Add( self.m_collapsiblePane7, 0, wx.EXPAND |wx.ALL, 5 )

        self.m_collapsiblePane6 = wx.CollapsiblePane( self.m_scrolledWindow2, wx.ID_ANY, _(u"Frame-dependent data"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane6.Collapse( False )

        self.m_collapsiblePane6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
        self.m_collapsiblePane6.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        self.m_collapsiblePane6.SetMinSize( wx.Size( 60,-1 ) )

        bSizer27 = wx.BoxSizer( wx.VERTICAL )

        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.HORIZONTAL )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_ALL )

        self.m_staticText91 = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Stay"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText91.Wrap( -1 )

        gbSizer1.Add( self.m_staticText91, wx.GBPosition( 0, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.stayNum = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Num: 0 (0%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stayNum.Wrap( -1 )

        gbSizer1.Add( self.stayNum, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.stayNumGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.stayNumGauge.SetValue( 0 )
        gbSizer1.Add( self.stayNumGauge, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.stayArea = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Area: 0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stayArea.Wrap( -1 )

        gbSizer1.Add( self.stayArea, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.stayAreaGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.stayAreaGauge.SetValue( 0 )
        gbSizer1.Add( self.stayAreaGauge, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.m_staticText911 = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Flow"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText911.Wrap( -1 )

        gbSizer1.Add( self.m_staticText911, wx.GBPosition( 2, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.flowNum = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Num: 0 (0%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.flowNum.Wrap( -1 )

        gbSizer1.Add( self.flowNum, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.flowNumGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.flowNumGauge.SetValue( 0 )
        gbSizer1.Add( self.flowNumGauge, wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.flowArea = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Area: 0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.flowArea.Wrap( -1 )

        gbSizer1.Add( self.flowArea, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.flowAreaGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.flowAreaGauge.SetValue( 0 )
        gbSizer1.Add( self.flowAreaGauge, wx.GBPosition( 3, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.m_staticText912 = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Detach\n(Out)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText912.Wrap( -1 )

        gbSizer1.Add( self.m_staticText912, wx.GBPosition( 4, 0 ), wx.GBSpan( 2, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.outNum = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Num: 0 (0%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.outNum.Wrap( -1 )

        gbSizer1.Add( self.outNum, wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.outNumGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.outNumGauge.SetValue( 0 )
        gbSizer1.Add( self.outNumGauge, wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.outArea = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Area: 0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.outArea.Wrap( -1 )

        gbSizer1.Add( self.outArea, wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.outAreaGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.outAreaGauge.SetValue( 0 )
        gbSizer1.Add( self.outAreaGauge, wx.GBPosition( 5, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.m_staticText26 = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Attach\n(Back)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText26.Wrap( -1 )

        gbSizer1.Add( self.m_staticText26, wx.GBPosition( 6, 0 ), wx.GBSpan( 2, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.backNum = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Num: 0 (0%)"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.backNum.Wrap( -1 )

        gbSizer1.Add( self.backNum, wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.backNumGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.backNumGauge.SetValue( 0 )
        gbSizer1.Add( self.backNumGauge, wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )

        self.backArea = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Area: 0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.backArea.Wrap( -1 )

        gbSizer1.Add( self.backArea, wx.GBPosition( 7, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        self.backAreaGauge = wx.Gauge( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.backAreaGauge.SetValue( 0 )
        gbSizer1.Add( self.backAreaGauge, wx.GBPosition( 7, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 5 )


        gbSizer1.AddGrowableCol( 2 )
        gbSizer1.AddGrowableRow( 0 )

        bSizer27.Add( gbSizer1, 0, wx.EXPAND, 5 )

        bSizer25 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer25.SetMinSize( wx.Size( -1,20 ) )
        self.m_staticText32 = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Frame:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText32.Wrap( -1 )

        bSizer25.Add( self.m_staticText32, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.frameSlider = wx.Slider( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, 0, 0, 1, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL|wx.SL_TOP )
        bSizer25.Add( self.frameSlider, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.framePicker = wx.SpinCtrl( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 1, 0 )
        bSizer25.Add( self.framePicker, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.frameNum = wx.StaticText( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"/0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.frameNum.Wrap( -1 )

        bSizer25.Add( self.frameNum, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer27.Add( bSizer25, 0, wx.EXPAND, 5 )

        self.saveSingle = wx.Button( self.m_collapsiblePane6.GetPane(), wx.ID_ANY, _(u"Save the statics of this frame as ..."), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer27.Add( self.saveSingle, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_collapsiblePane6.GetPane().SetSizer( bSizer27 )
        self.m_collapsiblePane6.GetPane().Layout()
        bSizer27.Fit( self.m_collapsiblePane6.GetPane() )
        rightSizer.Add( self.m_collapsiblePane6, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_collapsiblePane8 = wx.CollapsiblePane( self.m_scrolledWindow2, wx.ID_ANY, _(u"Size Distribution"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane8.Collapse( False )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        self.text_hint1 = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"Making Bubble Size Distribution Data"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_hint1.Wrap( -1 )

        bSizer18.Add( self.text_hint1, 0, wx.ALL, 5 )

        bSizer251 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer251.SetMinSize( wx.Size( -1,20 ) )
        self.m_staticText43 = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"From frame"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText43.Wrap( -1 )

        bSizer251.Add( self.m_staticText43, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.fromFramePicker_SizeDistribution = wx.SpinCtrl( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 1, 0 )
        bSizer251.Add( self.fromFramePicker_SizeDistribution, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.fromFrameNum_SizeDistribution = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"/0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.fromFrameNum_SizeDistribution.Wrap( -1 )

        bSizer251.Add( self.fromFrameNum_SizeDistribution, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.m_staticText44 = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"To Frame"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText44.Wrap( -1 )

        bSizer251.Add( self.m_staticText44, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.toFramePicker_SizeDistribution = wx.SpinCtrl( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 0, 1, 0 )
        bSizer251.Add( self.toFramePicker_SizeDistribution, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.toFrameNum_SizeDistribution = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"/0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.toFrameNum_SizeDistribution.Wrap( -1 )

        bSizer251.Add( self.toFrameNum_SizeDistribution, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


        bSizer18.Add( bSizer251, 0, wx.EXPAND, 5 )

        self.totalFrame_SizeDistribution = wx.StaticText( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"The image/csv will contain data from 1 frame(s)."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.totalFrame_SizeDistribution.Wrap( -1 )

        bSizer18.Add( self.totalFrame_SizeDistribution, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        bSizer21 = wx.BoxSizer( wx.VERTICAL )

        self.sizeDistributionImage = wx.StaticBitmap( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.sizeDistributionImage, 1, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5 )

        self.showSizeDistributionButton = wx.Button( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"Show size distribution"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.showSizeDistributionButton, 0, wx.ALL|wx.EXPAND, 5 )

        self.saveSizeDistributionImageButton = wx.Button( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"Save size distribution chart"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.saveSizeDistributionImageButton, 0, wx.ALL|wx.EXPAND, 5 )

        self.saveSizeDistributionDataButton = wx.Button( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"Save size distribution data"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer21.Add( self.saveSizeDistributionDataButton, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer18.Add( bSizer21, 0, wx.EXPAND, 5 )

        self.m_collapsiblePane9 = wx.CollapsiblePane( self.m_collapsiblePane8.GetPane(), wx.ID_ANY, _(u"Size Distribution Image Settings"), wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
        self.m_collapsiblePane9.Collapse( False )

        bSizer22 = wx.BoxSizer( wx.VERTICAL )

        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText41 = wx.StaticText( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, _(u"Bins of histrogram"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )

        gbSizer2.Add( self.m_staticText41, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.sizeDistributionImageBinsPicker = wx.SpinCtrlDouble( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT|wx.SP_ARROW_KEYS, 1, 100, 1.000000, 1 )
        self.sizeDistributionImageBinsPicker.SetDigits( 0 )
        gbSizer2.Add( self.sizeDistributionImageBinsPicker, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

        self.m_staticText42 = wx.StaticText( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, _(u"Image content"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText42.Wrap( -1 )

        gbSizer2.Add( self.m_staticText42, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        sizeDistributionImageTypePickerChoices = [ _(u"Stay Only"), _(u"Flow Only"), _(u"Detach/Out Only"), _(u"Re-attach/Back Only"), _(u"All") ]
        self.sizeDistributionImageTypePicker = wx.Choice( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, sizeDistributionImageTypePickerChoices, 0 )
        self.sizeDistributionImageTypePicker.SetSelection( 4 )
        gbSizer2.Add( self.sizeDistributionImageTypePicker, wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )

        self.staticBy = wx.StaticText( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, _(u"Statistic include"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.staticBy.Wrap( -1 )

        gbSizer2.Add( self.staticBy, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        sizeDistributionImagePerspectPickerChoices = [ _(u"Diamater"), _(u"Area"), _(u"Width"), _(u"Height") ]
        self.sizeDistributionImagePerspectPicker = wx.Choice( self.m_collapsiblePane9.GetPane(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, sizeDistributionImagePerspectPickerChoices, 0 )
        self.sizeDistributionImagePerspectPicker.SetSelection( 0 )
        gbSizer2.Add( self.sizeDistributionImagePerspectPicker, wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 5 )


        gbSizer2.AddGrowableCol( 1 )
        gbSizer2.AddGrowableCol( 2 )

        bSizer22.Add( gbSizer2, 0, wx.EXPAND, 5 )


        self.m_collapsiblePane9.GetPane().SetSizer( bSizer22 )
        self.m_collapsiblePane9.GetPane().Layout()
        bSizer22.Fit( self.m_collapsiblePane9.GetPane() )
        bSizer18.Add( self.m_collapsiblePane9, 0, wx.EXPAND |wx.ALL, 5 )


        self.m_collapsiblePane8.GetPane().SetSizer( bSizer18 )
        self.m_collapsiblePane8.GetPane().Layout()
        bSizer18.Fit( self.m_collapsiblePane8.GetPane() )
        rightSizer.Add( self.m_collapsiblePane8, 0, wx.EXPAND |wx.ALL, 5 )


        self.m_scrolledWindow2.SetSizer( rightSizer )
        self.m_scrolledWindow2.Layout()
        rightSizer.Fit( self.m_scrolledWindow2 )
        self.m_splitter1.SplitVertically( self.m_scrolledWindow1, self.m_scrolledWindow2, 250 )
        bSizer4.Add( self.m_splitter1, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer4 )
        self.Layout()
        self.gaugeRenewTimer = wx.Timer()
        self.gaugeRenewTimer.SetOwner( self, self.gaugeRenewTimer.GetId() )
        self.m_menubar2 = wx.MenuBar( 0 )
        self.m_menu5 = wx.Menu()
        self.m_menuItem10 = wx.MenuItem( self.m_menu5, wx.ID_ANY, _(u"Load data from ...")+ u"\t" + u"CTRL+O", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu5.Append( self.m_menuItem10 )

        self.m_menubar2.Append( self.m_menu5, _(u"File") )

        self.m_menu2 = wx.Menu()
        self.predictMenu = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"Predict and save results"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.predictMenu )

        self.stopMenu = wx.MenuItem( self.m_menu2, wx.ID_ANY, _(u"Stop running")+ u"\t" + u"ESC", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu2.Append( self.stopMenu )

        self.m_menubar2.Append( self.m_menu2, _(u"Control") )

        self.m_menu4 = wx.Menu()
        self.helpMenu = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"Help"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu4.Append( self.helpMenu )

        self.aboutProjectMenu = wx.MenuItem( self.m_menu4, wx.ID_ANY, _(u"This project"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu4.Append( self.aboutProjectMenu )

        self.m_menubar2.Append( self.m_menu4, _(u"About") )

        self.SetMenuBar( self.m_menubar2 )

        self.recverRenewTimer = wx.Timer()
        self.recverRenewTimer.SetOwner( self, self.recverRenewTimer.GetId() )
        self.recverRenewTimer.Start( 20 )

        self.FrontAlivePulser = wx.Timer()
        self.FrontAlivePulser.SetOwner( self, self.FrontAlivePulser.GetId() )
        self.FrontAlivePulser.Start( 1000 )


        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.OnClose )
        self.m_collapsiblePane1.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged1 )
        self.m_collapsiblePane2.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged2 )
        self.m_collapsiblePane5.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged3 )
        self.saveVideoPicker.Bind( wx.EVT_CHECKBOX, self.saveVideoPickerClicked )
        self.saveVideoWithLabelsPicker.Bind( wx.EVT_CHECKBOX, self.saveVideoWithLabelsPickerClicked )
        self.saveVideoWithConfidencePicker.Bind( wx.EVT_CHECKBOX, self.saveVideoWithConfidencePickerClicked )
        self.m_collapsiblePane4.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged4 )
        self.loadButton.Bind( wx.EVT_BUTTON, self.loadPickle )
        self.predictButton.Bind( wx.EVT_BUTTON, self.predict )
        self.stopButton.Bind( wx.EVT_BUTTON, self.stopRunning )
        self.m_collapsiblePane3.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChanged5 )
        self.m_collapsiblePane7.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChangedR1 )
        self.m_collapsiblePane6.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChangedR2 )
        self.frameSlider.Bind( wx.EVT_SCROLL, self.frameSilde )
        self.framePicker.Bind( wx.EVT_SPINCTRL, self.frameSet )
        self.saveSingle.Bind( wx.EVT_BUTTON, self.saveMono )
        self.m_collapsiblePane8.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChangedR3 )
        self.m_collapsiblePane8.Bind( wx.EVT_SIZE, self.rightSize3Change )
        self.fromFramePicker_SizeDistribution.Bind( wx.EVT_SPINCTRL, self.fromFrameSet_SizeDistribution )
        self.toFramePicker_SizeDistribution.Bind( wx.EVT_SPINCTRL, self.toFrameSet_SizeDistribution )
        self.showSizeDistributionButton.Bind( wx.EVT_BUTTON, self.showSizeDistribution )
        self.saveSizeDistributionImageButton.Bind( wx.EVT_BUTTON, self.saveSizeDistributionImage )
        self.saveSizeDistributionDataButton.Bind( wx.EVT_BUTTON, self.saveSizeDistributionData )
        self.m_collapsiblePane9.Bind( wx.EVT_COLLAPSIBLEPANE_CHANGED, self.collapseChangedR4 )
        self.Bind( wx.EVT_TIMER, self.gaugeRenew, id=self.gaugeRenewTimer.GetId() )
        self.Bind( wx.EVT_MENU, self.loadPickleMenu, id = self.m_menuItem10.GetId() )
        self.Bind( wx.EVT_MENU, self.predictMenuClick, id = self.predictMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.stopMenuClick, id = self.stopMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.helpMenuClick, id = self.helpMenu.GetId() )
        self.Bind( wx.EVT_MENU, self.aboutMenuClick, id = self.aboutProjectMenu.GetId() )
        self.Bind( wx.EVT_TIMER, self.recverRenew, id=self.recverRenewTimer.GetId() )
        self.Bind( wx.EVT_TIMER, self.FrontAlivePulse, id=self.FrontAlivePulser.GetId() )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def OnClose( self, event ):
        event.Skip()

    def collapseChanged1( self, event ):
        event.Skip()

    def collapseChanged2( self, event ):
        event.Skip()

    def collapseChanged3( self, event ):
        event.Skip()

    def saveVideoPickerClicked( self, event ):
        event.Skip()

    def saveVideoWithLabelsPickerClicked( self, event ):
        event.Skip()

    def saveVideoWithConfidencePickerClicked( self, event ):
        event.Skip()

    def collapseChanged4( self, event ):
        event.Skip()

    def loadPickle( self, event ):
        event.Skip()

    def predict( self, event ):
        event.Skip()

    def stopRunning( self, event ):
        event.Skip()

    def collapseChanged5( self, event ):
        event.Skip()

    def collapseChangedR1( self, event ):
        event.Skip()

    def collapseChangedR2( self, event ):
        event.Skip()

    def frameSilde( self, event ):
        event.Skip()

    def frameSet( self, event ):
        event.Skip()

    def saveMono( self, event ):
        event.Skip()

    def collapseChangedR3( self, event ):
        event.Skip()

    def rightSize3Change( self, event ):
        event.Skip()

    def fromFrameSet_SizeDistribution( self, event ):
        event.Skip()

    def toFrameSet_SizeDistribution( self, event ):
        event.Skip()

    def showSizeDistribution( self, event ):
        event.Skip()

    def saveSizeDistributionImage( self, event ):
        event.Skip()

    def saveSizeDistributionData( self, event ):
        event.Skip()

    def collapseChangedR4( self, event ):
        event.Skip()

    def gaugeRenew( self, event ):
        event.Skip()

    def loadPickleMenu( self, event ):
        event.Skip()

    def predictMenuClick( self, event ):
        event.Skip()

    def stopMenuClick( self, event ):
        event.Skip()

    def helpMenuClick( self, event ):
        event.Skip()

    def aboutMenuClick( self, event ):
        event.Skip()

    def recverRenew( self, event ):
        event.Skip()

    def FrontAlivePulse( self, event ):
        event.Skip()

    def m_splitter1OnIdle( self, event ):
        self.m_splitter1.SetSashPosition( 250 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )


