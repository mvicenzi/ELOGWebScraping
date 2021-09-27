# Introduction 



## Prerequisites and installation

For this project t is recommended the use of `phython version 3.9.1` or higher in a virtual environment: this can be easly created with `python3` doing: 
```shell
python -m env myenv
source myenv/bin/activate/
```
The scripts requires the python packages specified in the `requirements.txt` file. Packages can be easly installed using `pip`: 
```shell
pip install -r requirements.txt
```

Once the packages are successfully installed, it is important to edit the `scripts/config.py` with the `username` and `password` valid to access the [SBN-FD ELOG](https://dbweb8.fnal.gov:8443/ECL/sbnfd/E/index)

## Run the script 

The scripts is already configured to query the SBN-FD ELOG website, make a list of the ICARUS shifters who took shifts in the previous 6 months from the current date, and compare it the shifters that are on shift for the 3 months after. 
The collaborators who have not been on shift for the previous 6 months and who are not already scheduled for a shadow shift are printed to screen and saved to the file `vetted_shifters.txt`. 

To run the script using the standard configuration simpy do: 

```shell
python main.py

```
In case of error are returned, please verify the authorization credentials for the [SBN-FD ELOG](https://dbweb8.fnal.gov:8443/ECL/sbnfd/E/index) and the connection status. 

## Change intervals, verbosity, destination file

Passing the option `-h` or `--help` to the above command displays all the user configurable options: 
```shell
python main.py -h

usage: main.py [-h] [--backward_interval [-bwk ...]] [--forward_interval [-frw ...]] [--verbosity [-v ...]] [--filename [-f ...]]

Shift vetting tool usage

optional arguments:
  -h, --help            show this help message and exit
  --backward_interval [-bwk ...]
                        Number of months for the query of past shifters (number of months from today)
  --forward_interval [-frw ...]
                        Number of months for the query of future shifters (number of months from today)
  --verbosity [-v ...]  How much information print to screen and save to screen (levels: 0 to 2)
  --filename [-f ...]   Name of file where to save the information of the query

```
The interval over which the query for both previous and future shifters are fully configurable as well as they are the verbosity level and the name of the destination file.

## Request help

In case of help please contact Andrea Scarpelli (ascarpell@bnl.gov)
