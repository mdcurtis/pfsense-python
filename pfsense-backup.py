#!/usr/bin/env python

import sys

from pfsense_api import PfSenseAPI
from pfsense_cmdline import PfSenseOptionParser
from datetime import datetime


validAreas = [ 'all', 'dnsmasq', 'filter', 'interfaces', 'pptpd', 'rrddata', 'cron', 'system', 'sysctl', 'snmpd' ]
validAreasList = ', '.join( validAreas ) 

parser = PfSenseOptionParser()
parser.add_option("--area", dest="area",
                  help="Backup Area: %s" % ( validAreasList ), default='all')
parser.add_option('--no-rrd', dest='noRRD', action='store_true', help='Do not backup RRD (will result in large XML file). Only applicable if --area=all.' )
parser.add_option('--no-packages', dest='noPackages', action='store_true', help='Do not backup package info. Only applicable if --area=all.' )

parser.add_option('-o', '--output', dest='output', help='Output file (default: stdout)' )

(options, args) = parser.parse_args()

parser.checkOptions( options )

if not  options.area in validAreas:
	print '%s is not a valid area for backup. Options are: %s' % ( options.area, validAreasList )

if options.area != 'all' and (options.noRRD or options.noPackages):
	print '--no-rrd and --no-packages only make sense when combined with --area=all'
	sys.exit( 1 )

api = PfSenseAPI.fromConfig( options.config )


backupArea = options.area.lower()
if backupArea == 'all':
	backupArea = ''

apiData = { 
	'backuparea': backupArea,
	'Submit': 'Download configuration'
}

if options.noRRD:
	apiData[ 'donotbackuprrd' ] = 'yes'

if options.noPackages:
	apiData[ 'nopackages' ] = 'yes'

(rc, data, contentType) = api.call( '/diag_backup.php', 'POST',
	apiData = apiData )

api.logout()

if contentType != 'application/octet-stream':
	print 'Error: API parameters invalid (no XML file returned)'
	sys.exit( -1 )

if options.output:
	outputFile = open( options.output, 'w' )
	outputFile.write( data )
	outputFile.close()
else:
	print data
