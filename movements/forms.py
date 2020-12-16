from flask_wtf import FlaskForm
from wtforms import Form, StringField, SubmitField, HiddenField, DecimalField, FloatField
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields.html5 import DateField # Opcion de calendario
import datetime

class TaskForm(FlaskForm):
    empty = 'Debe completar este campo'

    fecha = DateField('Fecha:', validators=[DataRequired(empty)])
    cantidad = FloatField('Cantidad:', validators=[DataRequired(empty)])
    concepto = StringField('Concepto:', validators=[DataRequired(empty)])
    submit = SubmitField('Enviar')

    def validate_fecha(self, field):
        now = datetime.date.today()
        if self.fecha.data > now:
            raise ValidationError("Fecha incorrecta")