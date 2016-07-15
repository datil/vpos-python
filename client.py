import requests
import yaml

from flask import Flask
from jinja2 import Environment, PackageLoader, Template
from random import randint

# Setup web app and templates
env = Environment(loader=PackageLoader('client', 'templates'))
app = Flask(__name__)

# Load configuration
config = yaml.safe_load(open("config.yaml"))

# Setup API URLs
payment_request_url = config['payment_req_url'] % {'client_id': config['client_id'], 'env': config['env']}
payment_response_url = config['payment_res_url'] % {'client_id': config['client_id'], 'env': config['env']}

# Define headers for HTTP requests
headers = {'x-api-key': config['datil_api_key']}

# Define test payment data
test_payment = {'interest_amount': '000',
                'ice_tax_amount': '000',
                'iva_tax_exempt_amount': '000',
                'language': 'SP',
                'purchase_currency_code': '840',
                'commerce_mall_id': '1',
                'purchase_operation_number': str(randint(10000000000,99999999999)),
                'net_amount': '1000',
                'iva_tax_amount': '140',
                'purchase_amount': '1140'}

# Allows you to get a payment request object comprised of:
# - ciphered_xml
# - ciphered_session_key
# - ciphered_signature
# With this data, you can build the payment form
def get_payment_request(req):
    r = requests.post(payment_request_url, json = req, headers = headers)
    return r.json()

# Setup web server
@app.route("/")
def vpos_client():
    req = get_payment_request(test_payment)
    print req
    template = env.get_template('client.html')
    return template.render(payment_request=test_payment,
                           acquirer_id=config['acquirer_id'],
                           commerce_id=config['commerce_id'],
                           ciphered_xml=req['ciphered_xml'],
                           ciphered_signature=req['ciphered_signature'],
                           ciphered_session_key=req['ciphered_session_key'])

if __name__ == "__main__":
    app.run()
