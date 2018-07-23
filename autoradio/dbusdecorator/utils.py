'''
utils functions
'''

import dbus, re
import xml.etree.ElementTree as ET


I_INSPECT = 'org.freedesktop.DBus.Introspectable'

def _match_uri(name, pattern='.+'):
    '''
    Filter logic for get_players and get_player_uri
    @param name: string name to test
    @param pattern=None:  string RegEx to test
    @return: boolean
    '''
    return re.match(pattern, name)

def get_session():
    '''
        @return: dbus.SessionBus.get_session()
    '''
    return dbus.SessionBus.get_session()

def get_uri(pattern='.'):
    '''
    Return string of player bus name
    @param pattern=None: string RegEx that filter response
    @return: array string of players bus name
    '''
    for item in get_session().list_names():
        if _match_uri(item, pattern):
            yield item


def get_mainloop():
    '''
    @return: mainloop (with 'run' method)
    '''
    try:
        from dbus.mainloop.glib import DBusGMainLoop
        DBusGMainLoop(set_as_default=True)
        try:
            import gobject
            return gobject.MainLoop()
        except:
            pass
         
        try:
            import gi.repository.GLib
            return gi.repository.GLib.MainLoop()
        except:
            pass
    except:
        pass
    
    class PyQtMainLoop():
        def __init__(self, app):
            self.app = app
        
        def run(self):
            if hasattr(self.app, 'exec_'):
                self.app.exec_()
            if hasattr(self.app, 'exec'):
                method = getattr(self.app, 'exec')
                method(self.app)

    
    try:
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default=True)
        try:
            from PySide.QtGui import QApplication
            return PyQtMainLoop(QApplication([]))
        except:
            pass
    
        try:
            from PyQt5.QtWidgets import QApplication  
            return PyQtMainLoop(QApplication([]))
        except:
            pass
    
        try:
            from PyQt4 import Qt
            return PyQtMainLoop(Qt.QApplication([]))
        except:
            pass
    except:
        pass

    return None

def _introspect_uri(bus_name, path, bus):
    bus = bus or dbus.SessionBus.get_session()
    path = path.replace('//', '/') or '/'
    obj = bus.get_object(bus_name, path)
    xml = obj.Introspect(dbus_interface=I_INSPECT)
    return ET.fromstring(xml)

def list_paths(bus_name, path='/', bus=None):
    '''
    Return generator with all subpaths of uri
    @param bus_name: string dbus object name 
    @param path='/': string dbus object path
    @param bus=None: Conn dbus.Conn (commonly SessionBus or SystemBus)
    @return: generator with all paths that has interfaces
    '''
    nodes = _introspect_uri(bus_name, path, bus)
    if [iface for iface in nodes.findall('interface')]:
        yield path.replace('//', '/')

    for node in nodes.findall('node'):
        sub_path = path + '/'+ node.attrib['name']
        for path_name in list_paths(bus_name, sub_path, bus):
            yield path_name

def list_interfaces(bus_name, path, bus=None):
    '''
    Return generator with all interfaces of path 
    @param bus_name: string dbus object name 
    @param path: string dbus object path
    @param bus=None: Conn dbus.Conn (commonly SessionBus or SystemBus)
    @return: generator with all interfaces of path 
    '''
    nodes = _introspect_uri(bus_name, path, bus)    
    for interface in nodes.findall('interface'):
        yield interface.attrib['name']
        
def list_all_interface(bus_name, path='/', bus=None):
    '''
    Return generator with all interfaces of path and subpaths 
    @param bus_name: string dbus object name 
    @param path: string dbus object path
    @param bus=None: Conn dbus.Conn (commonly SessionBus or SystemBus)
    @return: generator with all interfaces of path and subpaths
    '''
    paths = list_paths(bus_name, path, bus)
    for sub_path in paths:
        for interface in list_interfaces(bus_name, sub_path, bus):
            yield sub_path, interface

def implements(uri, interface, path, bus=None):
    '''
    '''
    for iface in list_interfaces(uri, path, bus):
        if iface == interface:
            return True


if __name__ == '__main__':
    uri = None
    for uri in get_uri():
        if uri.count(':') == 0: 
            print(uri)
            
    if uri:
        for interface in list_all_interface(uri, '/'):
            print('\t', interface)
    else:
        print('Nothing running')
