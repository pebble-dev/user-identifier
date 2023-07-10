import os

domain_root = os.environ.get('DOMAIN_ROOT', 'rebble.io')
http_protocol = os.environ.get('HTTP_PROTOCOL', 'https')

DOMAIN_ROOT = domain_root
APPSTORE_DATABASE_URI = os.environ['APPSTORE_DATABASE_URI'].replace("postgres://", "postgresql://")
TIMELINE_DATABASE_URI = os.environ['TIMELINE_DATABASE_URI'].replace("postgres://", "postgresql://")
AUTH_DATABASE_URI = os.environ['AUTH_DATABASE_URI'].replace("postgres://", "postgresql://")
