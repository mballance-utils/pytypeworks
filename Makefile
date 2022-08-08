ROOTDIR=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

html :
	$(ROOTDIR)/packages/python/bin/sphinx-build -M html doc/source doc/build
