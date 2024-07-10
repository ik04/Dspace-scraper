'''
Plan: first scrape the stuff in a desirable manner, then use fastapi to connect it to kaizen tests section,
firts fetch the results and onclick fetch the file
'''
from bs4 import BeautifulSoup
import requests

def fetch_results():
    url = "http://dspace.srmist.edu.in/dspace/simple-search?query=Human+Resource+Management"

    content = requests.get(url=url)
    soup = BeautifulSoup(content.text,"lxml")
    results = soup.find_all("td",class_=["evenRowOddCol","oddRowOddCol"])
    data = []
    for result in results:
        details = {"date":"","title":"","link":"","author":""}
        details["title"] = result.a.contents[0]
        details["link"] = result.a["href"]
        prev_td = result.previous_sibling.previous_sibling
        next_td = result.next_sibling.next_sibling
        if prev_td is not None:
            details["date"] = prev_td.text.strip()
        if next_td is not None:
            details["author"] = next_td.text.strip()
        data.append(details)
    print(data)

def fetch_file():
    selected_url = "http://dspace.srmist.edu.in/dspace/handle/123456789/1257"
    content = requests.get(url=selected_url)
    soup = BeautifulSoup(content.text,"lxml")
    file = soup.find("td",class_="standard")
    file_link = file.a["href"]
    print(file_link)

fetch_file()