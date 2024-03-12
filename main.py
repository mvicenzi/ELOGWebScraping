import pandas as pd

from scripts.weblogin import WebLogin

from scripts.time_manager import get_days_future, get_days_past, get_today, get_today_str, str2dt

from scripts.scrapeutil import scrapeWebPage, findCollaborator, vetShifters
 
from scripts.arguments import sel_arguments


def main():

    args = sel_arguments()

    # Connect to the ecl website
    login = WebLogin()

    # Populate the base dataframe for the current month
    thisMonth = pd.DataFrame(columns=["day", "shift_type", "collaborator"])
    thisMonth = scrapeWebPage( login, get_today_str(), thisMonth )

    # Split the current months based on 'today' in past and future
    pastShifts = thisMonth[thisMonth.day<=get_today()]
    futureShifts = thisMonth[thisMonth.day>get_today()]

    # Query more past shift blocks 
    for day in get_days_past( args.backward_interval ):
        pastShifts = scrapeWebPage( login, day, pastShifts )

    pastShifts = pastShifts.sort_values('day').drop_duplicates('collaborator',keep='last')

    # Query more future shift blocks
    for day in get_days_future( args.forward_interval ):
        futureShifts = scrapeWebPage( login, day, futureShifts )
    futureShifts = futureShifts.sort_values('day').drop_duplicates('collaborator',keep='first')

    #Cross-compare the two databases
    print( "Vetting shifters: " )
    vetShifters( pastShifts,  futureShifts, args.backward_interval, args.verbosity, args.filename )
    print( "Results written to file '{}'".format(args.filename))

    # Logout
    login.logout()

    print("All done!")


if __name__ == "__main__":
    main()
