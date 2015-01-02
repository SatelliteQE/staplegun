"""Useful documentation goes here.

"""
from config import conf
from splinter import Browser

import logging


logger = logging.getLogger(__name__)  # pylint:disable=invalid-name

FLD_PASSWORD = u'login[password]'
FLD_USERNAME = u'login[login]'
BTN_LOGIN = u'commit'
MENU_ACCOUNT = u'account_menu'
MENU_LOGOUT = u'menu_item_logout'

# Notifications
NOTIF_SUCCESS = "//div[contains(@class, 'jnotify-notification-success')]"
NOTIF_WARN = "//div[contains(@class, 'jnotify-notification-warning')]"
NOTIF_ERROR = "//div[contains(@class, 'jnotify-notification-error')]"
NOTIF_CLOSE = "//a[@class='jnotify-close']"


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
            {FLD_USERNAME: username, FLD_PASSWORD: password})
        # Click the 'Login' button
        self.browser.find_by_name(BTN_LOGIN).click()

    def logout(self):
        """Performs a logout."""
        # Position the mouse over the account menu to expose submenus.
        self.browser.find_by_id(MENU_ACCOUNT).mouse_over()
        # Then, click the logout menu
        self.browser.find_by_id(MENU_LOGOUT).click()

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
