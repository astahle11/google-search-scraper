from googlesearch import search
from rich.console import Console
import csv
import requests
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS, ALL_REGIONS

def gatewayinit(gateway):
    
    gatewayurl = "https://apitest.com/path/parts"
    targeturl = "https://google.com"
    
    gateway = ApiGateway(gatewayurl)
    gateway.start()

    # Assign gateway to session
    session = requests.Session()
    session.mount(gatewayurl, gateway)
    
    # Send request (IP will be randomised)
    response = session.get(gatewayurl, params={"theme": "light"})
    
    print(response.status_code)
    
    return gateway
    
def gatewayshutdown():
    
    gateway = gatewayinit()
    # Delete gateways
    gateway.shutdown()

class EndProgramException(Exception):
    pass

def display_message(console, message):
    # Print a message to the console
    console.print(message)

if __name__ == '__main__':
    console = Console()
    query = 'Cats'  # Hardcoded query for this example; replace with input if needed
    num_results = 3
    data = []

    try:
        search_results = list(search(query, num_results, safe=True, advanced=True))

        file_path = "results.csv" 
        
        
        for result in search_results:
            href = result  # Assuming result is a URL string
            text = "N/A"  # Placeholder, as googlesearch typically returns just URLs
            title = result
            description = result
            
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file)
                data.append({'link': href,'\n' 'text': text,'\n' 'title': title,'\n' 'description': description})
                for row in data:
                    writer.writerow(data)
                
    except EndProgramException:
        console.print("Ending program.")
    except Exception as e:
        console.print(f"An error occurred: {e}")