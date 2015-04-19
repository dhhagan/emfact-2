import pandas as pd
from app import models,db
from app.models import *

df=pd.read_csv('CO2perRevenue.csv')
for i,row in df.iterrows():
	new=NAICS_data(code=row[0],industry=row[1], kwhperdollar=row[2])
	db.session.add(new)
db.session.commit()

