### [Function](Function.md).plot_gaussian (method)


```py

def plot_gaussian(self, x, unit=None, wrap_at=None, label=None, show=False, **kwargs)

```



Plot the gaussian distribution that would result from calling
[Function.to_gaussian](Function.to_gaussian.md) with the same arguments.

Note that for distributions in which [Function.to_gaussian](Function.to_gaussian.md) calls
[Function.to_histogram](Function.to_histogram.md) under-the-hood, this could result in slightly
different distributions for each call.

See also:

* [Function.plot](Function.plot.md)
* [Function.plot_sample](Function.plot_sample.md)
* [Function.plot_dist](Function.plot_dist.md)

Arguments
-----------
* `x` (np array): the numpy array at which to sample the value on the
    x-axis. If `unit` is not None, the value of `x` are assumed to be
    in the original units [Function.unit](Function.unit.md), not `unit`.
* `unit` (astropy.unit, optional, default=None): units to use along
    the x-axis.  Astropy must be installed.
* `wrap_at` (float, None, or False, optional, default=None): value to
    use for wrapping.  See [Function.wrap](Function.wrap.md).  If not provided or None,
    will use the value from [Function.wrap_at](Function.wrap_at.md).  Note: wrapping is
    computed before changing units, so `wrap_at` must be provided
    according to [Function.unit](Function.unit.md) not `unit`.
* `label` (string, optional, default=None): override the label on the
    x-axis.  If not provided or None, will use [Function.label](Function.label.md).  Will
    only be used if `show=True`.
* `show` (bool, optional, default=True): whether to show the resulting
    matplotlib figure.
* `**kwargs`: keyword arguments for `sigma`, `N`, `bins`, `range` will
    be passed on to [Function.to_gaussian](Function.to_gaussian.md) (must be accepted by the
    given distribution type).  All other keyword arguments will be passed
    on to [Gaussian.plot_dist](Gaussian.plot_dist.md) on the resulting distribution.

Returns
--------
* the return from plt.plot

Raises
--------
* ImportError: if matplotlib dependency is not met.
