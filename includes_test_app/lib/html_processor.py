# -*- coding: utf-8 -*-

import logging
from bs4 import BeautifulSoup  # https://www.crummy.com/software/BeautifulSoup/bs4/doc/


log = logging.getLogger(__name__)


def append_slashes( source_html ):
    """ Appends slashes to urls if necessary.
        Called by TBD. """
    source_html = source_html[0:750]
    log.debug( 'source_html, ```%s```' % source_html )
    soup = BeautifulSoup( source_html, 'html.parser' )
    links = soup.find_all( "a" )
    for link in links:
        log.debug( 'link, ```%s```' % link )
        log.debug( 'link["href"] initially, ```%s```' % link["href"] )
        if link['href'][-1:] != '/':
            link['href'] = '%s/' % link['href']
    changed = soup
    output = str( changed )
    log.debug( 'output, ```%s```' % output )
    return output
