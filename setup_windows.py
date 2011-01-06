#!/usr/bin/env python
from distutils.core import setup
from glob import glob
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "1.1"
        self.company_name = "ACe Design"
        self.copyright = "GPL"
        self.name = "PeakTime Standard Deviation Utility"

manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="PeakTime Standard Deviation Utility"
    type="win32"
/>
'''

PeakTimeStdDev = Target(
    description = "PeakTime Standard Deviation Utility",
    # what to build
    script = "PeakTimeStdDev.py",
    #other_resources = [(24, 1, manifest % dict(prog="PeakTimeStdDev"))],
    icon_resources = [(1, "img/heart.ico")],
    dest_base = "PeakTimeStdDev")

setup(name='PeakTimeStdDev',
	version="2.0",
	description="PeakTime Standard Deviation Utility",
	py_modules = ['PeakTimeStdDev'],
	license="GPL",
	options = {"py2exe" : {
						"bundle_files": 2,
						"packages": "encodings",
						"compressed": 1,
						"optimize": 2,
						"excludes": ["Tkconstants","Tkinter","tcl"],
						"dll_excludes": ["w9xpopen.exe"],
						"ascii": True
					}
			},
	data_files= [("img",glob("img/*")), ("", glob(r'Microsoft.VC90.CRT\*.*'))],
	windows = [PeakTimeStdDev],
	zipfile = None
)