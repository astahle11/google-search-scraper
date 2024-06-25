from googlesearch import search
from rich.console import Console
import csv

class EndProgramException(Exception):
    pass

def display_message(console, message):
    # Print a message to the console
    console.print(message)

if __name__ == '__main__':
    console = Console()
    query = 'Google'  # Hardcoded query for this example; replace with input if needed
    num_results = 3
    data = []

    try:
        search_results = list(search(query, num_results=num_results, safe=True, advanced=True))

        file_path = "data.csv"
            
        for result in search_results:
                with open(file_path, 'w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    href = result  # Assuming result is a URL string
                    text = "N/A"  # Placeholder, as googlesearch typically returns just URLs
                    title = result
                    description = result
                    data.append({'link': href,'\n' 'text': text,'\n' 'title': title,'\n' 'description': description})
                    for row in data:
                        writer.writerow(data)
                
    except EndProgramException:
        console.print("Ending program.")
    except Exception as e:
        console.print(f"An error occurred: {e}")