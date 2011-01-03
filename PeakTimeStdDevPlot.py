#-----------------------------------------------------------------------------
# Name:        wx.lib.plot.py
# Purpose:     Line, Bar and Scatter Graphs
#
#-----------------------------------------------------------------------------

import  string as _string
import  time as _time
import  wx
from wx.lib import plot

# Needs Numeric or numarray or NumPy
try:
    import numpy.oldnumeric as _Numeric
except:
    try:
        import numarray as _Numeric  #if numarray is used it is renamed Numeric
    except:
        try:
            import Numeric as _Numeric
        except:
            msg= """
            This module requires the Numeric/numarray or NumPy module,
            which could not be imported.  It probably is not installed
            (it's not part of the standard Python distribution). See the
            Numeric Python site (http://numpy.scipy.org) for information on
            downloading source or binaries."""
            raise ImportError, "Numeric,numarray or NumPy not found. \n" + msg


#-------------------------------------------------------------------------------
# Main window that you will want to import into your application.

class PlotControl(wx.PyControl):
    """
    Subclass of a wx.Panel which holds two scrollbars and the actual
    plotting canvas (self.canvas). It allows for simple general plotting
    of data with zoom, labels, and automatic axis scaling."""

    def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0, name="plotCanvas"):
        """Constructs a panel, which can be a child of a frame or
        any other non-control window"""

        wx.PyControl.__init__(self, parent, id, pos, size, style,
                              wx.DefaultValidator, name)
        #self.InheritAttributes()
        #self.SetInitialSize(size)
        # wx.Panel.__init__(self, parent, id, pos, size, style, name)

        sizer = wx.FlexGridSizer(2,2,0,0)
        self.canvas = wx.Window(self, -1, size=size)

        self.sb_vert = wx.ScrollBar(self, -1, style=wx.SB_VERTICAL)
        self.sb_vert.SetScrollbar(0,1000,1000,1000)
        self.sb_hor = wx.ScrollBar(self, -1, style=wx.SB_HORIZONTAL)
        self.sb_hor.SetScrollbar(0,1000,1000,1000)

        sizer.Add(self.canvas, 1, wx.EXPAND)
        sizer.Add(self.sb_vert, 0, wx.EXPAND)
        sizer.Add(self.sb_hor, 0, wx.EXPAND)
        sizer.Add((0,0))
        
        sizer.AddGrowableRow(0, 1)
        sizer.AddGrowableCol(0, 1)

        self.sb_vert.Show(False)
        self.sb_hor.Show(False)
        
        self.SetSizer(sizer)

        self.border = (1,1)

        self.SetBackgroundColour("white")
        
        # Create some mouse events for zooming
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnMouseLeftDown)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.OnMouseLeftUp)
        self.canvas.Bind(wx.EVT_MOTION, self.OnMotion)
        self.canvas.Bind(wx.EVT_LEFT_DCLICK, self.OnMouseDoubleClick)
        self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnMouseRightDown)

        # scrollbar events
        self.Bind(wx.EVT_SCROLL_THUMBTRACK, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_PAGEUP, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_PAGEDOWN, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_LINEUP, self.OnScroll)
        self.Bind(wx.EVT_SCROLL_LINEDOWN, self.OnScroll)

        # set curser as cross-hairs
        self.canvas.SetCursor(wx.CROSS_CURSOR)
        # self.HandCursor = wx.CursorFromImage(plot.getHandImage())
        # self.GrabHandCursor = wx.CursorFromImage(plot.getGrabHandImage())
        # self.MagCursor = wx.CursorFromImage(plot.getMagPlusImage())
            
        # Things for printing
        self.print_data = wx.PrintData()
        self.print_data.SetPaperId(wx.PAPER_LETTER)
        self.print_data.SetOrientation(wx.LANDSCAPE)
        self.pageSetupData= wx.PageSetupDialogData()
        self.pageSetupData.SetMarginBottomRight((25,25))
        self.pageSetupData.SetMarginTopLeft((25,25))
        self.pageSetupData.SetPrintData(self.print_data)
        self.printerScale = 1
        self.parent= parent

        # scrollbar variables
        self._sb_ignore = False
        self._adjustingSB = False
        self._sb_xfullrange = 0
        self._sb_yfullrange = 0
        self._sb_xunit = 0
        self._sb_yunit = 0
        
        self._dragEnabled = False
        self._screenCoordinates = _Numeric.array([0.0, 0.0])
        
        self._logscale = (False, False)

        # Zooming variables
        self._zoomInFactor =  0.5
        self._zoomOutFactor = 2
        self._zoomCorner1= _Numeric.array([0.0, 0.0]) # left mouse down corner
        self._zoomCorner2= _Numeric.array([0.0, 0.0])   # left mouse up corner
        self._zoomEnabled= False
        self._hasDragged= False
        
        # Drawing Variables
        self.last_draw = None
        self._pointScale= 1
        self._pointShift= 0
        self._xSpec= 'auto'
        self._ySpec= 'auto'
        self._gridEnabled= False
        self._legendEnabled= False
        
        # Fonts
        self._fontCache = {}
        self._fontSizeAxis= 10
        self._fontSizeTitle= 15
        self._fontSizeLegend= 7

        # pointLabels
        self._pointLabelEnabled= False
        self.last_PointLabel= None
        self._pointLabelFunc= None
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)

        self.canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        self.canvas.Bind(wx.EVT_SIZE, self.OnSize)
        # OnSize called to make sure the buffer is initialized.
        # This might result in OnSize getting called twice on some
        # platforms at initialization, but little harm done.
        self.OnSize(None) # sets the initial size based on client size

        self._gridColour = wx.NamedColour('black')

    def SetCursor(self, cursor):
        self.canvas.SetCursor(cursor)
        
    def GetGridColour(self):
        return self._gridColour

    def SetGridColour(self, colour):
        if isinstance(colour, wx.Colour):
            self._gridColour = colour
        else:
            self._gridColour = wx.NamedColour(colour)

        
    # SaveFile
    def SaveFile(self, fileName= ''):
        """Saves the file to the type specified in the extension. If no file
        name is specified a dialog box is provided.  Returns True if sucessful,
        otherwise False.
        
        .bmp  Save a Windows bitmap file.
        .xbm  Save an X bitmap file.
        .xpm  Save an XPM bitmap file.
        .png  Save a Portable Network Graphics file.
        .jpg  Save a Joint Photographic Experts Group file.
        """
        if _string.lower(fileName[-3:]) not in ['bmp','xbm','xpm','png','jpg']:
            dlg1 = wx.FileDialog(
                    self, 
                    "Choose a file with extension bmp, gif, xbm, xpm, png, or jpg", ".", "",
                    "BMP files (*.bmp)|*.bmp|XBM files (*.xbm)|*.xbm|XPM file (*.xpm)|*.xpm|PNG files (*.png)|*.png|JPG files (*.jpg)|*.jpg",
                    wx.SAVE|wx.OVERWRITE_PROMPT
                    )
            try:
                while 1:
                    if dlg1.ShowModal() == wx.ID_OK:
                        fileName = dlg1.GetPath()
                        # Check for proper exension
                        if _string.lower(fileName[-3:]) not in ['bmp','xbm','xpm','png','jpg']:
                            dlg2 = wx.MessageDialog(self, 'File name extension\n'
                            'must be one of\n'
                            'bmp, xbm, xpm, png, or jpg',
                              'File Name Error', wx.OK | wx.ICON_ERROR)
                            try:
                                dlg2.ShowModal()
                            finally:
                                dlg2.Destroy()
                        else:
                            break # now save file
                    else: # exit without saving
                        return False
            finally:
                dlg1.Destroy()

        # File name has required extension
        fType = _string.lower(fileName[-3:])
        if fType == "bmp":
            tp= wx.BITMAP_TYPE_BMP       # Save a Windows bitmap file.
        elif fType == "xbm":
            tp= wx.BITMAP_TYPE_XBM       # Save an X bitmap file.
        elif fType == "xpm":
            tp= wx.BITMAP_TYPE_XPM       # Save an XPM bitmap file.
        elif fType == "jpg":
            tp= wx.BITMAP_TYPE_JPEG      # Save a JPG file.
        else:
            tp= wx.BITMAP_TYPE_PNG       # Save a PNG file.
        # Save Bitmap
        res= self._Buffer.SaveFile(fileName, tp)
        return res

    def PageSetup(self):
        """Brings up the page setup dialog"""
        data = self.pageSetupData
        data.SetPrintData(self.print_data)
        dlg = wx.PageSetupDialog(self.parent, data)
        try:
            if dlg.ShowModal() == wx.ID_OK:
                data = dlg.GetPageSetupData() # returns wx.PageSetupDialogData
                # updates page parameters from dialog
                self.pageSetupData.SetMarginBottomRight(data.GetMarginBottomRight())
                self.pageSetupData.SetMarginTopLeft(data.GetMarginTopLeft())
                self.pageSetupData.SetPrintData(data.GetPrintData())
                self.print_data=wx.PrintData(data.GetPrintData()) # updates print_data
        finally:
            dlg.Destroy()
                
    def Printout(self, paper=None):
        """Print current plot."""
        if paper != None:
            self.print_data.SetPaperId(paper)
        pdd = wx.PrintDialogData(self.print_data)
        printer = wx.Printer(pdd)
        out = PlotPrintout(self)
        print_ok = printer.Print(self.parent, out)
        if print_ok:
            self.print_data = wx.PrintData(printer.GetPrintDialogData().GetPrintData())
        out.Destroy()

    def PrintPreview(self):
        """Print-preview current plot."""
        printout = PlotPrintout(self)
        printout2 = PlotPrintout(self)
        self.preview = wx.PrintPreview(printout, printout2, self.print_data)
        if not self.preview.Ok():
            wx.MessageDialog(self, "Print Preview failed.\n" \
                               "Check that default printer is configured\n", \
                               "Print error", wx.OK|wx.CENTRE).ShowModal()
        self.preview.SetZoom(40)
        # search up tree to find frame instance
        frameInst= self
        while not isinstance(frameInst, wx.Frame):
            frameInst= frameInst.GetParent()
        frame = wx.PreviewFrame(self.preview, frameInst, "Preview")
        frame.Initialize()
        frame.SetPosition(self.GetPosition())
        frame.SetSize((600,550))
        frame.Centre(wx.BOTH)
        frame.Show(True)

    def setLogScale(self, logscale):
        if type(logscale) != tuple:
            raise TypeError, 'logscale must be a tuple of bools, e.g. (False, False)'
        if self.last_draw is not None:
            graphics, xAxis, yAxis= self.last_draw
            graphics.setLogScale(logscale)
            self.last_draw = (graphics, None, None)
        self.SetXSpec('min')
        self.SetYSpec('min')
        self._logscale = logscale

    def getLogScale(self):
        return self._logscale
    
    def SetFontSizeAxis(self, point= 10):
        """Set the tick and axis label font size (default is 10 point)"""
        self._fontSizeAxis= point
        
    def GetFontSizeAxis(self):
        """Get current tick and axis label font size in points"""
        return self._fontSizeAxis
    
    def SetFontSizeTitle(self, point= 15):
        """Set Title font size (default is 15 point)"""
        self._fontSizeTitle= point

    def GetFontSizeTitle(self):
        """Get current Title font size in points"""
        return self._fontSizeTitle
    
    def SetFontSizeLegend(self, point= 7):
        """Set Legend font size (default is 7 point)"""
        self._fontSizeLegend= point
        
    def GetFontSizeLegend(self):
        """Get current Legend font size in points"""
        return self._fontSizeLegend

    def SetShowScrollbars(self, value):
        """Set True to show scrollbars"""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        if value == self.GetShowScrollbars():
            return
        self.sb_vert.Show(value)
        self.sb_hor.Show(value)
        wx.CallAfter(self.Layout)

    def GetShowScrollbars(self):
        """Set True to show scrollbars"""
        return self.sb_vert.IsShown()

    def SetEnableDrag(self, value):
        """Set True to enable drag."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        if value:
            if self.GetEnableZoom():
                self.SetEnableZoom(False)
            self.SetCursor(self.HandCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._dragEnabled = value
    
    def GetEnableDrag(self):
        return self._dragEnabled
    
    def SetEnableZoom(self, value):
        """Set True to enable zooming."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        if value:
            if self.GetEnableDrag():
                self.SetEnableDrag(False)
            self.SetCursor(self.MagCursor)
        else:
            self.SetCursor(wx.CROSS_CURSOR)
        self._zoomEnabled= value

    def GetEnableZoom(self):
        """True if zooming enabled."""
        return self._zoomEnabled

    def SetEnableGrid(self, value):
        """Set True to enable grid."""
        if value not in [True,False,'Horizontal','Vertical']:
            raise TypeError, "Value should be True, False, Horizontal or Vertical"
        self._gridEnabled= value
        self.Redraw()

    def GetEnableGrid(self):
        """True if grid enabled."""
        return self._gridEnabled

    def SetEnableLegend(self, value):
        """Set True to enable legend."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        self._legendEnabled= value 
        self.Redraw()

    def GetEnableLegend(self):
        """True if Legend enabled."""
        return self._legendEnabled

    def SetEnablePointLabel(self, value):
        """Set True to enable pointLabel."""
        if value not in [True,False]:
            raise TypeError, "Value should be True or False"
        self._pointLabelEnabled= value 
        self.Redraw()  #will erase existing pointLabel if present
        self.last_PointLabel = None

    def GetEnablePointLabel(self):
        """True if pointLabel enabled."""
        return self._pointLabelEnabled

    def SetPointLabelFunc(self, func):
        """Sets the function with custom code for pointLabel drawing
            ******** more info needed ***************
        """
        self._pointLabelFunc= func

    def GetPointLabelFunc(self):
        """Returns pointLabel Drawing Function"""
        return self._pointLabelFunc

    def Reset(self):
        """Unzoom the plot."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None:
            self._Draw(self.last_draw[0])
        
    def ScrollRight(self, units):          
        """Move view right number of axis units."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None:
            graphics, xAxis, yAxis= self.last_draw
            xAxis= (xAxis[0]+units, xAxis[1]+units)
            self._Draw(graphics,xAxis,yAxis)

    def ScrollUp(self, units):
        """Move view up number of axis units."""
        self.last_PointLabel = None        #reset pointLabel
        if self.last_draw is not None:
             graphics, xAxis, yAxis= self.last_draw
             yAxis= (yAxis[0]+units, yAxis[1]+units)
             self._Draw(graphics,xAxis,yAxis)

    def GetXY(self, event):
        """Wrapper around _getXY, which handles log scales"""
        x,y = self._getXY(event)
        if self.getLogScale()[0]:
            x = _Numeric.power(10,x)
        if self.getLogScale()[1]:
            y = _Numeric.power(10,y)
        return x,y
        
    def _getXY(self,event):
        """Takes a mouse event and returns the XY user axis values."""
        x,y= self.PositionScreenToUser(event.GetPosition())
        return x,y

    def PositionUserToScreen(self, pntXY):
        """Converts User position to Screen Coordinates"""
        userPos= _Numeric.array(pntXY)
        x,y= userPos * self._pointScale + self._pointShift
        return x,y
        
    def PositionScreenToUser(self, pntXY):
        """Converts Screen position to User Coordinates"""
        screenPos= _Numeric.array(pntXY)
        x,y= (screenPos-self._pointShift)/self._pointScale
        return x,y
        
    def SetXSpec(self, type= 'auto'):
        """xSpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:
            'none' - shows no axis or tick mark values
            'min' - shows min bounding box values
            'auto' - rounds axis range to sensible values
        """
        self._xSpec= type
        
    def SetYSpec(self, type= 'auto'):
        """ySpec- defines x axis type. Can be 'none', 'min' or 'auto'
        where:
            'none' - shows no axis or tick mark values
            'min' - shows min bounding box values
            'auto' - rounds axis range to sensible values
        """
        self._ySpec= type

    def GetXSpec(self):
        """Returns current XSpec for axis"""
        return self._xSpec
    
    def GetYSpec(self):
        """Returns current YSpec for axis"""
        return self._ySpec
    
    def GetXMaxRange(self):
        xAxis = self._getXMaxRange()
        if self.getLogScale()[0]:
            xAxis = _Numeric.power(10,xAxis)
        return xAxis

    def _getXMaxRange(self):
        """Returns (minX, maxX) x-axis range for displayed graph"""
        graphics= self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        xAxis = self._axisInterval(self._xSpec, p1[0], p2[0]) # in user units
        return xAxis

    def GetYMaxRange(self):
        yAxis = self._getYMaxRange()
        if self.getLogScale()[1]:
            yAxis = _Numeric.power(10,yAxis)
        return yAxis

    def _getYMaxRange(self):
        """Returns (minY, maxY) y-axis range for displayed graph"""
        graphics= self.last_draw[0]
        p1, p2 = graphics.boundingBox()     # min, max points of graphics
        yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
        return yAxis

    def GetXCurrentRange(self):
        xAxis = self._getXCurrentRange()
        if self.getLogScale()[0]:
            xAxis = _Numeric.power(10,xAxis)
        return xAxis

    def _getXCurrentRange(self):
        """Returns (minX, maxX) x-axis for currently displayed portion of graph"""
        return self.last_draw[1]
    
    def GetYCurrentRange(self):
        yAxis = self._getYCurrentRange()
        if self.getLogScale()[1]:
            yAxis = _Numeric.power(10,yAxis)
        return yAxis

    def _getYCurrentRange(self):
        """Returns (minY, maxY) y-axis for currently displayed portion of graph"""
        return self.last_draw[2]

    def Draw(self, graphics, xAxis = None, yAxis = None, dc = None):
        """Wrapper around _Draw, which handles log axes"""
        
        graphics.setLogScale(self.getLogScale())
        
        # check Axis is either tuple or none
        if type(xAxis) not in [type(None),tuple]:
            raise TypeError, "xAxis should be None or (minX,maxX)"+str(type(xAxis))
        if type(yAxis) not in [type(None),tuple]:
            raise TypeError, "yAxis should be None or (minY,maxY)"+str(type(xAxis))
             
        # check case for axis = (a,b) where a==b caused by improper zooms
        if xAxis != None:
            if xAxis[0] == xAxis[1]:
                return
            if self.getLogScale()[0]:
                xAxis = _Numeric.log10(xAxis)
        if yAxis != None:
            if yAxis[0] == yAxis[1]:
                return
            if self.getLogScale()[1]:
                yAxis = _Numeric.log10(yAxis)
        self._Draw(graphics, xAxis, yAxis, dc)
        
    def _Draw(self, graphics, xAxis = None, yAxis = None, dc = None):
        """\
        Draw objects in graphics with specified x and y axis.
        graphics- instance of PlotGraphics with list of PolyXXX objects
        xAxis - tuple with (min, max) axis range to view
        yAxis - same as xAxis
        dc - drawing context - doesn't have to be specified.    
        If it's not, the offscreen buffer is used
        """

        if dc == None:
            # sets new dc and clears it 
            dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
            dc.Clear()
        
        dc.Clear()        
        dc.BeginDrawing()
        
        # set font size for every thing but title and legend
        dc.SetFont(self._getFont(self._fontSizeAxis))

        # sizes axis to axis type, create lower left and upper right corners of plot
        if xAxis == None or yAxis == None:
            # One or both axis not specified in Draw
            p1, p2 = graphics.boundingBox()     # min, max points of graphics
            if xAxis == None:
                xAxis = self._axisInterval(self._xSpec, p1[0], p2[0]) # in user units
            if yAxis == None:
                yAxis = self._axisInterval(self._ySpec, p1[1], p2[1])
            # Adjust bounding box for axis spec
            p1[0],p1[1] = xAxis[0], yAxis[0]     # lower left corner user scale (xmin,ymin)
            p2[0],p2[1] = xAxis[1], yAxis[1]     # upper right corner user scale (xmax,ymax)
        else:
            # Both axis specified in Draw
            p1= _Numeric.array([xAxis[0], yAxis[0]])    # lower left corner user scale (xmin,ymin)
            p2= _Numeric.array([xAxis[1], yAxis[1]])     # upper right corner user scale (xmax,ymax)

        self.last_draw = (graphics, _Numeric.array(xAxis), _Numeric.array(yAxis))       # saves most recient values

        # Get ticks and textExtents for axis if required
        if self._xSpec is not 'none':        
            xticks = self._xticks(xAxis[0], xAxis[1])
            xTextExtent = dc.GetTextExtent(xticks[-1][1])# w h of x axis text last number on axis
        else:
            xticks = None
            xTextExtent= (0,0) # No text for ticks
        if self._ySpec is not 'none':
            yticks = self._yticks(yAxis[0], yAxis[1])
            if self.getLogScale()[1]:
                yTextExtent = dc.GetTextExtent('-2e-2')
            else:
                yTextExtentBottom = dc.GetTextExtent(yticks[0][1])
                yTextExtentTop = dc.GetTextExtent(yticks[-1][1])
                yTextExtent= (max(yTextExtentBottom[0],yTextExtentTop[0]),
                              max(yTextExtentBottom[1],yTextExtentTop[1]))
        else:
            yticks = None
            yTextExtent= (0,0) # No text for ticks

        # TextExtents for Title and Axis Labels
        titleWH, xLabelWH, yLabelWH= self._titleLablesWH(dc, graphics)

        # TextExtents for Legend
        legendBoxWH, legendSymExt, legendTextExt = self._legendWH(dc, graphics)

        # room around graph area
        rhsW= max(xTextExtent[0], legendBoxWH[0]) # use larger of number width or legend width
        lhsW= yTextExtent[0]+ yLabelWH[1]
        bottomH= max(xTextExtent[1], yTextExtent[1]/2.)+ xLabelWH[1]
        topH= yTextExtent[1]/2. + titleWH[1]
        textSize_scale= _Numeric.array([rhsW+lhsW,bottomH+topH]) # make plot area smaller by text size
        textSize_shift= _Numeric.array([lhsW, bottomH])          # shift plot area by this amount

        # drawing title and labels text
        dc.SetFont(self._getFont(self._fontSizeTitle))
        titlePos= (self.plotbox_origin[0]+ lhsW + (self.plotbox_size[0]-lhsW-rhsW)/2.- titleWH[0]/2.,
                 self.plotbox_origin[1]- self.plotbox_size[1])
        dc.DrawText(graphics.getTitle(),titlePos[0],titlePos[1])
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabelPos= (self.plotbox_origin[0]+ lhsW + (self.plotbox_size[0]-lhsW-rhsW)/2.- xLabelWH[0]/2.,
                 self.plotbox_origin[1]- xLabelWH[1])
        dc.DrawText(graphics.getXLabel(),xLabelPos[0],xLabelPos[1])
        yLabelPos= (self.plotbox_origin[0],
                 self.plotbox_origin[1]- bottomH- (self.plotbox_size[1]-bottomH-topH)/2.+ yLabelWH[0]/2.)
        if graphics.getYLabel():  # bug fix for Linux
            dc.DrawRotatedText(graphics.getYLabel(),yLabelPos[0],yLabelPos[1],90)

        # drawing legend makers and text
        if self._legendEnabled:
            self._drawLegend(dc,graphics,rhsW,topH,legendBoxWH, legendSymExt, legendTextExt)

        # allow for scaling and shifting plotted points
        
        scale = (self.plotbox_size-textSize_scale) / (p2-p1)* _Numeric.array((1,-1))
        shift = -p1*scale + self.plotbox_origin + textSize_shift * _Numeric.array((1,-1))
        self._pointScale= scale  # make available for mouse events
        self._pointShift= shift        
        self._drawAxes(dc, p1, p2, scale, shift, xticks, yticks)
        
        graphics.scaleAndShift(scale, shift)
        graphics.setPrinterScale(self.printerScale)  # thicken up lines and markers if printing
        
        # set clipping area so drawing does not occur outside axis box
        ptx,pty,rectWidth,rectHeight= self._point2ClientCoord(p1, p2)
        dc.SetClippingRegion(ptx,pty,rectWidth,rectHeight)
        # Draw the lines and markers
        #start = _time.clock()
        graphics.draw(dc)
        # print "entire graphics drawing took: %f second"%(_time.clock() - start)
        # remove the clipping region
        dc.DestroyClippingRegion()
        dc.EndDrawing()

        self._adjustScrollbars()
        
    def Redraw(self, dc=None):
        """Redraw the existing plot."""
        if self.last_draw is not None:
            graphics, xAxis, yAxis= self.last_draw
            self._Draw(graphics,xAxis,yAxis,dc)

    def Clear(self):
        """Erase the window."""
        self.last_PointLabel = None        #reset pointLabel
        dc = wx.BufferedDC(wx.ClientDC(self.canvas), self._Buffer)
        dc.Clear()
        self.last_draw = None

    def Zoom(self, Center, Ratio):
        """ Zoom on the plot
            Centers on the X,Y coords given in Center
            Zooms by the Ratio = (Xratio, Yratio) given
        """
        self.last_PointLabel = None   #reset maker
        x,y = Center
        if self.last_draw != None:
            (graphics, xAxis, yAxis) = self.last_draw
            w = (xAxis[1] - xAxis[0]) * Ratio[0]
            h = (yAxis[1] - yAxis[0]) * Ratio[1]
            xAxis = ( x - w/2, x + w/2 )
            yAxis = ( y - h/2, y + h/2 )
            self._Draw(graphics, xAxis, yAxis)
        
    def GetClosestPoints(self, pntXY, pointScaled= True):
        """Returns list with
            [curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            list for each curve.
            Returns [] if no curves are being plotted.
            
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        if self.last_draw == None:
            #no graph available
            return []
        graphics, xAxis, yAxis= self.last_draw
        l = []
        for curveNum,obj in enumerate(graphics):
            #check there are points in the curve
            if len(obj.points) == 0:
                continue  #go to next obj
            #[curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            cn = [curveNum]+ [obj.getLegend()]+ obj.getClosestPoint( pntXY, pointScaled)
            l.append(cn)
        return l

    def GetClosetPoint(self, pntXY, pointScaled= True):
        """Returns list with
            [curveNumber, legend, index of closest point, pointXY, scaledXY, distance]
            list for only the closest curve.
            Returns [] if no curves are being plotted.
            
            x, y in user coords
            if pointScaled == True based on screen coords
            if pointScaled == False based on user coords
        """
        #closest points on screen based on screen scaling (pointScaled= True)
        #list [curveNumber, index, pointXY, scaledXY, distance] for each curve
        closestPts= self.GetClosestPoints(pntXY, pointScaled)
        if closestPts == []:
            return []  #no graph present
        #find one with least distance
        dists = [c[-1] for c in closestPts]
        mdist = min(dists)  #Min dist
        i = dists.index(mdist)  #index for min dist
        return closestPts[i]  #this is the closest point on closest curve

    def UpdatePointLabel(self, mDataDict):
        """Updates the pointLabel point on screen with data contained in
            mDataDict.

            mDataDict will be passed to your function set by
            SetPointLabelFunc.  It can contain anything you
            want to display on the screen at the scaledXY point
            you specify.

            This function can be called from parent window with onClick,
            onMotion events etc.            
        """
        if self.last_PointLabel != None:
            #compare pointXY
            if _Numeric.sometrue(mDataDict["pointXY"] != self.last_PointLabel["pointXY"]):
                #closest changed
                self._drawPointLabel(self.last_PointLabel) #erase old
                self._drawPointLabel(mDataDict) #plot new
        else:
            #just plot new with no erase
            self._drawPointLabel(mDataDict) #plot new
        #save for next erase
        self.last_PointLabel = mDataDict

    # event handlers **********************************
    def OnMotion(self, event):
        if self._zoomEnabled and event.LeftIsDown():
            if self._hasDragged:
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
            else:
                self._hasDragged= True
            self._zoomCorner2[0], self._zoomCorner2[1] = self._getXY(event)
            self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # add new
        elif self._dragEnabled and event.LeftIsDown():
            coordinates = event.GetPosition()
            newpos, oldpos = map(_Numeric.array, map(self.PositionScreenToUser, [coordinates, self._screenCoordinates]))
            dist = newpos-oldpos
            self._screenCoordinates = coordinates

            if self.last_draw is not None:
                graphics, xAxis, yAxis= self.last_draw
                yAxis -= dist[1]
                xAxis -= dist[0]
                self._Draw(graphics,xAxis,yAxis)
            
    def OnMouseLeftDown(self,event):
        self._zoomCorner1[0], self._zoomCorner1[1]= self._getXY(event)
        self._screenCoordinates = _Numeric.array(event.GetPosition())
        if self._dragEnabled:
            self.SetCursor(self.GrabHandCursor)
            self.canvas.CaptureMouse()

    def OnMouseLeftUp(self, event):
        if self._zoomEnabled:
            if self._hasDragged == True:
                self._drawRubberBand(self._zoomCorner1, self._zoomCorner2) # remove old
                self._zoomCorner2[0], self._zoomCorner2[1]= self._getXY(event)
                self._hasDragged = False  # reset flag
                minX, minY= _Numeric.minimum( self._zoomCorner1, self._zoomCorner2)
                maxX, maxY= _Numeric.maximum( self._zoomCorner1, self._zoomCorner2)
                self.last_PointLabel = None        #reset pointLabel
                if self.last_draw != None:
                    self._Draw(self.last_draw[0], xAxis = (minX,maxX), yAxis = (minY,maxY), dc = None)
            #else: # A box has not been drawn, zoom in on a point
            ## this interfered with the double click, so I've disables it.
            #    X,Y = self._getXY(event)
            #    self.Zoom( (X,Y), (self._zoomInFactor,self._zoomInFactor) )
        if self._dragEnabled:
            self.SetCursor(self.HandCursor)
            if self.canvas.HasCapture():
                self.canvas.ReleaseMouse()

    def OnMouseDoubleClick(self,event):
        if self._zoomEnabled:
            # Give a little time for the click to be totally finished
            # before (possibly) removing the scrollbars and trigering
            # size events, etc.
            wx.FutureCall(200,self.Reset)
        
    def OnMouseRightDown(self,event):
        if self._zoomEnabled:
            X,Y = self._getXY(event)
            self.Zoom( (X,Y), (self._zoomOutFactor, self._zoomOutFactor) )

    def OnPaint(self, event):
        # All that is needed here is to draw the buffer to screen
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel) #erase old
            self.last_PointLabel = None
        dc = wx.BufferedPaintDC(self.canvas, self._Buffer)

    def PrintSize(self):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = wx.Size(550,300)
        
        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._PrintBuffer = wx.EmptyBitmap(Size.width, Size.height)
        self._setSize(Size.width,Size.height)

        self.last_PointLabel = None        #reset pointLabel

        if self.last_draw is None:
            self.Clear()
        else:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics,xSpec,ySpec, wx.MemoryDC(self._PrintBuffer))    
            
    
    def OnSize(self,event):
        # The Buffer init is done here, to make sure the buffer is always
        # the same size as the Window
        Size  = self.canvas.GetClientSize()
        Size.width = max(1, Size.width)
        Size.height = max(1, Size.height)
        
        # Make new offscreen bitmap: this bitmap will always have the
        # current drawing in it, so it can be used to save the image to
        # a file, or whatever.
        self._Buffer = wx.EmptyBitmap(Size.width, Size.height)
        self._setSize()

        self.last_PointLabel = None        #reset pointLabel

        if self.last_draw is None:
            self.Clear()
        else:
            graphics, xSpec, ySpec = self.last_draw
            self._Draw(graphics,xSpec,ySpec)

    def OnLeave(self, event):
        """Used to erase pointLabel when mouse outside window"""
        if self.last_PointLabel != None:
            self._drawPointLabel(self.last_PointLabel) #erase old
            self.last_PointLabel = None

    def OnScroll(self, evt):
        if not self._adjustingSB:
            self._sb_ignore = True
            sbpos = evt.GetPosition()
        
            if evt.GetOrientation() == wx.VERTICAL:
                fullrange,pagesize = self.sb_vert.GetRange(),self.sb_vert.GetPageSize()
                sbpos = fullrange-pagesize-sbpos
                dist = sbpos*self._sb_yunit-(self._getYCurrentRange()[0]-self._sb_yfullrange[0])
                self.ScrollUp(dist)
            
            if evt.GetOrientation() == wx.HORIZONTAL:
                dist = sbpos*self._sb_xunit-(self._getXCurrentRange()[0]-self._sb_xfullrange[0])
                self.ScrollRight(dist)
               
    # Private Methods **************************************************
    def _setSize(self, width=None, height=None):
        """DC width and height."""
        if width == None:
            (self.width,self.height) = self.canvas.GetClientSize()
        else:
            self.width, self.height= width,height    
        self.plotbox_size = 0.97*_Numeric.array([self.width, self.height])
        xo = 0.5*(self.width-self.plotbox_size[0])
        yo = self.height-0.5*(self.height-self.plotbox_size[1])
        self.plotbox_origin = _Numeric.array([xo, yo])
    
    def _setPrinterScale(self, scale):
        """Used to thicken lines and increase marker size for print out."""
        # line thickness on printer is very thin at 600 dot/in. Markers small
        self.printerScale= scale
     
    def _printDraw(self, printDC):
        """Used for printing."""
        if self.last_draw != None:
            graphics, xSpec, ySpec= self.last_draw
            self._Draw(graphics,xSpec,ySpec,printDC)

    def _drawPointLabel(self, mDataDict):
        """Draws and erases pointLabels"""
        width = self._Buffer.GetWidth()
        height = self._Buffer.GetHeight()
        tmp_Buffer = wx.EmptyBitmap(width,height)
        dcs = wx.MemoryDC()
        dcs.SelectObject(tmp_Buffer)
        dcs.Clear()
        dcs.BeginDrawing()
        self._pointLabelFunc(dcs,mDataDict)  #custom user pointLabel function
        dcs.EndDrawing()

        dc = wx.ClientDC( self.canvas )
        #this will erase if called twice
        dc.Blit(0, 0, width, height, dcs, 0, 0, wx.EQUIV)  #(NOT src) XOR dst
        

    def _drawLegend(self,dc,graphics,rhsW,topH,legendBoxWH, legendSymExt, legendTextExt):
        """Draws legend symbols and text"""
        # top right hand corner of graph box is ref corner
        trhc= self.plotbox_origin+ (self.plotbox_size-[rhsW,topH])*[1,-1]
        legendLHS= .091* legendBoxWH[0]  # border space between legend sym and graph box
        lineHeight= max(legendSymExt[1], legendTextExt[1]) * 1.1 #1.1 used as space between lines
        dc.SetFont(self._getFont(self._fontSizeLegend))
        for i in range(len(graphics)):
            o = graphics[i]
            s= i*lineHeight
            if isinstance(o,PolyMarker):
                # draw marker with legend
                pnt= (trhc[0]+legendLHS+legendSymExt[0]/2., trhc[1]+s+lineHeight/2.)
                o.draw(dc, self.printerScale, coord= _Numeric.array([pnt]))
            elif isinstance(o,PolyLine):
                # draw line with legend
                pnt1= (trhc[0]+legendLHS, trhc[1]+s+lineHeight/2.)
                pnt2= (trhc[0]+legendLHS+legendSymExt[0], trhc[1]+s+lineHeight/2.)
                o.draw(dc, self.printerScale, coord= _Numeric.array([pnt1,pnt2]))
            else:
                raise TypeError, "object is neither PolyMarker or PolyLine instance"
            # draw legend txt
            pnt= (trhc[0]+legendLHS+legendSymExt[0], trhc[1]+s+lineHeight/2.-legendTextExt[1]/2)
            dc.DrawText(o.getLegend(),pnt[0],pnt[1])
        dc.SetFont(self._getFont(self._fontSizeAxis)) # reset

    def _titleLablesWH(self, dc, graphics):
        """Draws Title and labels and returns width and height for each"""
        # TextExtents for Title and Axis Labels
        dc.SetFont(self._getFont(self._fontSizeTitle))
        title= graphics.getTitle()
        titleWH= dc.GetTextExtent(title)
        dc.SetFont(self._getFont(self._fontSizeAxis))
        xLabel, yLabel= graphics.getXLabel(),graphics.getYLabel()
        xLabelWH= dc.GetTextExtent(xLabel)
        yLabelWH= dc.GetTextExtent(yLabel)
        return titleWH, xLabelWH, yLabelWH
    
    def _legendWH(self, dc, graphics):
        """Returns the size in screen units for legend box"""
        if self._legendEnabled != True:
            legendBoxWH= symExt= txtExt= (0,0)
        else:
            # find max symbol size
            symExt= graphics.getSymExtent(self.printerScale)
            # find max legend text extent
            dc.SetFont(self._getFont(self._fontSizeLegend))
            txtList= graphics.getLegendNames()
            txtExt= dc.GetTextExtent(txtList[0])
            for txt in graphics.getLegendNames()[1:]:
                txtExt= _Numeric.maximum(txtExt,dc.GetTextExtent(txt))
            maxW= symExt[0]+txtExt[0]    
            maxH= max(symExt[1],txtExt[1])
            # padding .1 for lhs of legend box and space between lines
            maxW= maxW* 1.1
            maxH= maxH* 1.1 * len(txtList)
            dc.SetFont(self._getFont(self._fontSizeAxis))
            legendBoxWH= (maxW,maxH)
        return (legendBoxWH, symExt, txtExt)

    def _drawRubberBand(self, corner1, corner2):
        """Draws/erases rect box from corner1 to corner2"""
        ptx,pty,rectWidth,rectHeight= self._point2ClientCoord(corner1, corner2)
        # draw rectangle
        dc = wx.ClientDC( self.canvas )
        dc.BeginDrawing()                 
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.SetBrush(wx.Brush( wx.WHITE, wx.TRANSPARENT ) )
        dc.SetLogicalFunction(wx.INVERT)
        dc.DrawRectangle( ptx,pty, rectWidth,rectHeight)
        dc.SetLogicalFunction(wx.COPY)
        dc.EndDrawing()

    def _getFont(self,size):
        """Take font size, adjusts if printing and returns wx.Font"""
        s = size*self.printerScale
        of = self.GetFont()
        # Linux speed up to get font from cache rather than X font server
        key = (int(s), of.GetFamily (), of.GetStyle (), of.GetWeight ())
        font = self._fontCache.get (key, None)
        if font:
            return font                 # yeah! cache hit
        else:
            font =  wx.Font(int(s), of.GetFamily(), of.GetStyle(), of.GetWeight())
            self._fontCache[key] = font
            return font


    def _point2ClientCoord(self, corner1, corner2):
        """Converts user point coords to client screen int coords x,y,width,height"""
        c1= _Numeric.array(corner1)
        c2= _Numeric.array(corner2)
        # convert to screen coords
        pt1= c1*self._pointScale+self._pointShift
        pt2= c2*self._pointScale+self._pointShift
        # make height and width positive
        pul= _Numeric.minimum(pt1,pt2) # Upper left corner
        plr= _Numeric.maximum(pt1,pt2) # Lower right corner
        rectWidth, rectHeight= plr-pul
        ptx,pty= pul
        return ptx, pty, rectWidth, rectHeight 
    
    def _axisInterval(self, spec, lower, upper):
        """Returns sensible axis range for given spec"""
        if spec == 'none' or spec == 'min':
            if lower == upper:
                return lower-0.5, upper+0.5
            else:
                return lower, upper
        elif spec == 'auto':
            range = upper-lower
            if range == 0.:
                return lower-0.5, upper+0.5
            log = _Numeric.log10(range)
            power = _Numeric.floor(log)
            fraction = log-power
            if fraction <= 0.05:
                power = power-1
            grid = 10.**power
            lower = lower - lower % grid
            mod = upper % grid
            if mod != 0:
                upper = upper - mod + grid
            return lower, upper
        elif type(spec) == type(()):
            lower, upper = spec
            if lower <= upper:
                return lower, upper
            else:
                return upper, lower
        else:
            raise ValueError, str(spec) + ': illegal axis specification'

    def _drawAxes(self, dc, p1, p2, scale, shift, xticks, yticks):
        
        penWidth= self.printerScale        # increases thickness for printing only
        dc.SetPen(wx.Pen(self._gridColour, penWidth))
        
        # set length of tick marks--long ones make grid
        if self._gridEnabled:
            x,y,width,height= self._point2ClientCoord(p1,p2)
            if self._gridEnabled == 'Horizontal':
                yTickLength= width/2.0 +1
                xTickLength= 3 * self.printerScale
            elif self._gridEnabled == 'Vertical':
                yTickLength= 3 * self.printerScale
                xTickLength= height/2.0 +1
            else:
                yTickLength= width/2.0 +1
                xTickLength= height/2.0 +1
        else:
            yTickLength= 3 * self.printerScale  # lengthens lines for printing
            xTickLength= 3 * self.printerScale
        
        if self._xSpec is not 'none':
            lower, upper = p1[0],p2[0]
            text = 1
            for y, d in [(p1[1], -xTickLength), (p2[1], xTickLength)]:   # miny, maxy and tick lengths
                a1 = scale*_Numeric.array([lower, y])+shift
                a2 = scale*_Numeric.array([upper, y])+shift
                dc.DrawLine(a1[0],a1[1],a2[0],a2[1])  # draws upper and lower axis line
                for x, label in xticks:
                    pt = scale*_Numeric.array([x, y])+shift
                    dc.DrawLine(pt[0],pt[1],pt[0],pt[1] + d) # draws tick mark d units
                    if text:
                        dc.DrawText(label,pt[0],pt[1])
                text = 0  # axis values not drawn on top side

        if self._ySpec is not 'none':
            lower, upper = p1[1],p2[1]
            text = 1
            h = dc.GetCharHeight()
            for x, d in [(p1[0], -yTickLength), (p2[0], yTickLength)]:
                a1 = scale*_Numeric.array([x, lower])+shift
                a2 = scale*_Numeric.array([x, upper])+shift
                dc.DrawLine(a1[0],a1[1],a2[0],a2[1])
                for y, label in yticks:
                    pt = scale*_Numeric.array([x, y])+shift
                    dc.DrawLine(pt[0],pt[1],pt[0]-d,pt[1])
                    if text:
                        dc.DrawText(label,pt[0]-dc.GetTextExtent(label)[0],
                                    pt[1]-0.5*h)
                text = 0    # axis values not drawn on right side

    def _xticks(self, *args):
        if self._logscale[0]:
            return self._logticks(*args)
        else:
            return self._ticks(*args)
    
    def _yticks(self, *args):
        if self._logscale[1]:
            return self._logticks(*args)
        else:
            return self._ticks(*args)
        
    def _logticks(self, lower, upper):
        #lower,upper = map(_Numeric.log10,[lower,upper])
        #print 'logticks',lower,upper
        ticks = []
        mag = _Numeric.power(10,_Numeric.floor(lower))
        if upper-lower > 6:
            t = _Numeric.power(10,_Numeric.ceil(lower))
            base = _Numeric.power(10,_Numeric.floor((upper-lower)/6))
            def inc(t):
                return t*base-t
        else:
            t = _Numeric.ceil(_Numeric.power(10,lower)/mag)*mag
            def inc(t):
                return 10**int(_Numeric.floor(_Numeric.log10(t)+1e-16))
        majortick = int(_Numeric.log10(mag))
        while t <= pow(10,upper):
            if majortick != int(_Numeric.floor(_Numeric.log10(t)+1e-16)):
                majortick = int(_Numeric.floor(_Numeric.log10(t)+1e-16))
                ticklabel = '1e%d'%majortick
            else:
                if upper-lower < 2:
                    minortick = int(t/pow(10,majortick)+.5)
                    ticklabel = '%de%d'%(minortick,majortick)
                else:
                    ticklabel = ''
            ticks.append((_Numeric.log10(t), ticklabel))
            t += inc(t)
        if len(ticks) == 0:
            ticks = [(0,'')]
        return ticks
    
    def _ticks(self, lower, upper):
        ideal = (upper-lower)/7.
        log = _Numeric.log10(ideal)
        power = _Numeric.floor(log)
        fraction = log-power
        factor = 1.
        error = fraction
        for f, lf in self._multiples:
            e = _Numeric.fabs(fraction-lf)
            if e < error:
                error = e
                factor = f
        grid = factor * 10.**power
        if power > 4 or power < -4:
            format = '%+7.1e'        
        elif power >= 0:
            digits = max(1, int(power))
            format = '%' + `digits`+'.0f'
        else:
            digits = -int(power)
            format = '%'+`digits+2`+'.'+`digits`+'f'
        ticks = []
        t = -grid*_Numeric.floor(-lower/grid)
        while t <= upper:
            ticks.append( (t, format % (t,)) )
            t = t + grid
        return ticks

    _multiples = [(2., _Numeric.log10(2.)), (5., _Numeric.log10(5.))]


    def _adjustScrollbars(self):
        if self._sb_ignore:
            self._sb_ignore = False
            return

        self._adjustingSB = True
        needScrollbars = False
        
        # horizontal scrollbar
        r_current = self._getXCurrentRange()
        r_max = list(self._getXMaxRange())
        sbfullrange = float(self.sb_hor.GetRange())

        r_max[0] = min(r_max[0],r_current[0])
        r_max[1] = max(r_max[1],r_current[1])
            
        self._sb_xfullrange = r_max

        unit = (r_max[1]-r_max[0])/float(self.sb_hor.GetRange())
        pos = int((r_current[0]-r_max[0])/unit)
        
        if pos >= 0:
            pagesize = int((r_current[1]-r_current[0])/unit)

            self.sb_hor.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
            self._sb_xunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_hor.SetScrollbar(0, 1000, 1000, 1000)

        # vertical scrollbar
        r_current = self._getYCurrentRange()
        r_max = list(self._getYMaxRange())
        sbfullrange = float(self.sb_vert.GetRange())

        r_max[0] = min(r_max[0],r_current[0])
        r_max[1] = max(r_max[1],r_current[1])
            
        self._sb_yfullrange = r_max
        
        unit = (r_max[1]-r_max[0])/sbfullrange
        pos = int((r_current[0]-r_max[0])/unit)
        
        if pos >= 0:
            pagesize = int((r_current[1]-r_current[0])/unit)
            pos = (sbfullrange-1-pos-pagesize)
            self.sb_vert.SetScrollbar(pos, pagesize, sbfullrange, pagesize)
            self._sb_yunit = unit
            needScrollbars = needScrollbars or (pagesize != sbfullrange)
        else:
            self.sb_vert.SetScrollbar(0, 1000, 1000, 1000)

        self.SetShowScrollbars(needScrollbars)
        self._adjustingSB = False