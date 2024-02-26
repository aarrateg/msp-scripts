#  MSP Guideline Scripts for Cisco Secure MSP Center - Umbrella

This repository contains individual standalone scripts that should only be used as educational reference by anyone accessing them. The scripts in here represent examples on how to leverage the API endpoints from Umbrella.  These scripts will not be maintained, and do not provide error handling techniques, their objective is to serve as an educational reference, it is the end user's responsibility to verify and guarantee the security of the code they use in their environment. 

--------------

## Brief Summary of Scripts:

- [**customer_creation_update_deletion.py:**](https://github.com/aarrateg/msp-scripts/blob/main/umbrella/customer_creation_update_deletion.py)<br>
Shows an example on how to create, update and delete a customer programmatically in the Umbrella MSP dashboard. Note that if run all together the creation and modifitcations in the dashboard wouldn´t be seen as the customer is deleted, it would be visible only in the Audit Logs of the MSP Dashbaord (Settings>Audit Log). This can enable use cases like auto trial setup from MSP's website. <br>Required API Scope: admin.customers:write

- [**dns_overusage.py:**](https://github.com/aarrateg/msp-scripts/blob/main/umbrella/dns_overusage.py)<br>
Shows an example on how to retrieve the seats assigned to MSP customers, and compute a seat estimation based on the traffic they generated for the ongoing month. This enables customer conversations to find out reasons for over usage (i.e., There was an increase of users in the customer's organization, hence the MSP is under billing, there is an upsell opportunity).<br>Required API Scope: reports.customers:read, admin.customers:read

- [**investigate_api_domain_enrichment.py:**](https://github.com/aarrateg/msp-scripts/blob/main/umbrella/investigate_api_domain_enrichment.py)<br>
Shows an example on how to enrich the information that we know aorund a domain by leveragiing the Umbrella Investigate API, available in the Umbrella Advantage package. This can be leveraged to show value and understanding to customers through detail threat reporting, but most importantly enables organizations to take data driven actions on the threats they encounter.



  
