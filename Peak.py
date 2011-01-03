#Boa:Frame:peakTimeStdDevFrame

import wx
from wx.html import HtmlEasyPrinting
from wx.lib import plot
from PeakTimeStdDevPlot import PlotControl
from math import pow, sqrt, exp
from sys import argv, exit
from os import path, remove
from copy import copy
from numpy.fft import fft
from numpy import array

def create(parent):
    return peakTimeStdDevFrame(parent)

[wxID_PEAKTIMESTDDEVFRAME, wxID_PEAKTIMESTDDEVFRAMEBOX_CROSSCORR, 
 wxID_PEAKTIMESTDDEVFRAMEBOX_CURVEINCLUSE, 
 wxID_PEAKTIMESTDDEVFRAMEBOX_MEDIADEV, wxID_PEAKTIMESTDDEVFRAMEBOX_PLOT, 
 wxID_PEAKTIMESTDDEVFRAMEBOX_RUMORE, wxID_PEAKTIMESTDDEVFRAMEBOX_TUS, 
 wxID_PEAKTIMESTDDEVFRAMEBOX_VALUES, 
 wxID_PEAKTIMESTDDEVFRAMEBUTTON_CROSSDETAIL, 
 wxID_PEAKTIMESTDDEVFRAMEBUTTON_OPEN, wxID_PEAKTIMESTDDEVFRAMEBUTTON_PRINT, 
 wxID_PEAKTIMESTDDEVFRAMEBUTTON_RICALCOLA, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_COLORGREEN, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_COLORMAGENTA, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_COLORRED, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEBLUE, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_CURVECYAN, 
 wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEYELLOW, 
 wxID_PEAKTIMESTDDEVFRAMEEDIT_CROSSCORR, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_ASTERISCO, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_AVTIME, wxID_PEAKTIMESTDDEVFRAMELABEL_ENDLINE, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_FILENAME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_MAXTIME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME2, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME4, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME6, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NUMLINES, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_SEARCHING, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_STDDEVTIME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_STRAIN, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME2, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME4, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME6, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL2, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL4, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL6, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_FINALTIME, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_STARTTIME, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_VALUETYPE, 
 wxID_PEAKTIMESTDDEVFRAMEPANEL_STRAIN, wxID_PEAKTIMESTDDEVFRAMESTATICBITMAP1, 
 wxID_PEAKTIMESTDDEVFRAMESTATICLINE1, wxID_PEAKTIMESTDDEVFRAMESTATICTEXT1, 
 wxID_PEAKTIMESTDDEVFRAMESTATICTEXT2, wxID_PEAKTIMESTDDEVFRAMESTATICTEXT3, 
 wxID_PEAKTIMESTDDEVFRAMESTATUSBAR, wxID_PEAKTIMESTDDEVFRAMETEXT_AVTIME, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL1, wxID_PEAKTIMESTDDEVFRAMETEXT_COL2, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL3, wxID_PEAKTIMESTDDEVFRAMETEXT_COL4, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL5, wxID_PEAKTIMESTDDEVFRAMETEXT_COL6, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_CROSSCORR, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_FILENAME, wxID_PEAKTIMESTDDEVFRAMETEXT_MAXMIN, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_MAXTIME, wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME2, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME4, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME6, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NUMLINES, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_STDDEVTIME, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME2, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME4, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME6, wxID_PEAKTIMESTDDEVFRAMETEXT_TUS, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_UNIFORMITY, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL2, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL4, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL6, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSBEGIN, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSEND, wxID_PEAKTIMESTDDEVFRAMEPANEL_PLOT
] = [wx.NewId() for _init_ctrls in range(92)]

class peakTimeStdDevFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_PEAKTIMESTDDEVFRAME,
              name='peakTimeStdDevFrame', parent=prnt, pos=wx.Point(-4, 146),
              size=wx.Size(1036, 572),
              style=wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION|wx.SYSTEM_MENU|wx.CLIP_CHILDREN,
              title='Calcolo Deviazione Standard Tempi di picco di STRAIN')
        self.SetIcon(wx.Icon(u'img/heart.ico',wx.BITMAP_TYPE_ICO))
        self.SetClientSize(wx.Size(1028, 545))
        self.SetForegroundColour(wx.Colour(0, 230, 0))

        self.statusBar = wx.StatusBar(id=wxID_PEAKTIMESTDDEVFRAMESTATUSBAR,
              name='statusBar', parent=self, style=0)
        self.SetStatusBar(self.statusBar)

        self.panel_strain = wx.Panel(id=wxID_PEAKTIMESTDDEVFRAMEPANEL_STRAIN,
              name='panel_strain', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1028, 525), style=wx.TAB_TRAVERSAL)

        self.button_open = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_OPEN,
              label='Apri file', name='button_open', parent=self.panel_strain,
              pos=wx.Point(504, 10), size=wx.Size(91, 23), style=0)
        self.button_open.Bind(wx.EVT_BUTTON, self.OnButton_openButton,
              id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_OPEN)

        self.label_FileName = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_FILENAME,
              label='Nome file:', name='label_FileName',
              parent=self.panel_strain, pos=wx.Point(8, 16), size=wx.Size(49,
              13), style=0)

        self.text_FileName = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_FILENAME,
              name='text_FileName', parent=self.panel_strain, pos=wx.Point(64,
              12), size=wx.Size(432, 21), style=0, value='')
        self.text_FileName.SetEditable(False)

        self.label_searching = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_SEARCHING,
              label='Si cercano i valori', name='label_searching',
              parent=self.panel_strain, pos=wx.Point(8, 48), size=wx.Size(84,
              13), style=0)

        self.label_numLines = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NUMLINES,
              label='Righe nel file:', name='label_numLines',
              parent=self.panel_strain, pos=wx.Point(216, 48), size=wx.Size(66,
              13), style=0)

        self.text_maxTime = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_MAXTIME,
              name='text_maxTime', parent=self.panel_strain, pos=wx.Point(536,
              44), size=wx.Size(64, 21), style=0, value='')
        self.text_maxTime.SetEditable(False)

        self.box_values = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_VALUES,
              label='Valori', name='box_values', parent=self.panel_strain,
              pos=wx.Point(8, 72), size=wx.Size(592, 256), style=0)

        self.box_mediadev = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_MEDIADEV,
              label='Media e deviazione', name='box_mediadev',
              parent=self.panel_strain, pos=wx.Point(8, 328), size=wx.Size(592,
              54), style=0)

        self.text_col4 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL4,
              name='text_col4', parent=self.panel_strain, pos=wx.Point(24, 192),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col4.SetEditable(False)

        self.text_col1 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL1,
              name='text_col1', parent=self.panel_strain, pos=wx.Point(24, 96),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col1.SetEditable(False)

        self.text_col2 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL2,
              name='text_col2', parent=self.panel_strain, pos=wx.Point(24, 128),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col2.SetEditable(False)

        self.text_col5 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL5,
              name='text_col5', parent=self.panel_strain, pos=wx.Point(24, 224),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col5.SetEditable(False)

        self.text_col6 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL6,
              name='text_col6', parent=self.panel_strain, pos=wx.Point(24, 256),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col6.SetEditable(False)

        self.text_col3 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_COL3,
              name='text_col3', parent=self.panel_strain, pos=wx.Point(24, 160),
              size=wx.Size(100, 21), style=0, value='')
        self.text_col3.SetEditable(False)

        self.label_val2 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL2,
              label='Valore', name='label_val2', parent=self.panel_strain,
              pos=wx.Point(152, 130), size=wx.Size(31, 13), style=0)

        self.label_val3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL3,
              label='Valore', name='label_val3', parent=self.panel_strain,
              pos=wx.Point(152, 160), size=wx.Size(31, 16), style=0)

        self.label_val4 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL4,
              label='Valore', name='label_val4', parent=self.panel_strain,
              pos=wx.Point(152, 194), size=wx.Size(31, 13), style=0)

        self.label_val5 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL5,
              label='Valore', name='label_val5', parent=self.panel_strain,
              pos=wx.Point(152, 226), size=wx.Size(31, 13), style=0)

        self.label_val6 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL6,
              label='Valore', name='label_val6', parent=self.panel_strain,
              pos=wx.Point(152, 258), size=wx.Size(31, 13), style=0)

        self.label_time2 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME2,
              label='Tempo', name='label_time2', parent=self.panel_strain,
              pos=wx.Point(320, 130), size=wx.Size(33, 13), style=0)

        self.text_val2 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL2,
              name='text_val2', parent=self.panel_strain, pos=wx.Point(192,
              128), size=wx.Size(96, 21), style=0, value='')
        self.text_val2.SetEditable(False)

        self.text_val3 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL3,
              name='text_val3', parent=self.panel_strain, pos=wx.Point(192,
              160), size=wx.Size(96, 21), style=0, value='')
        self.text_val3.SetEditable(False)

        self.text_val4 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL4,
              name='text_val4', parent=self.panel_strain, pos=wx.Point(192,
              192), size=wx.Size(96, 21), style=0, value='')
        self.text_val4.SetEditable(False)

        self.text_val5 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL5,
              name='text_val5', parent=self.panel_strain, pos=wx.Point(192,
              224), size=wx.Size(96, 21), style=0, value='')
        self.text_val5.SetEditable(False)

        self.text_val6 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL6,
              name='text_val6', parent=self.panel_strain, pos=wx.Point(192,
              256), size=wx.Size(96, 21), style=0, value='')
        self.text_val6.SetEditable(False)

        self.text_time2 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME2,
              name='text_time2', parent=self.panel_strain, pos=wx.Point(360,
              128), size=wx.Size(72, 21), style=0, value='')
        self.text_time2.SetEditable(False)

        self.label_val1 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL1,
              label='Valore', name='label_val1', parent=self.panel_strain,
              pos=wx.Point(152, 98), size=wx.Size(31, 13), style=0)

        self.label_time3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME3,
              label='Tempo', name='label_time3', parent=self.panel_strain,
              pos=wx.Point(320, 162), size=wx.Size(33, 13), style=0)

        self.label_time4 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME4,
              label='Tempo', name='label_time4', parent=self.panel_strain,
              pos=wx.Point(320, 194), size=wx.Size(33, 13), style=0)

        self.label_time5 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME5,
              label='Tempo', name='label_time5', parent=self.panel_strain,
              pos=wx.Point(320, 226), size=wx.Size(33, 13), style=0)

        self.label_time6 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME6,
              label='Tempo', name='label_time6', parent=self.panel_strain,
              pos=wx.Point(320, 258), size=wx.Size(33, 13), style=0)

        self.label_normTime2 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME2,
              label='(Normalizzato)', name='label_normTime2',
              parent=self.panel_strain, pos=wx.Point(448, 130), size=wx.Size(69,
              13), style=0)

        self.text_val1 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VAL1,
              name='text_val1', parent=self.panel_strain, pos=wx.Point(192, 96),
              size=wx.Size(96, 21), style=0, value='')
        self.text_val1.SetEditable(False)

        self.text_time3 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME3,
              name='text_time3', parent=self.panel_strain, pos=wx.Point(360,
              160), size=wx.Size(72, 21), style=0, value='')
        self.text_time3.SetEditable(False)

        self.text_time4 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME4,
              name='text_time4', parent=self.panel_strain, pos=wx.Point(360,
              192), size=wx.Size(72, 21), style=0, value='')
        self.text_time4.SetEditable(False)

        self.text_time5 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME5,
              name='text_time5', parent=self.panel_strain, pos=wx.Point(360,
              224), size=wx.Size(72, 21), style=0, value='')
        self.text_time5.SetEditable(False)

        self.text_time6 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME6,
              name='text_time6', parent=self.panel_strain, pos=wx.Point(360,
              256), size=wx.Size(72, 21), style=0, value='')
        self.text_time6.SetEditable(False)

        self.text_normTime2 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME2,
              name='text_normTime2', parent=self.panel_strain, pos=wx.Point(528,
              128), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime2.SetEditable(False)

        self.label_time1 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIME1,
              label='Tempo', name='label_time1', parent=self.panel_strain,
              pos=wx.Point(320, 98), size=wx.Size(33, 13), style=0)

        self.label_normTime3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME3,
              label='(Normalizzato)', name='label_normTime3',
              parent=self.panel_strain, pos=wx.Point(448, 162), size=wx.Size(69,
              13), style=0)

        self.label_normTime4 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME4,
              label='(Normalizzato)', name='label_normTime4',
              parent=self.panel_strain, pos=wx.Point(448, 194), size=wx.Size(69,
              13), style=0)

        self.label_normTime5 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME5,
              label='(Normalizzato)', name='label_normTime5',
              parent=self.panel_strain, pos=wx.Point(448, 226), size=wx.Size(69,
              13), style=0)

        self.label_normTime6 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME6,
              label='(Normalizzato)', name='label_normTime6',
              parent=self.panel_strain, pos=wx.Point(448, 258), size=wx.Size(69,
              13), style=0)

        self.label_normTime1 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME1,
              label='(Normalizzato)', name='label_normTime1',
              parent=self.panel_strain, pos=wx.Point(448, 98), size=wx.Size(69,
              13), style=0)

        self.text_time1 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIME1,
              name='text_time1', parent=self.panel_strain, pos=wx.Point(360,
              96), size=wx.Size(72, 21), style=0, value='')
        self.text_time1.SetEditable(False)

        self.text_normTime3 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME3,
              name='text_normTime3', parent=self.panel_strain, pos=wx.Point(528,
              160), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime3.SetEditable(False)

        self.text_normTime4 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME4,
              name='text_normTime4', parent=self.panel_strain, pos=wx.Point(528,
              192), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime4.SetEditable(False)

        self.text_normTime5 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME5,
              name='text_normTime5', parent=self.panel_strain, pos=wx.Point(528,
              224), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime5.SetEditable(False)

        self.text_normTime6 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME6,
              name='text_normTime6', parent=self.panel_strain, pos=wx.Point(528,
              256), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime6.SetEditable(False)

        self.text_normTime1 = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME1,
              name='text_normTime1', parent=self.panel_strain, pos=wx.Point(528,
              96), size=wx.Size(48, 21), style=0, value='')
        self.text_normTime1.SetEditable(False)

        self.label_stdDevTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_STDDEVTIME,
              label='Deviazione standard tempi normalizzati:',
              name='label_stdDevTime', parent=self.panel_strain,
              pos=wx.Point(269, 352), size=wx.Size(194, 13), style=0)

        self.text_stdDevTime = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_STDDEVTIME,
              name='text_stdDevTime', parent=self.panel_strain,
              pos=wx.Point(475, 348), size=wx.Size(113, 21), style=0, value='')
        self.text_stdDevTime.SetEditable(False)

        self.label_avTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_AVTIME,
              label='Media tempi normalizzati:', name='label_avTime',
              parent=self.panel_strain, pos=wx.Point(23, 352), size=wx.Size(124,
              13), style=0)

        self.text_avTime = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_AVTIME,
              name='text_avTime', parent=self.panel_strain, pos=wx.Point(155,
              348), size=wx.Size(97, 21), style=0, value='')
        self.text_avTime.SetEditable(False)

        self.text_numLines = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NUMLINES,
              name='text_numLines', parent=self.panel_strain, pos=wx.Point(296,
              44), size=wx.Size(64, 21), style=0, value='')
        self.text_numLines.SetEditable(False)

        self.label_maxtime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_MAXTIME,
              label='Intervallo temporale di norm.:', name='label_maxtime',
              parent=self.panel_strain, pos=wx.Point(376, 48), size=wx.Size(144,
              13), style=0)

        self.box_rumore = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_RUMORE,
              label='Tempi di cut-off (filtraggio picchi di rumore)',
              name='box_rumore', parent=self.panel_strain, pos=wx.Point(8, 474),
              size=wx.Size(512, 52), style=0)

        self.label_endLine = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_ENDLINE,
              label='Tempo finale valutazione:', name='label_endLine',
              parent=self.panel_strain, pos=wx.Point(279, 496),
              size=wx.Size(124, 13), style=0)

        self.text_zeroPassEnd = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSEND,
              name='text_zeroPassEnd', parent=self.panel_strain,
              pos=wx.Point(415, 493), size=wx.Size(72, 21), style=0, value='')
        self.text_zeroPassEnd.Bind(wx.EVT_CHAR, self.OnText_zeroPassEndChar)

        self.button_print = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_PRINT,
              label='Stampa', name='button_print', parent=self.panel_strain,
              pos=wx.Point(528, 500), size=wx.Size(75, 24), style=0)
        self.button_print.Bind(wx.EVT_BUTTON, self.OnButton_printButton,
              id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_PRINT)

        self.staticText1 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT1,
              label='Tempo iniziale di valutazione:', name='staticText1',
              parent=self.panel_strain, pos=wx.Point(22, 496), size=wx.Size(144,
              13), style=0)

        self.text_zeroPassBegin = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSBEGIN,
              name='text_zeroPassBegin', parent=self.panel_strain,
              pos=wx.Point(184, 493), size=wx.Size(64, 21), style=0, value='')
        self.text_zeroPassBegin.Bind(wx.EVT_CHAR, self.OnText_zeroPassBeginChar)

        self.staticLine1 = wx.StaticLine(id=wxID_PEAKTIMESTDDEVFRAMESTATICLINE1,
              name='staticLine1', parent=self.panel_strain, pos=wx.Point(608,
              16), size=wx.Size(1, 504), style=0)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'img/heart_geometric.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_PEAKTIMESTDDEVFRAMESTATICBITMAP1,
              name='staticBitmap1', parent=self.panel_strain, pos=wx.Point(851,
              362), size=wx.Size(174, 159), style=0)

        self.label_strain = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_STRAIN,
              label='Analysis', name='label_strain', parent=self.panel_strain,
              pos=wx.Point(688, 464), size=wx.Size(175, 58), style=0)
        self.label_strain.SetFont(wx.Font(36, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))
        self.label_strain.SetExtraStyle(0)

        self.staticText2 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT2,
              label='Strain', name='staticText2', parent=self.panel_strain,
              pos=wx.Point(616, 401), size=wx.Size(127, 58), style=0)
        self.staticText2.SetFont(wx.Font(36, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))
        self.staticText2.SetExtraStyle(0)
        self.staticText2.SetLayoutDirection(1)
        self.staticText2.SetHelpText('')

        self.label_asterisco = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_ASTERISCO,
              label="* Se il tempo di picco appare all'inizio dell'intervallo si assume",
              name='label_asterisco', parent=self.panel_strain, pos=wx.Point(32,
              288), size=wx.Size(560, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT3,
              label='un valore di 100 normalizzato per massimizzare la dispersione.',
              name='staticText3', parent=self.panel_strain, pos=wx.Point(40,
              304), size=wx.Size(297, 13), style=0)

        self.box_plot = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_PLOT,
              label='Data plot', name='box_plot', parent=self.panel_strain,
              pos=wx.Point(616, 51), size=wx.Size(424, 304), style=0)

        self.button_ricalcola = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_RICALCOLA,
              label='Ricalcola', name='button_ricalcola',
              parent=self.panel_strain, pos=wx.Point(528, 474), size=wx.Size(75,
              23), style=0)
        self.button_ricalcola.Bind(wx.EVT_BUTTON, self.OnButton_ricalcolaButton,
              id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_RICALCOLA)

        self.text_MaxMin = wx.Choice(choices=['MINIMI', 'MASSIMI'],
              id=wxID_PEAKTIMESTDDEVFRAMETEXT_MAXMIN, name='text_MaxMin',
              parent=self.panel_strain, pos=wx.Point(104, 44), size=wx.Size(80,
              21), style=0)
        self.text_MaxMin.Bind(wx.EVT_CHOICE, self.OnText_MaxMinChoice,
              id=wxID_PEAKTIMESTDDEVFRAMETEXT_MAXMIN)

        self.text_uniformity = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMETEXT_UNIFORMITY,
              label='Indice di Uniformit\xe0 Temporale di Strain (TUS):',
              name='text_uniformity', parent=self.panel_strain, pos=wx.Point(22,
              400), size=wx.Size(222, 13), style=0)

        self.text_TUS = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TUS,
              name='text_TUS', parent=self.panel_strain, pos=wx.Point(257, 398),
              size=wx.Size(330, 21), style=0, value='')
        self.text_TUS.SetEditable(False)

        self.modlabel_finalTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_FINALTIME,
              label='', name='modlabel_finalTime', parent=self.panel_strain,
              pos=wx.Point(495, 497), size=wx.Size(16, 13), style=0)

        self.modlabel_valueType = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_VALUETYPE,
              label='', name='modlabel_valueType', parent=self.panel_strain,
              pos=wx.Point(188, 47), size=wx.Size(16, 13), style=0)

        self.text_crosscorr = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMETEXT_CROSSCORR,
              label='Media normalizzata di cross-correlazione:',
              name='text_crosscorr', parent=self.panel_strain, pos=wx.Point(23,
              447), size=wx.Size(196, 13), style=0)

        self.box_tus = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_TUS,
              label='TUS', name='box_tus', parent=self.panel_strain,
              pos=wx.Point(8, 381), size=wx.Size(592, 45), style=0)

        self.box_crosscorr = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_CROSSCORR,
              label='Cross-Correlazione', name='box_crosscorr',
              parent=self.panel_strain, pos=wx.Point(8, 426), size=wx.Size(592,
              47), style=0)

        self.edit_crosscorr = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMEEDIT_CROSSCORR,
              name='edit_crosscorr', parent=self.panel_strain, pos=wx.Point(257,
              443), size=wx.Size(261, 21), style=0, value='')
        self.edit_crosscorr.SetEditable(False)

        self.button_crossdetail = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_CROSSDETAIL,
              label='Dettagli', name='button_crossdetail',
              parent=self.panel_strain, pos=wx.Point(528, 442), size=wx.Size(63,
              23), style=0)
        self.button_crossdetail.Bind(wx.EVT_BUTTON,
              self.OnButton_ricalcolaButton,
              id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_CROSSDETAIL)

        self.box_curveIncluse = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_CURVEINCLUSE,
              label='Curve incluse', name='box_curveIncluse',
              parent=self.panel_strain, pos=wx.Point(616, 5), size=wx.Size(411,
              46), style=0)

        self.check_curveBlue = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEBLUE,
              label='Blue', name='check_curveBlue', parent=self.panel_strain,
              pos=wx.Point(628, 26), size=wx.Size(46, 13), style=0)
        self.check_curveBlue.SetForegroundColour(wx.Colour(0, 0, 255))
        self.check_curveBlue.SetValue(False)

        self.check_curveCyan = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVECYAN,
              label='Cyan', name='check_curveCyan', parent=self.panel_strain,
              pos=wx.Point(689, 27), size=wx.Size(46, 13), style=0)
        self.check_curveCyan.SetForegroundColour(wx.Colour(0, 223, 223))
        self.check_curveCyan.SetValue(False)

        self.check_curveYellow = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEYELLOW,
              label='Yellow', name='check_curveYellow',
              parent=self.panel_strain, pos=wx.Point(750, 27), size=wx.Size(49,
              13), style=0)
        self.check_curveYellow.SetForegroundColour(wx.Colour(255, 255, 0))
        self.check_curveYellow.SetValue(False)
        self.check_curveYellow.Bind(wx.EVT_CHECKBOX,
              self.OnCheck_curveYellowCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEYELLOW)

        self.check_colorRed = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORRED,
              label='Red', name='check_colorRed', parent=self.panel_strain,
              pos=wx.Point(821, 27), size=wx.Size(46, 13), style=0)
        self.check_colorRed.SetForegroundColour(wx.Colour(255, 0, 0))
        self.check_colorRed.SetValue(False)

        self.check_colorGreen = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORGREEN,
              label='Green', name='check_colorGreen', parent=self.panel_strain,
              pos=wx.Point(884, 27), size=wx.Size(46, 13), style=0)
        self.check_colorGreen.SetForegroundColour(wx.Colour(0, 159, 0))
        self.check_colorGreen.SetValue(False)

        self.check_colorMagenta = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORMAGENTA,
              label='Magenta', name='check_colorMagenta',
              parent=self.panel_strain, pos=wx.Point(950, 27), size=wx.Size(65,
              13), style=0)
        self.check_colorMagenta.SetForegroundColour(wx.Colour(255, 0, 255))
        self.check_colorMagenta.SetValue(False)

        self.modlabel_startTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_STARTTIME,
              label='', name='modlabel_startTime', parent=self.panel_strain,
              pos=wx.Point(252, 497), size=wx.Size(16, 13), style=0)

        self.panel_plot = PlotControl(id=wxID_PEAKTIMESTDDEVFRAMEPANEL_PLOT,
              name='panel_plot', parent=self.panel_strain,
              pos=wx.Point(626, 69), size=wx.Size(404, 276), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)

        self.visualCols = []
        self.visualCols.append(self.text_col1)
        self.visualCols.append(self.text_col2)
        self.visualCols.append(self.text_col3)
        self.visualCols.append(self.text_col4)
        self.visualCols.append(self.text_col5)
        self.visualCols.append(self.text_col6)

        self.visualValues = []
        self.visualValues.append(self.text_val1)
        self.visualValues.append(self.text_val2)
        self.visualValues.append(self.text_val3)
        self.visualValues.append(self.text_val4)
        self.visualValues.append(self.text_val5)
        self.visualValues.append(self.text_val6)

        self.visualTimes = []
        self.visualTimes.append(self.text_time1)
        self.visualTimes.append(self.text_time2)
        self.visualTimes.append(self.text_time3)
        self.visualTimes.append(self.text_time4)
        self.visualTimes.append(self.text_time5)
        self.visualTimes.append(self.text_time6)

        self.visualNormTimes = []
        self.visualNormTimes.append(self.text_normTime1)
        self.visualNormTimes.append(self.text_normTime2)
        self.visualNormTimes.append(self.text_normTime3)
        self.visualNormTimes.append(self.text_normTime4)
        self.visualNormTimes.append(self.text_normTime5)
        self.visualNormTimes.append(self.text_normTime6)

        self.statusBar.SetStatusText("Strain evaluation utility v0.3, coded by Andrea Chiarini")
        self.button_print.Enable(False)

        self.fileName = ''

    def OnButton_openButton(self, event):
        dlg = wx.FileDialog(self, "Scegli un file di acquisizione", path.dirname(self.fileName), "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.fileName = dlg.GetPath()
                self.text_FileName.SetValue(path.basename(self.fileName))
                self.analyseFile(self.fileName)
                self.statusBar.SetStatusText("Evaluation verified correctly!")
                self.button_print.Enable(True)
        finally:
            dlg.Destroy()

    def analyseFile(self, fileName):
        # Apertura del file
        try:
            inputFile = open(fileName)
        except IOError:
            self.statusBar.SetStatusText("Errore durante la lettura del file")
            dlg = wx.MessageDialog(self, "Errore durante la lettura del file.","Attenzione!",wx.OK | wx.ICON_HAND)
            dlg.ShowModal()                
            return
        
        # Variabile booleana
        # Inizialmente supponiamo di stare cercando il minimo
        self.searchingMin = True
        self.matrixEnd = 2

        # Se c'e' RAD nel nome del file, allora cerchiamo il massimo
        if "rad" in fileName.lower():
            self.searchingMin = False
            # Per file Radial, la matrice finisce dopo
            self.matrixEnd = 1

        # Variabile line, ci verranno salvate le righe del file
        # man mano che vengono lette
        line = ""

        # Cerco la riga con i titoli delle colonne
        # Leggo una riga alla volta fin quando non
        # trovo la riga contenente "Time (s)"
        while "Time (s)" not in line:
            line = inputFile.readline()
            if line == '':
                #raise WrongFormatException
                self.statusBar.SetStatusText("Formato non corretto!")
                dlg = wx.MessageDialog(self, "Formato del file non corretto.","Verificare formato file",wx.OK | wx.ICON_HAND)
                dlg.ShowModal()                
                return
        
        # Una volta trovata, salvo in una lista tutti
        # i campi separati da tablature (\t), e li
        # salvo in un array, che conterra' quindi
        # tutti i nomi delle colonne
        self.columns = line.split('\t')
        for i in range(1, len(self.columns) - self.matrixEnd ):
            self.columns[i] = self.columns[i].strip(' ')

        # Preparo una matrice vuota
        self.valueMatrix = []

        # Leggo all'infinito una riga dal file
        while 1:
            valueMatrixLine = []

            line = inputFile.readline()

            # Se trovo una riga vuota, mi fermo ed esco dal ciclo
            if line == "": break
            # Per ogni valore separato da tablatura,
            # lo trasformo in numero in virgola mobile
            # e me lo salvo
            for value in line.split('\t'):
                valueMatrixLine.append(float(value))

            # Salvo nella matrice la fila di numeri appena letta
            self.valueMatrix.append( valueMatrixLine )




        # Primo passaggio, ricerca passaggi comuni per lo zero
        zeroLinePassMatrix = []

        # Searching columns between the second (the first columns are
        # evaluation times) and the matrixEnd (first or second to last, depending
        # on file type)
        for col in range( 1, len(self.valueMatrix[0]) - self.matrixEnd ):
            zeroLinePasses = []
            for line in range( 0, len(self.valueMatrix) - 1):
                # Cerco passaggi dallo zero
                if  ( self.valueMatrix[line][col] == 0):
                    # If exact zero pass, appending only line number
                    zeroLinePasses.append( (line, line) )
                else:
                    if (( (self.valueMatrix[line][col] < 0) and (self.valueMatrix[line + 1][col] > 0) ) or
                       ( (self.valueMatrix[line][col] > 0) and (self.valueMatrix[line + 1][col] < 0) )):
                        # If inexact zero pass (line before below 0 and
                        # line after above or the other way around,
                        # marking both lines
                        zeroLinePasses.append( ( line, line + 1 ) )

            # Aggiungo alla matrice tutti i passaggi dallo zero rilevati per la singola colonna
            zeroLinePassMatrix.append(zeroLinePasses)

        # Matrix holding all possible tuples for each possible permutation on the zeroLinePassMatrix
        tupleMatrix = [ ]

        # Analyzing all tuples
        for line in zeroLinePassMatrix[0]:
            tupleMatrix.append( [ line ] )

        for col in range(1, len(zeroLinePassMatrix) ):
            l = len(tupleMatrix)

            for h in range(0, len(zeroLinePassMatrix[col]) - 1 ):
                for i in range(0, l):
                    tupleMatrix.append( copy(tupleMatrix[i]) )

            for h in range(0, len(zeroLinePassMatrix[col]) ):
                for i in range(0,l):
                    tupleMatrix[i + (l*h)].append( zeroLinePassMatrix[col][h] )

        commonZeroPasses = []
        for line in tupleMatrix:
            tempLeft = []
            tempRight = []
            for el in line:
                tempLeft.append(el[0])
                tempRight.append(el[1])

            foundMin = min(tempLeft)
            foundMax = max(tempRight)

            if (foundMin >= foundMax - 2) and (foundMin <= foundMax):
                commonZeroPasses.append( (foundMin,foundMax) )

        zeroLines = []
        # Choosing startLine and endLine from zero pass matrix
        for tuple in commonZeroPasses:
            if tuple[0] == tuple[1]:
                zeroLines.append(tuple[0])

            else:
                if tuple[0] == tuple[1] - 1:
                    zeroLines.append(tuple[0])
                else:
                    if tuple[0] == tuple[1] - 2:
                        zeroLines.append(tuple[0] + 1)

        # Considerero' solo le righe posteriori al primo passaggio dallo zero di tutte
        # le curve e antecedenti all'ultimo.
        self.startLine = 0
        self.endLine = len(self.valueMatrix) - 1
        if len(zeroLines) > 0:
            # Checking first zero pass line occurs in first half of valueMatrix
            if zeroLines[0] < len(self.valueMatrix) / 2:
                self.startLine = zeroLines[0]
                
            if len(zeroLines) > 1:
                # Checking last zero pass line occurs in second half of valueMatrix
                if zeroLines[-1] > len(self.valueMatrix) / 2:
                    self.endLine = zeroLines[-1]


        # Stampo informazioni generali sul file
        self.text_numLines.SetValue( str( len(self.valueMatrix) ) )
        
        self.modlabel_valueType.SetLabel('')
        self.modlabel_finalTime.SetLabel('')
        self.modlabel_startTime.SetLabel('')
        
        self.findPeaks()

    def findPeaks(self):
        if self.startLine == 0:
            self.text_zeroPassBegin.SetValue(str(self.valueMatrix[self.startLine][0])  + ' (inizio)')
        else:
            self.text_zeroPassBegin.SetValue(str(self.valueMatrix[self.startLine][0]))
            
        if self.endLine == len(self.valueMatrix) - 1:
            self.text_zeroPassEnd.SetValue(str(self.valueMatrix[self.endLine][0]) + ' (fine)')
        else:
            self.text_zeroPassEnd.SetValue(str(self.valueMatrix[self.endLine][0]))

        if self.searchingMin:
            self.text_MaxMin.SetSelection(0)
        else:
            self.text_MaxMin.SetSelection(1)

        # Array destinato a contenere i tempi corrispondenti
        # ai valori massimi e minimi trovati per poi calcolarci
        # la deviazione standard.
        foundTimes = []
        
        # Trovo il tempo totale per la normalizzazione (differenza tempi riga di partenza e finale, prima colonna della matrice)
        startTime =  self.valueMatrix[self.startLine][0]
        endTime = self.valueMatrix[self.endLine][0]
        totalTime = endTime - startTime

        # Stampo informazioni generali sul file
        self.text_maxTime.SetValue( str( totalTime ) )

        peaks = []
            
        # Per ogni colonna della matrice (a parte la prima, dei tempi, e le ultime due)
        for col in range( 1, len(self.valueMatrix[0]) - self.matrixEnd ):
            temp = []
            foundValue = 0

            # Per ogni riga (di quelle da considerare) della matrice,
            # salvo il valore in quella colonna in una lista a parte
            for line in range( self.startLine, self.endLine + 1):
                temp.append(self.valueMatrix[line][col])

            # Mi segno il tempo (prima colonna) delle righe
            # che risultano le minime (o le massime) per una
            # data colonna.
            if self.searchingMin:
                foundValue = min(temp)
            else:
                foundValue = max(temp)
            # Mi segno il tempo corrispondente al valore trovato
            time = self.valueMatrix[ self.startLine + temp.index(foundValue) ][0]
            
            # Storing peaks for graphic plot
            peaks.append((time, foundValue))

            # Metto via il tempo normalizzato
            # Se picco sullo startTime (all'inizio), prendo 100
            if (time == startTime):
                foundTimes.append(100)
            else:
                foundTimes.append( ((time - startTime) *100) / totalTime)

            self.visualCols[col - 1].SetValue(str( self.columns[col] ))

            # Stampo il valore minimo (o massimo)
            if self.searchingMin:
                self.visualValues[col - 1].SetValue( str( foundValue ) )
            else:
                self.visualValues[col - 1].SetValue( str( foundValue ) )

            # Stampo il tempo normalizzato (e assoluto)
            self.visualTimes[col - 1].SetValue(str(time))
            if (time == startTime):
                self.visualNormTimes[col - 1].SetValue(str(100) + '*')
            else:
                self.visualNormTimes[col - 1].SetValue(str(round(((time - startTime)*100)/ totalTime , 2)) )

        # Calcolo media
        average = 0
        for val in foundTimes:
            average += val
        average = average / len(foundTimes)
        self.text_avTime.SetValue( str(round(average, 2) ) )

        # Adesso calcolo la deviazione standard
        devSquare = 0
        for val in foundTimes:
            devSquare += pow(val - average, 2)

        stdDev = sqrt( devSquare / ( len(foundTimes) - 1 ) )
        self.text_stdDevTime.SetValue( str( round(stdDev,5) ) )
        
        # TUS
        self.text_TUS.SetValue(str(self.calculateTUS()))
        
        # Cross Correlation
        self.edit_crosscorr.SetValue(str(self.findCrossCorrelationAverage()))
        
        self.plotMatrix(startTime, endTime, peaks)
    
    def calculateTUS(self):
        f = open('TUS_Debug.log', 'w')
        continuous_component = 0
        first_harmonic = 0

        temp = []

        for line in range( self.startLine, self.endLine + 1):        
            temp = []
            for col in range( 1, len(self.valueMatrix[0]) - self.matrixEnd ):        
                temp.append(self.valueMatrix[line][col])
            
            f.write('Line ' + str(line) + ':\n')
            f.write(str(temp) + '\n')
            
            cont = abs(fft(temp,2).real[0])
            fh = abs(fft(temp,2).real[1])
            
            f.write('FFT Continuous component: ' + str(cont) + '\n')
            f.write('FFT first harmonic: ' + str(fh) + '\n\n')
            
            continuous_component += cont
            first_harmonic += fh
        
        f.close()
        return round( (sqrt(float(continuous_component) / float(continuous_component + first_harmonic)))**3, 6)
    
    def findCrossCorrelationAverage(self):
        crossCorrValue = 0
        crossCorrCounter = 0
        
        for colStart in range (1, 7):
            
            for colEnd in range (colStart + 1, 7):
                
                crossCorrValue += self.findCrossCorrelationPeak(colStart, colEnd)
                crossCorrCounter += 1
        
        return crossCorrValue / crossCorrCounter
    
    def findCrossCorrelationPeak(self, curveIndex1, curveIndex2):
        averageCurve1 = 0
        averageCurve2 = 0
        sampleCount = 0
        
        for line in range( self.startLine, self.endLine + 1):        
            averageCurve1 += self.valueMatrix[line][curveIndex1]
            averageCurve2 += self.valueMatrix[line][curveIndex2]
            sampleCount += 1
        
        averageCurve1 = averageCurve1 / sampleCount
        averageCurve2 = averageCurve2 / sampleCount

        den1 = 0
        den2 = 0
        
        for line in range( self.startLine, self.endLine + 1):        
            den1 += pow(self.valueMatrix[line][curveIndex1] - averageCurve1, 2)
            den2 += pow(self.valueMatrix[line][curveIndex2] - averageCurve2, 2)
        
        den = sqrt(den1*den2)
        
        crossCorrSeries = []    

        for phase in range(0, self.endLine - self.startLine):
            
            num = 0

            for line in range( self.startLine, self.endLine + 1):
                factor1 = self.valueMatrix[line][curveIndex1] - averageCurve1
                factor2 = self.valueMatrix[line - phase][curveIndex2] - averageCurve2

                num += factor1 * factor2 
                
            crossCorrSeries.append( num / den )
    
        print 'Curve ' + str(curveIndex1) + ' to curve ' + str(curveIndex2) + ' = ' + str(max(crossCorrSeries))
        return max(crossCorrSeries)
    
    def plotMatrix(self, startTime, endTime, peaks):
        colorArray = copy(self.columns)
        
        curves = []
        foundMin = 0
        foundMax = 0
        
        for col in range( 1, len(self.valueMatrix[0]) - self.matrixEnd ):
            data = []
            for line in range(0, len(self.valueMatrix)):
                data.append( (self.valueMatrix[line][0], self.valueMatrix[line][col] ) )
                if self.valueMatrix[line][col] < foundMin:
                    foundMin = self.valueMatrix[line][col]
                if self.valueMatrix[line][col] > foundMax:
                    foundMax = self.valueMatrix[line][col]
            
            curves.append(data)
        linesToPlot = []
        
        del colorArray[0]
        
        for i in range(0, len(curves)):
            linesToPlot.append( plot.PolyLine(curves[i], legend='', colour=colorArray[i], width=2) )
            # Line indicating peak
            linesToPlot.append( plot.PolyLine([(peaks[i][0],0), peaks[i]], legend='', colour=colorArray[i], width=2, style=wx.DOT) )
        
        # X-Axis
        linesToPlot.append( plot.PolyLine([(0, 0), (self.valueMatrix[len(self.valueMatrix) - 1][0], 0)], legend='', colour='black', width=2, style=wx.SOLID) )
        
        # Interval initial cut-off curve
        linesToPlot.append( plot.PolyLine([(startTime, foundMin - 1), (startTime, foundMax + 1)], legend='', colour='black', width=2, style=wx.DOT_DASH) )
        # Interval final cut-off curve        
        linesToPlot.append( plot.PolyLine([(endTime, foundMin - 1), (endTime, foundMax + 1)], legend='', colour='black', width=2, style=wx.DOT_DASH) )

        self.panel_plot._setSize()
        gc = plot.PlotGraphics(linesToPlot, 'Grafico curve di strain', 'Tempi di acquisizione', 'Valori Strain')
        self.panel_plot.Draw(gc, xAxis= (0,self.valueMatrix[len(self.valueMatrix) - 1][0] ), yAxis= (foundMin - 1,foundMax + 1))

    def OnButton_printButton(self, event):
        # Costruzione Testo da stampare
        (fp, fn) = path.split(self.fileName)
        report = "<br><div align=\"right\"><i><font size=\"1\">Analisi di Strain eseguita da PeakTimeStdDev, coded by Andrea Chiarini</font></i></div><br><br>"
        report += "<b>File di input:</b> " + fn + "\n\n"

        report += "<b>Valori cercati:</b> " + self.text_MaxMin.GetStringSelection()
        if 'M' in self.modlabel_valueType.GetLabel(): report += ' (*)'
        
        report += "\n<b>Righe nel file:</b> " + self.text_numLines.GetValue() + "\n"
        report += "<b>Tempo massimo:</b> " + self.text_maxTime.GetValue() + "\n"

        report += "<b>Rapporto analisi:</b>\n\n"

        reportLine = ''

        report += '<table border="1" width="100%">'
        report += '<tr><td><b>Colonna</b></td><td><b>Valore</b></td><td><b>Tempo Ass.</b></td><td><b>Tempo Norm.</b></td></tr>'

        for col in range(0, len(self.visualCols)):
            report += '<tr>'
            report += '<td>' + self.visualCols[col].GetValue() + '</td>'
            # Stampo il valore minimo (o massimo)
            report += '<td>' + self.visualValues[col].GetValue() + '</td>'
            # Stampo il tempo normalizzato (e assoluto)
            report += '<td>' + self.visualTimes[col].GetValue() + '</td>'
            report += '<td>' + self.visualNormTimes[col].GetValue() + '</td>'
            report += '</tr>'
        report += '</table>\n\n'

        report += "<b>Tempo iniziale valutazione:</b> " + self.text_zeroPassBegin.GetValue()
        if 'M' in self.modlabel_startTime.GetLabel(): report += ' (*)'
        report += "\n<b>Tempo finale valutazione:</b> " + self.text_zeroPassEnd.GetValue()
        if 'M' in self.modlabel_finalTime.GetLabel(): report += ' (*)'
        
        report += "\n\n<b>Media tempi normalizzati:</b> " + self.text_avTime.GetValue() + "\n"
        report += "<b>Deviazione standard tempi normalizzati:</b> " + self.text_stdDevTime.GetValue() + "\n"
        report += "<b>Indice di uniformit&agrave temporale di strain:</b> " + self.text_TUS.GetValue() + "\n"
        report += "<br><div align=\"right\"><i><font size=\"1\">(*) Nota: I valori marcati con asterischi sono stati modificati dall'operatore.</font></i></div><br>"
        report += "<br><br><br><br>"
        report += "<div align=\"center\"><img src=\"plot.png\" width=\"550\" height=\"300\"></div>"


        self.printer = Printer()
        self.panel_plot.PrintSize()
        self.panel_plot._PrintBuffer.SaveFile('plot.png', wx.BITMAP_TYPE_PNG)
        self.printer.Print(report,"Analisi di Strain")
        self.statusBar.SetStatusText("Report inviato alla stampante")
        remove('plot.png')

    def OnButton_ricalcolaButton(self, event):
        # Establishing startLine based on time
        newStartTime = 0
        newEndTime = 0
        try:
            newStartTime = float(self.text_zeroPassBegin.GetValue().strip(' (inizio)'))
            newEndTime = float(self.text_zeroPassEnd.GetValue().strip(' (fine)'))
        except ValueError:
            self.statusBar.SetStatusText("Valore inserito non valido!")
            dlg = wx.MessageDialog(self, "Errore durante l'operazione di ricalcolo. Verificare i dati immessi dall'utente","Attenzione!",wx.OK | wx.ICON_HAND)
            dlg.ShowModal()
            return
            
        # Boundary check on inserted values
        realStart = self.valueMatrix[0][0]
        realEnd = self.valueMatrix[len(self.valueMatrix) - 1][0]
        
        if newStartTime < realStart: newStartTime = realStart
        if newEndTime > realEnd: newEndTime = realEnd
        if newStartTime >= newEndTime: newStartTime = newEndTime
        
        line = 0
        while newStartTime > self.valueMatrix[line][0]:
            line += 1
            
        if (line > 0):
            if abs(newStartTime - self.valueMatrix[line - 1][0]) > \
                abs(newStartTime - self.valueMatrix[line][0]):
                self.startLine = line
            else:
                self.startLine = line - 1
        else:
            self.startLine = 0

        while newEndTime > self.valueMatrix[line][0]:
            line += 1

        if abs(newEndTime - self.valueMatrix[line - 1][0]) > \
            abs(newEndTime - self.valueMatrix[line][0]):
            self.endLine = line
        else:
            self.endLine = line - 1
        # Establishing endLine based on time
        
        self.findPeaks()

    def OnText_MaxMinChoice(self, event):
        self.modlabel_valueType.SetLabel('(M)')
        if self.text_MaxMin.GetSelection() == 0:
            self.searchingMin = True
        else:
            self.searchingMin = False
    
    def OnText_zeroPassEndChar(self, event):
        self.modlabel_finalTime.SetLabel('(M)')
        event.Skip()                

    def OnText_zeroPassBeginChar(self, event):
        self.modlabel_startTime.SetLabel('(M)')
        event.Skip()                

    def OnCheck_curveYellowCheckbox(self, event):
        event.Skip()

class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)

    def GetHtmlText(self,text):
        html_text = text.replace('\n\n','<P>')
        html_text = text.replace('\n', '<BR>')
        return html_text

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.PrintText(self.GetHtmlText(text),doc_name)

    def PreviewText(self, text, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetHtmlText(text))
