#Boa:Frame:peakTimeStdDevFrame

import wx
from wx.html import HtmlEasyPrinting
from wx.lib import plot
from PeakTimeStdDevPlot import PlotControl
from sys import argv, exit
from os import path, remove
from PeakTimeStdDevLib import *
import crossCorr_details

def create(parent):
    return peakTimeStdDevFrame(parent)

[wxID_PEAKTIMESTDDEVFRAME, wxID_PEAKTIMESTDDEVFRAMEBOX_CROSSCORR, 
 wxID_PEAKTIMESTDDEVFRAMEBOX_CURVEINCLUSE, wxID_PEAKTIMESTDDEVFRAMEBOX_GLOBAL, 
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
 wxID_PEAKTIMESTDDEVFRAMELABEL_AVERAGEGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_AVTIME, wxID_PEAKTIMESTDDEVFRAMELABEL_ENDLINE, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_FILENAME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_MAXTIME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME2, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME4, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIME6, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIMEGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_NUMLINES, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_SEARCHING, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_STDDEVTIME, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_STRAIN, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME2, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME4, wxID_PEAKTIMESTDDEVFRAMELABEL_TIME5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIME6, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_TIMEGLOBAL, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL1, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL2, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL3, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL4, wxID_PEAKTIMESTDDEVFRAMELABEL_VAL5, 
 wxID_PEAKTIMESTDDEVFRAMELABEL_VAL6, wxID_PEAKTIMESTDDEVFRAMELABEL_VALGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_FINALTIME, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_STARTTIME, 
 wxID_PEAKTIMESTDDEVFRAMEMODLABEL_VALUETYPE, 
 wxID_PEAKTIMESTDDEVFRAMEPANEL_STRAIN, wxID_PEAKTIMESTDDEVFRAMESTATICBITMAP1, 
 wxID_PEAKTIMESTDDEVFRAMESTATICLINE1, wxID_PEAKTIMESTDDEVFRAMESTATICTEXT1, 
 wxID_PEAKTIMESTDDEVFRAMESTATICTEXT2, wxID_PEAKTIMESTDDEVFRAMESTATICTEXT3, 
 wxID_PEAKTIMESTDDEVFRAMESTATUSBAR, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_AVERAGEGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_AVTIME, wxID_PEAKTIMESTDDEVFRAMETEXT_COL1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL2, wxID_PEAKTIMESTDDEVFRAMETEXT_COL3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL4, wxID_PEAKTIMESTDDEVFRAMETEXT_COL5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_COL6, wxID_PEAKTIMESTDDEVFRAMETEXT_CROSSCORR, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_FILENAME, wxID_PEAKTIMESTDDEVFRAMETEXT_MAXMIN, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_MAXTIME, wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME2, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME4, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIME6, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIMEGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_NUMLINES, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_STDDEVTIME, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME1, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME2, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME3, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME4, wxID_PEAKTIMESTDDEVFRAMETEXT_TIME5, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TIME6, wxID_PEAKTIMESTDDEVFRAMETEXT_TIMEGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_TUS, wxID_PEAKTIMESTDDEVFRAMETEXT_UNIFORMITY, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL1, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL2, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL3, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL4, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VAL5, wxID_PEAKTIMESTDDEVFRAMETEXT_VAL6, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_VALGLOBAL, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSBEGIN, 
 wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSEND, 
] = [wx.NewId() for _init_ctrls in range(100)]

class peakTimeStdDevFrame(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_PEAKTIMESTDDEVFRAME,
              name='peakTimeStdDevFrame', parent=prnt, pos=wx.Point(44, 111),
              size=wx.Size(1036, 598),
              style=wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION|wx.SYSTEM_MENU|wx.CLIP_CHILDREN,
              title='Calcolo Deviazione Standard Tempi di picco di STRAIN (v. 08/12/2010)')
        self.SetIcon(wx.Icon(u'img/heart.ico',wx.BITMAP_TYPE_ICO))
        self.SetClientSize(wx.Size(1028, 571))
        self.SetForegroundColour(wx.Colour(0, 230, 0))

        self.statusBar = wx.StatusBar(id=wxID_PEAKTIMESTDDEVFRAMESTATUSBAR,
              name='statusBar', parent=self, style=0)
        self.SetStatusBar(self.statusBar)

        self.panel_strain = wx.Panel(id=wxID_PEAKTIMESTDDEVFRAMEPANEL_STRAIN,
              name='panel_strain', parent=self, pos=wx.Point(0, 0),
              size=wx.Size(1028, 551), style=wx.TAB_TRAVERSAL)

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
              label=u'Si cercano i picchi', name='label_searching',
              parent=self.panel_strain, pos=wx.Point(8, 48), size=wx.Size(83,
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
              label=u'Picchi', name='box_values', parent=self.panel_strain,
              pos=wx.Point(8, 72), size=wx.Size(592, 256), style=0)

        self.box_mediadev = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_MEDIADEV,
              label='Media e deviazione', name='box_mediadev',
              parent=self.panel_strain, pos=wx.Point(8, 383), size=wx.Size(592,
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
              label=u'Picco', name='label_val2', parent=self.panel_strain,
              pos=wx.Point(152, 130), size=wx.Size(24, 13), style=0)

        self.label_val3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL3,
              label=u'Picco', name='label_val3', parent=self.panel_strain,
              pos=wx.Point(152, 160), size=wx.Size(24, 13), style=0)

        self.label_val4 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL4,
              label=u'Picco', name='label_val4', parent=self.panel_strain,
              pos=wx.Point(152, 194), size=wx.Size(24, 13), style=0)

        self.label_val5 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL5,
              label=u'Picco', name='label_val5', parent=self.panel_strain,
              pos=wx.Point(152, 226), size=wx.Size(24, 13), style=0)

        self.label_val6 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VAL6,
              label=u'Picco', name='label_val6', parent=self.panel_strain,
              pos=wx.Point(152, 258), size=wx.Size(24, 13), style=0)

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
              label=u'Picco', name='label_val1', parent=self.panel_strain,
              pos=wx.Point(152, 98), size=wx.Size(24, 13), style=0)

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
              pos=wx.Point(269, 407), size=wx.Size(194, 13), style=0)

        self.text_stdDevTime = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_STDDEVTIME,
              name='text_stdDevTime', parent=self.panel_strain,
              pos=wx.Point(475, 403), size=wx.Size(113, 21), style=0, value='')
        self.text_stdDevTime.SetEditable(False)

        self.label_avTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_AVTIME,
              label='Media tempi normalizzati:', name='label_avTime',
              parent=self.panel_strain, pos=wx.Point(23, 407), size=wx.Size(124,
              13), style=0)

        self.text_avTime = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_AVTIME,
              name='text_avTime', parent=self.panel_strain, pos=wx.Point(155,
              403), size=wx.Size(97, 21), style=0, value='')
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
              name='box_rumore', parent=self.panel_strain, pos=wx.Point(8, 490),
              size=wx.Size(512, 52), style=0)

        self.label_endLine = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_ENDLINE,
              label='Tempo finale valutazione:', name='label_endLine',
              parent=self.panel_strain, pos=wx.Point(279, 512),
              size=wx.Size(124, 13), style=0)

        self.text_zeroPassEnd = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSEND,
              name='text_zeroPassEnd', parent=self.panel_strain,
              pos=wx.Point(407, 509), size=wx.Size(72, 21), style=0, value='')
        self.text_zeroPassEnd.Bind(wx.EVT_CHAR, self.OnText_zeroPassEndChar)

        self.button_print = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_PRINT,
              label='Stampa', name='button_print', parent=self.panel_strain,
              pos=wx.Point(528, 519), size=wx.Size(75, 24), style=0)
        self.button_print.Bind(wx.EVT_BUTTON, self.OnButton_printButton,
              id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_PRINT)

        self.staticText1 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT1,
              label='Tempo iniziale di valutazione:', name='staticText1',
              parent=self.panel_strain, pos=wx.Point(22, 512), size=wx.Size(144,
              13), style=0)

        self.text_zeroPassBegin = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_ZEROPASSBEGIN,
              name='text_zeroPassBegin', parent=self.panel_strain,
              pos=wx.Point(176, 509), size=wx.Size(64, 21), style=0, value='')
        self.text_zeroPassBegin.Bind(wx.EVT_CHAR, self.OnText_zeroPassBeginChar)

        self.staticLine1 = wx.StaticLine(id=wxID_PEAKTIMESTDDEVFRAMESTATICLINE1,
              name='staticLine1', parent=self.panel_strain, pos=wx.Point(608,
              16), size=wx.Size(1, 526), style=0)

        self.staticBitmap1 = wx.StaticBitmap(bitmap=wx.Bitmap(u'img/heart_geometric.gif',
              wx.BITMAP_TYPE_GIF), id=wxID_PEAKTIMESTDDEVFRAMESTATICBITMAP1,
              name='staticBitmap1', parent=self.panel_strain, pos=wx.Point(851,
              370), size=wx.Size(174, 159), style=0)

        self.label_strain = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_STRAIN,
              label='Analysis', name='label_strain', parent=self.panel_strain,
              pos=wx.Point(688, 480), size=wx.Size(175, 58), style=0)
        self.label_strain.SetFont(wx.Font(36, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))
        self.label_strain.SetExtraStyle(0)

        self.staticText2 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT2,
              label='Strain', name='staticText2', parent=self.panel_strain,
              pos=wx.Point(616, 417), size=wx.Size(127, 58), style=0)
        self.staticText2.SetFont(wx.Font(36, wx.SWISS, wx.ITALIC, wx.NORMAL,
              False, 'Tahoma'))
        self.staticText2.SetExtraStyle(0)
        self.staticText2.SetLayoutDirection(1)
        self.staticText2.SetHelpText('')

        self.label_asterisco = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_ASTERISCO,
              label="* Se il tempo di picco appare all'inizio dell'intervallo si assume",
              name='label_asterisco', parent=self.panel_strain, pos=wx.Point(32,
              288), size=wx.Size(392, 13), style=0)

        self.staticText3 = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMESTATICTEXT3,
              label='un valore di 100 normalizzato per massimizzare la dispersione.',
              name='staticText3', parent=self.panel_strain, pos=wx.Point(40,
              304), size=wx.Size(297, 13), style=0)

        self.box_plot = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_PLOT,
              label='Data plot', name='box_plot', parent=self.panel_strain,
              pos=wx.Point(616, 51), size=wx.Size(424, 304), style=0)

        self.button_ricalcola = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_RICALCOLA,
              label='Ricalcola', name='button_ricalcola',
              parent=self.panel_strain, pos=wx.Point(528, 493), size=wx.Size(75,
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
              label=u'TUS:', name='text_uniformity', parent=self.panel_strain,
              pos=wx.Point(22, 462), size=wx.Size(23, 13), style=0)

        self.text_TUS = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TUS,
              name='text_TUS', parent=self.panel_strain, pos=wx.Point(62, 459),
              size=wx.Size(190, 21), style=0, value='')
        self.text_TUS.SetEditable(False)

        self.modlabel_finalTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_FINALTIME,
              label='', name='modlabel_finalTime', parent=self.panel_strain,
              pos=wx.Point(495, 497), size=wx.Size(16, 13), style=0)

        self.modlabel_valueType = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_VALUETYPE,
              label='', name='modlabel_valueType', parent=self.panel_strain,
              pos=wx.Point(188, 47), size=wx.Size(16, 13), style=0)

        self.text_crosscorr = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMETEXT_CROSSCORR,
              label=u'Media normalizzata:', name='text_crosscorr',
              parent=self.panel_strain, pos=wx.Point(285, 461), size=wx.Size(95,
              14), style=0)

        self.box_tus = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_TUS,
              label=u'Indice di uniformit\xe0 temporale di strain (TUS)',
              name='box_tus', parent=self.panel_strain, pos=wx.Point(8, 439),
              size=wx.Size(259, 48), style=0)

        self.box_crosscorr = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_CROSSCORR,
              label=u'Cross-Correlazione', name='box_crosscorr',
              parent=self.panel_strain, pos=wx.Point(271, 440),
              size=wx.Size(328, 48), style=0)

        self.edit_crosscorr = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMEEDIT_CROSSCORR,
              name='edit_crosscorr', parent=self.panel_strain, pos=wx.Point(393,
              459), size=wx.Size(126, 21), style=0, value='')
        self.edit_crosscorr.SetEditable(False)

        self.button_crossdetail = wx.Button(id=wxID_PEAKTIMESTDDEVFRAMEBUTTON_CROSSDETAIL,
              label='Dettagli', name='button_crossdetail',
              parent=self.panel_strain, pos=wx.Point(528, 458), size=wx.Size(63,
              23), style=0)
        self.button_crossdetail.Bind(wx.EVT_BUTTON,
              self.OnButton_crossdetailButton,
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
        self.check_curveBlue.Bind(wx.EVT_CHECKBOX,
              self.OnCheck_curveBlueCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVEBLUE)

        self.check_curveCyan = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVECYAN,
              label='Cyan', name='check_curveCyan', parent=self.panel_strain,
              pos=wx.Point(689, 27), size=wx.Size(46, 13), style=0)
        self.check_curveCyan.SetForegroundColour(wx.Colour(0, 223, 223))
        self.check_curveCyan.SetValue(False)
        self.check_curveCyan.Bind(wx.EVT_CHECKBOX,
              self.OnCheck_curveCyanCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_CURVECYAN)

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
        self.check_colorRed.Bind(wx.EVT_CHECKBOX, self.OnCheck_colorRedCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORRED)

        self.check_colorGreen = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORGREEN,
              label='Green', name='check_colorGreen', parent=self.panel_strain,
              pos=wx.Point(884, 27), size=wx.Size(46, 13), style=0)
        self.check_colorGreen.SetForegroundColour(wx.Colour(0, 159, 0))
        self.check_colorGreen.SetValue(False)
        self.check_colorGreen.Bind(wx.EVT_CHECKBOX,
              self.OnCheck_colorGreenCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORGREEN)

        self.check_colorMagenta = wx.CheckBox(id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORMAGENTA,
              label='Magenta', name='check_colorMagenta',
              parent=self.panel_strain, pos=wx.Point(950, 27), size=wx.Size(65,
              13), style=0)
        self.check_colorMagenta.SetForegroundColour(wx.Colour(255, 0, 255))
        self.check_colorMagenta.SetValue(False)
        self.check_colorMagenta.Bind(wx.EVT_CHECKBOX,
              self.OnCheck_colorMagentaCheckbox,
              id=wxID_PEAKTIMESTDDEVFRAMECHECK_COLORMAGENTA)

        self.modlabel_startTime = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMEMODLABEL_STARTTIME,
              label='', name='modlabel_startTime', parent=self.panel_strain,
              pos=wx.Point(252, 497), size=wx.Size(16, 13), style=0)

        self.box_global = wx.StaticBox(id=wxID_PEAKTIMESTDDEVFRAMEBOX_GLOBAL,
              label=u'Curva GLOBAL', name=u'box_global',
              parent=self.panel_strain, pos=wx.Point(8, 328), size=wx.Size(592,
              54), style=0)

        self.text_valGlobal = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_VALGLOBAL,
              name=u'text_valGlobal', parent=self.panel_strain,
              pos=wx.Point(192, 352), size=wx.Size(96, 21), style=0, value=u'')

        self.text_timeGlobal = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_TIMEGLOBAL,
              name=u'text_timeGlobal', parent=self.panel_strain,
              pos=wx.Point(360, 352), size=wx.Size(72, 21), style=0, value=u'')

        self.text_normTimeGlobal = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_NORMTIMEGLOBAL,
              name=u'text_normTimeGlobal', parent=self.panel_strain,
              pos=wx.Point(528, 352), size=wx.Size(48, 21), style=0, value=u'')

        self.text_averageGlobal = wx.TextCtrl(id=wxID_PEAKTIMESTDDEVFRAMETEXT_AVERAGEGLOBAL,
              name=u'text_averageGlobal', parent=self.panel_strain,
              pos=wx.Point(62, 352), size=wx.Size(75, 21), style=0, value=u'')

        self.label_valGlobal = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_VALGLOBAL,
              label=u'Picco', name=u'label_valGlobal', parent=self.panel_strain,
              pos=wx.Point(152, 354), size=wx.Size(24, 13), style=0)

        self.label_timeGlobal = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_TIMEGLOBAL,
              label='Tempo', name=u'label_timeGlobal', parent=self.panel_strain,
              pos=wx.Point(320, 354), size=wx.Size(33, 13), style=0)

        self.label_normTimeGlobal = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_NORMTIMEGLOBAL,
              label='(Normalizzato)', name=u'label_normTimeGlobal',
              parent=self.panel_strain, pos=wx.Point(448, 354), size=wx.Size(69,
              13), style=0)

        self.label_averageGlobal = wx.StaticText(id=wxID_PEAKTIMESTDDEVFRAMELABEL_AVERAGEGLOBAL,
              label=u'Media', name=u'label_averageGlobal',
              parent=self.panel_strain, pos=wx.Point(20, 354), size=wx.Size(37,
              13), style=0)

    def __init__(self, parent):
        self._init_ctrls(parent)
        
        self.panel_plot = PlotControl(id=wx.NewId(),
              name='panel_plot', parent=self.panel_strain,
              pos=wx.Point(626, 69), size=wx.Size(404, 276), style=0)    

        self.fileName = ''
        self.crossCorrDebug = None

        self.statusBar.SetStatusText("Strain evaluation utility v0.41 beta, coded by Andrea Chiarini")
        self.button_print.Enable(False)

    def OnButton_openButton(self, event):
        dlg = wx.FileDialog(self, "Scegli un file di acquisizione", path.dirname(self.fileName), "", "*.*", wx.OPEN)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                self.fileName = dlg.GetPath()
                self.text_FileName.SetValue(path.basename(self.fileName))
                self.loadFile(self.fileName)
                self.analyseFile()
                self.statusBar.SetStatusText("Evaluation verified correctly!")
                self.button_print.Enable(True)
        finally:
            dlg.Destroy()
   
    def loadFile( self, fileName ):
        # Opening file
        try:
            inputFile = open(fileName)
        except IOError:
            self.statusBar.SetStatusText("Errore durante la lettura del file")
            dlg = wx.MessageDialog(self, "Errore durante la lettura del file.","Attenzione!",wx.OK | wx.ICON_HAND)
            dlg.ShowModal()                
            return
            
        # Extracting data from file and inserting in data structure
        self.rawCurves, self.searchMaximums = extractRawDataFromFile( inputFile )
                
        # Exception if file format not correct
        if self.rawCurves == None:
            #raise WrongFormatException
            self.statusBar.SetStatusText("Formato non corretto!")
            dlg = wx.MessageDialog(self, "Formato del file non corretto.","Verificare formato file",wx.OK | wx.ICON_HAND)
            dlg.ShowModal()                
            return

        self.initializeGUI( self.rawCurves['Curves'] )
        
        # Gives the start line and endline where common zero passes are found
        self.startLine, self.endLine = findCommonZeroPasses( self.rawCurves['Curves'].values() )
        
        # Resetting labels indicating if a value was modified
        self.modlabel_valueType.SetLabel('')
        self.modlabel_finalTime.SetLabel('')
        self.modlabel_startTime.SetLabel('')
        
        # Printing total analysis time
        self.text_maxTime.SetValue( str( self.rawCurves['Time'][-1] - self.rawCurves['Time'][0] ) )        

        # Printing general information
        self.text_numLines.SetValue( str( len(self.rawCurves['Time']) - 1 ) )

        # Setting if searching maximum or minimum
        self.text_MaxMin.SetSelection( int(self.searchMaximums) )

    def analyseFile( self ):
        
        # Show if no globalCurve present in raw data or loading less then 6 curves, GLOBAL is calculated
        if self.rawCurves['GlobalCurve'] == [] or len(self.curvesToLoad) < 6:
            self.peakFields['GLOBAL']['NameField'].SetLabel("Curva GLOBAL (calcolata)")
        else:
            # Taking GLOBAL curve from file
            self.peakFields['GLOBAL']['NameField'].SetLabel("Curva GLOBAL")
        
        # New copy of curve data without border noise
        strippedCurves = stripNoiseFromRawData( self.rawCurves, self.startLine, self.endLine, self.curvesToLoad )
        
        # Printing start and stop times
        if self.startLine == 0:
            self.text_zeroPassBegin.SetValue(str(strippedCurves['Time'][0])  + ' (inizio)')
        else:
            self.text_zeroPassBegin.SetValue(str(strippedCurves['Time'][0]))
            
        if self.endLine == len(self.rawCurves['Time']) - 1:
            self.text_zeroPassEnd.SetValue(str(strippedCurves['Time'][-1]) + ' (fine)')
        else:
            self.text_zeroPassEnd.SetValue(str(strippedCurves['Time'][-1]))
            
        # Calculates peaks (minimum or maximum)
        peaks, globalPeak = findPeaks( strippedCurves, self.searchMaximums )
        
        # Show peak data in text boxes
        self.showPeaks( peaks, globalPeak, strippedCurves['Time'] )
        
        # Show mean value of GLOBAL curve
        self.text_averageGlobal.SetValue( str( round(average( strippedCurves['GlobalCurve'] ), 2) ) )
        
        # Show peak average
        peakTimes = [ normalizeTime ( strippedCurves['Time'], peaks[curveName]['PeakTime'] ) \
                            for curveName in strippedCurves['Curves'] ]
        self.text_avTime.SetValue( str( round( average( peakTimes ) , 2) ) )
        
        # Show peak standard deviation
        self.text_stdDevTime.SetValue( str( round( standardDeviation( peakTimes ) ,5) ) )

        # Calculate TUS
        self.text_TUS.SetValue( str( calculateTUS( strippedCurves ) ) )

        # Calculate Cross Correlation
        crossCorrAv, self.crossCorrDebug = findCrossCorrelationAverage( strippedCurves )
        self.edit_crosscorr.SetValue( str( crossCorrAv ) )
        
        # Plot curves
        self.plotMatrix( peaks )
        
    def showPeaks(self, peaks, globalPeak, times):
        
        for curveName in peaks:
            self.peakFields[curveName]['NameField'].SetValue( curveName )
            self.peakFields[curveName]['ValueField'].SetValue( str( peaks[curveName]['PeakValue'] ) )
            self.peakFields[curveName]['TimeField'].SetValue( str( peaks[curveName]['PeakTime'] ) )
            self.peakFields[curveName]['NormalizedTimeField'].SetValue( str( normalizeTime(times, peaks[curveName]['PeakTime']) ) )
        
        self.peakFields['GLOBAL']['ValueField'].SetLabel( str( globalPeak['PeakValue'] ) )
        self.peakFields['GLOBAL']['TimeField'].SetLabel( str( globalPeak['PeakTime'] ) )
        self.peakFields['GLOBAL']['NormalizedTimeField'].SetLabel( str( normalizeTime(times, globalPeak['PeakTime']) ) )

    
    def plotMatrix(self, peaks):
        linesToPlot = []
        
        # Searching global min and global max to resize plotted surface accordingly
        globalMin = 0
        globalMax = 0
        
        for curveName in self.rawCurves['Curves']:

            globalMin = min( globalMin, min(self.rawCurves['Curves'][curveName]) )
            globalMax = max( globalMax, max(self.rawCurves['Curves'][curveName]) )

            curvePlotData = [ ( self.rawCurves['Time'][i], self.rawCurves['Curves'][curveName][i] ) for i in range(0, len(self.rawCurves['Time']))]

            if self.peakFields[curveName]['CurveActivation'].GetValue():
                # Activated curve
                peakPlotData = [ (peaks[curveName]['PeakTime'],0), (peaks[curveName]['PeakTime'], peaks[curveName]['PeakValue']) ]                
                
                # Curve plot data                
                linesToPlot.append( plot.PolyLine(curvePlotData, legend='', colour=curveName, width=2) )
                
                # Curve peak indicator (vertical line)
                linesToPlot.append( plot.PolyLine(peakPlotData, legend='', colour=curveName, width=2, style=wx.DOT) )                        
            else:
                # Deactivated curve (no peak indicator)
                linesToPlot.append( plot.PolyLine(curvePlotData, legend='', colour=curveName, width=1, style=wx.DOT) )

        # X-Axis
        linesToPlot.append( plot.PolyLine([(0, 0), ( self.rawCurves['Time'][-1], 0)], legend='', colour='black', width=2, style=wx.SOLID) )
        
        # Cut-off values
        startTime = self.rawCurves['Time'][self.startLine]
        endTime = self.rawCurves['Time'][self.endLine]
        
        # Interval initial cut-off curve (also sets vertical scale)
        linesToPlot.append( plot.PolyLine([(startTime, globalMin - 1), (startTime, globalMax + 1)], legend='', colour='black', width=2, style=wx.DOT_DASH) )
        # Interval final cut-off curve (also sets vertical scale)
        linesToPlot.append( plot.PolyLine([(endTime, globalMin - 1), (endTime, globalMax + 1)], legend='', colour='black', width=2, style=wx.DOT_DASH) )

        # Plotting graph
        self.panel_plot._setSize()
        gc = plot.PlotGraphics(linesToPlot, 'Grafico curve di strain', 'Tempi di acquisizione', 'Valori Strain')
        self.panel_plot.Draw(gc, xAxis= (0,self.rawCurves['Time'][-1] ), yAxis= (globalMin - 1,globalMax + 1))

    def initializeGUI(self, curves):
        self.peakFields = {}
        self.curvesToLoad = []
        
        self.text_col1.Disable()
        self.text_col1.SetValue('')
        self.text_val1.Disable()
        self.text_val1.SetValue('')
        self.text_time1.Disable()
        self.text_time1.SetValue('')
        self.text_normTime1.Disable()
        self.text_normTime1.SetValue('')
        
        self.text_col2.Disable()
        self.text_col2.SetValue('')
        self.text_val2.Disable()
        self.text_val2.SetValue('')
        self.text_time2.Disable()
        self.text_time2.SetValue('')
        self.text_normTime2.Disable()
        self.text_normTime2.SetValue('')
        
        self.text_col3.Disable()
        self.text_col3.SetValue('')
        self.text_val3.Disable()
        self.text_val3.SetValue('')
        self.text_time3.Disable()
        self.text_time3.SetValue('')
        self.text_normTime3.Disable()
        self.text_normTime3.SetValue('')
        
        self.text_col4.Disable()
        self.text_col4.SetValue('')
        self.text_val4.Disable()
        self.text_val4.SetValue('')
        self.text_time4.Disable()
        self.text_time4.SetValue('')
        self.text_normTime4.Disable()
        self.text_normTime4.SetValue('')
        
        self.text_col5.Disable()
        self.text_col5.SetValue('')
        self.text_val5.Disable()
        self.text_val5.SetValue('')
        self.text_time5.Disable()
        self.text_time5.SetValue('')
        self.text_normTime5.Disable()
        self.text_normTime5.SetValue('')
        
        self.text_col6.Disable()
        self.text_col6.SetValue('')
        self.text_val6.Disable()
        self.text_val6.SetValue('')
        self.text_time6.Disable()
        self.text_time6.SetValue('')
        self.text_normTime6.Disable()
        self.text_normTime6.SetValue('')
        
        for curveName in curves:
            self.peakFields[curveName] = {}
            self.curvesToLoad.append(curveName)

        if(len(self.peakFields) > 0):
            self.text_col1.Disable()
            self.text_val1.Disable()
            self.text_time1.Disable()
            self.text_normTime1.Disable()
            
            self.peakFields[self.peakFields.keys()[0]]['NameField'] = self.text_col1
            self.peakFields[self.peakFields.keys()[0]]['ValueField'] = self.text_val1
            self.peakFields[self.peakFields.keys()[0]]['TimeField'] = self.text_time1
            self.peakFields[self.peakFields.keys()[0]]['NormalizedTimeField'] = self.text_normTime1

        if(len(self.peakFields) > 1):
            self.text_col2.Disable()
            self.text_val2.Disable()
            self.text_time2.Disable()
            self.text_normTime2.Disable()
            
            self.peakFields[self.peakFields.keys()[1]]['NameField'] = self.text_col2
            self.peakFields[self.peakFields.keys()[1]]['ValueField'] = self.text_val2
            self.peakFields[self.peakFields.keys()[1]]['TimeField'] = self.text_time2
            self.peakFields[self.peakFields.keys()[1]]['NormalizedTimeField'] = self.text_normTime2
            
        if(len(self.peakFields) > 2):
            self.text_col3.Disable()
            self.text_val3.Disable()
            self.text_time3.Disable()
            self.text_normTime3.Disable()
            
            self.peakFields[self.peakFields.keys()[2]]['NameField'] = self.text_col3
            self.peakFields[self.peakFields.keys()[2]]['ValueField'] = self.text_val3
            self.peakFields[self.peakFields.keys()[2]]['TimeField'] = self.text_time3
            self.peakFields[self.peakFields.keys()[2]]['NormalizedTimeField'] = self.text_normTime3
        
        if(len(self.peakFields) > 3):
            self.text_col4.Disable()
            self.text_val4.Disable()
            self.text_time4.Disable()
            self.text_normTime4.Disable()
            
            self.peakFields[self.peakFields.keys()[3]]['NameField'] = self.text_col4
            self.peakFields[self.peakFields.keys()[3]]['ValueField'] = self.text_val4
            self.peakFields[self.peakFields.keys()[3]]['TimeField'] = self.text_time4
            self.peakFields[self.peakFields.keys()[3]]['NormalizedTimeField'] = self.text_normTime4
            
        if(len(self.peakFields) > 4):
            self.text_col5.Disable()
            self.text_val5.Disable()
            self.text_time5.Disable()
            self.text_normTime5.Disable()
            
            self.peakFields[self.peakFields.keys()[4]]['NameField'] = self.text_col5
            self.peakFields[self.peakFields.keys()[4]]['ValueField'] = self.text_val5
            self.peakFields[self.peakFields.keys()[4]]['TimeField'] = self.text_time5
            self.peakFields[self.peakFields.keys()[4]]['NormalizedTimeField'] = self.text_normTime5
        
        if(len(self.peakFields) > 5):
            self.text_col6.Disable()
            self.text_val6.Disable()
            self.text_time6.Disable()
            self.text_normTime6.Disable()
            
            self.peakFields[self.peakFields.keys()[5]]['NameField'] = self.text_col6
            self.peakFields[self.peakFields.keys()[5]]['ValueField'] = self.text_val6
            self.peakFields[self.peakFields.keys()[5]]['TimeField'] = self.text_time6
            self.peakFields[self.peakFields.keys()[5]]['NormalizedTimeField'] = self.text_normTime6

        self.peakFields['GLOBAL'] = {}
        
        self.peakFields['GLOBAL']['NameField'] = self.box_global
        self.peakFields['GLOBAL']['AverageField'] = self.text_averageGlobal
        self.peakFields['GLOBAL']['ValueField'] = self.text_valGlobal
        self.peakFields['GLOBAL']['TimeField'] = self.text_timeGlobal 
        self.peakFields['GLOBAL']['NormalizedTimeField'] = self.text_normTimeGlobal
        
        # Checkboxes
        if('YELLOW') in self.peakFields: 
            self.check_curveYellow.Enable()
            self.peakFields['YELLOW']['CurveActivation'] = self.check_curveYellow
        else:
            self.check_curveYellow.Disable()
            
        if('RED') in self.peakFields: 
            self.check_colorRed.Enable();
            self.peakFields['RED']['CurveActivation'] = self.check_colorRed
        else:
            self.check_colorRed.Disable();
            
        if('MAGENTA') in self.peakFields: 
            self.check_colorMagenta.Enable();
            self.peakFields['MAGENTA']['CurveActivation'] = self.check_colorMagenta
        else:
            self.check_colorMagenta.Disable();
            
        if('BLUE') in self.peakFields: 
            self.check_curveBlue.Enable();
            self.peakFields['BLUE']['CurveActivation'] = self.check_curveBlue
        else:
            self.check_curveBlue.Disable();
        
        if('CYAN') in self.peakFields: 
            self.check_curveCyan.Enable();
            self.peakFields['CYAN']['CurveActivation'] = self.check_curveCyan
        else:
            self.check_curveCyan.Disable();
        
        if('GREEN') in self.peakFields: 
            self.check_colorGreen.Enable();
            self.peakFields['GREEN']['CurveActivation'] = self.check_colorGreen
        else:
            self.check_colorGreen.Disable();
        
        for curveName in curves:
            self.peakFields[curveName]['NameField'].Enabled = True
            self.peakFields[curveName]['ValueField'].Enabled = True
            self.peakFields[curveName]['TimeField'].Enabled = True
            self.peakFields[curveName]['NormalizedTimeField'].Enabled = True
            self.peakFields[curveName]['CurveActivation'].SetValue(True)

    def OnButton_printButton(self, event):
        # Building HTML report
        (fp, fn) = path.split(self.fileName)
        report = "<br><div align=\"right\"><i><font size=\"1\">Analisi di Strain eseguita da PeakTimeStdDev, coded by Andrea Chiarini</font></i></div><br><br>"
        report += "<b>File di input:</b> " + fn + "\n\n"

        report += "<b>Valori cercati:</b> " + self.text_MaxMin.GetStringSelection()
        if 'M' in self.modlabel_valueType.GetLabel(): report += ' (*)'
        
        report += "\n<b>Righe nel file:</b> " + self.text_numLines.GetValue() + "\n"
        report += "<b>Tempo massimo:</b> " + self.text_maxTime.GetValue() + "\n"

        report += "<b>Rapporto analisi:</b>\n\n"

        report += '<table border="1" width="100%">'
        report += '<tr><td><b>Colonna</b></td><td><b>Valore</b></td><td><b>Tempo Ass.</b></td><td><b>Tempo Norm.</b></td></tr>'

        # Single curve data
        for curveName in self.peakFields:
            if curveName != 'GLOBAL':
                report += '<tr>'
                report += '<td>' + self.peakFields[curveName]['NameField'].GetValue() + '</td>'
                
                if ( self.peakFields[curveName]['CurveActivation'].GetValue() ):
                    # Stampo il valore minimo (o massimo)
                    report += '<td>' + self.peakFields[curveName]['ValueField'].GetValue() + '</td>'
                    # Stampo il tempo normalizzato (e assoluto)
                    report += '<td>' + self.peakFields[curveName]['TimeField'].GetValue() + '</td>'
                    report += '<td>' + self.peakFields[curveName]['NormalizedTimeField'].GetValue() + '</td>'
                else:
                    report += '<td>---</td><td>---</td><td>---</td>'
                report += '</tr>'
        report += '</table>\n\n'

        # Global curve data
        report += '<B>' + self.peakFields['GLOBAL']['NameField'].GetLabel() + '</B><BR>'
        report += '<table border="1" width="100%">'
        report += '<tr><td><B>Media</B></td><td><B>Valore</B></td><td><B>Tempo Ass.</B></td><td><B>Temp Norm.</B></td></tr>'
        report += '<tr>'
        
        report += '<td>' + self.peakFields['GLOBAL']['AverageField'].GetValue() + '</td>'
        report += '<td>' + self.peakFields['GLOBAL']['ValueField'].GetValue() + '</td>'
        report += '<td>' + self.peakFields['GLOBAL']['TimeField'].GetValue() + '</td>'
        report += '<td>' + self.peakFields['GLOBAL']['NormalizedTimeField'].GetValue() + '</td>'        
        report += '</tr>'
        report += '</table>\n\n'
        
        report += "<b>Tempo iniziale valutazione:</b> " + self.text_zeroPassBegin.GetValue()
        if 'M' in self.modlabel_startTime.GetLabel(): report += ' (*)'
        report += "\n<b>Tempo finale valutazione:</b> " + self.text_zeroPassEnd.GetValue()
        if 'M' in self.modlabel_finalTime.GetLabel(): report += ' (*)'
        
        report += "\n\n<b>Media tempi normalizzati:</b> " + self.text_avTime.GetValue() + "\n"
        report += "<b>Deviazione standard tempi normalizzati:</b> " + self.text_stdDevTime.GetValue() + "\n"
        report += "<b>Indice di uniformit&agrave temporale di strain:</b> " + self.text_TUS.GetValue() + "\n"
        report += "<b>Media dei valori di cross-correlazione normalizzati:</b> " + self.edit_crosscorr.GetValue() + "\n"
        report += "<br><div align=\"right\"><i><font size=\"1\">(*) Nota: I valori marcati con asterischi sono stati modificati dall'operatore.</font></i></div><br>"
        report += "<br><br>"
        report += "<div align=\"center\"><img src=\"plot.png\" width=\"550\" height=\"300\"></div>"

        self.printer = Printer()
        self.panel_plot.PrintSize()
        self.panel_plot._PrintBuffer.SaveFile('plot.png', wx.BITMAP_TYPE_PNG)
        self.printer.Print(report,"Analisi di Strain")
        self.statusBar.SetStatusText("Report inviato alla stampante")
        remove('plot.png')

    def OnButton_ricalcolaButton(self, event):
        # Clearing curve peak boxes
        for curveName in self.rawCurves['Curves']:
            self.peakFields[curveName]['NameField'].SetValue('')
            self.peakFields[curveName]['ValueField'].SetValue('')
            self.peakFields[curveName]['TimeField'].SetValue('')
            self.peakFields[curveName]['NormalizedTimeField'].SetValue('')
        
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
        realStart = self.rawCurves['Time'][0]
        realEnd = self.rawCurves['Time'][-1]
        
        if newStartTime < realStart: newStartTime = realStart
        if newEndTime > realEnd: newEndTime = realEnd
        if newStartTime >= newEndTime: newStartTime = newEndTime
        
        line = 0
        while newStartTime > self.rawCurves['Time'][line]:
            line += 1
            
        if (line > 0):
            if abs(newStartTime - self.rawCurves['Time'][line - 1]) > \
                abs(newStartTime - self.rawCurves['Time'][line]):
                self.startLine = line
            else:
                self.startLine = line - 1
        else:
            self.startLine = 0

        while newEndTime > self.rawCurves['Time'][line]:
            line += 1

        # Establishing endLine based on time
        if abs(newEndTime - self.rawCurves['Time'][line - 1]) > \
            abs(newEndTime - self.rawCurves['Time'][line]):
            self.endLine = line
        else:
            self.endLine = line - 1
        
        self.analyseFile()

    def OnText_MaxMinChoice(self, event):
        self.modlabel_valueType.SetLabel('(M)')
        if self.text_MaxMin.GetSelection() == 0:
            self.searchMaximums = False
        else:
            self.searchMaximums = True
            
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)
    
    def OnText_zeroPassEndChar(self, event):
        self.modlabel_finalTime.SetLabel('(M)')
        event.Skip()                

    def OnText_zeroPassBeginChar(self, event):
        self.modlabel_startTime.SetLabel('(M)')
        event.Skip() 

    def OnCheck_curveYellowCheckbox(self, event):
        checkedState = self.peakFields['YELLOW']['CurveActivation'].GetValue()
        
        # Keeping at least two curves present at any time
        if checkedState == False and len(self.curvesToLoad) <= 2 :
            self.peakFields['YELLOW']['CurveActivation'].SetValue(True)
        
        self.setCurveActivation('YELLOW', self.peakFields['YELLOW']['CurveActivation'].GetValue() )        
        
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)

    def OnCheck_curveBlueCheckbox(self, event):
        checkedState = self.peakFields['BLUE']['CurveActivation'].GetValue()
        
        # Keeping at least two curves present at any time
        if checkedState == False and len(self.curvesToLoad) <= 2 :
            self.peakFields['BLUE']['CurveActivation'].SetValue(True)
        
        self.setCurveActivation('BLUE', self.peakFields['BLUE']['CurveActivation'].GetValue() )        
        
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)

    def OnCheck_curveCyanCheckbox(self, event):
        checkedState = self.peakFields['CYAN']['CurveActivation'].GetValue()
        
        # Keeping at least two curves present at any time
        if checkedState == False and len(self.curvesToLoad) <= 2 :
            self.peakFields['CYAN']['CurveActivation'].SetValue(True)
        
        self.setCurveActivation('CYAN', self.peakFields['CYAN']['CurveActivation'].GetValue() )        
        
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)

    def OnCheck_colorRedCheckbox(self, event):
        checkedState = self.peakFields['RED']['CurveActivation'].GetValue()
        
        # Keeping at least two curves present at any time
        if checkedState == False and len(self.curvesToLoad) <= 2 :
            self.peakFields['RED']['CurveActivation'].SetValue(True)
        
        self.setCurveActivation('RED', self.peakFields['RED']['CurveActivation'].GetValue() )        
        
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)

    def OnCheck_colorGreenCheckbox(self, event):
        if 'GREEN' in self.peakFields:
            checkedState = self.peakFields['GREEN']['CurveActivation'].GetValue()
        
            # Keeping at least two curves present at any time
            if checkedState == False and len(self.curvesToLoad) <= 2 :
                self.peakFields['GREEN']['CurveActivation'].SetValue(True)
        
            self.setCurveActivation('GREEN', self.peakFields['GREEN']['CurveActivation'].GetValue() )        
        
            # Reanalysing file
            self.OnButton_ricalcolaButton(None)

    def OnCheck_colorMagentaCheckbox(self, event):
        checkedState = self.peakFields['MAGENTA']['CurveActivation'].GetValue()
        
        # Keeping at least two curves present at any time
        if checkedState == False and len(self.curvesToLoad) <= 2 :
            self.peakFields['MAGENTA']['CurveActivation'].SetValue(True)
            
        self.setCurveActivation('MAGENTA', self.peakFields['MAGENTA']['CurveActivation'].GetValue() )                
        
        # Reanalysing file
        self.OnButton_ricalcolaButton(None)
        
    def setCurveActivation(self, curveName, curveActivated):
        self.peakFields[curveName]['NameField'].Enabled = curveActivated
        self.peakFields[curveName]['ValueField'].Enabled = curveActivated
        self.peakFields[curveName]['TimeField'].Enabled = curveActivated
        self.peakFields[curveName]['NormalizedTimeField'].Enabled = curveActivated
        
        if curveActivated:
            if curveName not in self.curvesToLoad: self.curvesToLoad.append(curveName)
        else:
            if curveName in self.curvesToLoad: self.curvesToLoad.remove(curveName)

    def OnButton_crossdetailButton(self, event):
        crossCorrDetails = crossCorr_details.create(self)
        crossCorrDetails.Show()

class Printer(HtmlEasyPrinting):
    def __init__(self):
        HtmlEasyPrinting.__init__(self)

    def GetHtmlText(self,text):
        html_text = text.replace('\n\n','<P>')
        html_text = text.replace('\n', '<BR>')
        return html_text

    def Print(self, text, doc_name):
        self.SetHeader(doc_name)
        self.SetStandardFonts()
        self.PrintText(self.GetHtmlText(text),doc_name)

    def PreviewText(self, text, doc_name):
        self.SetHeader(doc_name)
        HtmlEasyPrinting.PreviewText(self, self.GetHtmlText(text))
