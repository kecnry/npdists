### [Samples](Samples.md).plot_uncertainties (function)


```py

def plot_uncertainties(self, sigma=1, unit=None, show=False, **kwargs)

```



Plot uncertainties as vertical lines and as a latex representation in
the axes title.

See also:

* [Samples.uncertainties](Samples.uncertainties.md)
* [Samples.plot](Samples.plot.md)
* [Samples.plot_sample](Samples.plot_sample.md)
* [Samples.plot_pdf](Samples.plot_pdf.md)
* [Samples.plot_cdf](Samples.plot_cdf.md)
* [Samples.plot_gaussian](Samples.plot_gaussian.md)

Arguments
------------
* `sigma` (int, optional, default=1): sigma to use for uncertainties,
    passed directly to [Samples.uncertainties](Samples.uncertainties.md)
* `unit` (astropy.unit, optional, default=None): units to use along
    the x-axis.  Astropy must be installed.
* `show` (bool, optional, default=True): whether to show the resulting
    matplotlib figure.
* `**kwargs`: keyword arguments for will be passed on to plt.axvline.

Returns
--------
* the return from the plt.axvline calls.

Raises
--------
* ImportError: if matplotlib dependency is not met.

