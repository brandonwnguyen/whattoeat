from flask import Flask, render_template, request
app = Flask(__name__)


CONSUMER_KEY = "JzXHzJh93S8OoeL097HIvg"
CONSUMER_SECRET = "nK_ZbxgbPyvh06mlMhG-XstrE0w"
TOKEN = "ouPPhi03URwOyH2OK2hq4d7n-_6I4l6I"
TOKEN_SECRET = "6N0xJ7LqUWsEUwXgfqJCEv-NPT0"



import argparse
import json
import pprint
import sys
import urllib
import urllib2
import random
import oauth2

API_HOST = 'api.yelp.com'

path = '/v2/search/'



def request_yelp(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    
    url = 'https://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    print u'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
        total = response['total'] - 1
        #response = response['businesses'][2]
        #temp = response['name']
    finally:
        conn.close()

    return response


@app.route("/")
def index():
	return render_template('website_index.html')

@app.route("/wte/")
def hello():
	url_params = {'term': 'restaurants', 'location': 'Berkeley, CA', 'sort' : 2}
	response = request_yelp(API_HOST, path, url_params)
	#return response
	return render_template('index.html')

@app.route("/wte/search", methods=['POST'])
def search():
	# return request.form['location']
	url_params = {'term': request.form['genre'], 'location': request.form['location'], 'sort' : 2}
	response = request_yelp(API_HOST, path, url_params)
	total = 40
	total2 = response['total'] - 1
	url_params = {'offset' : random.randint(1, 40),'term': request.form['genre'], 'location': request.form['location'], 'limit' : 1, 'sort' : 2}
	response = request_yelp(API_HOST, path, url_params)
	temp = response['businesses'][0]
	return render_template('results.html', business = temp, location=request.form["location"], genre=request.form["genre"])


@app.route("/random")
def rand():
	url_params = {'term': 'restaurants', 'location': 'Berkeley, CA', 'sort' : 2}
	response = request_yelp(API_HOST, path, url_params)
	total = 40
	total2 = response['total'] - 1
	url_params = {'offset' : random.randint(1, 40),'term': 'restaurants', 'location': 'Berkeley, CA', 'limit' : 1, 'sort' : 2}
	response = request_yelp(API_HOST, path, url_params)
	temp = response['businesses'][0]
	return str(temp)


if __name__ == "__main__":
	app.debug = True
	app.run()