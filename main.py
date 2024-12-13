from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler
import logging
import requests
from requests.adapters import HTTPAdapter
import boto3
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json


def extract_results(soup):
    main = soup.select_one("#main")

    res = []
    for gdiv in main.select('.g, .fP1Qef'):
        res.append(extract_section(gdiv))
    return res

def extract_section(gdiv):
    # Getting our elements
    title = gdiv.select_one('h3')
    link = gdiv.select_one('a')
    description = gdiv.find('.BNeawe')
    return {
        # Extract title's text only if text is found 
        'title': title.text if title else None,

        'link': extract_href(link['href']) if link else None,
        'description': description.text if description else None
    }

def extract_href(href):
    url = urlparse(href)
    query = parse_qs(url.query)
    if not ('q' in query and query['q'] and len(query['q']) > 0):
        return None
    return href,query['q'][0]

def start_gatewayinit():
    
    gatewayiniturl = ""  # Enter an AWS gateway here
    
    # Assign gateway to session
    session = requests.Session()
    
    # Mount the HTTPAdpater object to the session
    session.mount('https://', adapter)

    return session
    
def start_gatewayshutdown(gatewayinit):
    
    gatewayshutdown = start_gatewayinit(gatewayinit)
    # Delete gateways
    gatewayshutdown.shutdown()

class EndProgramException(Exception):
    pass

def display_message(console, message):
    # Print a message to the console
    console.print(message)

if __name__ == '__main__':
    
    # Start the rich console
    console = Console()
    
    # Make rich.console the default traceback handler
    install()
    FORMAT = "%(message)s"
    logging.basicConfig(
    level="ERROR", format=FORMAT, datefmt="[%X]", handlers=[RichHandler(rich_tracebacks=True)])
    
    # AWS STUFF
    # Authentication via aws-shell config file
    console.print("Configuring API")
    session = boto3.Session(profile_name='default')
    session.resource('s3')
    
    # Create an HTTPAdapter object and configure connection pooling and retries
    adapter = HTTPAdapter(pool_connections=20, pool_maxsize=5, max_retries=3)
    
    session = start_gatewayinit()
    # AWS STUFF DONE
    console.print("Success")
    
    
    try:
        
        #query = input("Search: ")
        query = 'cats'
        file_path = "results.html" 
        console.print("Sending request")
        response = session.get("https://www.google.com/search?q=" + query)
        
        print("RESPONSE ", response.status_code)
        
        soup = BeautifulSoup(response.text, 'html.parser')

        console.print("Extracting results")
        res = extract_results(soup)
       
        with open('results.json', "w") as outfile:
            json.dump(res, outfile)
        
        console.print(res)
        console.print("\n( ͡° ͜ʖ ͡°)👍 Your did it")
        
        
    except EndProgramException:
        console.print_exception("Ending program.")
        
    except Exception as e:
        console.print_exception(f"An error occurred: {e}")
    
