### [Uniform](Uniform.md).to_json (function)


```py

def to_json(self, **kwargs)

```



Return the json representation of the distribution object.

The resulting dictionary can be restored to the original object
via [distl.from_json](distl.from_json.md).

See also:

* [Uniform.to_dict](Uniform.to_dict.md)
* [Uniform.to_file](Uniform.to_file.md)

Arguments
---------
* `**kwargs`: all keyword arguments will be sent to json.dumps

Returns
--------
* string

