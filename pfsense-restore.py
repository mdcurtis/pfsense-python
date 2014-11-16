#!/usr/bin/env python

import sys

from pfsense_api import PfSenseAPI
from pfsense_cmdline import PfSenseOptionParser
from datetime import datetime
from HTMLParser import HTMLParser

import email.mime.text

validAreas = [ 'all', 'aliases', 'captiveportal', 'voucher', 'dnsmasq', 'dhcpd', 'dhcpdv6',
     'filter', 'interfaces', 'ipsec', 'nat', 'openvpn', 'installedpackages', 'pptpd', 'rrddata', 'cron', 'syslog', 'system',
     'staticroutes', 'sysctl', 'snmpd', 'shaper', 'vlans', 'wol' ]
validAreasList = ', '.join( validAreas ) 

parser = PfSenseOptionParser()
parser.add_option("--area", dest="area",
                  help="Restore Area: %s" % ( validAreasList ), default='all')

parser.add_option('-i', '--input', dest='input', help='Input file (default: stdin)' )

(options, args) = parser.parse_args()

parser.checkOptions( options )

if not  options.area in validAreas:
    print '%s is not a valid area for restore. Options are: %s' % ( options.area, validAreasList )

api = PfSenseAPI.fromConfig( options.config )


restoreArea = options.area.lower()
if restoreArea == 'all':
    restoreArea = ''

apiData = { 
    'restorearea': restoreArea,
    'Submit': 'Restore configuration'
}

filename = 'stdin.xml'
if options.input:
    filename = options.input
    xmlFile = open( options.input, 'r' )
    xmlData = xmlFile.read()
else:
    xmlData = sys.stdin.read()

attachment = email.mime.text.MIMEText( xmlData, 'xml' )
attachment.set_param( 'filename', filename )
apiData[ 'conffile' ] = attachment

(rc, data, contentType) = api.call( '/diag_backup.php', 'POST',
    apiData = apiData )

api.logout()

# Nasty screen-scraping required here
class ExtractMsg( HTMLParser ):
    msg = ''
    inMsg = False

    def handle_starttag( self, tag, attrs ):
        attrDict = dict( attrs )
        if tag == 'td' and 'class' in attrDict and attrDict[ 'class' ] == 'infoboxnptd2':
            self.inMsg = True

    def handle_endtag( self, tag ):
        if self.inMsg:
            self.inMsg = False

    def handle_data( self, data ):
        if self.inMsg:
            self.msg += data

msgExtractor = ExtractMsg()
msgExtractor.feed( data )

print msgExtractor.msg.strip()