import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0  Chrome/116.0.5845.187  Safari/16.5"

# Function to get all forms
def fetch_forms(page_url):
    soup = BeautifulSoup(session.get(page_url).content, "html.parser")
    return soup.find_all("form")

def extract_form_details(form):
    form_details={}
    action_url = form.attrs.get("action")
    method_type = form.attrs.get("method", "get")
    form_inputs = []

    for input_field in form.find_all("input"):
        input_type = input_field.attrs.get("type", "text")
        input_name = input_field.attrs.get("name")
        input_value = input_field.attrs.get("value", "")
        form_inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    form_details['action'] = action_url
    form_details['method'] = method_type
    form_details['inputs'] = form_inputs
    return form_details

def is_vulnerable(response):
    known_errors = {"Improperly terminated quoted string",
              "Unclosed quotation mark after the string",
              "SQL syntax error detected"
              }
    for error in known_errors:
        if error in response.content.decode().lower():
            return True
        return False
    
def scan_for_sqli(target_url):
    forms_on_page = fetch_forms(target_url)
    print(f"[+] Detected {len(forms_on_page)} forms on {target_url}.")

    for form in forms_on_page:
        form_info = extract_form_details(form)

        for quote in "\"'":
            data = {}
            for input_field in form_info["inputs"]:
                if input_field["type"] == "hidden" or input_field["value"]:
                    data[input_field['name']] = input_field["value"] + quote
                elif input_field["type"]  != "submit":
                    data[input_field['name']] = f"test{quote}"

            print(target_url)
            extract_form_details(form)

            if form_info["method"] == "post":
                response = session.post(target_url, data=data)
            elif form_info["method"] == "get":
                response = session.get(target_url, params=data)
            if is_vulnerable(res):
                print("SQL Injection vulnerability detected in URL: ", target_url)
            else:
                print("No SQL Injection vulenrability detected")
                break

if __name__ == "_main__":
    url_to_check = "https://url.com"
    scan_for_sqli(url_to_check)