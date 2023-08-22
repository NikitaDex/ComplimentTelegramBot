import requests
from bs4 import BeautifulSoup as BS
import sqlite3

def fill_db(array):
    conn = sqlite3.connect('smalldb.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS compliments (id int auto_increment primary_key, text varchar(100))')
    # create db
    for comp in array:
        cur.execute("INSERT INTO compliments (text) VALUES ('%s')" % (comp))
        # fill db with compliments from parsed site
    conn.commit()
    cur.close()
    conn.close()



def get_array():
    compliment_arr = []
    page = 2
    while True:
        url = 'http://kompli.me/komplimenty-zhenshhine/page/' + str(page)
        r = requests.get(url)
        html = BS(r.content,'html.parser')

        if (page <= 38):
        # site has 38 pages
            for el in html.select('.post-card__description'):
                if(el.text != ''):
                    compliment_arr.append(el.text)
            page += 1
        else:
            break
    return compliment_arr
    
fill_db(get_array())