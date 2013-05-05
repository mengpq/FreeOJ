#!/usr/bin/env python
# coding: utf-8
from BeautifulSoup import BeautifulSoup
import urllib, urllib2, cookielib, MultipartPostHandler, re

class codeforces:
	
	def __init__(self):
		self.languageid = {'C++':1,'C':4,'Python':8}
		self.username = ''
		self.password = ''
		self.login_url = 'http://www.codeforces.com/enter'
		self.submit_url = 'http://www.codeforces.com/problemset/submit'
		self.problem_url = 'http://www.codeforces.com/problemset/problem/'
		self.cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj),MultipartPostHandler.MultipartPostHandler)
		self.login_data = urllib.urlencode({'_tta' :'141', 'action':'enter', 'handle':self.username, 'password':self.password, 'remember':'on', 'xsrf':'180b269e390e5391272f36202df822d4'})
		self.opener.open(self.login_url, self.login_data)
		self.submit_data = {'xsrf':'180b269e390e5391272f36202df822d4', 'action':'submitSolutionFormSubmitted', 'contestId':'', 'submittedProblemIndex':'', 'programTypeId':'1', 'sourceFile':'', '_tta':'141','source':''}

	def submit(self, language, source_id, source_code):
		contest_id = re.findall('\d+',source_id)[0]
		problem_index = source_id[len(contest_id):]
		self.submit_data['contestId'] = contest_id
		self.submit_data['submittedProblemIndex'] = problem_index
		self.submit_data['source'] = source_code
		self.submit_data['programTypeId'] = self.languageid[language]
		self.opener.open(self.submit_url,self.submit_data)
	
	def get_result(self, submission_id):
		resp = self.opener.open('http://www.codeforces.com/submissions/' + self.username)
		soup = BeautifulSoup(resp.read())
		submitlist = soup.findAll('tr')
		for item in submitlist:
			if re.search('data-submission-id',str(item)):
				source_id = ''
				hrefs = item.findAll('a')
				for href in hrefs:
					if re.search('problemset',str(href)):
						source_id = re.findall('\w+',href.next.strip())[0]
				view_source = item.findAll('a',{'class':'view-source'})[0]
				runid = re.findall('\d+',str(view_source))[0]
				if not submission_id: submission_id = runid
				if runid != submission_id: continue
				runtime = item.findAll('td',{'class':'time-consumed-cell'})[0].string.strip()
				memory = item.findAll('td',{'class':'memory-consumed-cell'})[0].string.strip()
				temp = item.findAll('td',{'class':'status-cell status-small status-verdict-cell'})[0].contents[1]
				result = ''
				if len(temp.contents)>1:
					result = temp.contents[0] + temp.contents[1].string
				else:
					result =temp.contents[0]

				memory = re.findall('\w+',memory)[0]
				runtime = re.findall('\w+',runtime)[0]
				return {'submission_id':submission_id, 'result':result, 'runtime':runtime, 'memory':memory, 'source_id':source_id}
