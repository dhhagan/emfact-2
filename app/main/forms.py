from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField
from wtforms.validators import Required, Length, Email

class ReactorForm(Form):
	name = StringField('Name', validators = [Required()])
	power = FloatField('Power')
	efficiency = FloatField('Efficiency')
	submitReactor = SubmitField('Add')

class HeatXForm(Form):
	name = StringField('Name')
	flowrate = FloatField('FlowRate')
	heatcapacity = FloatField('HeatCapacity')
	tempIn = FloatField('TempIn')
	tempOut = FloatField('TempOut')
	efficiency = FloatField('Efficiency')
	submitHeatX = SubmitField('Add')

class PlantInfoForm(Form):
    title = StringField('title')
    description = StringField('description')
    location = StringField('location')
    revenue = FloatField('revenue') 
    NAICS = IntegerField('NAICS')   
    submitInfo = SubmitField('Update')
