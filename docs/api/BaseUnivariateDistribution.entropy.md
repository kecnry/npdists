### [BaseUnivariateDistribution](BaseUnivariateDistribution.md).entropy (function)


```py

def entropy(self)

```



Expose the (differental) entropy.

See [scipy docs](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.rv_continuous.entropy.html)

This method is just a wrapper around the scipy.stats method on
[BaseUnivariateDistribution.dist_constructor_object](BaseUnivariateDistribution.dist_constructor_object.md) after doing any requested unit-conversions.

Returns
---------
* (float) entropy

