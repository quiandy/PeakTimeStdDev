#!/usr/bin/env python
from distutils.core import setup
from glob import glob
import py2exe

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.2"
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

<description>SNooMPy</description>
<dependency>
	<dependentAssembly>
		<assemblyIdentity 
            type="win32" 
            name="Microsoft.VC90.CRT" 
            version="9.0.30729.4918" 
            processorArchitecture="x86" 
            publicKeyToken="1fc8b3b9a1e18e3b" 
        />
	</dependentAssembly>
</dependency>
</assembly>
'''

PeakTimeStdDev = Target(
    # used for the versioninfo resource
    description = "PeakTime Standard Deviation Utility",
    # what to build
    script = "PeakTimeStdDev.py",
    other_resources = [(24, 1, manifest % dict(prog="PeakTimeStdDev"))],
    icon_resources = [(1, "img/heart.ico")],
    dest_base = "PeakTimeStdDev")

setup(name='PeakTimeStdDev',
	version="0.2",
	description="PeakTime Standard Deviation Utility",
	author="Andrea Chiarini",
	author_email="migratore@libero.it",
	url="",
	py_modules = ['PeakTimeStdDev'],
	license="GPL",
	options = {"py2exe" : {
						"packages": "encodings",
						"compressed": 1,
						"optimize": 2,
						"dll_excludes": ["w9xpopen.exe"]
					}
			},
	data_files= [("img",glob("img/*"))],
	windows = [PeakTimeStdDev],
	zipfile = None
)