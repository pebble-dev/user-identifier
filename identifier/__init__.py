from rws_common import honeycomb
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


from . import config
from .models import init_app as init_models
from .api import init_app as init_api

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

honeycomb.init(app, 'user-identifier')

init_models(app)
init_api(app)

@app.route('/heartbeat')
def heartbeat():
    return 'ok'
