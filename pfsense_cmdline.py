
import sys
from optparse import OptionParser

class PfSenseOptionParser( OptionParser ):

    def __init__( self,  *args, **kwargs ):
        OptionParser.__init__( self, *args, **kwargs )

        self.add_option("-c", '--config', dest="config",
                  help="API configuration file (host name, username & password)", metavar="config.ini" )
    
    def checkOptions( self, options ):
        if options.config is None:
            print '%s: You must provide a config file with --config config.ini  (see: %s --help for details)' % ( self.get_prog_name(), self.get_prog_name() )
            sys.exit( 1 )
        