### [Samples](Samples.md).moment (function)


```py

def moment(self, m)

```



Expose the non-central moment of order `m`.

See [scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.moment.html)

This method is just a wrapper around the scipy.stats method on
[Samples.dist_constructor_object](Samples.dist_constructor_object.md).

Arguments
----------
* `m` (int): order

Returns
---------
* (float) non-central moment

