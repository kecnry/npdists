import numpy as _np
import json as _json
from collections import OrderedDict

import matplotlib.pyplot as _plt

try:
    from astropy import units as _units
except ImportError:
    _has_astropy = False
else:
    _has_astropy = True

try:
    import dill as _dill
except ImportError:
    _has_dill = False
else:
    _has_dill = True

_math_symbols = {'__mul__': '*', '__add__': '+', '__sub__': '-', '__div__': '/'}

################## VALIDATORS ###################

# these all must accept a single value and return a boolean if it matches the condition as well as any alterations to the value
# NOTE: the docstring is used as the error message if the test fails

def is_distribution(value):
    """must be an npdists Distribution object"""
    if isinstance(value, dict) and 'npdists' in value.keys():
        # TODO: from_dict probably not available since its in __init__.py
        return True, from_dict(value)
    return isinstance(value, BaseDistribution), value

def is_distribution_or_none(value):
    """must be an npdists Distribution object or None"""
    if value is None:
        return True, value
    else:
        return is_distribution(value)

def is_math(value):
    """must be a valid math operator"""
    # TODO: make this more robust checking
    valid_maths = ['__add__', '__radd__', '__sub__', '__rsub__', '__mul__', '__rmul__', '__div__', '__rdiv__']
    valid_maths += ['sin', 'cos', 'tan']
    return value in valid_maths, value

def is_callable(value):
    """must be a callable function"""
    if isinstance(value, str):
        # try to "undill"
        if _has_dill:
            value = _dill.loads(value)
        else:
            raise ImportError("'dill' package required to load functions")
    return hasattr(value, 'func_name'), value

def is_unit(value):
    """must be an astropy unit"""
    if not _has_astropy:
        raise ImportError("astropy must be installed for unit support")
    if (isinstance(value, _units.Unit) or isinstance(value, _units.IrreducibleUnit) or isinstance(value, _units.CompositeUnit)):
        return True, value
    else:
        return False, value

def is_unit_or_unitstring(value):
    """must be an astropy.unit"""
    if is_unit(value)[0]:
        return True, value
    try:
        unit = _units.Unit(value)
    except:
        return False, value
    else:
        return True, unit

def is_unit_or_unitstring_or_none(value):
    """must be an astropy unit or None"""
    if value is None:
        return True, value
    return is_unit_or_unitstring(value)

def is_bool(value):
    """must be boolean"""
    return isinstance(value, bool), value

def is_float(value):
    """must be a float"""
    return isinstance(value, float) or isinstance(value, int) or isinstance(value, _np.float64), float(value)

def is_int(value):
    """must be an integer"""
    return isinstance(value, int), value

def is_int_positive(value):
    """must be a positive integer"""
    return isinstance(value, int) and value > 0, value

def is_int_positive_or_none(value):
    """must be a postive integer or None"""
    return is_int_positive or value is None, value

def is_valid_shape(value):
    """must be a positive integer or a tuple/list of positive integers"""
    if is_int_positive(value):
        return True, value
    elif isinstance(value, tuple) or isinstance(value, list):
        for v in value:
            if not is_int_positive(v):
                return False, value
        return True, value
    else:
        return False, value

def is_iterable(value):
    """must be an iterable (list, array, tuple)"""
    return isinstance(value, _np.ndarray) or isinstance(value, list) or isinstance(value, tuple), value



######################## DISTRIBUTION FUNCTIONS ###############################

def delta(x, value):
    return _np.asarray(x==value, dtype='int')

def gaussian(x, loc, scale):
    return 1./_np.sqrt(2*_np.pi*scale**2) * _np.exp(-(x-loc)**2/(2.*scale**2))

def uniform(x, low, high):
    return _np.asarray((x >= low) * (x <= high), dtype='int') / float(high - low)

######################## DISTRIBUTION ABSTRACT CLASS ###########################

class BaseDistribution(object):
    """
    BaseDistribution should be subclassed by any type of distribution creation classesAny subclass
    MUST define the following:
    __init__ (see docs below)
    mean, std properties
    """
    def __init__(self, unit, label,
                 dist_func, dist_args,
                 sample_func, sample_args,
                 *args):
        """
        all subclasses MUST parse args and send in as tuples via super so that
        order is preserved.
        For example:
        def __init__(self, start, stop, step):
            super(MyClass, self).__init__(('start', start, is_float), ('stop', stop, is_float), ('step', step, is_float))
        All of these "descriptors" will then be available to get and set via
        their attribute names
        """
        self._descriptors = OrderedDict()
        self._validators = OrderedDict()

        self._dist_func = dist_func
        self._dist_args = dist_args

        self._sample_func = sample_func
        self._sample_args = sample_args

        self.label = label
        self.unit = unit

        for item in args:
            valid, validated_value = item[2](item[1])
            if valid:
                self._descriptors[item[0]] = validated_value
            else:
                raise ValueError("{} {}, got {}".format(item[0], item[2].__doc__, item[1]))
            self._validators[item[0]] = item[2]

    def __getattr__(self, name):
        """
        for anything that isn't overriden here, call the method on the array itself
        """
        if name in ['_descriptors', '_validators', '_sample_func', '_sample_args', '_dist_func', '_dist_args', '_unit', 'unit', '_label', 'label']:
            # then we need to actually get the attribute
            return super(BaseDistribution, self).__getattr__(name)
        elif name in self._descriptors.keys():
            # then get the item in the dictionary
            return self._descriptors.get(name)
        else:
            raise AttributeError("{} does not have attribute '{}'".format(self.__class__.__name__.lower(), name))

    def __setattr__(self, name, value):
        """
        """
        if name in ['_descriptors', '_validators', '_sample_func', '_sample_args', '_dist_func', '_dist_args', '__class__', '_unit', 'unit', '_label', 'label']:
            return super(BaseDistribution, self).__setattr__(name, value)
        elif name in self._descriptors.keys():
            valid, validated_value = self._validators[name](value)
            if valid:
                self._descriptors[name] = validated_value
            else:
                raise ValueError("{} {}".format(name, validator.__doc__))
        else:
            raise AttributeError("{} does not have attribute '{}'".format(self.__class__.__name__.lower(), name))

    def __repr__(self):
        descriptors = " ".join(["{}={}".format(k,v) for k,v in self._descriptors.items()])
        return "<npdists.{} {} unit={}>".format(self.__class__.__name__.lower(), descriptors, self.unit)

    def __str__(self):
        if self.label is not None:
            return "{"+self.label+"}"
        else:
            return self.__repr__()

    def __float__(self):
        """
        by default, have the float representation come from sampling, but
        subclasses can/should override this to be the central/median/mode if
        possible
        """
        return self.sample()

    def __lt__(self, other):
        if isinstance(other, BaseDistribution):
            return self.__float__() < other.__float__()
        return self.__float__() < other

    def __le__(self, other):
        if isinstance(other, BaseDistribution):
            return self.__float__() <= other.__float__()
        return self.__float__() <= other

    def __gt__(self, other):
        if isinstance(other, BaseDistribution):
            return self.__float__() > other.__float__()
        return self.__float__() > other

    def __ge__(self, other):
        if isinstance(other, BaseDistribution):
            return self.__float__() >= other.__float__()
        return self.__float__() >= other

    def __copy__(self):
        return self.__class__(unit=self.unit, label=self.label, **self._descriptors)

    def __deepcopy__(self, memo):
        return self.__copy__()

    def copy(self):
        return self.__copy__()

    def __mul__(self, other):
        if _has_astropy and is_unit(other)[0]:
            copy = self.copy()
            copy.unit = other
            return copy

        elif isinstance(other, BaseDistribution):
            return Composite("__mul__", self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return self.__mul__(Delta(other))
        else:
            raise TypeError("cannot multiply {} by type {}".format(self.__class__.__name__, type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __div__(self, other):
        if isinstance(other, BaseDistribution):
            return Composite("__div__", self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return self.__div__(Delta(other))
        else:
            raise TypeError("cannot divide {} by type {}".format(self.__class__.__name__, type(other)))

    def __rdiv__(self, other):
        if isinstance(other, BaseDistribution):
            return Composite("__rdiv__", self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return self.__rdiv__(Delta(other))
        else:
            raise TypeError("cannot divide {} by type {}".format(self.__class__.__name__, type(other)))

    def __add__(self, other):
        if isinstance(other, BaseDistribution):
            return Composite("__add__", self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return self.__add__(Delta(other))
        else:
            raise TypeError("cannot add {} by type {}".format(self.__class__.__name__, type(other)))

    # def __radd__(self, other):
    #     return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, BaseDistribution):
            return Composite("__sub__", self, other)
        elif isinstance(other, float) or isinstance(other, int):
            return self.__sub__(Delta(other))
        else:
            raise TypeError("cannot subtract {} by type {}".format(self.__class__.__name__), type(other))

    def sin(self):
        return Composite("sin", self)

    def cos(self):
        return Composite("cos", self)

    def tan(self):
        return Composite("tan", self)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        if not (label is None or isinstance(label, str)):
            raise TypeError("label must be of type str")

        self._label = label

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, unit):
        if not (unit is None or isinstance(unit, _units.Unit) or isinstance(unit, _units.CompositeUnit) or isinstance(unit, _units.IrreducibleUnit)):
            raise TypeError("unit must be of type astropy.units.Unit")

        self._unit = unit

    def to(self, unit):
        """
        """
        if not _has_astropy:
            raise ImportError("astropy required to handle units")

        if self.unit is None:
            raise ValueError("distribution object does not have a unit")

        factor = self.unit.to(unit)

        new_dist = self.copy()
        new_dist.unit = unit
        new_dist *= factor
        return new_dist

    @property
    def mean(self):
        raise NotImplementedError

    @property
    def std(self):
        raise NotImplementedError

    @property
    def dist_func(self):
        return self._dist_func

    @property
    def dist_args(self):
        return tuple(getattr(self, k) for k in self._dist_args)

    @property
    def sample_func(self):
        return self._sample_func

    @property
    def sample_args(self):
        return tuple(getattr(self, k) for k in self._sample_args)

    def _return_with_units(self, value, unit=None, as_quantity=False):
        if (as_quantity or unit) and not _has_astropy:
            raise ImportError("astropy required to return quantity objects")

        if unit is None and not as_quantity:
            return value

        if self.unit is not None:
            value *= self.unit

        if unit is not None:
            if self.unit is None:
                raise ValueError("can only return unit if unit is set for distribution")

            if not _has_astropy:
                raise ImportError("astropy must be installed for unit support")

            value = value.to(unit)


        if as_quantity:
            return value
        else:
            return value.value

    def sample(self, size=None, unit=None, as_quantity=False):
        return self._return_with_units(self.sample_func(*self.sample_args, size=size), unit=unit, as_quantity=as_quantity)

    def distribution(self, x, unit=None, as_quantity=False):
        # x is assumed to be in the new units
        if unit is not None:
            if self.unit is None:
                raise ValueError("can only convert units on Distributions with units set")
            # convert to original units
            x = (x * unit).to(self.unit).value
        return self._return_with_units(self.dist_func(x, *self.dist_args), unit=unit, as_quantity=as_quantity)


    # def plot_func(self, show=False, **kwargs):
    #     ret = _plt.hist(self.sample(size), **kwargs)
    #     if show:
    #         _plt.show()
    #
    #     return ret

    def _xlabel(self, unit=None):
        l = 'value'
        if _has_astropy and self.unit is not None:
            l += ' ({})'.format(unit if unit is not None else self.unit)

        return l


    def plot(self, size=100000, unit=None, plot_sample=True, plot_dist=True, show=False, **kwargs):
        ret = []

        if plot_sample:
            kwargs.setdefault('bins', 25)

            ret_sample = self.plot_sample(size=size, unit=unit, show=False, **kwargs)
            xmin, xmax = _plt.gca().get_xlim()
        else:
            ret_sample = None
            sample = self.sample(size=size, unit=unit)
            xmin = _np.min(sample)
            xmax = _np.max(sample)

        if plot_dist:
            x = _np.linspace(xmin, xmax, 1001)
            ret_dist = self.plot_dist(x, unit=unit, show=False, **{k:v for k,v in kwargs.items() if k not in ['bins']})
        else:
            ret_dist = None

        if show:
            _plt.xlabel(self._xlabel(unit))
            _plt.ylabel('density')
            _plt.show()

        return (ret_sample, ret_dist)


    def plot_sample(self, size=1000, unit=None, show=False, **kwargs):
        ret = _plt.hist(self.sample(size, unit=unit), density=True, **kwargs)
        if show:
            _plt.xlabel(self._xlabel(unit))
            _plt.ylabel('density')
            _plt.show()

        return ret

    def plot_dist(self, x, unit=None, show=False, **kwargs):
        # x is assumed to be in new units
        if self.dist_func is not None:
            ret = _plt.plot(x, self.distribution(x, unit=unit, as_quantity=False), **kwargs)
        else:
            ret = None

        if show:
            _plt.xlabel(self._xlabel(unit))
            _plt.ylabel('density')
            _plt.show()

        return ret

    def to_dict(self):
        """
        dump a representation of the nparray object to a dictionary.  The
        nparray object should then be able to be fully restored via
        nparray.from_dict
        """
        def _json_safe(v):
            if isinstance(v, _np.ndarray):
                return v.tolist()
            elif isinstance(v, list) or isinstance(v, tuple):
                return [_json_safe(li) for li in v]
            elif isinstance(v, BaseDistribution):
                return v.to_dict()
            elif hasattr(v, 'func_name'):
                if _has_dill:
                    return _dill.dumps(v)
                else:
                    raise ImportError("'dill' package required to export functions to dictionary")
            # elif is_unit(v)[0]:
            #     return v.to_string()
            else:
                return v
        d = {k:_json_safe(v) for k,v in self._descriptors.items()}
        d['npdists'] = self.__class__.__name__.lower()
        if self.unit is not None:
            d['unit'] = self.unit.to_string()
        if self.label is not None:
            d['label'] = self.label
        return d

    def to_json(self, **kwargs):
        """
        dump a representation of the nparray object to a json-formatted string.
        The nparray object should then be able to be fully restored via
        nparray.from_json
        """
        try:
            return _json.dumps(self.to_dict(), ensure_ascii=True, **kwargs)
        except:
            if _has_dill:
                return _dill.dumps(self)
            else:
                raise ImportError("dumping file requires 'dill' package")

    def to_file(self, filename, **kwargs):
        """
        dump a representation of the nparray object to a json-formatted file.
        The nparray object should then be able to be fully restored via
        nparray.from_file
        @parameter str filename: path to the file to be created (will overwrite
            if already exists)
        @rtype: str
        @returns: the filename
        """
        f = open(filename, 'w')
        f.write(self.to_json(**kwargs))
        f.close()
        return filename


####################### DISTRIBUTION SUB-CLASSES ###############################

class Composite(BaseDistribution):
    def __init__(self, math, dist1, dist2=None, unit=None, label=None):
        super(Composite, self).__init__(unit, label,
                                        None, None,
                                        self._sample_from_children, ('math', 'dist1', 'dist2'),
                                        ('math', math, is_math), ('dist1', dist1, is_distribution), ('dist2', dist2, is_distribution_or_none))

        if _has_astropy:
            if dist1.unit is not None:
                if dist2 is None:
                    # trig always gives unitless
                    self.unit = _units.dimensionless_unscaled
                elif dist2.unit is not None:
                    if math in ['__add__', '__sub__']:
                        if dist1.unit == dist2.unit:
                            self.unit = dist1.unit
                        else:
                            # TODO: if they're convertible, we should handle the scaling automatically
                            raise ValueError("units do not match")
                    elif hasattr(dist1.unit, math):
                        self.unit = getattr(dist1.unit, math)(dist2.unit)
                    else:
                        raise ValueError("cannot determine new unit from {}{}{}".format(dist1.unit, _math_symbols.get(math, math), dist2.unit))
                else:
                    self.unit = dist1.unit
            elif dist2 is not None and dist2.unit is not None:
                self.unit = dist2.unit
            else:
                self.unit = None


    def __repr__(self):
        return "<npdists.{} {} unit={}>".format(self.__class__.__name__.lower(), self.__str__(), self.unit if self.unit is not None else "None")

    def __str__(self):
        if self.dist2 is not None:
            return "{}{}{}".format(self.dist1.__str__(), _math_symbols.get(self.math, self.math), self.dist2.__str__())
        else:
            return "{}({})".format(_math_symbols.get(self.math, self.math), self.dist1.__str__())


    def _sample_from_children(self, math, dist1, dist2, size=None):
        if self.dist2 is not None:
            return getattr(dist1.sample(size=size), math)(dist2.sample(size=size))
        else:
            # if math in ['sin', 'cos', 'tan'] and _has_astropy and dist1.unit is not None:
            #     unit = _units.rad
            # else:
            #     unit = None
            return getattr(_np, math)(dist1.sample(size=size, as_quantity=_has_astropy and self.unit not in [None, _units.dimensionless_unscaled]))

    def __float__(self):
        return self.mean
        # return self.sample()

    @property
    def mean(self):
        return self.to_histogram(N=10000, bins=100).mean

    @property
    def std(self):
        return self.to_histogram(N=10000, bins=100).std

    def to_histogram(self, N=1000, bins=10, range=None):
        return Histogram.from_data(self.sample(size=N), bins=bins, range=range, label=self.label, unit=self.unit)

    def to_gaussian(self, N=1000, bins=10, range=None):
        return self.to_histogram(N=N, bins=bins, range=range, label=self.label, unit=self.unit).to_gaussian()

    def to_uniform(self, sigma=1.0, N=1000, bins=10, range=None):
        return self.to_histogram(N=N, bins=bins, range=range, label=self.label, unit=self.unit).to_uniform(sigma=sigma)

class Function(BaseDistribution):
    def __init__(self, func, unit, label, *args):
        super(Function, self).__init__(unit, label,
                                       None, None,
                                       self._sample_from_function, ('func', 'args'),
                                       ('func', func, is_callable), ('args', args, is_iterable))

    def _sample_from_function(self, func, args, size=None):
        args = (a.sample(size=size) if isinstance(a, BaseDistribution) else a for a in args)
        return func(*args)

    def __float__(self):
        return self.mean
        # return self.sample()

    @property
    def mean(self):
        return self.to_histogram(N=10000, bins=100).mean

    @property
    def std(self):
        return self.to_histogram(N=10000, bins=100).std

    def to_histogram(self, N=1000, bins=10, range=None):
        return Histogram.from_data(self.sample(size=N), bins=bins, range=range, label=self.label, unit=self.unit)

    def to_gaussian(self, N=1000, bins=10, range=None):
        return self.to_histogram(N=N, bins=bins, range=range, label=self.label, unit=self.unit).to_gaussian()

    def to_uniform(self, sigma=1.0, N=1000, bins=10, range=None):
        return self.to_histogram(N=N, bins=bins, range=range, label=self.label, unit=self.unit).to_uniform(sigma=sigma)


class Histogram(BaseDistribution):
    def __init__(self, bins, density, unit=None, label=None):
        super(Histogram, self).__init__(unit, label,
                                        None, None,
                                        self._sample_from_hist, ('bins', 'density'),
                                        ('bins', bins, is_iterable), ('density', density, is_iterable))

    @classmethod
    def from_data(cls, data, bins=10, range=None, weights=None, label=None, unit=None):
        hist, bin_edges = _np.histogram(data, bins=bins, range=range, weights=weights, density=True)

        return cls(bin_edges, hist, label=label, unit=unit)

    def _sample_from_hist(self, bins, counts, size=None):
        if size is None:
            size = 1
            # if not isinstance(size, int):
                # raise TypeError("size must be of type int or None")

            # return np.array([self._sample_from_hist(bins=bins, counts=counts, size=None) for size in range(size)])

        # adopted from: https://stackoverflow.com/a/17822210
        bin_midpoints = self.bins[:-1] + _np.diff(self.bins)/2
        cdf = _np.cumsum(self.density)
        cdf = cdf / float(cdf[-1])

        values = _np.random.rand(size)
        value_bins = _np.searchsorted(cdf, values)
        random_from_cdf = bin_midpoints[value_bins]

        return random_from_cdf

    def __float__(self):
        return self.mean
        # return self.sample()

    @property
    def mean(self):
        bin_midpoints = self.bins[:-1] + _np.diff(self.bins)/2
        mean = _np.average(bin_midpoints, weights=self.density)
        return mean

    @property
    def std(self):
        bin_midpoints = self.bins[:-1] + _np.diff(self.bins)/2
        mean = _np.average(bin_midpoints, weights=self.density)

        var = _np.average((bin_midpoints - mean)**2, weights=self.density)
        sigma = _np.sqrt(var)
        return sigma

    def to_gaussian(self):
        return Gaussian(self.mean, self.std, label=self.label, unit=self.unit)

    def to_uniform(self, sigma=1.0):
        return self.to_gaussian(label=self.label, unit=self.unit).to_uniform(sigma=sigma)

class Delta(BaseDistribution):
    def __init__(self, value, unit=None, label=None):
        super(Delta, self).__init__(unit, label,
                                    delta, ('value',),
                                    self._sample_from_delta, ('value',),
                                    ('value', value, is_float))

    def _sample_from_delta(self, value, size=None):
        if size is None:
            return value
        else:
            return _np.full(size, value)

    def __mul__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.value *= other
            return dist

        return super(Delta, self).__mul__(other)

    def __div__(self, other):
        return self.__mul__(1./other)

    def __add__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.value += other
            return dist

        return super(Delta, self).__add__(other)

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __float__(self):
        return self.value

    @property
    def mean(self):
        return self.value

    @property
    def std(self):
        return 0.0

    def to_uniform(self):
        low = self.value
        high = self.value
        return Uniform(low, high, label=self.label, unit=self.unit)

    def to_gaussian(self):
        return Gaussian(self.value, 0.0, label=self.label, unit=self.unit)

    def to_histogram(self, N=1000, bins=10, range=None):
        return Histogram.from_data(self.sample(size=N), bins=bins, range=range, label=self.label, unit=self.unit)


class Gaussian(BaseDistribution):
    def __init__(self, loc=0.0, scale=0.0, unit=None, label=None):
        super(Gaussian, self).__init__(unit, label,
                                       gaussian, ('loc', 'scale'),
                                       _np.random.normal, ('loc', 'scale'),
                                       ('loc', loc, is_float), ('scale', scale, is_float))

    def __mul__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.loc *= other
            dist.scale *= other
            return dist

        return super(Gaussian, self).__mul__(other)

    def __div__(self, other):
        return self.__mul__(1./other)

    def __add__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.loc += other
            return dist

        return super(Gaussian, self).__add__(other)

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __float__(self):
        return self.loc
        # return self.sample()

    @property
    def mean(self):
        return self.loc

    @property
    def std(self):
        return self.scale

    def to_uniform(self, sigma=1.0):
        low = self.loc - self.scale * sigma
        high = self.loc + self.scale * sigma
        return Uniform(low, high, label=self.label, unit=self.unit)

    def to_histogram(self, N=1000, bins=10, range=None):
        return Histogram.from_data(self.sample(size=N), bins=bins, range=range, label=self.label, unit=self.unit)

class Uniform(BaseDistribution):
    def __init__(self, low=0.0, high=1.0, unit=None, label=None):
        super(Uniform, self).__init__(unit, label,
                                      uniform, ('low', 'high'),
                                      _np.random.uniform, ('low', 'high'),
                                      ('low', low, is_float), ('high', high, is_float))

    def __mul__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.low *= other
            dist.high *= other
            return dist

        return super(Uniform, self).__mul__(other)


    def __div__(self, other):
        return self.__mul__(1./other)

    def __add__(self, other):
        if (isinstance(other, float) or isinstance(other, int)):
            dist = self.copy()
            dist.low += other
            dist.high += other
            return dist
        # elif isinstance(other, Uniform):
            ## NOTE: this does not seem to be true as we should get a trapezoid if sampling separately
            # dist = self.copy()
            # dist.low += other.low
            # dist.high += other.high
            # return dist

        return super(Uniform, self).__add__(other)


    def __sub__(self, other):
        return self.__add__(-1*other)

    def __float__(self):
        return self.mean
        # return self.sample()

    @property
    def mean(self):
        return (self.low+self.high) / 2.0

    def to_gaussian(self, sigma=1.0):
        loc = self.mean
        scale = (self.high - self.low) / (2.0 * sigma)
        return Gaussian(loc, scale, unit=self.unit, label=self.label)

    def to_histogram(self, N=1000, bins=None, range=None):
        return Histogram.from_data(self.sample(size=N), bins=bins, range=range, unit=self.unit, label=self.label)
