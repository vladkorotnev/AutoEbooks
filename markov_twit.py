 # -*- coding: utf-8 -*-

# AutoEbooks by vladkorotnev

import oauth2 as oauth
import urlparse
import codecs
import re
true = 1
false = 0

# //// SETTINGS ////

ebooksed_user = 'EDIT ME' #whose ebooks it is :)
statuses_count=1000 #how much statuses to get on input
remove_links=true #remove links
remove_mentions=true #remove @mentions
bad_translation=true #perform badtranslation via bing on results
bad_translation_cycles=10 #badtranslator cycles
bad_translation_log=1 #badtranslator loglevel, 0=no, 1=progress, 2=alltranslations
automatic_mode=false #don't ask "[Tweet this? y/n]" - good for cron
consumer_key = 'EDIT ME' #consumer key
consumer_secret = 'EDIT ME' #consumer sekret
bad_translation_appid='EDIT ME' #Bing AppId

# /////////////////

request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'

consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)


print "-= AutoEbooks by vladkorotnev ver 0.0.1 =-"
print "+== Authorizing application.."

try:
   with open('oauth_tok.cfg') as f: pass
except IOError as e:
	print "First time auth"
	resp, content = client.request(request_token_url, "GET")
	if resp['status'] != '200':
  	  raise Exception("Invalid response %s." % resp['status'])
	
	request_token = dict(urlparse.parse_qsl(content))
	
	print "+=== Got Response"
	print
	
	
	print "!!! Go to the following link in your browser:"
	print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
	print 
	
	accepted = 'n'
	while accepted.lower().strip() == 'n':
	    accepted = raw_input('Have you authorized me? (y/n) ')
	oauth_verifier = raw_input('What is the PIN? ')
	
	token = oauth.Token(request_token['oauth_token'],
    request_token['oauth_token_secret'])
	token.set_verifier(oauth_verifier)
	client = oauth.Client(consumer, token)

	resp, content = client.request(access_token_url, "POST")
	access_token = dict(urlparse.parse_qsl(content))

	print "+=== Saving configs with auth tokens!"
	
	oato = open('oauth_tok.cfg','w')
	oase = open('oauth_sec.cfg','w')
	oato.write(access_token['oauth_token'])
	oase.write(access_token['oauth_token_secret'])
	oato.close()
	oase.close()
	
	print "+=== Auth done. you won't have to do that anymore."
	
oato = open('oauth_tok.cfg','r')
oase = open('oauth_sec.cfg','r')
oauth_token = oato.read()
oauth_secret = oase.read()
oato.close()
oase.close()


import markov_gen
import bad_translate
import twitter

twt = twitter.Api(consumer_key,consumer_secret,oauth_token,oauth_secret)
bt = bad_translate.BadTrans(bad_translation_appid)

print "+== Logging in"
print "+== Will ebooks user ",ebooksed_user
print "+== Getting Statuses" 
statuses = twt.GetUserTimeline(ebooksed_user,count=statuses_count)
tempf = codecs.open("tempor.tmp", "wb", "utf8")
print "+== Listing Statuses"

for s in statuses:
	tstr = s.text.replace("\n","").replace("\"","")
	
	if remove_links == true:
		tstr = re.sub(r'(http://t.co/)\S*','',tstr,flags=re.IGNORECASE)
		tstr = re.sub(r'(https://t.co/)\S*','',tstr,flags=re.IGNORECASE)
		
	if remove_mentions == true:
		tstr = re.sub(r'(@)\S*','',tstr,flags=re.IGNORECASE)
		
	tempf.write("%s\n" % tstr)
	#tempf.write(' ')
else:
	tempf.close()
	print "+== Generating Data file"

tempf = codecs.open("tempor.tmp", "rb", "utf8")
mar = markov_gen.Markov(tempf)

if automatic_mode == false:
	accepted = 'n'
	while accepted.lower().strip() == 'n':
		generated = mar.generate_text(20)
		if bad_translation == true:
			generated = bt.bad_translate(generated,cycle=bad_translation_cycles,srclang='en',loglevel=bad_translation_log)
		print
		print generated
		print
		accepted = raw_input('[Tweet this? y/n]')
else:
	generated = mar.generate_text(20)
	if bad_translation == true:
			generated = bt.bad_translate(generated,cycle=bad_translation_cycles,srclang='en',loglevel=bad_translation_log)
	

print 
print "-==== POSTING: =====-"
print
print generated
print
twt.PostUpdate(generated)
print
print "-====  POSTED.  ====-"