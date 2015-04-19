from app import db
from app.models import *
#from ..decorators import admin_required, permission_required

n = NAICS_data.query.filter_by(code=325193).first() #ethyl alcohol plant
#r=Report.query.filter_by(id=8).first()
r=Report()
r.title         = "Example Plant - Ethanol Production"
r.description     = "A prototype example for Clean Earth Hackathon"
r.location     = "MIT"
r.revenue        = 437982*300
r.NAICS        = n.id
newreactor=Reactor(name='fluidized cracker',power=10000,efficiency=.7,report_id=r.id)
db.session.add(newreactor)
newheatX=HeatExchanger(name='preheater',tempIn=450, tempOut=400,specificHeat=100,flowrate=100,efficiency=.5,report_id=r.id)
db.session.add(newheatX)
newdryer=Dryer(name='product finisher',power=3000,efficiency=.3,report_id=r.id)
db.session.add(newdryer)
newequip=OtherEquipment(name='conveyor belt',power=2000,efficiency=.8,report_id=r.id)
db.session.add(newequip)
db.session.commit()
#equip=r.largest_producer()
#improvement=r.improve_efficiency(equip=newequip,eff_increase=0.2)
#replacingcoal=r.reduced_ghg_replace_coal_ng()



#pandas import
import pandas as pd
df=pd.read_csv('CO2perRevenue.csv')
for i,row in df.iterrows():
    newdata = NAICS_data(code=row[0],industry=row[1],kwhperdollar=row[2])
    db.session.add(newdata)
db.session.commit()
