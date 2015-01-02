from client import Client, NOTIF_SUCCESS

URL = u'/organizations'
BTN_DELETE = u"//a[@class='delete' and contains(@data-confirm, '{0}')]"
BTN_EDIT = (u"//a[normalize-space(.)='{0}' and contains"
            "(@href,'organizations')]/"
            "../../td/div/a[@data-toggle='dropdown']")
BTN_NEW = u'/organizations/new'
BTN_PROCEED = u"//a[@class='btn btn-default' and contains(@href, '/edit')]"
BTN_SEARCH = u"//button[contains(@type,'submit')]"
BTN_SUBMIT = u'commit'
FLD_DESCRIPTION = u'organization[description]'
FLD_LABEL = u'organization[label]'
FLD_NAME = u'organization[name]'
FRM_SEARCH = u'search'
ORG_NAME = u"//a[contains(@href,'organizations')]/span[contains(.,'{0}')]"


def create(name, label, description):
    """Creates a new organization.


    """
    with Client() as client:
        client.visit(client.base_url)
        client.login()

        # Go to the organizations page
        client.visit(u'{0}{1}'.format(client.base_url, URL))
        # Click button to create new organization
        client.browser.find_link_by_href(BTN_NEW).click()
        # Fill out the form
        client.browser.fill_form(
            {FLD_NAME: name,
             FLD_LABEL: label,
             FLD_DESCRIPTION: description})
        # Submit
        client.browser.find_by_name(BTN_SUBMIT).click()
        # Proceed to Edit
        client.browser.find_by_xpath(BTN_PROCEED).click()
        # Final submit
        client.browser.find_by_name(BTN_SUBMIT).click()


def delete(name, really=True):
    """Deletes an organization by name.

    """
    with Client() as client:
        client.visit(client.base_url)
        client.login()

        # Search for the organization
        search(name, client)
        # Click the 'Edit' dropdown button
        client.browser.find_by_xpath(BTN_EDIT.format(name)).click()
        # Click the 'Delete' button
        client.browser.find_by_xpath(BTN_DELETE.format(name)).click()
        # Handle the confirmation dialog
        alert_dlg = client.browser.get_alert()

        # Really delete the organization?
        if really:
            alert_dlg.accept()
        else:
            alert_dlg.dismiss()

        # Check for success notification
        client.is_element_present_by_xpath(NOTIF_SUCCESS, wait_time=5)


def edit():
    """Edits an existing organization."""
    pass


def search(name, client):
    """Search for an organization by ``name``,

    :param str name: The name of the organization to be searched for.
    :param client: A Splinter Browser instance.

    :returns: A Splinter ``WebDriverElement`` for the found organization.
    :rtype: ``WebDriverElement``
    :raises: ``ElementDoesNotExist`` if the organization cannot be found.

    """
    # Go to the organizations page
    client.visit(u'{0}{1}'.format(client.base_url, URL))
    # Search for the organization
    client.browser.fill(FRM_SEARCH, name)
    # Click the 'Search' button
    client.browser.find_by_xpath(BTN_SEARCH).click()
    # Locate the organization from the results returned
    org = client.browser.find_by_xpath(ORG_NAME.format(name)).first

    return org
