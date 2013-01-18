'''
Created on Nov 5, 2011

@author: hugosenari
'''
from pydbusdecorator.dbus_decorator import DbusDecorator
from pydbusdecorator.undefined_param import UNDEFINED_PARAM
from pydbusdecorator.dbus_interface import DbusInterface


class DbusAttr(DbusDecorator):
    '''
    Wrap some method as attribute
    
    Works like @property, but for dbus
    '''

    def __init__(self, meth=None, iface=None,
                  produces=lambda resp: resp,
                  to_primitive=lambda resp: resp,
                  override_none_val=UNDEFINED_PARAM,
                  override_none_return=True, *args, **kw):
        '''
        Instantiate one new DbusAttr decoreator
        By default pass received val to method
        @param meth: 
            function overrided
        @param iface: 
            str dbus intercafe string with this property
        @param produces: 
            callable, function or class with one param, that converts received data
        @param to_primitive: 
            callable, function or class with one param, that converts data to send
        @param override_none_val: 
            Set if override val to call decorated attr (method) with value of dbus attr response   
            Any value of val different than UNDEFINED_PARAM is not 'None' 
        @param override_none_return:
            Set if override response of call decorated attr (method) with value of dbus attr response
        '''
        super(DbusAttr, self).__init__(*args, **kw)
        self.attr = meth
        self.iface = iface
        self.produces = produces
        self.to_primitive = to_primitive
        self.override_val = override_none_val
        self.override_return = override_none_return

    def __call__(self, meth, *args, **kw):
        self.attr = meth
        return self

    def _get_set_dbus(self, obj, val=UNDEFINED_PARAM, *args, **kw):
        properties = DbusInterface.get_bus_properties(obj)
        iface = self.iface or DbusInterface.get_bus_iface(obj)
        #vals is UndefinedParam, try to get val from object
        if val is UNDEFINED_PARAM:
            mval = properties.Get(iface, self.attr.__name__)
            DbusInterface.store_result(obj, mval)
            if self.override_val:
                val = mval
        #else set val in property (meth.__name__)
        else:
            to_primitve = self.to_primitive
            properties.Set(iface, self.attr.__name__, val)
            DbusInterface.store_result(obj, to_primitve(val))
        result = self.attr(val, *args, **kw)
        if result is None and self.override_return:
            result = properties.Get(iface, self.attr.__name__)
        produces = self.produces
        return produces(result)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self._get_set_dbus(obj)

    def __set__(self, obj, value):
        if obj:
            self._get_set_dbus(obj, value)
        else:
            self.attr = value

    def __delete__(self, obj):
        raise AttributeError, "can't delete attribute"

    @property
    def attr(self):
        return self._attr

    @attr.setter
    def attr(self, value):
        self._attr = value
        if hasattr(value, "__doc__"):
            self.__doc__ = value.__doc__

