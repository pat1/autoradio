'''
Created on Nov 5, 2011

@author: hugosenari
'''

from pydbusdecorator.dbus_decorator import DbusDecorator
from pydbusdecorator.undefined_param import UNDEFINED_PARAM
from functools import wraps


class DBUS_INJECTED_ATTRS(object):
    #defalt var names in object 
    dbus_interface_info_at = 'dbus_interface_info'
    #default keywords params for decorated class constructor
    iface_at = 'dbus_iface'
    path_at = 'dbus_path'
    uri_at = 'dbus_uri'
    obj_at = 'dbus_object'
    session_at = 'dbus_session'
    last_fn_return_at = 'last_fn_return'
    on_change_at = 'on_change'
    prop_iface_at ='dbus_prop_iface'

   
class DBUS_DEFAULT_ATTRS(object):
    #default values
    iface = None
    path = None
    uri = None
    obj = None
    session = None
    retur = None
    on_change = None
    prop_iface = "org.freedesktop.DBus.Properties"
    dbus_interface_info = None

    
class DbusInterfaceInfo(DbusDecorator):
    ''' Object with this lib vars '''
    
    def __init__(self,
           #default values
           dbus_iface=DBUS_DEFAULT_ATTRS.iface,
           dbus_path=DBUS_DEFAULT_ATTRS.path,
           dbus_uri=DBUS_DEFAULT_ATTRS.uri,
           dbus_object=DBUS_DEFAULT_ATTRS.obj,
           dbus_session=DBUS_DEFAULT_ATTRS.session,
           last_fn_return=DBUS_DEFAULT_ATTRS.retur,
           on_change=DBUS_DEFAULT_ATTRS.on_change,
           dbus_prop_iface=DBUS_DEFAULT_ATTRS.iface,
           *args, **kw):
        ''' Constructor '''
        
        self.dbus_interfaces = {}
        self.dbus_obj = dbus_object
        self.dbus_obj_uri = dbus_uri
        self.dbus_path = dbus_path
        self.dbus_session = dbus_session
        self.dbus_iface = dbus_iface
        self.dbus_prop_iface = dbus_prop_iface
        self.last_return = last_fn_return
        self.on_change = on_change


class DbusInterface(DbusDecorator):
    ''' Wraps some class that define dbus interface '''
    
    #constructor of decorator
    def __init__(self,
            #default values
            iface=DBUS_DEFAULT_ATTRS.iface,
            path=DBUS_DEFAULT_ATTRS.path,
            uri=DBUS_DEFAULT_ATTRS.uri,
            obj=DBUS_DEFAULT_ATTRS.obj,
            session=DBUS_DEFAULT_ATTRS.session,
            retur=DBUS_DEFAULT_ATTRS.retur,
            on_change=DBUS_DEFAULT_ATTRS.on_change,
            prop_iface=DBUS_DEFAULT_ATTRS.prop_iface,
            dbus_interface_info=DBUS_DEFAULT_ATTRS.dbus_interface_info,
            #defalt attr name in object 
            dbus_interface_info_at=DBUS_INJECTED_ATTRS.dbus_interface_info_at,
            *args, **kw):
        ''' Init this decorator
        @param iface: str dbus object interface
        @param path: str dbus object path
        @param uri: str dbus object uri (org.mpris.MediaPlayer2.banshee)
        @param obj: dbus.proxies.ProxyObject
        @param session: dbus dbus.SessionBus.get_session()
        @param retur: object, last function return
        @param on_change: callable, reserved key but not in use
        @param prop_iface: str dbus object default interface for properties
        @param dbus_interface_info: DbusInterfaceInfo, object with DbusInterface infos 
        @param dbus_interface_info_at: str where store DbusInterface properties in this obj 
        
        @see: mpris2.mediaplayer2 to see some examples
        '''
        super(DbusInterface, self).__init__(*args, **kw)
        
        self._dbus_default_attrs = {
            'dbus_iface' : iface,
            'dbus_path' : path,
            'dbus_uri' : uri,
            'dbus_object' : obj,
            'dbus_session' : session,
            'last_fn_return' : retur,
            'on_change' : on_change,
            'dbus_prop_iface' : prop_iface,
            'dbus_interface_info' : dbus_interface_info
        }
        self._dbus_default_keys = {}

        self._dbus_interface_info_at = dbus_interface_info_at
        self._dbus_interface_info = dbus_interface_info
        self._meth = None
    
    #constructor of decorated class
    def __call__(self, meth, *args, **kw):
        ''' Called when any decorated class is loaded'''
        self._meth = meth
        
        @wraps(meth)
        def dbusWrapedInterface(*args, **kw):
            return self.dbusWrapedInterface(*args, **kw)
            
        return dbusWrapedInterface
    
    def dbusWrapedInterface(self, *args, **kw):
        ''' Called when some decoreted class was called
        Inject attrs from decorator at new object then return object
        
        @param *args: list of args to call constructor
        @param **kw: dict of keywords, can redefine class default parameters
        @return: instance of decoreted class, with new attributes
        @see: mpris2.mediaplayer2 to see some examples
        '''
        #shift dbus interface info from keywords
        kw = self.remove_interface_info_from_kw(**kw)
        #call decorated class constructor
        new_obj = self._meth(*args, **kw)
        if new_obj:
            self.inject_interface_info(new_obj)
        elif len(args) > 0:
            self.inject_interface_info(args[0])
        #inject dbus interface info
        
        return new_obj
    
    def remove_interface_info_from_kw(self, **kw):
        ''' Remove dbus interface info from keyords and set it in _dbus_interface_info '''
        constructor_keys = {} #dict to create new DbusInterfaceInfo
        dbus_info_at = DBUS_INJECTED_ATTRS.dbus_interface_info_at
        attr_keys = (DBUS_INJECTED_ATTRS.dbus_interface_info_at,
            DBUS_INJECTED_ATTRS.iface_at,
            DBUS_INJECTED_ATTRS.path_at,
            DBUS_INJECTED_ATTRS.uri_at,
            DBUS_INJECTED_ATTRS.obj_at,
            DBUS_INJECTED_ATTRS.session_at,
            DBUS_INJECTED_ATTRS.last_fn_return_at,
            DBUS_INJECTED_ATTRS.on_change_at,
            DBUS_INJECTED_ATTRS.prop_iface_at) 
        keys_for_keys = {DBUS_INJECTED_ATTRS.dbus_interface_info_at : 'dbus_interface_info',
            DBUS_INJECTED_ATTRS.iface_at : 'dbus_iface',
            DBUS_INJECTED_ATTRS.path_at : 'dbus_path',
            DBUS_INJECTED_ATTRS.uri_at : 'dbus_uri',
            DBUS_INJECTED_ATTRS.obj_at : 'dbus_object',
            DBUS_INJECTED_ATTRS.session_at : 'dbus_session',
            DBUS_INJECTED_ATTRS.last_fn_return_at : 'last_fn_return',
            DBUS_INJECTED_ATTRS.on_change_at : 'on_change',
            DBUS_INJECTED_ATTRS.prop_iface_at : 'dbus_prop_iface'
        }
        self._dbus_default_keys = keys_for_keys # 'from to' for kw and constructor_keys
        has_same_key_in_kw = False # infor if this constructor changes dbus_interface_info
        not_user_interface_info = True # inform if this constructor NOT pass dbus_interface_info param
        #remove dbus interface info keyword from kw for constructor
        dbus_interface_info = kw.get(dbus_info_at)
        if dbus_interface_info:
            del kw[dbus_info_at]
        for key in attr_keys:
            default_val = self._dbus_default_attrs.get(key)
            if dbus_interface_info and key in dbus_interface_info and dbus_interface_info[key] is not default_val:
                has_same_key_in_kw = True
                constructor_keys[keys_for_keys[key]] = dbus_interface_info[key]
            else:
                constructor_keys[keys_for_keys[key]] = self._dbus_default_attrs.get(key)
        
        #kw has dbus_interface_info param?
        if not_user_interface_info:
            #kw has info that diff from class definition?
            #or we not had dbus_interface_info?
            if has_same_key_in_kw \
                    or not self._dbus_interface_info:
                self._dbus_interface_info = DbusInterfaceInfo(**constructor_keys)
        
        return kw
    
    def inject_interface_info(self, new_obj):
        #set dbus_interface_info as attr in new_obj
        setattr(new_obj,
                DBUS_INJECTED_ATTRS.dbus_interface_info_at,
                self._dbus_interface_info)        
    
    #core info getter
    @staticmethod
    def attr_name_at(at, attr_id=DBUS_INJECTED_ATTRS.dbus_interface_info_at,
                     val=UNDEFINED_PARAM):
        ''' gets/sets objs attributes
        @param at: object where get/set
        @param attr_id: str internal name of attribute
        @param val: object, new value
        @return:  attribute value or val
        '''
        #return None if at, attr_id
        if not (at and 
                attr_id and
                #And if at has attr attr_id
                hasattr(at, attr_id)):
            return None
        if UNDEFINED_PARAM == val:
            setattr(at, attr_id, val)
        return getattr(at, attr_id)
    
    @staticmethod
    def get_dbus_interface_info(at):
        ''' Use to get dbus_interface_info in object
        @param at: object where get dbus_interface_info 
        @return session object
         '''
        return DbusInterface.attr_name_at(at, DBUS_INJECTED_ATTRS.dbus_interface_info_at)     

    #simple info getters
    @staticmethod
    def get_path(at):
        ''' return dbus object path attribute
        @param at: object where get this path
        @return: str object dbus path
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            return dbus_interface_info.dbus_path
    
    @staticmethod
    def get_uri(at):
        ''' return dbus object uri attribute
        @param at: object where get this uri
        @return: str object dbus uri
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            return dbus_interface_info.dbus_obj_uri
    
    @staticmethod
    def get_bus_iface(at):
        ''' return dbus_iface str of 'at'
        @param at: object where get this dbus object
        @return: str of dbus interface
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            return dbus_interface_info.dbus_iface
    
    @staticmethod
    def get_bus_prop_iface(at):
        ''' return bus_prop_iface str of 'at'
        @param at: object where get this dbus object
        @return: str of dbus interface for properties
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            return dbus_interface_info.dbus_prop_iface \
                 or DbusInterface.get_bus_iface(at)
    
    #complex info getter
    @staticmethod
    def get_session(at):
        ''' Use to get dbus_session in object
        @param at: object where get session previously criated
        @return session object
         '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            dbus_session = dbus_interface_info.dbus_session
            if not dbus_session:
                dbus_session = DbusInterface.dbus_lib.SessionBus.get_session()
                dbus_interface_info.dbus_session =  dbus_session
            return dbus_session
    
    @staticmethod
    def get_bus_obj(at):
        ''' return dbus object
        @param at: object where get this dbus object
        @return: dbus proxy object
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            obj = dbus_interface_info.dbus_obj
            if not obj:
                uri = DbusInterface.get_uri(at)
                if uri:
                    path = DbusInterface.get_path(at)
                    if path:
                        session = DbusInterface.get_session(at)
                        obj = session.get_object(uri, path)
                        dbus_interface_info.dbus_obj = obj
            return obj
        
    @staticmethod
    def get_bus_properties(at, iface=None):
        ''' return bus propeterty proxy for 'at'
        @param at: object where get this dbus object
        @param iface: str for property dbus interfacece (dbus properties by default)
        @return: dbus proxy object of iface  
        '''
        return DbusInterface.iface(at, iface)

    #utilities
    @staticmethod
    def iface(at, dbus_str_iface=None, dbus_obj=None):
        ''' Get iface from dict or create one and append it'''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            dbus_str_iface = dbus_str_iface \
                or dbus_interface_info.dbus_prop_iface
            result  = dbus_interface_info.dbus_interfaces.get(dbus_str_iface)
            if not result:
                result = DbusInterface.dbus_lib.Interface(
                    dbus_obj or DbusInterface.get_bus_obj(at),
                    dbus_str_iface)
                dbus_interface_info.dbus_interfaces[dbus_str_iface] = result
            return result

    @staticmethod
    def store_result(at, val=UNDEFINED_PARAM):
        ''' use to set last call result
        @param at: object where set
        @param val: object to set
        @return:  val
        '''
        dbus_interface_info = DbusInterface.get_dbus_interface_info(at)
        if dbus_interface_info:
            if val is UNDEFINED_PARAM:
                dbus_interface_info.last_return = val
            else:
                val = dbus_interface_info.last_return
        return val