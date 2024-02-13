"""
Customer and Trial Creation, Editing and Deletion
-----------------------------
This script shows a example on how to create new customers (in this case trials, not paid, though possible), edit them, and delete them.
If everything is run sequentially without stopping the dashboard won´t reflect anything, as the customer is deleted as a last step. 
"""
#
# Imports
#
import requests
from requests.auth import HTTPBasicAuth
import json

#
# API Details
# -- As a best practice consider loading this from environment variables in a secure fashion. This script has been simplified for educational purposes  
mssp_key = "mssp_key"                      # < SUBSTITUTE MSSP API Key                                     
mssp_secret = "mssp_secret"                   # < SUBSTITUTE MSSP Token    
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
Creates a new customer in the MSP dashbaord
"""
def create_customer(jwtToken, customer_parameters) -> dict:
    url = "https://api.umbrella.com/admin/v2/providers/customers"
    
    headers = {'Authorization': 'Bearer {}'.format(jwtToken), "Accept": "application/json"}

    # Create Request's session if not yet created and update headers with jwtToken
    session = requests.Session()
    session.headers.update(headers)
    
    r = session.post(url, data = customer_parameters, verify=True, timeout=60)
    
    return r.json()

"""
Update to paid customer in the MSP dashbaord
"""
def update_paid_customer(jwtToken, customer_parameters, customerId) -> dict:
    url = "https://api.umbrella.com/admin/v2/providers/customers/"+str(customerId)
    
    headers = {'Authorization': 'Bearer {}'.format(jwtToken), "Accept": "application/json"}

    # Create Request's session if not yet created and update headers with jwtToken
    session = requests.Session()
    session.headers.update(headers)
    
    r = session.put(url, data = customer_parameters, verify=True, timeout=60)
    
    return r.json()

"""
Update a trial customer in the MSP dashbaord
"""
def update_customer(jwtToken, customer_parameters, customerId) -> dict:
    url = "https://api.umbrella.com/admin/v2/providers/customers/"+str(customerId)
    
    headers = {'Authorization': 'Bearer {}'.format(jwtToken), "Accept": "application/json"}

    # Create Request's session if not yet created and update headers with jwtToken
    session = requests.Session()
    session.headers.update(headers)
    
    r = session.put(url, data = customer_parameters, verify=True, timeout=60)
    
    return r

"""
Delete a customer in the MSP dashbaord
"""
def delete_customer(jwtToken, customerId):
    url = "https://api.umbrella.com/admin/v2/providers/customers/"+str(customerId)
    
    headers = {'Authorization': 'Bearer {}'.format(jwtToken), "Accept": "application/json"}

    # Create Request's session if not yet created and update headers with jwtToken
    session = requests.Session()
    session.headers.update(headers)
    
    r = session.delete(url, data = customer_parameters, verify=True, timeout=60)
    
    return r
#
# Main - Logic
#
if __name__ == "__main__":

    #Define parameters for the new customer to be created
    customer_parameters = {
        "licenseType": "msla",
        "isTrial": True,
        "packageId": 248,
        "seats": 9,
        "city": "asdf",
        "countryCode": "12",
        "customerName": "API Test",
        "dealId": None,
        "state": "asdf",
        "streetAddress": "asdf",
        "streetAddress2": "asdf",
        "zipCode": "adsf",
        "adminEmails": ['asdf@cisco.com','asdf@csico.com'],
        "ccwDealOwnerEmails": ['asdf@cisco.com', 'asdf@cisco.com']
    }
    # Get the Umbrella token for authentication
    mssp_token = get_token(mssp_key, mssp_secret, mssp_id)

    # Create a new customer trial in the MSP dashboard
    resp = create_customer(mssp_token, customer_parameters)
    new_customerId = resp['customerId']
    print('Customer created...')

    # Update customer
    new_customer_parameters = {
        "packageId": 248,
        "seats": 90,
        "city": "asdf",
        "countryCode": "12",
        "customerName": "API Test",
        "dealId": None,
        "state": "asdf",
        "streetAddress": "asdf",
        "streetAddress2": "asdf",
        "zipCode": "adsf",
        "adminEmails": ['asdf@cisco.com','asdf@csico.com'],
        "ccwDealOwnerEmails": ['asdf@cisco.com', 'asdf@cisco.com']
    }
    update_customer(mssp_token, new_customer_parameters, new_customerId)
    print('Customer Updated...')

    # Delete customer
    delete_customer(mssp_token, new_customerId)
    print('Customer deleted...')


