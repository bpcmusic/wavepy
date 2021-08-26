# WAVEPY
# Wavetable generator for the TelexO and TelexO+
# (c) 2018 Brendon Cassidy; MIT Licensed

import wave, struct, sys, getopt, computed

turboCutoff = 45
turboTriggered = 0

wtCount = 0
wtNames = []

def writeTable(outputfile, table, wavfilename):
	global wtCount, wtNames
	wtNames.append("wt" + str(wtCount))	
	outputfile.write("// " + wavfilename + "\n")
	outputfile.write("const int wt" + str(wtCount) + "[513] = { ")
	outputfile.write(', '.join(map(str, table)))
	outputfile.write(" };\n\n")
	wtCount += 1


argv = sys.argv[1:]

try:
	opts, args = getopt.getopt(argv,"i::",["input="])
except getopt.GetoptError:
	print("wavepy.py -i <inputfile>")
	sys.exit(2)

inputfile = ""
outputfile = "wavetables.h"

notecounter = []

for opt, arg in opts:
	if opt in ("-i", "--ifile"):
		inputfile = arg

	if opt in ("-o", "--ofile"):
		outputfile = arg

	if inputfile == "":
		print("no input file specified (-i)")
		sys.exit(2)


print("")
print("WAVEPY Wavetable Processor")
print("(c) 2018 Brendon Cassidy; MIT Licensed")
print("--------------------------")
print("Input File:", inputfile)
print("Output File:", outputfile)
print("")

filelist = []

with open(inputfile) as list:
	for wavfilename in list:
		wavfilename = wavfilename.strip()
		filelist.append(wavfilename)


with open(outputfile, "w") as hfile:

	hfile.write("/*\n")
	hfile.write(" * TELEXo Eurorack Module\n")
	hfile.write(" * (c) 2016-2018 Brendon Cassidy\n")
	hfile.write(" * MIT License\n")
	hfile.write(" */\n\n")

	hfile.write("#ifndef Wavetables_h\n")
	hfile.write("#define Wavetables_h\n\n")

	hfile.write("#include \"defines.h\"\n\n")

	# do the basic wavetables sine, triangle, saw

	writeTable(hfile, computed.sine(), "computed sine")
	writeTable(hfile, computed.triangle(), "computed triangle")
	writeTable(hfile, computed.sawtooth(), "computed sawtooth")

	# notice

	hfile.write("/*\n")
	hfile.write(" * the following wavetables are selected from\n")
	hfile.write(" * Adventure Kid's Public Domain waveform collection\n")
	hfile.write(" * more info here: https://www.adventurekid.se/akrt/waveforms/adventure-kid-waveforms/\n")
	hfile.write(" *\n")
	hfile.write(" * they were resampled (to 37650Hz) in order to make them 512 samples long\n")
	hfile.write(" */\n\n")

	wtNames.append("NULL")
	wtCount += 1

	for wavfilename in filelist:

		if wtCount >= turboCutoff and turboTriggered < 1:
			hfile.write("#ifdef TURBO\n\n")
			turboTriggered = 1

		print("Reading File:", wavfilename)

		waveFile = wave.open(wavfilename, 'r')

		samples = []

		length = waveFile.getnframes()
		for i in range(0,length):

			waveData = waveFile.readframes(1)
			data = struct.unpack("<h", waveData)

			sample = hex(int(data[0]))
			samples.append(sample)

		samples.append(samples[0])

		waveFile.close()

		writeTable(hfile, samples, wavfilename)


	hfile.write("const int *wavetables[] = { ")
	hfile.write(', '.join(wtNames))
	hfile.write(" };\n\n")

	hfile.write("#define WAVETABLECOUNT " + str(wtCount) + " \n\n")

	if turboTriggered == 1:
		hfile.write("#else\n\n")

		hfile.write("const int *wavetables[] = { ")
		hfile.write(', '.join(wtNames[0:turboCutoff]))
		hfile.write(" };\n\n")

		hfile.write("#define WAVETABLECOUNT " + str(turboCutoff) + " \n\n")

		hfile.write("#endif\n\n")



	hfile.write("#endif")

print("\nOperation Complete\n")



