import bingtrans
import random

class BadTrans(object):

	def __init__(self, appId):
		self.langs = ['en','ru','ja','ko','zh-CHT','zh-CHS','mww','ar','bg','hu','vi','ht','el','da','he','id','es','it','ca','lv','lt','de','nl','no','fa','pl','pt','ro','sk','sl','th','tr','uk','fi','fr','hi','cs','sv','et']

		bingtrans.set_app_id(appId)
		
	def bad_translate(self, text, cycle, srclang='en', loglevel=0):
		result = text
		cyclesCompleted = 0
		srcLang=srclang
		curLang=''
		while cyclesCompleted < cycle:
			if loglevel==1:
				print '+== Bad Translator: cycles completed: ',cyclesCompleted
			curLang = random.choice(self.langs)
			result = bingtrans.translate(result,srcLang,curLang)
			result = bingtrans.translate(result,curLang,srcLang)
			if loglevel==2:
				print '+== Bad Translator: cycles ',cyclesComplete
				print result
				print
			cyclesCompleted = cyclesCompleted + 1
		return result