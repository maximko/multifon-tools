#!/usr/bin/env python
#coding: utf8

from lxml import objectify
import requests
import sys

routes = ['phone','multifon', 'both', 'get'] #using index as routing number (excluding 'get'), see http://multifon.ru/help/
uri = 'https://sm.megafon.ru/sm/client/routing'

if len(sys.argv) < 4 or sys.argv[1] not in routes:
    print "Usage: %s <get|phone|multifon|both> <number> <password>" % sys.argv[0]
    sys.exit(1)

options = {'login': sys.argv[2] + '@multifon.ru',
           'password': sys.argv[3]} #GET parameters

if sys.argv[1] == 'get':
    r = requests.get(uri, params=options)
    response = objectify.fromstring(r.text.encode("utf-8")) #XML magic
    if response.result.code == 200:
        print '%s: %s' % (response.result.description, routes[int(response.routing)])
    else:
        print 'Error #%s: %s' % (response.result.code, response.result.description)
else:
    options['routing'] = routes.index(sys.argv[1])
    uri += '/set'
    r = requests.get(uri, params=options)
    response = objectify.fromstring(r.text.encode("utf-8"))
    print '%s: %s' % (response.result.code, response.result.description)