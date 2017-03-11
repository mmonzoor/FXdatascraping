import sys
import requests
from datetime import datetime, timedelta
import pandas as pd

base_url = 'http://api.fixer.io/'
foreign_currencies = ['GBP', 'USD', 'EUR', 'INR']
base_rate = 'CAD'


def get_currency_rate(foreign_currency, base_rate, current_time):
  query = base_url + str(current_time) +'?base=%s&symbols=%s' % (base_rate, ','.join(foreign_currencies))
  try:
    r = requests.get(query, timeout=80)
    # print("[%s] %s" % (response.status_code, response.url))
    if r.status_code != 200:
      r = 'N/A'
      return r
    else:
      rates = r.json()
      print(rates)
      breakdown = []

      for key in rates["rates"].keys():
        a = str(key)
        print a
        rates[key] = rates["rates"][a]
        currency_breakdown = {"RATES":rates["rates"][a],"CURR_TYPE":a,"DATES":rates["date"]}
        breakdown.append(currency_breakdown)

      del rates["base"] 
      del rates["rates"]

      print(rates)
      return breakdown 

      # rate_in_currency = rates["rates"][base_rate]
      # return rate_in_currency

  except requests.ConnectionError as error:
    print error
    sys.exit(1)

def everyday(foreign_currencies, base_rate):
  today = datetime.now()
  days_ls = []
  for _ in range(360*5):

    today = today - timedelta(days=1)
    print (today.date())
    days_ls.extend(get_currency_rate(foreign_currencies, base_rate, today.date()))
  return days_ls


def main():
  days_ls = everyday(foreign_currencies,base_rate)
  print days_ls

  df = pd.DataFrame(days_ls)
  df.to_csv("all_fx_data.csv")

if __name__ == '__main__':
  main()