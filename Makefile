PYUIC = pyuic5
all: thermui.py

thermui.py: therm.ui
	$(PYUIC) -o thermui.py therm.ui

clean:
	rm -f thermui.py thermui.pyc
