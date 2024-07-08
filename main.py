import logging
import json

import requests
from requests.adapters import HTTPAdapter

import boto3

from bs4 import BeautifulSoup

from urllib.parse import urlparse, parse_qs

from rich.console import Console
from rich.traceback import install
from rich.logging import RichHandler

def advance_page(console, soup, pages_scraped):
    console.print("Attempting to advance page...")
        
    parent_div = soup.find('body', jsmodel="hspDDf")
        
    if parent_div:
        child_div = parent_div.find('div', class_='child')
        if child_div:
            nested_div = child_div.find('div', class_='nested')
            if nested_div:
                nested_a = nested_div.find('a')
                if nested_a:
                    print("Found nested <a> tag:")
                    print("Text:", nested_a.text)
                    print("URL:", nested_a['href'])
                else:
                    print("No <a> tag found inside nested <div>.")
            else:
                print("No 'nested' <div> found.")
        else:
            print("No 'child' <div> found.")
    else:
        print("No 'parent' <div> found.")
        
    next_link = soup.find('div', style="display:block")
    next_url = next_link['href']
    requests.get(next_url)
    
    return
    

def extract_results(soup):
    main = soup.select_one("#main")

    res = []
    for gdiv in main.select(".g, .fP1Qef"):
        res.append(extract_section(gdiv))
    return res


def extract_section(gdiv):
    # Getting our elements
    title = gdiv.select_one("h3")
    link = gdiv.select_one("a")
    description = gdiv.find(".BNeawe")
    return {
        # Extract title's text only if text is found
        "title": title.text if title else None,
        "link": extract_href(link["href"]) if link else None,
        "description": description.text if description else None,
    }


def extract_href(href):
    url = urlparse(href)
    query = parse_qs(url.query)
    if not ("q" in query and query["q"] and len(query["q"]) > 0):
        return None
    return href, query["q"][0]


def start_gatewayinit():
    # Assign gateway to session
    session = requests.Session()

    adapter = HTTPAdapter(pool_connections=20, pool_maxsize=5, max_retries=3)

    # Mount the HTTPAdpater object to the session
    session.mount("https://", adapter)

    return session


class EndProgramException(Exception):
    pass


def display_message(console, message):
    # Print a message to the console
    console.print(message)


def main():
    print("Initializing...")

    console = Console()

    install()  # Make rich.console the default traceback handler
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="ERROR",
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )

    console.print("Configuring API")  # Authentication via aws-shell config file
    session = boto3.Session(profile_name="default")
    session.resource("s3")

    session = start_gatewayinit()
    # AWS STUFF DONE
    console.print("Success")

    try:
        max_pages = 5
        pages_scraped = 0
        # query = input("Search: ")
        query = "cats"
        console.print("Sending request")
        response = session.get("https://www.google.com/search?q=" + query)

        print("RESPONSE", response.status_code)

        while pages_scraped < max_pages:
            soup = BeautifulSoup(response.text, "lxml")

            console.print("Extracting results")
            res = extract_results(soup)
            console.print("Results extracted")
            
            try:
                advance_page(console, soup)
                pages_scraped + 1
                console.print("Page advanced")
                
            except Exception as e:
                console.print(f"An error occurred: {e}")
            
        try:
            # Serialize Python object (res) to JSON string
            pretty_json = json.dumps(res, indent=4)
            
            # Write JSON stirng to file
            with open("results.json", "w") as outfile:
                json.dump(pretty_json, outfile)
                
                console.print("results.json written successfuly")
                
        except json.JSONDecodeError as e:
            console.print(f"Error decoding JSON: {e}")

        console.print(res)
        console.print("\n( ͡° ͜ʖ ͡°)👍 Your did it")

        input("Press any key to continue")

    except EndProgramException:
        console.print_exception("Ending program.")

    except Exception as e:
        console.print_exception(f"An error occurred: {e}")


if __name__ == "__main__":
    while True:
        main()
        # Ask the user if they want to restart the program
        restart = input("Rerun script? (y/n): ").strip().lower()
        if restart != "n":
            break
