#Boa:MiniFrame:frame_crossCorrDetails

import wx

def create(parent):
    return frame_crossCorrDetails(parent)

[wxID_FRAME_CROSSCORRDETAILS, wxID_FRAME_CROSSCORRDETAILSBUTTON_CLOSE, 
 wxID_FRAME_CROSSCORRDETAILSPANEL1, wxID_FRAME_CROSSCORRDETAILSSTATICBOX1, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUE, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUECYAN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEGREEN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEMAGENTA, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUERED, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEYELLOW, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYAN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYANGREEN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYANMAGENTA, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYANRED, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYANYELLOW, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_CYAN_V, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_GREEN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_GREENMAGENTA, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_GREEN_V, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_MAGENTA, wxID_FRAME_CROSSCORRDETAILSTEXT_RED, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_REDGREEN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_REDMAGENTA, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_RED_V, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOW, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWGREEN, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWMAGENTA, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWRED, 
 wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOW_V, 
] = [wx.NewId() for _init_ctrls in range(29)]

class frame_crossCorrDetails(wx.MiniFrame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.MiniFrame.__init__(self, id=wxID_FRAME_CROSSCORRDETAILS,
              name='frame_crossCorrDetails', parent=prnt, pos=wx.Point(413,
              325), size=wx.Size(357, 276), style=wx.DEFAULT_FRAME_STYLE,
              title='Dettagli sul calcolo di cross-correlazione')
        self.SetClientSize(wx.Size(349, 249))
        self.SetToolTipString('Dettagli sul calcolo di cross-correlazione')

        self.panel1 = wx.Panel(id=wxID_FRAME_CROSSCORRDETAILSPANEL1,
              name='panel1', parent=self, pos=wx.Point(0, 0), size=wx.Size(349,
              249), style=wx.TAB_TRAVERSAL)

        self.staticBox1 = wx.StaticBox(id=wxID_FRAME_CROSSCORRDETAILSSTATICBOX1,
              label='Griglia di cross-correlazione fra le curve',
              name='staticBox1', parent=self.panel1, pos=wx.Point(5, 8),
              size=wx.Size(339, 208), style=0)

        self.button_close = wx.Button(id=wxID_FRAME_CROSSCORRDETAILSBUTTON_CLOSE,
              label='Chiudi', name='button_close', parent=self.panel1,
              pos=wx.Point(264, 221), size=wx.Size(75, 23), style=0)
        self.button_close.Bind(wx.EVT_BUTTON, self.OnButton_closeButton,
              id=wxID_FRAME_CROSSCORRDETAILSBUTTON_CLOSE)

        self.text_cyan_v = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYAN_V,
              label='Cyan', name='text_cyan_v', parent=self.panel1,
              pos=wx.Point(76, 32), size=wx.Size(25, 13), style=0)

        self.text_blueYellow = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEYELLOW,
              name='text_blueYellow', parent=self.panel1, pos=wx.Point(124, 53),
              size=wx.Size(37, 21), style=0, value='')

        self.text_yellow_v = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOW_V,
              label='Yellow', name='text_yellow_v', parent=self.panel1,
              pos=wx.Point(128, 32), size=wx.Size(31, 13), style=0)

        self.text_red_v = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_RED_V,
              label='Red', name='text_red_v', parent=self.panel1,
              pos=wx.Point(189, 32), size=wx.Size(19, 13), style=0)

        self.text_green_v = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_GREEN_V,
              label='Green', name='text_green_v', parent=self.panel1,
              pos=wx.Point(236, 32), size=wx.Size(29, 13), style=0)

        self.text_green = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_GREEN,
              label='Green', name='text_green', parent=self.panel1,
              pos=wx.Point(23, 185), size=wx.Size(29, 13), style=0)

        self.text_magenta = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_MAGENTA,
              label='Magenta', name='text_magenta', parent=self.panel1,
              pos=wx.Point(288, 32), size=wx.Size(42, 13), style=0)

        self.text_blue = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUE,
              label='Blue', name='text_blue', parent=self.panel1,
              pos=wx.Point(23, 57), size=wx.Size(32, 13), style=0)

        self.text_cyan = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYAN,
              label='Cyan', name='text_cyan', parent=self.panel1,
              pos=wx.Point(23, 87), size=wx.Size(25, 13), style=0)

        self.text_yellow = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOW,
              label='Yellow', name='text_yellow', parent=self.panel1,
              pos=wx.Point(23, 120), size=wx.Size(31, 13), style=0)

        self.text_red = wx.StaticText(id=wxID_FRAME_CROSSCORRDETAILSTEXT_RED,
              label='Red', name='text_red', parent=self.panel1, pos=wx.Point(23,
              154), size=wx.Size(19, 13), style=0)

        self.text_blueGreen = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEGREEN,
              name='text_blueGreen', parent=self.panel1, pos=wx.Point(235, 53),
              size=wx.Size(37, 21), style=0, value='')

        self.text_blueRed = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUERED,
              name='text_blueRed', parent=self.panel1, pos=wx.Point(180, 53),
              size=wx.Size(37, 21), style=0, value='')

        self.text_blueMagenta = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUEMAGENTA,
              name='text_blueMagenta', parent=self.panel1, pos=wx.Point(291,
              53), size=wx.Size(37, 21), style=0, value='')

        self.text_yellowMagenta = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWMAGENTA,
              name='text_yellowMagenta', parent=self.panel1, pos=wx.Point(291,
              117), size=wx.Size(37, 21), style=0, value='')

        self.text_cyanGreen = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYANGREEN,
              name='text_cyanGreen', parent=self.panel1, pos=wx.Point(235, 85),
              size=wx.Size(37, 21), style=0, value='')

        self.text_cyanMagenta = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYANMAGENTA,
              name='text_cyanMagenta', parent=self.panel1, pos=wx.Point(291,
              85), size=wx.Size(37, 21), style=0, value='')

        self.text_cyanYellow = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYANYELLOW,
              name='text_cyanYellow', parent=self.panel1, pos=wx.Point(124, 85),
              size=wx.Size(37, 21), style=0, value='')

        self.text_cyanRed = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_CYANRED,
              name='text_cyanRed', parent=self.panel1, pos=wx.Point(180, 85),
              size=wx.Size(37, 21), style=0, value='')

        self.text_redGreen = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_REDGREEN,
              name='text_redGreen', parent=self.panel1, pos=wx.Point(235, 149),
              size=wx.Size(37, 21), style=0, value='')

        self.text_yellowRed = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWRED,
              name='text_yellowRed', parent=self.panel1, pos=wx.Point(180, 117),
              size=wx.Size(37, 21), style=0, value='')

        self.text_yellowGreen = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_YELLOWGREEN,
              name='text_yellowGreen', parent=self.panel1, pos=wx.Point(235,
              117), size=wx.Size(37, 21), style=0, value='')

        self.text_redMagenta = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_REDMAGENTA,
              name='text_redMagenta', parent=self.panel1, pos=wx.Point(291,
              149), size=wx.Size(37, 21), style=0, value='')

        self.text_greenMagenta = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_GREENMAGENTA,
              name='text_greenMagenta', parent=self.panel1, pos=wx.Point(291,
              181), size=wx.Size(37, 21), style=0, value='')

        self.text_blueCyan = wx.TextCtrl(id=wxID_FRAME_CROSSCORRDETAILSTEXT_BLUECYAN,
              name='text_blueCyan', parent=self.panel1, pos=wx.Point(68, 53),
              size=wx.Size(37, 21), style=0, value='')

    def __init__(self, parent):
        self._init_ctrls(parent)
        self.fillFrame(parent.crossCorrDebug)

    def fillFrame(self, crossCorrDebugInfo):
        if crossCorrDebugInfo != None:
            for info in crossCorrDebugInfo:
                if 'BLUE' in info['Curves'] and 'GREEN' in info['Curves']:
                    self.text_blueGreen.SetValue(str(info['PeakValue']))
                    
                if 'BLUE' in info['Curves'] and 'RED' in info['Curves']:
                    self.text_blueRed.SetValue(str(info['PeakValue']))
                    
                if 'BLUE' in info['Curves'] and 'MAGENTA' in info['Curves']:
                    self.text_blueMagenta.SetValue(str(info['PeakValue']))

                if 'BLUE' in info['Curves'] and 'CYAN' in info['Curves']:
                    self.text_blueCyan.SetValue(str(info['PeakValue']))
                    
                if 'CYAN' in info['Curves'] and 'MAGENTA' in info['Curves']:
                    self.text_cyanMagenta.SetValue(str(info['PeakValue']))
                    
                if 'YELLOW' in info['Curves'] and 'MAGENTA' in info['Curves']:
                    self.text_yellowMagenta.SetValue(str(info['PeakValue']))
                    
                if 'CYAN' in info['Curves'] and 'GREEN' in info['Curves']:
                    self.text_cyanGreen.SetValue(str(info['PeakValue']))
                    
                if 'CYAN' in info['Curves'] and 'YELLOW' in info['Curves']:
                    self.text_cyanYellow.SetValue(str(info['PeakValue']))
                    
                if 'CYAN' in info['Curves'] and 'RED' in info['Curves']:
                    self.text_cyanRed.SetValue(str(info['PeakValue']))

                if 'RED' in info['Curves'] and 'GREEN' in info['Curves']:
                    self.text_redGreen.SetValue(str(info['PeakValue']))
                    
                if 'YELLOW' in info['Curves'] and 'RED' in info['Curves']:
                    self.text_yellowRed.SetValue(str(info['PeakValue']))
                    
                if 'YELLOW' in info['Curves'] and 'GREEN' in info['Curves']:
                    self.text_yellowGreen.SetValue(str(info['PeakValue']))
                    
                if 'RED' in info['Curves'] and 'MAGENTA' in info['Curves']:
                    self.text_redMagenta.SetValue(str(info['PeakValue']))
                    
                if 'GREEN' in info['Curves'] and 'MAGENTA' in info['Curves']:
                    self.text_greenMagenta.SetValue(str(info['PeakValue']))
                    
                if 'BLUE' in info['Curves'] and 'YELLOW' in info['Curves']:
                    self.text_blueYellow.SetValue(str(info['PeakValue']))
                    
    def OnButton_closeButton(self, event):
        self.Close()
