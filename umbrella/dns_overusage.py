"""
DNS Overusage Report
-----------------------------
This script shows a example on how to find customers with an overusage for Umbrella. The computation is based in the current formula used by Umbrella, which can be found in here:
    https://docs.umbrella.com/deployment-umbrella/docs/limitations-and-range-limits 
"""
#
# Imports
#
import requests
from requests.auth import HTTPBasicAuth
import json
import math
import datetime

#
# API Details
# -- As a best practice consider loading this from environment variables in a secure fashion. This script has been simplified for educational purposes  
mssp_key = "mssp_key"                      # < SUBSTITUTE MSSP API Key                                     
mssp_secret = "msSp_secret"                   # < SUBSTITUTE MSSP Token    
mssp_id = XXXXXXX                                                  # < SUBSTITUTE MSSP Console id


#
# Methods
#

"""
Retrieves the necessary token to authenticate the Umbrella API calls
"""
def get_token(key:str, secret:str, org_id:int) -> str:
                               
    session = requests.Session()
    payload = ""    
    
    # If org_id is passed then add X-Umbrella-OrgID header with OrgID
    if org_id:
        headers = {'X-Umbrella-OrgID': str(org_id), "Content-Type": "application/json"}
    else:
        headers = {'Content-Type': 'application/json'}
    
    url = "https://api.umbrella.com/auth/v2/token"
    
    session.headers.update(headers)
    # Post to obtain token
    r = session.post(url, auth=HTTPBasicAuth(key, secret),data=payload)

    # Extract Token from Response Payload
    jwtToken = json.loads(r.text)["access_token"]
    
    return jwtToken

"""
Retrieves the customer list for the MSP
"""
def get_customer_list(jwtToken) -> dict:

    url = "https://api.umbrella.com/admin/v2/providers/customers"
    headers = {'Authorization': 'Bearer {}'.format(jwtToken), "Accept": "application/json"}

    session = requests.Session()
    session.headers.update(headers)
    
    r = session.get(url, verify=True, timeout=60)
    
    return r.json()

"""
Retrieves the activity (requests volume) for each of the customers of the MSP
"""
def get_customers_activity(jwtToken, from_, to_, limit_) -> dict:

    url = "https://api.umbrella.com/reports/v2/providers/requests-by-org"
    headers = {'Authorization': 'Bearer {}'.format(jwtToken),
               "Accept": "application/json",
              }
    
    payload = {'from' : from_,
             'to' : to_,
             'limit': limit_}

    session = requests.Session()
    session.headers.update(headers)
    
    r = session.get(url, params=payload, verify=True, timeout=60)
    
    return r.json()

"""
Generates a timestamp that corresponds with the beggining of the month
"""
def get_firstDayMonth_timestamp():
    now = datetime.datetime.now()
    # Get the first day of the current month
    first_day = datetime.datetime(now.year, now.month, 1, 0, 0, 0)
    # Convert to timestamp
    return str(int(first_day.timestamp()*1000))

"""
Returns the number of days past for the ongoing month
"""
def get_dayOfMonth():
    return (datetime.datetime.today() - datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, 1, 0, 0, 0)).days
"""
Prints the details of a organization with overusage in a user friendly maneer
"""
def report_overusage(org):
    print('Organization '+org['customerName']+' exceeded seat usage by '+str(org['seatUtilization'])+'%')
    print('\tUpsell opportunity: '+str(org['consumedSeats']-org['seats']) +' seats')


#
# Main - Logic
#
if __name__ == "__main__":

    # Get the Umbrella token for authentication
    mssp_token = get_token(mssp_key, mssp_secret, mssp_id)
    # Get the customer list for the MSP
    mssp_customer_list = get_customer_list(mssp_token)
    # Generate the first day's of the month timestamp
    first_day_moth_timestamp = get_firstDayMonth_timestamp()
    # Compute current day of the month
    dayOfMoth = get_dayOfMonth()
    # Get the activity for customers from the first day of the month to now
    activity_response = get_customers_activity(mssp_token,first_day_moth_timestamp,'now','200')['data']

    # Build a dictionary for the customer list in which to merge all retrieved data for customers
    over_usage_check = {}

    for customer in mssp_customer_list:
        customer_ = {}
        customer_['customerName'] = customer['customerName']
        customer_['customerId'] = customer['customerId']
        customer_['seats'] = customer['seats']
        customer_['isTrial'] = customer['isTrial']
        customer_['monthlyTopRequests'] = customer['seats']*31*5000
        customer_['totalRequests'] = 0
        customer_['consumedSeats'] = 0
        customer_['seatUtilization'] = 0
        
        over_usage_check[customer['customerId']] = customer_


    for org in activity_response:
        over_usage_check[org['organization']['id']]['totalRequests'] = org['counts']['total']
        over_usage_check[org['organization']['id']]['consumedSeats'] = math.ceil(org['counts']['total']/dayOfMoth/5000)
        over_usage_check[org['organization']['id']]['seatUtilization'] =  100 * math.ceil(org['counts']['total']/dayOfMoth/5000)/over_usage_check[org['organization']['id']]['seats']

    #Print the over usage report for those customers exceeding a 100% seat utilization
    for org in over_usage_check.keys():
        if over_usage_check[org]['seatUtilization'] > 100:
            report_overusage(over_usage_check[org])
            print()
