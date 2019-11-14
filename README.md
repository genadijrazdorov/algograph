# algograph

[![Travis (.org)](https://img.shields.io/travis/genadijrazdorov/algograph?logo=travis)](https://travis-ci.org/genadijrazdorov/algograph)
[![codecov](https://codecov.io/gh/genadijrazdorov/algograph/branch/master/graph/badge.svg)](https://codecov.io/gh/genadijrazdorov/algograph)
[![GitHub](https://img.shields.io/github/license/genadijrazdorov/algograph)](https://github.com/genadijrazdorov/algograph/blob/master/LICENSE)

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

For the console script usage try:

```
$ algograph --help
```
