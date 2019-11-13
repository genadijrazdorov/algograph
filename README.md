# algograph

![Travis (.org)](https://img.shields.io/travis/genadijrazdorov/algograph?logo=travis)
![GitHub](https://img.shields.io/github/license/genadijrazdorov/algograph)

Algorithm to graph translator.

## Usage example

Here is the LC/MS troubleshooting algorithm:

```python
# algo.py

if not system_suitable:
    if low_signal:
	if not test(mass_spectrometer):
	    fix(mass_spectrometer)

	elif not test(loading_pump):
	    fix(loading_pump)

	elif test(loading_leak):
	    tighten(loading)

	elif not test(autosampler):
	    fix(autosampler)

    if rt_shift:
	change(solvent)

	if not test(gradient_pump):
	    fix(gradient_pump)

	elif test(system_leak):
	    tighten(system_leak)

	else:
	    change(suitability_column)

    if peak_misshape:
	if peak_widening:
	    pass

	elif peak_tailing:
	    pass

	elif peak_fronting:
	    pass

```

... which is easily translated to flowchart:

```bash
$ algograph algo.py

```

## Help

For the complete help try:

```
$ algograph --help
usage: algograph [-h] [-V] algorithm 

Translates an algorithm to directional graph.

positional arguments:
algorithm	algorithm file name

optional arguments:
-h, --help	show this help message and exit
-V, --version	show version and exit

```
