### [Delta](Delta.md).isf (function)


```py

def isf(self, x=None, unit=None)

```



Expose the inverse of the survival function (isf).

See [scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.isf.html)

This method is just a wrapper around the scipy.stats method on
[Delta.dist_constructor_object](Delta.dist_constructor_object.md) after doing any requested unit-conversions.

See also:

* [Delta.sf](Delta.sf.md)
* [Delta.cdf](Delta.cdf.md)
* [Delta.logsf](Delta.logsf.md)

Arguments
----------
* `x` (float or array, optional, default=None): x-values at which to
    expose the isf.  If None or not provided, [Delta.cached_sample](Delta.cached_sample.md)
    will be used if available, or raise an error if no cached samples
    are available.
* `unit` (astropy.unit, optional, default=None): unit of the values
    in `x`.  If None or not provided, will assume they're provided in
    [Delta.unit](Delta.unit.md).

Returns
---------
* (float or array) osf values of the same type/shape as `x`

