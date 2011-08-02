"""Json Framework Extension for Cement."""

import sys
import jsonpickle
from zope import interface

from cement2.core import handler, output, backend, hook
Log = backend.minimal_logger(__name__)

class JsonOutputHandler(object):
    interface.implements(output.IOutputHandler)
    class meta:
        type = 'output'
        label = 'json'
        
    def __init__(self):
        """
        This handler implements the IOutputHandler interface.  It provides
        JSON output from a return dictionary and uses jsonpickle to dump it
        to STDOUT.
        
        Note: The cement framework detects the '--json' option and suppresses
        output (same as if passing --quiet).  Therefore, if debugging or 
        troubleshooting issues you must pass the --debug option to see whats
        going on .
        
        """
        self.config = None
        
    def setup(self, config_obj):
        """
        Setup the handler for future use.
        
        Required Arguments:
        
            config_obj
                The application configuration object.  This is a config object 
                that implements the IConfigHandler interface and not a config 
                dictionary, though some config handler implementations may 
                also function like a dict (i.e. configobj).
        
        Returns: N/A
        
        """
        self.config = config_obj
        
    def render(self, data_dict, template=None, unpicklable=False):
        """
        Take a data dictionary and render it as Json output.  Note that the
        template option is received here per the interface, however this 
        handler just ignores it.
        
        Required Arguments:
        
            data_dict
                The data dictionary to render.
                
        Optional Arguments:
        
            template
                This option is completely ignored.
                
            unpicklable
                Whether or not the object is unpicklable (default: False)
                
        Returns: string (json)
        
        """
        Log.debug("rendering output as Json via %s" % self.__module__)
        sys.stdout = backend.SAVED_STDOUT
        sys.stderr = backend.SAVED_STDERR
        return jsonpickle.encode(data_dict, unpicklable=unpicklable)
            
handler.register(JsonOutputHandler)

@hook.register()
def cement_add_args_hook(config, arg_obj):
    """
    Adds the '--json' argument to the argument object.
    
    """
    arg_obj.add_argument('--json', dest='output_handler', 
        action='store_const', help='toggle json output handler', const='json')