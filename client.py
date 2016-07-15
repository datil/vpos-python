import requests
import yaml

from flask import Flask, request, jsonify
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
# An API key is always needed
headers = {'x-api-key': config['datil_api_key']}

# Generate a random order identificator for the purpose of this demo.
# In a production environment, your e-commerce software or ERP should
# generate a unique order id for each payment request.
# It must be a numeric id of length 11.
def random_order():
    return str(randint(10000000000,99999999999))

# Define a test payment request
test_payment = {'interest_amount': '000',
                'ice_tax_amount': '000',
                'iva_tax_exempt_amount': '000',
                'language': 'SP',
                'purchase_currency_code': '840',
                'commerce_mall_id': '1',
                'purchase_operation_number': random_order(),
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

# Allows you to get a decrypted payment response comprised of:
# - authorization_code
# - tax_amount
# - commerce_id
# - authorization_result
# - terminal_code
# - cvv_cvc2_validation
# - error_message
# - error_code
# - language
# - purchase_operation_number
# - vci
# - interests
# - card_expiration_month
# - card_number
# - purchase_ip_address
# - purchase_currency_code
# - acquirer_id
# - card_expiration_year
# - eci
# - net_amount
# - card_type
# - purchase_amount
#
# With this data, you can build the payment "thank you" page and let
# the payer know if the payment was successful.
#
# You need to look at "authorization_result". If it is "00", it means the payment
# was processed successfully. Any other code means it was declined.
#
# If the transaction was successful, you can obtain the authorization code from
# "authorization_code".
#
# If thee transaction was declined, you can get a detailed error from "error_message"
# and "error_code"
def get_payment_response(res):
    r = requests.post(payment_response_url, json = res, headers = headers)
    return r.json()

# Visit this route to generate a payment request.
@app.route("/")
def vpos_request():
    req = get_payment_request(test_payment)
    print req
    template = env.get_template('client.html')
    return template.render(payment_request=test_payment,
                           acquirer_id=config['acquirer_id'],
                           commerce_id=config['commerce_id'],
                           ciphered_xml=req['ciphered_xml'],
                           ciphered_signature=req['ciphered_signature'],
                           ciphered_session_key=req['ciphered_session_key'])

# Captures the POST parameters sent by the Alignet VPOS Gateway and sends them
# to the Datil VPOS API for decryption.
# Returns the response as JSON for demo purposes.
@app.route("/response", methods=['POST'])
def vpos_response():
    ciphered_xml = request.form['XMLREQ']
    ciphered_signature = request.form['DIGITALSIGN']
    ciphered_session_key = request.form['SESSIONKEY']
    res = get_payment_response({'ciphered_xml': ciphered_xml,
                                'ciphered_signature': ciphered_signature,
                                'ciphered_session_key': ciphered_session_key})
    return jsonify(res)

if __name__ == "__main__":
    app.run()
