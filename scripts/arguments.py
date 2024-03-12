import argparse

from scripts.time_manager import get_today_str


def sel_arguments():

    parser = argparse.ArgumentParser(description='Shift vetting tool usage')
    parser.add_argument('--backward_interval', metavar='-bwk', type=int, help='Number of months for the query of past shifters (number of months from today)', default=6)
    parser.add_argument('--forward_interval', metavar='-frw', type=int, help='Number of months for the query of future shifters (number of months from today)', default=3)
    parser.add_argument('--verbosity', metavar='-v', type=int, help='How much information print to screen and save to screen (levels: 0 to 2)', default=0)
    parser.add_argument('--filename', metavar='-f', type=str, help='Name of file where to save the information of the query', default='vetted_shifters.txt')
    args = parser.parse_args()

    # readback the arguments set
    loglevels = [ "Only shifters that needs to take a shadow shift are reported",
               "Also shifters that scheduled a shadow shift are reported",
               "All shifters for the next {} months are reported".format(args.forward_interval) ]

    print( "Today is {}".format( get_today_str() ) )
    print( "Vet shifters signed for the next {} months.".format(args.forward_interval) )
    print( "Shifters has to be on a shift in the past {} months.".format(args.backward_interval) )
    print( "Verbosity level is {}: \n".format(args.verbosity, loglevels) )
    
    return args
