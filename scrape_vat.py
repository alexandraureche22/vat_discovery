import requests
from bs4 import BeautifulSoup
import time

#using the exact POST endpoint and form fiend name i found by inspecting the site's network tab
def search_vat(company_name):
    url = "https://vat-lookup.co.uk/verify/search.php"
    data = {"CompanyName": company_name}
    response = requests.post(url, data=data, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")

    # the page has multiple <table> elements (layout tables in the header),
    # so I can't just grab the first one — I look specifically for the
    # table whose header row contains "VAT Number"
    table = None
    for t in soup.find_all("table"):
        if "VAT Number" in t.get_text():
            table = t
            break
    #no table in the response means no results were returned at all
    if not table:
        return None
    # skip the header row (Company Name/VAT Number/Company ID)
    rows = table.find_all("tr")[1:]
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            continue
        found_name = cells[0].get_text(strip=True)
        vat_number = cells[2].get_text(strip=True)
        # also I noticed manually (and confirmed via the site's own
        # "About" page which mentions Levenshtein similarity) that this
        # source returns fuzzy/similar matches, not just exact ones
        # -searching "PIXAR LTD" also returned "PIXAR 55 LTD"
        # taking the first result blindly would risk grabbing the wrong
        # company's VAT number, so I only accept an exact name match here
        if found_name.upper() == company_name.upper():
            return vat_number
    return None

#i tested the companies i verified manually first, so I can compare the script's results against what
#i already found and confirm the logic is working correctly before scaling up to a larger sample
companies_to_check = [
    "AVE IT MEDIA LTD",
    "'B' SAFE ELECTRICAL SERVICES LIMITED",
    "BASICALLY PLANTS WILL SAVE US LIMITED",
    "00 ADVERTISING, LTD.",
    "AUDIO LIMITED",
    "00 BAR LIMITED",
    "00 CABS LIMITED",
    "107 STATION STREET LIMITED",
    "107 STORMONT ROAD LIMITED",
    "107 SUNNYHILL ROAD RTM COMPANY LTD",
    "ANGLIAN INTERNET LIMITED",
    "ANGLIAN INTUMESCENT LTD",
    "ANGLIAN IT LTD",
    "ANGLIAN KNIGHT LTD",
    "ANGLIAN PIPEWORK LTD",
    "BRU GLOBAL LIMITED",
    "BRU GROUP COVER LIMITED",
    "BRU HOLDINGS LTD",
    "BRU HOUSE COFFEE COMPANY LTD",
    "BRU HUB LTD",
    "BROWN FEATHER LTD",
    "BROWN FILMS (INDIAN SUMMER) LIMITED",
    "BROWN FILMS LIMITED",
    "BROWN FINANCIAL SERVICES LIMITED",
    "BROWN FINCH LIMITED",
]

for company in companies_to_check:
    vat = search_vat(company)
    print(f"{company}: {vat if vat else 'NOT FOUND'}")
    time.sleep(1)