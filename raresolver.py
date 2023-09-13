import requests
import sys

def test_https_redirection(url, headers=False):
    # Make sure the URL starts with http:// to ensure it's not already HTTPS
    if not url.startswith('http://'):
        url = 'http://' + url

    try:
        if headers == True:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                        }
        else:
            headers = {}
        response = requests.get(url, headers=headers, allow_redirects=True)

        # Check if the final URL is HTTPS
        if response.url.startswith('https://'):
            return True, [res.status_code for res in response.history]
        else:            
            return False, False
        
    except requests.RequestException as e:
        print(f"Error while checking {url}: {e}")
        return False, False



def return_clean_str_web():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <website_url_without_http_or_https>")
        sys.exit(1)
    
    url_to_test = sys.argv[1]
    url = url_to_test.replace("http://", "").replace("https://", "")
    
    return url


def main():
    url_to_test = return_clean_str_web()
    print(f"Starting to test the webpage: {url_to_test}")
    
    redi, statuses = test_https_redirection(url_to_test)
    if redi:
        print(f"{url_to_test} redirects to HTTPS correctly!")
        if statuses:
            print(f"Satuses: {statuses}")
    else:
        redi, statuses =test_https_redirection(url_to_test, headers=True)
        if redi:
            print(f"{url_to_test} DOES redirect to HTTPS, but only with browser headers.")  
            if statuses:
                print(f"Satuses: {statuses}")            
        else:
            print(f"{url_to_test} does NOT redirect to HTTPS.")
         

if __name__ == '__main__':
    main()

