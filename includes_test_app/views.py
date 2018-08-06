# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
import urllib.parse
import requests
from . import settings_app
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

log = logging.getLogger(__name__)


def info( request ):
    """ Returns basic info.
        Getting this running shows that logging is working, and that the settings_app file is properly reading env-vars. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    start = datetime.datetime.now()
    log.info( 'start, `%s`' % str(start) )
    rtrn_dct = {
        'query': {
            'date_time': str( start ),
            'url': '{schm}://{hst}{uri}'.format( schm=request.scheme, hst=request.META['HTTP_HOST'], uri=request.META.get('REQUEST_URI', request.META['PATH_INFO']) ) },  # REQUEST_URI not available via run-server
        'response': {
            'documentation': settings_app.README_URL,
            'elapsed_time': str( datetime.datetime.now() - start ),
            'message': 'ok' } }
    return HttpResponse( json.dumps(rtrn_dct, sort_keys=True, indent=2), content_type='application/javascript; charset=utf-8' )


def proxy( request, slug=None ):
    log.debug( 'slug, `%s`' % slug )
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    gets = request.GET
    log.debug( 'gets, `%s`' % gets )
    fetch_url = settings_app.FETCH_DIR_URL  # includes trailing slash
    proxy_url = reverse( 'proxy_url' )  # includes trailing slash
    js_rewrite_url = '%s%s' % ( fetch_url, 'doubletreejs/' )
    if slug:
        fetch_url = '%s%s' % ( fetch_url, urllib.parse.unquote_plus(slug) )
    if gets:
        r = requests.get( fetch_url, params=gets )
    else:
        r = requests.get( fetch_url )
    log.debug( 'r.url, ```%s```' % r.url )
    raw = r.content.decode( 'utf-8' )
    log.debug( 'raw, ```%s```' % raw )
    rewritten = raw.replace(
        'href="../', 'href="%s' % proxy_url ).replace(
        '<script src="doubletreejs/', '<script src="%s' % js_rewrite_url ).replace(
        'textRequest.open("GET", "doubletree-data.txt"', 'textRequest.open("GET", "%sdoubletree-data.txt"' % proxy_url
        )
    log.debug( 'rewritten, ```%s```' % rewritten )
    if request.META['PATH_INFO'][-5:] == '.xml/':
        resp = HttpResponse( rewritten, content_type='application/xml; charset=utf-8' )
    else:
        resp = HttpResponse( rewritten )
    return resp

def proxy_doubletree( request ):
    log.debug( 'starting' )
    url = '%s%s' % ( settings_app.FETCH_DIR_URL, 'doubletree-data.txt' )
    r = requests.get( url )
    return HttpResponse( r.content )

def just_internal( request ):
    """ Returns minimal view from base and extended template. """
    context = { 'foo': 'bar' }
    resp = render( request, 'includes_test_templates/internal_extender.html', context )
    return resp


def external( request ):
    """ Returns minimal view from base and extended template. """
    context = { 'MAIN_INCLUDE_URL': settings_app.MAIN_INCLUDED_URL }
    resp = render( request, 'includes_test_templates/external_extender.html', context )
    return resp


def bul_search( request ):
    """ Triggered by user entering search term into banner-search-field.
        Redirects query to search.library.brown.edu """
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    redirect_url = 'https://search.library.brown.edu?%s' % request.META['QUERY_STRING']
    return HttpResponseRedirect( redirect_url )

