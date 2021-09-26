import requests

from config import username, password

class WebLogin:
    """
    Handles the login, the logout, and the requests to the ELOG website
    """

    def __init__( self ):
        """
        Create the web browsing session in the ELOG website for the user 
        with username and password configured configure.py
        """
       
        self.form_data = {
            'ret_url'  : "",
            'username' : username,
            'password' : password
        }

        self.top_level_url='https://dbweb8.fnal.gov:8443/ECL/sbnfd/U/doLogin'

        self.session = requests.session()
        response = self.session.post( self.top_level_url, data=self.form_data )

        #TODO ADD ERROR MESSAGES


    def getURL(self, url):
        """
        Get the given URL from the ELOG website (Provided the seesion to be active)
        """

        page = self.session.get(url)

        #TODO: ADD ERRORS ON THE WEBSITE QUERY
        
        return page

    def logout(self):
        """
        Close the current session 
        """

        self.session.close()