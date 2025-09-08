run:
	cp ./*.py /Volumes/CIRCUITPY/

install folder_or_file:
	cp -r $(folder_or_file) /Volumes/CIRCUITPY/lib/
	rsync -av --delete /Volumes/CIRCUITPY/lib/ lib/
