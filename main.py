from googlesearch import search
from rich.console import Console
import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS
from dotenv import load_dotenv
import os

def start_gatewayinit():
    
    gatewayiniturl = "https://08e7900et4.execute-api.us-east-2.amazonaws.com"
    
    gatewayinit = ApiGateway(gatewayiniturl)
    gatewayinit.start()

    # Assign gateway to session
    session = requests.Session()
    session.mount(gatewayiniturl, gateway)
    
    # Send request (IP will be randomised)
    response = session.get(gatewayiniturl, params={"theme": "light"})
    
    console.print(response.status_code)
    
    return gatewayinit
    
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
    
    load_dotenv() 
    
    ID = os.getenv("ID")
    KEY = os.getenv("KEY")
 
    console = Console()
    
    gateway = ApiGateway("https://www.google.com", regions="us-east-2", access_key_id=ID,access_key_secret=KEY)
    gateway.start()
    session1 = requests.Session()
    
    file_path = "results.csv" 
    data = []
    
    start_gatewayinit()

    try:
        session1.mount("https://www.google.com", gateway)
        session1.get("https://www.google.com/search?q=test")
        
        for result in session1:
            
            href = result  # Assuming result is a URL string
            text = "N/A"  # Placeholder, as googlesearch typically returns just URLs
            title = result
            description = result
            
            with open(file_path, 'w', newline='') as text_file:
                data.append({'link': href,'\n' 'text': text,'\n' 'title': title,'\n' 'description': description})
                
    except EndProgramException:
        console.print("Ending program.")
        start_gatewayshutdown()
        
    except Exception as e:
        console.print(f"An error occurred: {e}")
        start_gatewayshutdown()
        
    start_gatewayshutdown()