# Technical Analysis Simulator 📈

A [web application](https://tasimulator.herokuapp.com/) that generates trade signals with technical analysis indicators for cryptocurrency assets.
The app facilitates exploration and subscription to various technical indicators on a variety of crypto currencies. The application 
utilises `pandas` for technical analysis computation 🧮 , `matplotlib` for data visualisation 👀 , `streamlit` for user interface 🤖 , `sendgrid` for email notifications 🚨 , `heroku` for web hosting, database, and scheduling request to yahoo finance for most recent price data 🌩️.

## Features
Users no longer need to keep a constant eye on technical indicators charts to identify trading opportunity. Computations for technical indicators are done automatically on a daily basis and subscribers are notified when there are price movements of interest, allowing them to cling on to trading opportunities. 🚀 🌑

* Daily price charts update.
* Simulate trading based on technical indicator signals.
* Detailed summary of indicator's historical performance.
* Detailed hypothetical trade history for transparency.
* Subscription service for notification of significant price movements.

![dashboard](https://github.com/Justinhoejj/Technical-Analysis-Simulator/blob/master/docs/dashboardchart.png)

![tradesummary](https://github.com/Justinhoejj/Technical-Analysis-Simulator/blob/master/docs/tradesummary.png)

![notification](https://github.com/Justinhoejj/Technical-Analysis-Simulator/blob/master/docs/emailnotification.png)


Visit the actual site [here](https://tasimulator.herokuapp.com/). 
