#

# Change this to point to your Python2 exectuable
PYTHON24 = python2.4
PYTHON25 = python2.5
PYTHON = python2.5

# This should be the Python that generated RPMs depend on and install
# into; this may be different from the Python used to build the RPM.
RPM_TARGET_PYTHON=/usr/bin/python


all:	rpm

ins:
	soup $(PYTHON) setup.py install

kit:	doc sdist eggs # make a kit

#rpm:	ZSI/version.py
#	rm -f dist/*
#	#$(PYTHON) setup.py bdist_rpm --python=$(RPM_TARGET_PYTHON)

sdist:	ZSI/version.py
	rm -rf dist/*
	$(PYTHON) setup.py sdist

eggs:	ZSI/version.py
	$(PYTHON24) setup.py bdist_egg
	$(PYTHON25) setup.py bdist_egg

doc:	doc/version.tex		# build the docs
	$(MAKE) -C doc

ver:			# update the build number
	$(PYTHON) newver.py --incr

.PHONY: all ins kit rpm doc ver

ZSI/version.py doc/version.tex:	setup.cfg
	$(PYTHON) newver.py
