run:
	cp ./code.py /Volumes/CIRCUITPY/code.py

install folder_or_file:
	cp -r $(folder_or_file) /Volumes/CIRCUITPY/lib/
	rsync -av --delete /Volumes/CIRCUITPY/lib/ lib/
