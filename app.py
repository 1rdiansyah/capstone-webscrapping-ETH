from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row_date = table.find_all('th')

row_date_length = len(row_date)

temp = [] #initiating a tuple

for i in range(0, row_date_length):
    #get dates
    date = table.find_all('th', attrs={'scope':'row'})[i].text
    date = date.strip()
    #get volume
    volume = table.select("tr > td:nth-of-type(2)")[i].text
    volume = volume.strip()
    
    temp.append((date,volume))

#change into dataframe
dfr = pd.DataFrame(temp, columns = ('date','volume'))

#insert data wrangling here
dfr['date'] = dfr['date'].astype('datetime64')
dfr['volume'] = dfr['volume'].str.replace(",", "").str.replace("$", "")
dfr['volume'] = dfr['volume'].astype('float64')
dfr = dfr.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	# generate card_data
	card_data = f"{round(dfr['volume'].mean(),2)}"

	# generate plot
	ax = dfr.plot(figsize = (10,4)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# generate plot2
	ax = dfr.plot(kind='box', vert=False, figsize = (10,4))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result2 = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result,
		plot_result2=plot_result2
		)


if __name__ == "__main__": 
    app.run(debug=True)
