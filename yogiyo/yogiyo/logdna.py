import logging
from logdna import LogDNAHandler

key = 'd1efdbf0a0f73d0e2f5d91439dbcfe39'

log = logging.getLogger('logdna')
log.setLevel(logging.INFO)

options = {
  'hostname': 'pytest',
  'ip': '10.0.1.1',
  'mac': 'C0:FF:EE:C0:FF:EE'
}

# Defaults to False; when True meta objects are searchable
options['index_meta'] = True

test = LogDNAHandler(key, options)

log.addHandler(test)

log.warning("Warning message", {'app': 'bloop'})
log.info("Info message")
