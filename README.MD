# Technical Analysis Simulator

A [web application](https://tasimulator.herokuapp.com/) that generates trade signals with technical analysis indicators for cryptocurrency assets.
The app facilitates exploration and subscription to various technical indicators on a variety of crypto currencies. The application 
utilises `pandas` for technical analysis computation, `matplotlib` for data visualisation, `streamlit` for user interface, `sendgrid` for email notifications,
`heroku` for web hosting, database, and scheduling request to yahoo finance for most recent price data.

## Features
Users no longer need to constantly watch technical indicators charts to identify trading opportunity. Computations for technical indicators are 
done automatically on a daily basis and subscribers are notified when there are price movements of interest to catch on trading opportunities.

* Daily price charts update.
* Simulate trading based on technical indicator signals.
* Detailed summary of indicator's historical performance.
* Detailed hypothetical trade history for transparency.
* Subscription service for notification of significant price movements.

![dashboard]()
![tradesummary]()
![notification]()


Visit the actual site [here](https://tasimulator.herokuapp.com/). 