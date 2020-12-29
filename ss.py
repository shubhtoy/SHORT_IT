import mechanize
from fake_useragent import UserAgent

ua = UserAgent()
cookies = [
    {
        "domain": ".facebook.com",
        "httpOnly": False,
        "name": "presence",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "EDvF3EtimeF1603218583EuserFA21B56796881554A2EstateFDutF1603218583838CEchF_7bCC",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1634754579,
        "httpOnly": True,
        "name": "xs",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "44%3ADv93AlvW6RQ36w%3A2%3A1603218580%3A-1%3A-1",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1610994577,
        "httpOnly": True,
        "name": "fr",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "1GmiiqspRP8W4q9CQ.AWW4PUCZgoEYYgsLCXYzLyjO6_M.BfhJlT.5T.AAA.0.0.BfjyyU.AWXf1RG1XyM",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1634754579,
        "httpOnly": False,
        "name": "c_user",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "100056796881554",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1603823375,
        "httpOnly": False,
        "name": "locale",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "en_GB",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1603308581,
        "httpOnly": True,
        "name": "spin",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "r.1002851535_b.trunk_t.1603218581_s.1_v.2_",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1603823383,
        "httpOnly": False,
        "name": "wd",
        "path": "/",
        "sameSite": "Lax",
        "secure": True,
        "value": "1070x710",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1603823379,
        "httpOnly": False,
        "name": "dpr",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "1.25",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1665597532,
        "httpOnly": True,
        "name": "datr",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "U5mEX8JAYveNt7fK7sRD4Orl",
    },
    {
        "domain": ".facebook.com",
        "expiry": 1666290581,
        "httpOnly": True,
        "name": "sb",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "value": "U5mEX1DH7cdIqFeF3Cunmqq3",
    },
]
# print(ua.chrome)
user_agent = [
    (
        "User-agent",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    )
]
browser = mechanize.Browser()
browser.set_handle_robots(False)
cookies = mechanize.CookieJar()

browser.addheaders = user_agent
browser.set_handle_refresh(False)

url = "http://www.facebook.com"
browser.open(url)
browser.set_cookiejar(cookies)
browser.open(url)
response = browser.response()
with open("data.txt", "w+") as f:
    f.write(str(response.read()))