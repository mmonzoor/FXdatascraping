import sys
import requests
from datetime import datetime, timedelta
import pandas as pd


base_url = 'http://api.fixer.io/' 
foreign_currencies = ['USD','GBP','EUR','INR']
# foreign_currencies_str = ''.join(foreign_currencies) #this will join the list
base_rate = 'CAD'


def get_currency_rate(foreign_currencies, base_rate, current_date):

  query_search = base_url + str(current_date) +'?base=%s&symbols=%s' % (base_rate, ','.join(foreign_currencies))
  try:
    r = requests.get(query_search, timeout=60)#timeout is in 60 seconds
    # print("[%s] %s" % (response.status_code, response.url))
    if r.status_code != 200:
      r = 'N/A'
      return r
    else:
      rates = r.json()
      # rate_in_currency = rates["rates"][base_rate]
      for key in rates["rates"].keys():
        rates[key] = rates["rates"][key]
      del rates["rates"]
      return rates
  except requests.ConnectionError as error:
    print error
    sys.exit(1)

def everyday(foreign_currencies,base_rate):
  today = datetime.now()
  # print(today - timedelta(hours=24))
  days = []
  #for _ in range(365*10): this is the real one but takes too long to run
  for _ in range(3):

    today = today - timedelta(days=1)
    print(today.date())
    days.append(get_currency_rate(foreign_currencies, base_rate,today.date()))
  return days

def main():

  days = everyday(foreign_currencies, base_rate)#will be a list containing dicts everyday scraped 
  print days
  df = pd.DataFrame(days)
  # df.columns = ['Fx rates']
  df.to_csv("all_fx_data_in.csv")

if __name__ == '__main__':
  main()