### [MVSamples](MVSamples.md).pdf (function)


```py

def pdf(self, x=None)

```



Expose the probability density function (pdf) at values of `x`.

See [scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.pdf.html)

This method is just a wrapper around the scipy.stats method on
[MVSamples.dist_constructor_object](MVSamples.dist_constructor_object.md) after doing any requested unit-conversions.

See also:

* [MVSamples.logpdf](MVSamples.logpdf.md)
* [MVSamples.cdf](MVSamples.cdf.md)

Arguments
----------
* `x` (float or array, optional, default=None): x-values at which to
    expose the pdf.  If None or not provided, [MVSamples.cached_sample](MVSamples.cached_sample.md)
    will be used if available, or raise an error if no cached samples
    are available.
* `unit` (astropy.unit, optional, default=None): unit of the values
    in `x`.  If None or not provided, will assume they're provided in
    [MVSamples.unit](MVSamples.unit.md).

Returns
---------
* (float or array) pdf values of the same type/shape as `x`

