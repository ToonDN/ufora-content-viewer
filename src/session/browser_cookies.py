import browser_cookie3
import grequests
from config import browsers

url = 'https://ufora.ugent.be/d2l/api/lp/1.26/users/whoami'

def browser_cookies():
    maps = []
    for browser in browsers:
        cookiejar = None
        try:
            if browser == 'chrome':
                cookiejar = browser_cookie3.chrome(domain_name='ufora.ugent.be')
            elif browser == 'firefox':
                cookiejar = browser_cookie3.firefox(domain_name='ufora.ugent.be')
            elif browser == 'edge':
                cookiejar = browser_cookie3.edge(domain_name='ufora.ugent.be')
        except:
            pass

        cookies = None
        if cookiejar != None:
            try:
                cookies = {cookie.name: cookie.value for cookie in cookiejar._cookies['ufora.ugent.be']['/'].values()}
            except:
                pass
        
        if cookies != None:
            maps.append(cookies)

    rs = (grequests.get(url, cookies=cookies) for cookies in maps)
    responses = grequests.map(rs)
        
    for i, response in enumerate(responses):
        if response.status_code == 200:
            return maps[i]