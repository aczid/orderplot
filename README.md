# Orderplot

This is meant to monitor a trading bot like [TraderDaddy](https://traderdaddy.com/) in action while operating on the [Bittrex](https://bittrex.com/) exchange.
The script will graph your open buy/sell orders over the current bid price for the markets you are in.
Open orders are updated every 5 minutes, bid price is updated every 30 seconds.

You'll need `matplotlib` and `bittrex` python packages installed.

    apt-get install python-matplotlib
    pip install -r requirements.txt

Now just fill in your api key and secret into `orderplot.py` for a (new) key with 'read info' privileges and run it.

    ./orderplot.py

