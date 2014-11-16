pfSense-python
==============

Some simple python scripts for programmatically changing settings in pfsense.

The code is rather ugly, but should work across most 2.x versions of python and has minimal dependencies.

Two example scripts are provided:
 - pfsense-backup: download any XML file for backup purposes
 - pfsense-updateCRL: update (modify) a Certificate Recovation List

For updateCRL, the CRL must already exist in pfSense (you can create one with no / nonsensical certificate data initially).  Once you have created it, go to the edit screen for the CRL and note down the id=[hex string] part of the URL.  This is what you must provide to --id on the command line.  Note that updateCRL will automatically append a string like '(last refresh: 2014-11-16T17:01:15.058446)' to the description to make it clear that the CRL was programmatically updated and when.  This currently cannot be turned off.

Example usage:
`  pfsense-updateCRL --config pfsense-config.ini --id=54683267e1bc5 --crl=crl.pem`
`  pfsense-backup -c pfsense-config.ini --area=all --no-rrd -o pfsense.all.xml`
`  pfsense-backup -c pfsense-config.ini --area=all --no-rrd | gpg --symmetric --passphrase 'somethingdecent' -o pfsense.all.xml.gpg`

Note that I haven't bothered implementing the encryption passphrase options for the backup script, on the basis that it's trivial (and more flexible) to pipe the output to GPG or similar for encryption.

To avoid specifying credentials on the command line, all scripts require a config.ini file, an example for which is provided in the repository (exampleConfig.ini).  In accordance with the principle of least priviledge, you should create a unique, dedicated service account in pfSense for each set of API operations you want to call.
