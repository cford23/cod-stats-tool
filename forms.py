from wtforms import form, StringField, SelectField

class musicsearchform(form):
    choices = [('artist', 'artist'),
               ('album', 'album'),
               ('publisher', 'publisher')]
    select = SelectField('search for music:', choices=choices)
    search = StringField('')