### [Function](Function.md).wrap_at (property)




Value at which to wrap all sampled values.  If [Function.unit](Function.unit.md) is not None,
then the value of `wrap_at` is the same as the set units.

If `False`: will not wrap
If `None`: will wrap on range 0-2pi (0-360 deg) if [Function.unit](Function.unit.md) are angular
    or 0-1 if [Function.unit](Function.unit.md) are cycles.
If float: will wrap on range 0-`wrap_at`.

See also:

* [Function.get_wrap_at](Function.get_wrap_at.md)
* [Function.wrap](Function.wrap.md)

Returns
---------
* (float or None)

