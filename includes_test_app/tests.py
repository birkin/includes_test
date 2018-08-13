# -*- coding: utf-8 -*-

import logging
from django.conf import settings
from django.test import SimpleTestCase as TestCase  # TestCase requires db, so if you're not using a db, and want tests, try this
from includes_test_app.lib import html_processor

log = logging.getLogger(__name__)
TestCase.maxDiff = None


class ProcessorTest( TestCase ):
    """ Checks code massaging proxied html. """

    def test_append_slash_needed(self):
        """ Checks for presence of appended slash. """
        with open( '%s/includes_test_app/test_data/index.html' % settings.BASE_DIR, 'rb' ) as f:
            source = f.read().decode( 'utf-8')
        processed = html_processor.append_slashes( source )
        self.assertTrue( 'href="./_.html"' in processed )

    ## end class ProcessorTest()


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    ## end class RootUrlTest()
