from datetime import date, datetime

from dateutil.relativedelta import relativedelta

def str2dt( strday ):
	return datetime.strptime(strday, "%Y-%m-%d")

def dt2str( day ):
	return day.strftime("%Y-%m-%d") 

def get_today_str():
	return dt2str( date.today() )

def get_today():
	return str2dt( get_today_str() )

def get_days_past( interval_months=6 ):
	"""
	Get an array of days starting from 'today' 
	backwards in time of the selected interval in months
	"""
	today = date.today()
	days = [ dt2str(today-relativedelta(months=i)) for i in range(1,interval_months+1) ]

	return days 

def get_days_future( interval_months=3 ):
	"""
	Get an array of days starting from 'today' 
	forward in time of the selected interval in months
	"""

	today = date.today()
	days = [ dt2str(today+relativedelta(months=i)) for i in range(1,interval_months+1) ]

	return days 

