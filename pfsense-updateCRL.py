#!/usr/bin/env python

import sys

from pfsense_api import PfSenseAPI
from datetime import datetime

from pfsense_cmdline import PfSenseOptionParser

parser = PfSenseOptionParser()
parser.add_option("--id", dest="crlID", help="ID of the CRL to update")
parser.add_option("--name", dest="name", help="Descriptive name of the CRL", default="Imported CRL")
parser.add_option("--crl", dest="crl", help="File containing CRL in PEM format" )

(options, args) = parser.parse_args()

parser.checkOptions( options )

if options.crlID is None or options.crl is None:
	print 'pfsense-updateCRL: options --id and --crl are required (see help: pfsense-updateCRL --help)'
	sys.exit( 1 )

crlFile = open( options.crl, 'rU' )
crl = crlFile.read()
crlFile.close()

api = PfSenseAPI.fromConfig( options.config )

(rc, data, contentType) = api.call( '/system_crlmanager.php', 'POST',
	apiData = { 
	  'method': 'existing',
	  'descr': '%s (last refresh: %s)' % (options.name, datetime.now().isoformat()),
	  'crltext': crl,
	  'submit': 'Save'
	},
	itemData = {
	  'id': options.crlID,
	  'act': 'editimported'
	})

api.logout()

if rc == 302:
	print 'CRL Update successful'
	sys.exit( 0 )
else:
	print 'CRL Update failed'
	sys.exit( -1 )
