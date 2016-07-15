# vpos-python
Use this code as a guide to implement a payment button for the Alignet VPOS Gateway using the Datil VPOS API.

## Requirements
* Python 2.7.x.
* pip 8.1.x.
* Linux or OSX.

## Quickstart
`pip install -r requirements.txt`

`python client.py`

Finally, visit _http://localhost:5000_ and click the _Pay_ button. You should be redirected to the VPOS payment page where you can enter your credit card information.

When you finalize the transaction at the VPOS screen, you will be redirected to the URL you registered in the VPOS Gateway.
