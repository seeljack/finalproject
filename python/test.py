from datetime import date
import sqlite3
import os
import matplotlib.pyplot as plt
import numpy as np
from itertools import count
import types
from unicodedata import name
import unittest
import json
import requests
import yfinance as yf
import numpy as np 
import datetime
from flask import Flask, render_template
import flask
import random
import subprocess
import time
app = Flask(__name__)


#For stock in the past

# https://dashboard.nbshare.io/api/v1/apps/reddit?date=2022-04-03


#Getting most relevent stocks on different days
##Gets Wall Street Bet data from API
def wall_street_bet_different_days(x, date):
    url = "https://dashboard.nbshare.io/api/v1/apps/reddit?date={}"
    formated_url = url.format(date)
    data = requests.get(formated_url)
    data1 = data.text
    data_list = json.loads(data1)
    return data_list

#Start of it and allows the user to input its own date
#Test_length is the amount of days you are taking in info. So 10 days you would be taking in 10 days worth of the stock data

@app.route('/wsb/<int:number1>/<int:number2>/<int:number3>/<int:number4>/<int:number5>')
def make_shit_happen(test_length):
    year = input("Select a year (2022)\n")
    month = input("Select a month (05)\n")
    day = input("Select a day (04)\n")
    date = year + '-' + month + '-' + day
    year = int(year)
    month = int(month)
    day = int(day)
    wall_street_bet_get_stock_from_previous_days(date, year, month, day, test_length)


   
#{Date} = The day you want to look at for the WSB stocks data (format: yyyy-mm-dd). The following day then 7 days after will be the one we take stock price from
#{NOC} = Number of comments (returns over that amount)
#{Sentiment} = Bearish or Bullish
#{SS} = sentiment score (returns over that amount)
#{number_of_stocks} = The amount of stocks you want to return

#Gets the tickers for the stocks you want given the restrictions, for stocks on previous days. Sorted by sentiment score.
    
def wall_street_bet_get_stock_from_previous_days(date, year, month, day, test_length, NOC = 0, Sentiment = "Bullish", SS = 0, number_of_stocks = 5):
    data_list = wall_street_bet_different_days("dog", date)
    stocks_good_set = []
    stocks_good_set_ticker = []
    for dic in data_list:
        if dic['no_of_comments'] > NOC:
            if dic['sentiment'] == Sentiment:
                if dic['sentiment_score'] > SS:
                    stocks_good_set.append(dic)
    stocks_good_set_sorted = sorted(stocks_good_set, key=lambda d: d['sentiment_score'], reverse=True) 
    counter = 0
    for i in stocks_good_set_sorted:
        if counter == number_of_stocks:
            break
        else:
            stocks_good_set_ticker.append(i['ticker'])
            counter += 1
    print("Trending stocks for day selected")
    print(stocks_good_set_ticker)
    c = get_stocks_change_in_value_from_WSB_previous_days(stocks_good_set_ticker, date, year, month, day, test_length)
    print(c)
    return c


#Takes the stocks from the certain criteria and then gets average change in stock price from a day after criterea was recieved to 7 days later. 
#(Gets the stock data from yahoo and then seperates each of the stocks and then goes into the average function to get the average change for each stock and gets total average)
def get_stocks_change_in_value_from_WSB_previous_days(stocks_good_set_ticker, date, year, month, day, test_length):
    list_of_prices = []
    ns = 0
    date = datetime.date(year, month, day)
    counter = 0
    #Converts the datetypes into the correct type for the yf.download
    start = ""
    end = ''
    test_length = int(test_length)
    for i in range(test_length + 1):     
        if counter == 1:
            start = date
        date += datetime.timedelta(days=1)
        if counter == test_length:
            end = date
        counter += 1
    start = str(start)
    end = str(end)
    print("Start: " + start + ", End: " + end)
    for i in stocks_good_set_ticker:
        data = yf.download(i, start, end)
        for i , y in data.tail().items():
            if i[1]:
                p = i[1]
                break
        for i , y in data.tail().items():
            for x in y:
                if 'Open' in i:
                    if i[1]:
                        if p == i[1]:
                            list_of_prices.append(x)
                            print(x)
                            ns = 0
            if ns == 0:
                list_of_prices.append("NewStock")
                ns = 1
    average_percent_change = percent_change_for_stocks_previous_date(list_of_prices)
    control_average_percent_change(start, end)
    return average_percent_change


#Get change in VOO over the same period for the wall street bets
def control_average_percent_change(start, end):
    data = yf.download('VOO', start, end)
    list_of_prices = []
    print(data)
    for i , y in data.tail().items():
        for x in y:
            if 'Open' in i:
                print(x)
                list_of_prices.append(x)
    b = list_of_prices[0]
    e = list_of_prices[-1]
    percent_change = ((e - b) / len(list_of_prices)) / 100
    print("Percent change for the VOO during the time period from " + str(start) + " to " + str(end) + " is " + str(percent_change) + '\n')

def percent_change_for_stocks_previous_date(list_of_prices):
    #For if you are doing multiple stocks and taking the average of the percent change

    #Deletes nan values from list_of_prices
    list_of_prices = [x for x in list_of_prices if x == x]

    if "NewStock" in list_of_prices:
        count = 0
        list_of_percent_changes = []
        for i in range(len(list_of_prices)):
            if list_of_prices[i] == "NewStock":
                count = 0
                end = list_of_prices[i-1]
                percent_change = (end - start) / start
                list_of_percent_changes.append(percent_change)
                continue
            if count == 0:
                start = list_of_prices[i]
                count += 1
        average_percent_change = sum(list_of_percent_changes) / len(list_of_percent_changes)
        return "This is the average Percent Change of top stocks in Wall Street Bets on the date selected " + str(average_percent_change) + '\n'
    #For if you are doing a single stock and just getting the percent change     
    else:
        start = list_of_prices[0]
        end = list_of_prices[-1]
        percent_change = (end - start) / start
        return "This is the Percent Change of top stocks in Wall Street Bets on the date selected " + str(percent_change) + '\n'



#--------------------------------------------------------------
#Databases SQLITE
#--------------------------------------------------------------


#Getting the database ready
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


list_of_dates_top5_Sentiment_score_with_SSabove5 = ['2019-05-01','2019-01-01','2021-01-01','2021-08-01','2021-08-01','2020-03-01','2020-06-01','2020-06-15','2022-04-15','2022-03-15']
list_of_percent_changes_top5_Sentiment_score_with_SSabove5 = ['0.00243466798504451','0.0298201246290855','0.0350999565380924','-0.0298935189545775','-0.0298935189545775','0.0140120269305533','0.0358315588763831','-0.0255221423895088','-0.0441186311985633','0.118389049705346']
#Creating Table with Percent Change
def create_table_top_ss_above5(cur,conn,percent_change,change,date):
    cur.execute("DROP TABLE IF EXISTS wsb_stocks_ss")
    cur.execute("CREATE TABLE IF NOT EXISTS wsb_stocks_ss (percent_change REAL, sentiment_score TEXT, date TEXT)")
    for i in range(len(list_of_dates_top5_Sentiment_score_with_SSabove5)):
        cur.execute("INSERT INTO wsb_stocks_ss (percent_change,sentiment_score,date) VALUES (?,?,?)",(list_of_percent_changes_top5_Sentiment_score_with_SSabove5[i],change,list_of_dates_top5_Sentiment_score_with_SSabove5[i]))
    conn.commit()



#Graph Functions
def graph_functions(cur,conn):

    #SS top 5 above .5
    cur.execute("SELECT percent_change FROM wsb_stocks_ss")
    database_percent_change_ss = cur.fetchall()
    data_ssbh = []
    for i in database_percent_change_ss:
        for x in i:
         data_ssbh.append(x)
    #Creating Boxplot
    plt.boxplot(data_ssbh)
    plt.title("Wall Street Bet top 5 stocks (according to sentiment score) percent change for 10 random dates")
    plt.show()







def main():
    print('Test stocks of given time frame')
    make_shit_happen(15)

    #Test not past stock
    # print('Trending stocks for today')
    # get_stocks_good_setiment(.5, 5)

    #Test past stock
    wall_street_bet_get_stock_from_previous_days()
    

    #DataBase Set Up
    cur, conn = setUpDatabase('WSBstocks.db')
    #percent_change = wall_street_bet_get_stock_from_previous_days()

    #Change the Change whenever you change a restraint
    #Sentiment Score
    change = ".5"

    #Date
    # date = '2022-03-15'

    #Database Funcetions
    #create_table_top_ss_above5(cur,conn,percent_change,change,date)


    #Graph functions
    print(graph_functions(cur,conn))






if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
    
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=5000, debug=True)

# @app.route('/lottery/<int:number1>/<int:number2>/<int:number3>/<int:number4>/<int:number5>')
# def lottery(number1,number2,number3,number4,number5):
# def wall_street_bet_get_stock_from_previous_days(date, year, month, day, test_length, NOC = 0, Sentiment = "Bullish", SS = 0, number_of_stocks = 5):
# 	data_list = wall_street_bet_different_days("dog", date)
# 	stocks_good_set = []
# 	stocks_good_set_ticker = []
# 	for dic in data_list:
# 		if dic['no_of_comments'] > NOC:
# 			if dic['sentiment'] == Sentiment:
# 				if dic['sentiment_score'] > SS:
# 					stocks_good_set.append(dic)
# 	stocks_good_set_sorted = sorted(stocks_good_set, key=lambda d: d['sentiment_score'], reverse=True) 
# 	counter = 0
# 	for i in stocks_good_set_sorted:
# 		if counter == number_of_stocks:
# 			break
# 		else:
# 			stocks_good_set_ticker.append(i['ticker'])
# 			counter += 1
# 	print("Trending stocks for day selected")
# 	print(stocks_good_set_ticker)
# 	c = get_stocks_change_in_value_from_WSB_previous_days(stocks_good_set_ticker, date, year, month, day, test_length)
# 	print(c)
# 	return c

	# return flask.Response(inner(), mimetype='text/html')