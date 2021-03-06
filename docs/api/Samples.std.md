### [Samples](Samples.md).std (function)


```py

def std(self, unit=None, as_quantity=False, wrap_at=None, N=1000000)

```



Expose the standard deviation of the  samples ([Samples.samples](Samples.samples.md) if [Samples.weights](Samples.weights.md)
is not provided, otherwise `N` draws from [Samples.sample](Samples.sample.md))

See also:

* [Samples.median](Samples.median.md)
* [Samples.mean](Samples.mean.md)
* [Samples.var](Samples.var.md)

Arguments
----------
* `unit` (astropy.unit, optional, default=None): unit of the values
    in `x` to expose.  If None or not provided, will assume they're in
    [Samples.unit](Samples.unit.md).
* `as_quantity` (bool, optional, default=False): whether to return an
    astropy quantity object instead of just the value.  Astropy must
    be installed.
* `wrap_at` (float, None, or False, optional, default=None): value to
    use for wrapping.  See [Samples.wrap](Samples.wrap.md).  If not provided or None,
    will use the value from [Samples.wrap_at](Samples.wrap_at.md).  Note: wrapping is
    computed before changing units, so `wrap_at` must be provided
    according to [Samples.unit](Samples.unit.md) not `unit`.
* `N` (int, optional, default=1e6): number of samples to draw before
    computing `std`.  Only applicable if [Samples.weights](Samples.weights.md) is not None.

Returns
---------
* (float) standard deviation of the distribution in units `unit`.

