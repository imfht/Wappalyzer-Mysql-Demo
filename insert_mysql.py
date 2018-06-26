import pymongo

from config import *

m_cli = pymongo.MongoClient()['wappalyzer']['data']
mysql_cli, cursor = get_mysql()
for i in m_cli.find():
    domain = i['url']
    for app in i['applications']:
        try:
            categ = app['categories'][0].keys()[0]
        except:
            categ = 0
        try:
            cursor.execute(
                'insert into cms (domain,name,confidence,version,icon,website,categorie) VALUES (%s,%s,%s,%s,%s,%s,%s)',
                (domain, app['name'], app['confidence'], app['version'], app['icon'], app['website'], categ))
        except Exception as e:
            continue
            print (e)
    mysql_cli.commit()

