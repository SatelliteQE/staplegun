from client import Client

URL = u'/organizations'
NEW_BTN = u'/organizations/new'
NAME_FLD = u'organization[name]'
LABEL_FLD = u'organization[label]'
DESCRIPTION_FLD = u'organization[description]'
SUBMIT_BTN = u'commit'
PROCEED_BTN = u"//a[@class='btn btn-default' and contains(@href, '/edit')]"
SEARCH_FORM = u'search'
SEARCH_BTN = u"//button[contains(@type,'submit')]"
EDIT_BTN = (u"//a[normalize-space(.)='{0}' and contains"
            "(@href,'organizations')]/"
            "../../td/div/a[@data-toggle='dropdown']")
DELETE_BTN = u"//a[@class='delete' and contains(@data-confirm, '{0}')]"


def create(name, label, description):
    """Creates a new organization.


    """
    with Client() as client:
        client.visit(client.base_url)
        client.login()

        # Go to the organizations page
        client.visit(u'{0}{1}'.format(client.base_url, URL))
        # Click button to create new organization
        client.browser.find_link_by_href(NEW_BTN).click()
        # Fill out the form
        client.browser.fill_form(
            {NAME_FLD: name,
             LABEL_FLD: label,
             DESCRIPTION_FLD: description})
        # Submit
        client.browser.find_by_name(SUBMIT_BTN).click()
        # Proceed to Edit
        client.browser.find_by_xpath(PROCEED_BTN).click()
        # Final submit
        client.browser.find_by_name(SUBMIT_BTN).click()


def edit():
    """Edits an existing organization."""
    pass


def delete(name, really=True):
    """Deletes an organization by name.

    """
    with Client() as client:
        client.visit(client.base_url)
        client.login()

        # Go to the organizations page
        client.visit(u'{0}{1}'.format(client.base_url, URL))
        # Search for the organization
        client.browser.fill(SEARCH_FORM, name)
        # Click the 'Search' button
        client.browser.find_by_xpath(SEARCH_BTN).click()
        # Click the 'Edit' dropdown button
        client.browser.find_by_xpath(EDIT_BTN.format(name)).click()
        # Click the 'Delete' button
        client.browser.find_by_xpath(DELETE_BTN.format(name)).click()
        # Handle the confirmation dialog
        alert_dlg = client.browser.get_alert()

        if really:
            alert_dlg.accept()
        else:
            alert_dlg.dismiss()
