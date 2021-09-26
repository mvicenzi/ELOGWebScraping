from weblogin import WebLogin

from bs4 import BeautifulSoup

import pandas as pd
        
def scrapeWebPage(log, startdate="2021-09-26"):
    """
    Perform a query to the ELOG Shift Calendar page using the startdate string
    Return the scraped information in a pandas dataset
    """

    # FISH WEBPAGE AT URL
    url = 'https://dbweb8.fnal.gov:8443/ECL/sbnfd/C/filter_shifts?shift%3AWeekday+Night=on&shift%3AWeekday+Day=on&shift%3AWeekday+Swing=on&shift%3AWeekend+Night=on&shift%3AWeekend+Day=on&shift%3AWeekend+Swing=on&startdate={}&action=Filter'.format(startdate)
    page = log.getURL( url )

    #Define the dataset where to save this query
    df=pd.DataFrame(columns=["day", "shift_type", "collaborator"])

    # SCRAPE THE INFORMATION FROM THE WEBPAGE
    soup = BeautifulSoup(page.content, 'html.parser')
    cell_dict = {};
    shift_cells = soup.find_all( 'div', class_='shift_cell active' )
    for cell in shift_cells:
        head = cell.find("div", class_="head")
        assigment = cell.find("td", class_="assignment")
        for link in head.find_all('a'):
            cell_dict["day"] = link['href'].split("dt=")[-1]
            cell_dict["shift_type"] = link.text.strip()
        cell_dict["collaborator"] = assigment.text.strip().split("request swap")[0].strip()
        
        df = df.append(cell_dict, ignore_index=True)

    # We return the dataframe for this query
    return df


def main():


    # DEFINE THE TIME INTERVAL FOR THE QUERIES
    today="2021-09-26"

    days = [ "2021-09-26", "2021-08-26", "2021-07-26" ]


    # CONNECT TO THE ECL WEBSITE
    log = WebLogin()

    # QUERY THE INFORMATION OF THE PAST SHIFTS
    pastShifts = pd.concat( [scrapeWebPage( log, day ) for day in days] )
    futureShifts = pd.concat( [scrapeWebPage( log, day ) for day in days] )

    
    #Cross the two databases



    # LOGOUT
    log.logout()

    print("ALL DONE!")


    
if __name__ == "__main__":
    main()


"""
WEB SCRAPER IN SHORT
 1) Query past  6 months information: official shifts + shadow shifts 
 2) Scrape the webpage and make a list of shifters of the past six months with the date of the last shift, and the type of shift 
 3) Scrape the webpage and make a list of shifters for the future month: separate shadow and actual shifts
    - Cross this list with the other list: 
        - All shifters that are on the list are good for shift: PRINT THOSE NAMES IN GREEN ON SCREEN
        - All shifters that are not on the list but are on the shadow shift list: PRINT NAMES IN ORANGE
        - All shifters that are not on no list: PRINT NAMES IN RED: they have to be contacted urgently for shadow shift
 4) Print all done

FUNCTION TO PARSE THE WEBPAGE AND CREATE THE DATABASE ( pandas? )
shifter, last shift, last shift type, next shift, next shift type
 ....  ,    ....   ,    ....        ,    ....   ,    ....  

"""  