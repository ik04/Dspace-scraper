from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests

app = FastAPI()

class Result(BaseModel):
    query: str

@app.post("/fetch_results/")
# ! this is only the first page -_-
async def fetch_results(query: Result,page:int = 0):
    query_string = "+".join(query.query.split())
    start = page * 10
    url = f"http://dspace.srmist.edu.in/dspace/simple-search?query={query_string}&start={start}"
    content = requests.get(url)
    soup = BeautifulSoup(content.text, "lxml")
    results = soup.find_all("td", class_=["evenRowOddCol", "oddRowOddCol"])
    data = []
    for result in results:
        details = {"date": "", "title": "", "link": "", "author": ""}
        details["title"] = result.a.contents[0]
        details["link"] = result.a["href"]
        prev_td = result.previous_sibling.previous_sibling
        next_td = result.next_sibling.next_sibling
        if prev_td is not None:
            details["date"] = prev_td.text.strip()
        if next_td is not None:
            details["author"] = next_td.text.strip()
        data.append(details)
    return {"results":data}

@app.post("/fetch_file/")
async def fetch_file(request: Request):
    data = await request.json()
    selected_url = data.get("link")
    if not selected_url:
        raise HTTPException(status_code=400, detail="Missing 'file_link' parameter.")
    
    content = requests.get(url=f"http://dspace.srmist.edu.in{selected_url}")
    soup = BeautifulSoup(content.text, "lxml")
    file = soup.find("td", class_="standard")
    file_link = file.a["href"]
    return {"file_link": file_link}
