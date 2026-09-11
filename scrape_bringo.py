import requests

company_number = "14157624"
url = f"https://bringo.co.uk/company/{company_number}"
response = requests.get(url, verify=False)
print("STATUS:", response.status_code)
print(response.text[:2000])