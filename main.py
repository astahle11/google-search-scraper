from googlesearch import search
from rich.console import Console
import requests
from requests_ip_rotator import ApiGateway
from requests.adapters import HTTPAdapter
import boto3

def start_gatewayinit():
    
    gatewayiniturl = "https://qqrqi9ye9c.execute-api.us-east-2.amazonaws.com/dev"
    
    gatewayinit = ApiGateway(gatewayiniturl)
    gatewayinit.start()

    # Assign gateway to session
    session = requests.Session()
    
    # Mount the HTTPAdpater object to the session
    session.mount('https://', adapter)
    
    # Send request (IP will be randomised)
    console.print(f'Sending test request to {gatewayiniturl}...')
    response = session.get('https://google.com')
    console.print(response.status_code)
    
    return gatewayinit, session
    
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
    
    file_path = "results.txt" 
    data = []
    
    console = Console()
    
    #Authentication via aws-shell config file
    session = boto3.Session(profile_name='default')
    session.resource('s3')
    
    # Create an HTTPAdapter object and configure connection pooling and retries
    adapter = HTTPAdapter(pool_connections=20, pool_maxsize=5, max_retries=3)
    
    session = start_gatewayinit()

    try:
        session = requests.Session()
        session.mount('https://', adapter)
        response = session.get("https://www.google.com/search?q=test")

        console.print(response.text)
        
        write_response = response.text
        
        for result in response:
            
            href = result  # Assuming result is a URL string
            text = "N/A"  # Placeholder, as googlesearch typically returns just URLs
            title = result
            description = result
            
            with open(file_path, 'w', newline='') as text_file:
                data.append({'link': href,'\n' 'text': text,'\n' 'title': title,'\n' 'description': description})
                
    except EndProgramException:
        console.print("Ending program.")
        
    except Exception as e:
        console.print(f"An error occurred: {e}")
    