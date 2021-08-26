# WAVEPY
## Wavetable generator for the TelexO and TelexO+

(c) 2018 Brendon Cassidy; MIT Licensed

## Usage

This simple utility reads from the `wavetables.txt` file the paths to the waveforms you would like to include in the `wavetables.h` (which supplies waveforms to the TelexO/TelexO+ project).

## Notes

* WAV files need to be 512 samples long
* update the `wavetables.txt` file to indicate the waveforms you want included
* 45 Wavetables will be shared with the TXo version; 322 With the TXo+
* If you put more than 322 waveforms in the list, it will add them to the output file. This will most likely result in an out of memory error when you attempt to compile the firmware.


## wavetables.txt Format

Each waveform gets a line in the file. Ensure that the utility can read from the referenced path. For example:

```
../AKWF-512/AKWF_0001.wav
../AKWF-512/AKWF_0002.wav
```

## Running the Utility

To generate wavetables.h from the wavetables.txt file (assumes resampled AdventureKid Waveforms in the referenced path), simply execute this python command:

`python -i wavetables.txt`

You can also specify alternate input and output files if you want to use other lists and generate different header files:

`python -i natural_wavetables.txt -o natural_wavetables.h`
