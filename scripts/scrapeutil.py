from bs4 import BeautifulSoup

from scripts.time_manager import str2dt

import pandas as pd

from scripts.colors import bcolors

def scrapeWebPage(log, startdate, df):
    """
    Perform a query to the ELOG Shift Calendar page using the startdate string
    Update the scraped information in a pandas dataset df
    """

    # Update the url with details of the query: 
    # filters on shifter's block type and startdate
    url = 'https://dbweb8.fnal.gov:8443/ECL/sbnfd/C/filter_shifts?shift%3AWeekday+Night=on&shift%3AWeekday+Day=on&shift%3AWeekday+Swing=on&shift%3AWeekend+Night=on&shift%3AWeekend+Day=on&shift%3AWeekend+Swing=on&startdate={}&action=Filter'.format(startdate)
    page = log.getURL( url )

    # Information from the webpage are scraped. 
    # Assumes static xtml is returned by the query
    soup = BeautifulSoup(page.content, 'html.parser')
    cell_dict = {};
    shift_cells = soup.find_all( 'div', class_='shift_cell active' )
    for cell in shift_cells:
        head = cell.find("div", class_="head")
        assigment = cell.find("td", class_="assignment")
        for link in head.find_all('a'):
            cell_dict["day"] = str2dt(link['href'].split("dt=")[-1])
            cell_dict["shift_type"] = link.text.strip()
        cell_dict["collaborator"] = assigment.text.strip().split("request swap")[0].strip()
        
        df = df.append(cell_dict, ignore_index=True)
    
    return df


def findCollaborator( df, name, surname ):
    """
    Return where in the database a collaborator took shifts 
    """
    queryString = '{} {}'.format( name, surname ) # need to add the hidden character   to separate Name and Surname
    print( df[df.collaborator==queryString] )



def vetShifters( pastDf, futureDf, verbose, filename):
    """
    Print the list of shifters that needs to take a shadow shift ( any verbosity level)
    Print the list of shifters that scheduled a shadow shift ( verbose 1 )
    Print the list of shifters that are certfied for their shift ( verbose 2 )
    """

    fp = open(filename, 'w')

    collabs = pastDf['collaborator'].values

    for index, row in futureDf.iterrows():
        if not row['collaborator'] in collabs:

            if 'Shadow' in row['shift_type']:

                message = bcolors.BOLD + "{} \n".format( row['collaborator'] ) 
                message = message + "Next shift block: {} on {}\n".format( row['shift_type'], row['day'] )
                message = message + "Signed for a shadow shift!\n"

                if verbose >= 1:
                    fp.write( message+"\n\n" )
                    print(bcolors.WARNING + message + bcolors.ENDC)

            else:
            
                message = bcolors.BOLD + "{} \n".format( row['collaborator'] )
                message = message + "Next shift block: {} on {}\n".format( row['shift_type'], row['day'] )
                message = message + "Needs to take a shadow shift!\n"

                fp.write( message+"\n\n" )
                print(bcolors.FAIL+ message + bcolors.ENDC)


        else:   

            QUERY_COLLAB=pastDf['collaborator']==row['collaborator']
            collabRow = pastDf[QUERY_COLLAB]

            message = "{} \n".format( row['collaborator'] )
            message = message + "Next shift block: {} on {}\n".format( row['shift_type'], row['day'] )
            message = message + "Previous shift on {}\n".format( collabRow['day'].values[0] )

            if verbose >= 2:
                fp.write( message+"\n\n" )
                print(bcolors.OKGREEN + message + bcolors.ENDC)

    fp.close()
