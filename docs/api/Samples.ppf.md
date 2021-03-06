### [Samples](Samples.md).ppf (function)


```py

def ppf(self, q, unit=None, as_quantity=False, wrap_at=None)

```



Expose the percent point function (ppf; iverse of cdf - percentiles) at
values of `q`.

For [Samples](Samples.md), this is done manually by sorting all [Samples.samples](Samples.samples.md)
and mapping `q` onto the range of the sum of [Samples.weights](Samples.weights.md) to select
the appropriate entry from [Samples.samples](Samples.samples.md).

See also:

* [Samples.pdf](Samples.pdf.md)
* [Samples.cdf](Samples.cdf.md)
* [Samples.sample](Samples.sample.md)

Arguments
----------
* `q` (float or array): percentiles at which to expose the ppf
* `unit` (astropy.unit, optional, default=None): unit of the exposed
    values.  If None or not provided, will assume they're provided in
    [Samples.unit](Samples.unit.md).
* `as_quantity` (bool, optional, default=False): whether to return an
    astropy quantity object instead of just the value.  Astropy must
    be installed.
* `wrap_at` (float, None, or False, optional, default=None): value to
    use for wrapping.  See [Samples.wrap](Samples.wrap.md).  If not provided or None,
    will use the value from [Samples.wrap_at](Samples.wrap_at.md).  Note: wrapping is
    computed before changing units, so `wrap_at` must be provided
    according to [Samples.unit](Samples.unit.md) not `unit`.

Returns
---------
* (float or array) ppf values of the same type/shape as `x`

