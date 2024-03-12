import pandas as pd

from scripts.weblogin import WebLogin

from scripts.time_manager import get_days_past, get_today, get_today_str, str2dt

from scripts.scrapeutil import scrapeExperts
 
from scripts.arguments import sel_arguments


def main():

    args = sel_arguments()

    # Connect to the ecl website
    login = WebLogin()

    # Populate the base dataframe for the current month
    thisMonth = pd.DataFrame(columns=["day", "shift_type", "collaborator"])
    thisMonth = scrapeExperts( login, get_today_str(), thisMonth )

    # Split the current months based on 'today' to look only in the past
    pastShifts = thisMonth[thisMonth.day<=get_today()]

    # Query more past shfits blocks
    for day in get_days_past( args.backward_interval ):
        pastShifts = scrapeExperts( login, day, pastShifts )

    # Logout
    login.logout()
    
    pastShifts.to_csv("expert_shifts.csv")

    print("All done!")


if __name__ == "__main__":
    main()
