#!/usr/bin/python2.7

from matplotlib import pyplot
from bittrex import *
from datetime import datetime
import time

b = Bittrex('API_KEY', 'API_SECRET')
b = Bittrex('cf4c0e2cc0434fd8afb54c414a1e1e64', '18c6881726674cd588e7291d4f470d7f')

def run():

    plot_data = {}

    from dateutil.parser import parse

    currencies = []

    open_orders = b.api_query('getopenorders')['result']
    for order in open_orders:
        cur = order['Exchange'].replace('BTC-', '')
        currencies.append(cur)
    currencies = list(set(currencies))

    f, plots = pyplot.subplots(len(currencies))
    pyplot.ion()

    import matplotlib.dates as md

    for i, cur in enumerate(filter(lambda x: x != 'BTC', currencies)):
        plot_data[cur] = {'plot': plots[i], 
                #'ask_data': [],
                'bid_data': [],
                'x_data': [],
                'bid_line': plots[i].plot([], [])[0],
                'sell_dots': plots[i].plot([], [])[0],
                'buy_dots': plots[i].plot([], [])[0],
                }
        plots[i].set_ylabel(cur)
        plots[i].set_autoscale_on(True)
        plots[i].xaxis_date()

    max_window = 10
    updates = 0

    while True:
        try:
            currencies = []

            if updates == 0:
                open_orders = b.api_query('getopenorders')['result']
                open_buys = []
                open_sales = []

                sell_data = {}
                buy_data = {}
                for order in open_orders:
                    cur = order['Exchange'].replace('BTC-', '')
                    if cur not in sell_data.keys():
                        sell_data[cur] = []
                    if cur not in buy_data.keys():
                        buy_data[cur] = []
                    if order['OrderType'] == 'LIMIT_SELL':
                        if order['Limit'] > 0.01 and cur == 'RBY':
                            continue
                        sell_data[cur].append(order['Limit'])
                    if order['OrderType'] == 'LIMIT_BUY':
                        buy_data[cur].append(order['Limit'])
                    currencies.append(cur)
                    currencies = list(set(currencies))

            summaries = b.get_market_summaries()['result']
            for market in summaries:
                cur = market['MarketName'].replace('BTC-', '')
                if cur in currencies:
                    if len(plot_data[cur]['x_data']) > max_window:
                        plot_data[cur]['x_data'] = plot_data[cur]['x_data'][1:]
                        plot_data[cur]['bid_data'] = plot_data[cur]['bid_data'][1:]
                        #plot_data[cur]['ask_data'] = plot_data[cur]['ask_data'][1:]
                    # Plot bids/asks
                    #plot_data[cur]['ask_data'].append(market['Ask'])
                    plot_data[cur]['bid_data'].append(market['Bid'])
                    plot_data[cur]['x_data'].append(parse(market['TimeStamp']))

                    plot_data[cur]['bid_line'].set_xdata(md.date2num(plot_data[cur]['x_data']))
                    plot_data[cur]['bid_line'].set_ydata(plot_data[cur]['bid_data'])
                    #plot_data[cur]['ask_line'].set_xdata(md.date2num(plot_data[cur]['x_data']))
                    #plot_data[cur]['ask_line'].set_ydata(plot_data[cur]['ask_data'])

                    timestamp = int(time.mktime(parse(market['TimeStamp']).timetuple()))
                    # Plot our open orders
                    plot_data[cur]['buy_dots'].set_xdata(md.date2num([datetime.fromtimestamp(x) for x in range(timestamp, timestamp+len(buy_data[cur]))]))
                    plot_data[cur]['buy_dots'].set_ydata(sorted(buy_data[cur])[::-1])

                    plot_data[cur]['sell_dots'].set_xdata(md.date2num([datetime.fromtimestamp(x) for x in range(timestamp, timestamp+len(sell_data[cur]))]))
                    plot_data[cur]['sell_dots'].set_ydata(sorted(sell_data[cur]))

                    # Rescale plot
                    plot_data[cur]['plot'].relim()
                    plot_data[cur]['plot'].autoscale_view(True,True,True)

            # redraw
            f.canvas.draw()
            f.show()

            pyplot.pause(30)
            updates += 1
            if updates == 10:
                updates = 0
        except KeyboardInterrupt:
            return
        except Exception, e:
            print e

run()
