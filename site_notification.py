import urllib3
import requests
import smtplib, ssl
import time
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')
from_email = config.get('from_email', 'address')
to_email = config.get('to_email', 'address')
password = config.get('password', 'value')

http = urllib3.PoolManager()

while True:
    url_list = {
        'Newegg':'https://www.newegg.com/p/pl?d=rtx+3070&N=100007709&isdeptsrh=1',
        'Best_Buy':'https://www.bestbuy.com/site/searchpage.jsp?st=rtx+3070',
        'Amazon':'https://www.amazon.com/stores/page/127E4131-DA71-49E3-902E-C382ABEC4AC3?tag=hawk-future-20&ascsubtag=trd-us-1979283231569090800-20',
        'Zotac':'https://www.zotacstore.com/us/graphics-cards/geforce-rtx-30-series/geforce-rtxtm-3070'
    }
    i = 0
    for x, y in url_list.items():
        i += 1
        try:
            response = http.request('GET', y, timeout=2.0)
        except:
            requests.get(y, timeout=5)
        soup = BeautifulSoup(response.data, features='html.parser')
        search_terms = ['ADD TO CART', 'VIEW DETAILS', 'See Details']
        in_stock = False
        for j in range(0, len(search_terms)):
            if str(soup).find(search_terms[j].title()) == -1 or str(soup).find(search_terms[j].lower()) == -1  or str(soup).find(search_terms[j].upper()) == -1:
                in_stock = False
                if i == len(url_list) and j == len(search_terms) - 1:
                    print('end of dictionary')
                    time.sleep(60)
                continue
            else:
                in_stock = True
                message = MIMEMultipart('alternative')
                message["Subject"] = "PAGE UPDATE NOTIFICATION -" + x
                message["From"] = from_email
                message["To"] = to_email

                text = """\Hey Trey! There is new stock available for the RTX 3070 at""" + x + """! Hurry before it's gone!""" +  y
                html_file_name = 'notification_message_' + x.lower() + '.html'
                message_file = open(html_file_name)
                html = message_file.read()

                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                message.attach(part1)
                message.attach(part2)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(from_email, password)
                    server.sendmail(from_email, to_email, message.as_string())
        if not in_stock:
            print('No RTX 3070s in stock at ' + x)
        else:
            print('RTX 3070 in stock NOW at ' + x + '!')