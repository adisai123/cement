"""Cement core extensions module."""

#from zope import interface

from cement2.core import backend, exc, interface

Log = backend.minimal_logger(__name__)
    
def extension_validator(obj):
    members = [
        'setup',
        'load_extension',
        'load_extensions',
        'loaded_extensions',
        ]
    interface.validate(IExtension, obj, members)
    
class IExtension(interface.Interface):
    """
    This class defines the Extension Handler Interface.  Classes that 
    implement this handler must provide the methods and attributes defined 
    below.
    
    Implementations do *not* subclass from interfaces.
    
    """
    
    # This is interface meta-deta, not part of the implemention
    class imeta:
        label = 'extension'
        validator = extension_validator
    
    # Must be provided by the implementation
    meta = interface.Attribute('Handler meta-data class')
    loaded_extensions = interface.Attribute('List of loaded extensions')
    
    def setup(defaults):
        """
        The setup function is called during application initialization and
        must 'setup' the handler object making it ready for the framework
        or the application to make further calls to it.
        
        Because the extension handler is called before the application 
        configuration is setup, the application defaults are passed rather
        than a config object.
        
        Required Arguments:
        
            defaults
                The applications default config dictionary.
                
        Returns: n/a
        
        """
    
    def load_extension(self, ext_module):
        """
        Load an extension whose module is 'ext_module'.  For example, 
        'cement2.ext.ext_configobj'.
        
        Required Arguments:
        
            ext_module
                The name of the extension to load.
                
        """
        
    def load_extensions(self, ext_list):
        """
        Load all extensions from ext_list.
        
        Required Arguments:
        
            ext_list
                A list of extension modules to load.  For example, 
                ['cement2.ext.ext_configobj', 'cement2.ext.ext_logging'].
        
        """

class CementExtensionHandler(object):
    """
    This is an implementation of the IExtentionHandler interface.  It handles
    loading framework extensions.
    
    """
    #interface.implements(IExtensionHandler)
    loaded_extensions = []
    
    class meta:
        interface = IExtension
        label = 'cement'
        
    def __init__(self):
        self.defaults = {}
        self.enabled_extensions = []
        
    def setup(self, defaults):
        self.defaults = defaults
        
    def load_extension(self, ext_module):
        if ext_module in self.loaded_extensions:
            Log.debug("framework extension '%s' already loaded" % ext_module)
            return 
            
        Log.debug("loading the '%s' framework extension" % ext_module)
        try:
            __import__(ext_module)
            self.loaded_extensions.append(ext_module)
        except ImportError as e:
            raise exc.CementRuntimeError(e.args[0])
    
    def load_extensions(self, ext_list):
        for ext in ext_list:
            self.load_extension(ext)