import datetime as dt

from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from database import *

db = DB()


class CheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SupportForm(FlaskForm):
    subjects = db.get_subjs_support()

    name = StringField('name', validators=[DataRequired(), Length(min=2)])
    nickname = StringField('nickname', validators=[DataRequired(), Length(min=2)])
    subject = SelectField('subject', choices=subjects)
    message = TextAreaField('message', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Отправить')


class RegistrationForm(FlaskForm):
    list_info = ['Номер телефона', 'Электронная почта']

    name = StringField('name', validators=[DataRequired(), length(min=2, max=20)])
    info = StringField('info', validators=[DataRequired()])
    password1 = PasswordField('password1', validators=[DataRequired(), Length(min=4, max=30)])
    password2 = PasswordField('password2', validators=[DataRequired(), Length(min=4, max=30)])
    radio = RadioField('radio', choices=[(info, info) for info in list_info], validators=[DataRequired()])
    checkbox = CheckboxField('Label', choices=[(False, 'Запомнить меня')])
    date = dt.datetime.now()
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    checkbox = CheckboxField('Label', choices=[(False, 'Запомнить меня')])
    submit = SubmitField('Войти')


class ExitForm(FlaskForm):
    submit1 = SubmitField('Выйти')


class AvatarForm(FlaskForm):
    links = [f'{IMG}avatar{i}.png' for i in range(1, 5)]
    radio = RadioField('radio', choices=[(i, i) for i in links])
    file = FileField('Выбери файл')
    submit = SubmitField('Подтвердить')


class AddTemplateForm(FlaskForm):
    value = '#втоп #рекомендации'
    header = StringField('header', validators=[Length(max=35)])
    text = TextAreaField('msg', validators=[DataRequired(), Length(min=5)])
    tags = TextAreaField('tags')
    tags_default = CheckboxField('Label', choices=[(value, 'Подключить хештеги по умолчанию')])
    submit = SubmitField('Опубликовать')
    date = dt.datetime.now()


class AddArticleForm(AddTemplateForm):
    subject = SelectField('subject', choices=db.get_subjs(), validators=[DataRequired()])


class AddStoryForm(AddTemplateForm):
    pass


class AddReasForm(AddTemplateForm):
    subject = SelectField('subject', choices=db.get_subjs(), validators=[DataRequired()])


class SearchForm(FlaskForm):
    checkbox_tags = CheckboxField('checkbox_tags', choices=db.get_tags())
    checkbox_subjs = CheckboxField('checkbox_subjs', choices=db.get_subjects_filter())
    checkbox_types = CheckboxField('checkbox_types', choices=db.get_types_of_post())
    check_all_choices = CheckboxField('all_choices', choices=[(True, f'Выбрать все ({db.get_count_posts()})')])
    check_with_user = CheckboxField('with_user',
                                    choices=[(True, f'Включить собственные публикации')])
    select_sort = SelectField('sort', choices=[('new', 'От новых к старым'), ('old', 'От старых к новым')])
    submit_filter = SubmitField('Подтвердить')
    search = StringField('search')
    submit_search = SubmitField()
    smile = SubmitField()


class ChoiceOfPostForm(FlaskForm):
    btn = SubmitField('Статья')


class Submit(FlaskForm):
    submit = SubmitField('Подтвердить')


class ChangeEmailForm(Submit):
    email = StringField(validators=[Email(), DataRequired()])


class ChangeNumberForm(Submit):
    number = StringField(validators=[DataRequired()])


class ChangeFioForm(Submit):
    first = StringField(validators=[Length(min=2), DataRequired()])
    sur = StringField(validators=[Length(min=2), DataRequired()])
    last = StringField(validators=[Length(min=2), DataRequired()])


class ChangeAboutMeForm(Submit):
    about_me = TextAreaField(validators=[DataRequired(), Length(min=5)])


class ChangePasswordForm1(Submit):
    old_password = PasswordField(validators=[DataRequired()])


class ChangePasswordForm2(Submit):
    password = PasswordField(validators=[DataRequired(), Length(min=4)])
    password_again = PasswordField(validators=[EqualTo('password', message='Пароли не совпадают!'), DataRequired()])


class GetPrizeAchieForm(FlaskForm):
    submit = SubmitField('Забрать награду')


class AddFriendForm(FlaskForm):
    submit = SubmitField('Добавить в друзья')


class AnswerRequestFriendForm(FlaskForm):
    submit_yes = SubmitField('Принять')
    submit_no = SubmitField('Отклонить')


class DeleteFriendForm(FlaskForm):
    submit = SubmitField('Удалить из друзей')