from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import Required, Length, Email

class ReactorForm(Form):
	name = StringField('Name')
	power = FloatField('Power')
	efficiency = FloatField('Efficiency')
	submit = SubmitField('Add')

class HeatXForm(Form):
	name = StringField('Name')
	flowrate = FloatField('FlowRate')
	heatcapacity = FloatField('HeatCapacity')
	tempIn = FloatField('TempIn')
	tempOut = FloatField('TempOut')
	efficiency = FloatField('Efficiency')
	submit = SubmitField('Add')