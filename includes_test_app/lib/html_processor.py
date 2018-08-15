# -*- coding: utf-8 -*-

import logging
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from django.core.urlresolvers import reverse


log = logging.getLogger(__name__)


def append_slashes( source_html ):
    """ Appends slashes to urls if necessary.
        Called by TBD. """
    # source_html = source_html[0:750]
    source_html = source_html
    # log.debug( 'source_html, ```%s```' % source_html )
    soup = BeautifulSoup( source_html, 'html.parser' )
    ##
    a_links = soup.find_all( 'a' )
    for a_link in a_links:
        # # log.debug( 'a_link, ```%s```' % a_link )
        # log.debug( 'a_link["href"] initially, ```%s```' % a_link["href"] )
        # if a_link['href'][-1:] != '/':
        #     a_link['href'] = '%s/' % a_link['href']
        # log.debug( 'a_link["href"] now, ```%s```' % a_link["href"] )
        a_linktext = a_link['href']
        log.debug( 'a_linktext initially, `%s`' % a_linktext )
        if a_linktext[0:2] == './' and len(a_linktext) > 2:
            a_link['href'] = '%s/' % a_linktext
        log.debug( 'a_linktext finally, `%s`' % a_link['href'] )
    ##
    links = soup.find_all( 'link' )
    for link in links:
        linktext = link['href']
        log.debug( 'linktext initially, `%s`' % linktext )
        if linktext[0:3] == '../' and len(linktext) > 3:
            link['href'] = '%s%s/' % ( reverse('proxy_url'), linktext[3:] )  # reverse('proxy_url') includes trailing slash
        log.debug( 'linktext finally, `%s`' % link['href'] )
    changed = soup
    output = str( changed )
    # log.debug( 'output, ```%s```' % output )
    return output
