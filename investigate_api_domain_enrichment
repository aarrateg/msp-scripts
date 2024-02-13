"""
Leveraging Umbrella Investigate Programmatically
-----------------------------
This script shows a example on how to interact via API with Umbrella Investigate. The starting point is just knowing a domain, we end up
knowing lots of details around the attributes of that domain. Some possible use cases (not limited to):

    - A customer asking why a domain was blocked. They need it working and you affected their production. Show to your customer why the decision was taken with
    the data provided by Investigate. You can then whitelist it and dispute the categorization if required.

    - A 3rd party tool reports a domain as malicious but you are not given any details. Leverage investigate to enrich what you know and take data driven actions
"""

#
# Imports
#
import requests
import datetime


#
# API Details
# -- As a best practice consider loading this from environment variables in a secure fashion. This script has been simplified for educational purposes  
#                                             
investigate_token = 'investigate_token' # < SUBSTITUTE Umbrella Investigate Token 


#
# Methods
#
"""
Retrieves domain categorization
"""
def investigate_domain_categorization(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/domains/categorization/"+_domain+"?showLabels"    
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return  response.json()

"""
Retrieves domain volume
"""
def investigate_domain_volume(_investigate_token, _domain, _start, _stop):
    url = "https://investigate.api.umbrella.com/domains/volume/"+_domain    
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    parameters = {'start':_start, 'stop':_stop}
    response = requests.get(url, verify=True, timeout=60, headers = headers, params = parameters)
    return response.json()

"""
Retrieves domain coocurrences
"""
def investigate_domain_coocurrences(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/recommendations/name/"+_domain+".json"   
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return response.json()

"""
Retrieves domain related domains
"""
def investigate_domain_related_domains(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/links/name/"+_domain   
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return response.json()

"""
Retrieves domain's tagging timeline
"""
def investigate_domain_tagging_timeline(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/timeline/"+_domain   
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return response.json()

"""
Retrieves domain security score
"""
def investigate_domain_security_score(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/security/name/"+_domain   
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return response.json()


"""
Retrieves domain whois information
"""
def investigate_domain_whois(_investigate_token, _domain):
    url = "https://investigate.api.umbrella.com/whois/"+_domain   
    headers = {'Authorization': 'Bearer {}'.format(_investigate_token), "Accept": "application/json"}
    response = requests.get(url, verify=True, timeout=60, headers = headers)
    return response.json()


"""
Print all the inrfomation I have for a domain in a user friendly maneer
"""
def whatDoIKnow(data):
    
    print('Domain: '+data['domain'])
    
    try:
        check = data['categorization']
        print('------------------')
        print('Security Categories: '+str(data['categorization'][data['domain']]['security_categories']))
        print('Content Categories: '+str(data['categorization'][data['domain']]['content_categories']))
        
        try:
            check = data['volume']
            print('------------------')
            print('Requests to the domain in the last 7 days:')
            print('\t- Total: '+str(sum(data['volume']['queries'])))
            print('\t- Av. per Hour: '+str(round(sum(data['volume']['queries'])/len(data['volume']['queries']),2)))
            print('\t- Max. per Hour: '+str(max(data['volume']['queries'])))        
            try:
                check = data['coocurrences']
                print('------------------')
                if data['coocurrences']['found']:
                    print('Co-ocurrences found: '+str(data['coocurrence']['pfs2']))
                else:
                    print('No Co-ocurrences found')
                try:
                    check = data['related']
                    print('------------------')
                    if data['related']['found']:
                        print('Related Domains found: '+str(r['pfs2']))
                    else:
                        print('No Related Domains found')
                    try:
                        check = data['tagging']
                        print('------------------')
                        if len(data['tagging']) > 0:
                            print('First category assigned')
                            print('\t- Date: '+str(datetime.datetime.fromtimestamp(data['tagging'][len(data['tagging'])-1]['timestamp']/1000).strftime("%Y-%m-%d")))
                            print('\t- Categories: '+str(data['tagging'][len(data['tagging'])-1]['categories']) )
                            print('Last category assigned')
                            print('\t- Date: '+str(datetime.datetime.fromtimestamp(data['tagging'][0]['timestamp']/1000).strftime("%Y-%m-%d")))
                            print('\t- Categories: '+str(data['tagging'][0]['categories']) )

                            category_history = []
                            attack_history = []
                            threat_history = []
                            for tag in data['tagging']:
                                category_history.extend(tag['categories'])
                                attack_history.extend(tag['attacks'])
                                threat_history.extend(tag['threatTypes'])

                            print('Categories assigned overtime: '+ str(set(category_history)))
                            print('Threats assigned overtime: '+ str(set(threat_history)))
                            print('Attacks assigned overtime: '+ str(set(attack_history)))
                        else:
                            print('No tagging timeline')
                        try:
                            check = data['security']
                            print('------------------')
                            print('Security Scores')
                            print('\t Associated Threats')
                            if data['security']['found']:
                                print('\t\t- Threat linked: '+str(data['security']['threat_type']))
                                print('\t\t- Attacks linked: '+str(data['security']['attack']))
                            else:
                                print('\t\t- Not found associated threats to the domain')

                            print('\t Algoritmical Generation Likelihoodness')
                            print('\t\t- DGA: '+str(data['security']['dga_score']*-1)+' %')
                            print('\t\t- Perplexity: '+str(data['security']['dga_score']*-1)+' %')

                            print('\tInternet Metrics:')
                            print('\t\t- Suspiciousness IP lookup behavior based: '+str(data['security']['securerank2']))
                            print('\t\t- Popularity based on Google: '+str(data['security']['pagerank']))
                            print('\t\t- ASN Score: '+str(data['security']['asn_score']))
                            print('\t\t- Suspiciousness of IP Prefix: '+str(data['security']['prefix_score']*-1)+' %')
                            print('\t\t- Suspiciousness of RIP Score: '+str(data['security']['rip_score']*-1)+' %')
                            print('\t\t- Domain popularity (Unique visitor IPs): '+str(round(data['security']['popularity'],2)))


                            print('\tGeographical Information:')
                            print('\t\t- Distance from physical locations serving the name from each other: '+str(data['security']['geoscore']))
                            if data['security']['ks_test'] == 0:
                                print('\t\t- Traffic matches what is expected for its TLD')
                            else:
                                print('\t\t- Traffic DOES NOT match what is expected for its TLD')

                            print('\t\t- Requester country list: ')
                            for requester in data['security']['geodiversity']:
                                print('\t\t\t'+str(requester[0])+' - '+str(requester[1]*100)+' %')
                            try:
                                check = data['whois']
                                print('------------------')
                                print('The domain was registered in '+data['whois']['registrantCountry'])
                                print('Administrative contact: '+data['whois']['administrativeContactName'])
                                print('Registrant:')
                                print('\tOrganization: '+data['whois']['registrantOrganization'])
                                print('\tEmail: '+data['whois']['registrantEmail'])
                                print('\tPhone: '+data['whois']['registrantTelephone'])
                                if r['recordExpired']:
                                      print('The record is EXPIRED')
                                else:
                                    print('The record has NOT expired')



                            except:
                                    pass    
                            
                        except:
                                pass
                    except:
                            pass
                except:
                        pass
            except:
                    pass
        except:
            pass
    except:
        pass


#
# Main - Logic
#
if __name__ == "__main__":

    # Define the domain to investigate
    domain = "primusth.com"
    data = {'domain': domain}

    #What do I know? Initially
    print('Intially all I can say is...')
    whatDoIKnow(data)

    print('\n\nEnriching with Umbrella Investigate API...\n\n')
    

    #Umbrella Investigate Enrichment
    data['categorization'] = investigate_domain_categorization(investigate_token, domain)
    data['volume'] = investigate_domain_volume(investigate_token, domain,'-7days','now')
    data['coocurrences'] = investigate_domain_coocurrences(investigate_token, domain)
    data['related'] = investigate_domain_related_domains(investigate_token, domain)
    data['tagging'] = investigate_domain_tagging_timeline(investigate_token, domain)
    data['security'] = investigate_domain_security_score(investigate_token, domain)
    
    #What do I know? After the Umbrella Investigate enrichment
    print('After Umbrella Investigate API enrichment I can leverage all of the following data to take action upon:')

    whatDoIKnow(data)
