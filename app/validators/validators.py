from flask_wtf._compat import string_types
from wtforms import validators
from wtforms.validators import StopValidation
from app.models.tables import User, Lab, Disciplina, Convite, Envios, User_Disciplina

class RequiredIfChoice(validators.DataRequired):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIfChoice, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field.data == True and field.data=="":
            raise StopValidation("Campo requerido asdjhashjdajsdj")


class NotExistsInDb(object):
    """
    Checks the field's data is 'truthy' otherwise stops the validation chain.

    This validator checks that the ``data`` attribute on the field is a 'true'
    value (effectively, it does ``if field.data``.) Furthermore, if the data
    is a string type, a string containing only whitespace characters is
    considered false.

    If the data is empty, also removes prior errors (such as processing errors)
    from the field.

    **NOTE** this validator used to be called `Required` but the way it behaved
    (requiring coerced data, not input data) meant it functioned in a way
    which was not symmetric to the `Optional` validator and furthermore caused
    confusion with certain fields which coerced data to 'falsey' values like
    ``0``, ``Decimal(0)``, ``time(0)`` etc. Unless a very specific reason
    exists, we recommend using the :class:`InputRequired` instead.

    :param message:
        Error message to raise in case of a validation error.
    """
    field_flags = ('not_exists', )

    def __init__(self,Entidade, message=None):
        self.message = message
        self.entidade = Entidade
        #self.dbcolumn = dbcolumn


    def __call__(self, form, field):

        res = False

        if self.entidade == Disciplina.__tablename__:
            res = Disciplina.query.filter_by(codigo_disc=field.data).first() is not None

        if self.entidade == User.__tablename__:
                res = User.query.filter_by(username = field.data).first() is not None

        if not field.data or res or isinstance(field.data, string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('Este código já existe, por favor, escolha outro')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)

