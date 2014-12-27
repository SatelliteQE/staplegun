"""Useful documentation goes here.

"""
from config import conf
from splinter import Browser

import logging
import os


logger = logging.getLogger(__name__)  # pylint:disable=invalid-name

USERNAME_FLD = u'login[login]'
PASSWORD_FLD = u'login[password]'
SUBMIT_BTN = u'commit'
ACCOUNT_MN = u'account_menu'
LOGOUT_MN = u'menu_item_logout'


class Client(object):
    """Proxy class which adds more functionatily to Splinter's Browser."""

    def __init__(self, browser_name='firefox', url=None):
        """Initial parameters for a web browser client.

        :param str browser_name: Name for the web browser type to instantiate.
        :param str url: The base url for your server.

        """
        self.browser = Browser(browser_name)
        # If a `url` is provided...
        if url is not None:
            # ...  use it ...
            self.base_url = url
        else:
            # ... else, use the one from configuration file
            self.base_url = conf.properties['url']

    def login(self, username=None, password=None):
        """Performs a login using the provided credentials.

        :param str username: A user name.
        :param str password: A user password.

        """

        if username is None:
            username = conf.properties['username']
        if password is None:
            password = conf.properties['password']

        # Fill the login form.
        self.browser.fill_form(
            {USERNAME_FLD: username, PASSWORD_FLD: password})
        # Click the 'Login' button
        self.browser.find_by_name(SUBMIT_BTN).click()

    def logout(self):
        """Performs a logout."""
        # Position the mouse over the account menu to expose submenus.
        self.browser.find_by_id(ACCOUNT_MN).mouse_over()
        # Then, click the logout menu
        self.browser.find_by_id(LOGOUT_MN).click()

    def __getattr__(self, name):
        """Proxy attr lookup to self.browser.

        Allows calling Splinter's Browser methods directly. If `name` is not
        a method found in either `Browser` or `Client`, then ``AttributeError``
        is raised.

        :param str name: Name for a supported method.
        :raises: ``AttributeError``

        """
        attr = getattr(self.browser, name, None)
        if attr is None:
            super(Client, self).__getattribute__(name)

        return attr

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.browser.__exit__(*exc)
