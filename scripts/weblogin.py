import requests

import getpass
from scripts.config import user, loginurl 

from bs4 import BeautifulSoup

class WebLogin:
    """
    Handles the login, the logout, and the requests to the ELOG website
    """

    def __init__( self ):
        """
        Create the web browsing session in the ELOG website for the user 
        with current username and ask for password, config.py can ovveride
        the default username 
        """
        
        username = getpass.getuser() ## ELOG username is GPVM username (always?)       
        print( "You are logging in as {}".format( username ) )

        # if config.py has a non-empty username, user it!
        if user != "":
            username = user

        try:
            password = getpass.getpass()
        except Exception as e:
            raise SystemExit(e)

        self.form_data = {
            'ret_url'  : "",
            'username' : username,
            'password' : password
        }

        self.top_level_url= loginurl

        self.session = requests.session()

        try:
            response = self.session.post( self.top_level_url, data=self.form_data )
        except requests.exceptions.Timeout:
            raise SystemExit(e)
        except requests.exceptions.TooManyRedirects:
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        message = self._verify_login(response)
        if message:
            print(message.text.strip())
            raise SystemExit()
        
        print("---> Login successful!")

    def _verify_login(self, resp):

        soup = BeautifulSoup(resp.content, 'html.parser')
        message = soup.find( 'p', class_='message' )  

        return message
          
    def getURL(self, url):
        """
        Get the given URL from the ELOG website (Provided the seesion to be active)
        """

        try:
            page = self.session.get(url)
        except requests.exceptions.Timeout:
            print( "Connection timeout" )
            raise SystemExit(e)
        except requests.exceptions.TooManyRedirects:
            print( "Invalid URL" )
            raise SystemExit(e)
        except requests.exceptions.RequestException as e:
            print( "Connection error" )
            raise SystemExit(e)
        
        return page

    def logout(self):
        """
        Close the current session 
        """

        self.session.close()
