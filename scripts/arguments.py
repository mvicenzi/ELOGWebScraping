import argparse


def sel_arguments():

    parser = argparse.ArgumentParser(description='Shift vetting tool usage')
    parser.add_argument('backward_interval', metavar='bwk', type=int, help='Number of months for the query of past shifters', default=6, nargs='*')
    parser.add_argument('forward_interval', metavar='frw', type=int, help='Number of months for the query of future shifters', default=3, nargs='*')
    parser.add_argument('verbosity', metavar='v', type=int, help='How much information print to screen and save to screen', default=0, nargs='*')
    parser.add_argument('filename', metavar='f', type=str, help='Name of file where to save the information of the query', default='vetted_shifters.txt', nargs='*')

    args = parser.parse_args()

    # readback the arguments set
    loglevels = [ "Only shifters that needs to take a shadow shift are reported",
               "Also shifters that scheduled a shadow shift are reported",
               "All shifters for the next {} months are reported".format(args.forward_interval) ]

    print( "Today is {}".format( get_today_str() ) )
    print( "Vet shifters signed for the next {} months.".format(args.forward_interval) )
    print( "Shifters has to be on a shift in the past {} months.".format(args.backward_interval) )
    print( "Verbosity level is {}: ".format(args.verbosity, loglevels) )
    
    return args