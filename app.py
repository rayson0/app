from string import *
from random import *

import phonenumbers
from validate_email import *
from werkzeug.utils import secure_filename

from forms import *
from user_login import *
from database import *
from flask_wtf.csrf import CSRFProtect

# const
UPLOAD_FOLDER = 'static/images/avatars'
CHECK_SYMBOLS = set(ascii_letters + digits + '_')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AVATAR_URL = '/static/images/avatars/'

db = DB()  # создаем экземпляр класса DB для работы с базой данных в файле database.py

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Необходимо авторизоваться для доступа к желаемой странице!'
login_manager.login_message_category = 'request'

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = ''.join(choices(ascii_letters, k=16))
app.config['WTF_CSRF_SECRET_KEY'] = ''.join(choices(ascii_letters, k=16))
csrf.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().add_info_user(user_id, db)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def check_verify_tags(tags):
    for tag in tags.split():
        if tag[0] != '#':
            return False
    return True


def check_login(name):
    global CHECK_SYMBOLS
    return (name & CHECK_SYMBOLS != name,
            len(name & set(ascii_letters)) == 0,
            ' '.join([symb for symb in (name ^ (name & CHECK_SYMBOLS))]))


def check_phone_number(number):
    number = phonenumbers.parse(number)
    return phonenumbers.is_valid_number(number)


def check_mail(email):
    return validate_email(email)


def limit(res, id):
    if res:
        flash(res,
              category='error')
        session['id_post'] = id
    else:
        click_reaction()


def click_reaction():
    flash('Вы успешно оставили реакцию!',
          category='success')


def flash_msgs(data, msg, cat):
    session['type_change_data'] = data
    flash(msg, category=cat)


def check_verify_fio(value):
    print(value[0][0].isupper())
    return all([x[0].isupper() and x[1:] == x[1:].lower() for x in value])


def check_verify_password(value):
    if len(set(value)) <= 2:
        return False, 'Должно быть 3 уникальных символа!'
    if len(value) <= 3:
        return False, 'Длина пароля не менее 4 символов!'
    return True,


def check_verify_info(data, value):
    if data == 'email':
        if value != db.check_unical_value('email', current_user):
            return True,
        return False, 'Почта не может совпадать с прошлой!'
    if data == 'number':
        if check_phone_number(value) and value != db.check_unical_value('number', current_user):
            return True,
        if check_phone_number(value):
            return False, 'Номер телефона не может совпадать с прошлым!'
        return False, 'Некорректный номер телефона!'
    if data == 'fio':
        if check_verify_fio(value) and any(
                [value[x] != db.check_unical_value('fio', current_user)[x] for x in range(3)]):
            return True,
        if check_verify_fio(value):
            return False, 'ФИО не может совпадать с прошлым!'
        return False, 'Вводите ФИО с большой буквы!'
    if data == 'password':
        if check_verify_password(value)[0] and value != db.check_unical_value('password', current_user):
            return True,
        if check_verify_password(value)[0]:
            return False, 'Пароль не может совпадать с прошлым!'
        return False, check_verify_password(value)[1]
    return True,


def success_flash(data):
    session['type_change_data'] = data
    flash('Данные успешно обновлены!', category='success')


@app.errorhandler(404)
def not_found_page(error):
    return render_template('error.html',
                           title='Посторонняя страница',
                           links_header=db.get_info_menu_right(current_user),
                           text='Извини! Я не могу найти страницу!')


@app.errorhandler(413)
def not_found_page(error):
    return render_template('big_size_file.html',
                           title='Посторонняя страница',
                           links_header=db.get_info_menu_right(current_user))


@app.route('/', methods=['POST', 'GET'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('profile',
                                name=current_user.get_name()))
    title = 'Главная страница'
    return render_template('index.html',
                           title=title,
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           cnt_users=db.cnt_users()['cnt'] - (db.cnt_users()['cnt'] % 10),
                           cnt_subjs=db.cnt_subjs()['cnt'],
                           redirect=redirect)


@app.route('/support', methods=['POST', 'GET'])
def support():
    name = False
    form = SupportForm()
    title = 'Обратная связь'
    if request.method == 'POST':

        number = db.post_support_req(request.form)

        if 'name' in request.form:
            flash(f'Запрос №{number} под логином {request.form["name"]} успешно отправлено!',
                  category='success')
        else:
            flash(f'Запрос №{number} под никнеймом {request.form["nickname"]} успешно отправлено!',
                  category='success')

    return render_template('support.html',
                           form=form,
                           title=title,
                           request_form=request.form,
                           name=name,
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           current_user=current_user)


@app.route('/read', methods=['POST', 'GET'])
def read():
    form = SearchForm()
    menu_filter = db.get_menu_filter()

    search = request.form['search'] if 'search' in request.form else False
    session['order'] = 'new' if session.get('order') is None else session['order']
    posts, req = db.filter_posts(session, current_user, search)
    if request.method == 'POST':
        session['all_choices'] = True
        session['with_user'] = True

        if 'checkbox_tags' in request.form:
            if len(tuple(request.form.getlist('checkbox_tags'))) == 1:
                tags = request.form.get('checkbox_tags')
            else:
                tags = request.form.getlist('checkbox_tags')
        else:
            tags = ''

        if 'checkbox_subjs' in request.form:
            if len(tuple(request.form.getlist('checkbox_subjs'))) == 1:
                subjs = request.form.get('checkbox_subjs')
            else:
                subjs = request.form.getlist('checkbox_subjs')
        else:
            subjs = ''

        if 'checkbox_types' in request.form:
            if len(tuple(request.form.getlist('checkbox_types'))) == 1:
                types = request.form.get('checkbox_types')
            else:
                types = request.form.getlist('checkbox_types')
        else:
            types = ''

        session['tags'] = tags
        session['subjs'] = subjs
        session['types'] = types
        posts, req = db.filter_posts(session, current_user, search)
    return render_template('read.html',
                           title='Читать статьи',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           form=form,
                           menu_filter=menu_filter,
                           len=len,
                           posts=posts,
                           request=req,
                           smiles=db.get_smiles(),
                           session=session,
                           str=str,
                           own_posts=db.get_own_posts(current_user),
                           cnt_posts=db.get_count_posts())


@app.route('/read/<id>', methods=['POST', 'GET'])
def read_post(id):
    print()
    if db.get_owner_post(id) != current_user.get_id() and db.check_is_been_views(current_user.get_id(), id) != 1:
        db.update_views(id)
        db.add_views(current_user.get_id(), id)
    form = SearchForm()
    return render_template('read_post.html',
                           title='Читать статьи',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           smiles=db.get_smiles(),
                           post=db.find_post(id),
                           len=len,
                           form=form,
                           str=str,
                           datetime=datetime,
                           strptime=dt.datetime.strptime,
                           get_user=db.get_user)


@app.route('/menu', methods=['POST', 'GET'])
def menu():
    if request.method == 'POST':
        if 'checkbox_tags' in request.form:
            if len(tuple(request.form.getlist('checkbox_tags'))) == 1:
                tags = request.form.get('checkbox_tags')
            else:
                tags = request.form.getlist('checkbox_tags')
        else:
            tags = ''

        if 'checkbox_subjs' in request.form:
            if len(tuple(request.form.getlist('checkbox_subjs'))) == 1:
                subjs = request.form.get('checkbox_subjs')
            else:
                subjs = request.form.getlist('checkbox_subjs')
        else:
            subjs = ''

        if 'checkbox_types' in request.form:
            if len(tuple(request.form.getlist('checkbox_types'))) == 1:
                types = request.form.get('checkbox_types')
            else:
                types = request.form.getlist('checkbox_types')
        else:
            types = ''

        session['tags'] = tags
        session['subjs'] = subjs
        session['types'] = types
        session['all_choices'] = 'check_all_choices' in request.form
        session['with_user'] = 'check_with_user' in request.form
        session['order'] = request.form['select_sort'] if 'select_sort' in request.form else 'new'
        print(request.form['select_sort'], session['order'])
        return redirect(url_for('read'))


@app.route('/smile_love_laugh/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile1(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('love_laugh', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_laugh/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile2(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('laugh', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_shock/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile3(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('shock', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_laugh_cry/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile4(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('laugh_cry', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_cry/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile5(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('cry', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_angry/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile6(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('angry', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/smile_terrible/<id>/<user_id>/<req>/<url>', methods=['POST', 'GET'])
def smile7(id, user_id, req, url):
    if request.method == 'POST':
        res = db.add_smile('terrible', id, current_user, user_id)
        limit(res, id)
        session['req'] = req
        if url == 'read':
            return redirect(url_for(url))
        return redirect(url_for(url, id=id))


@app.route('/choice_of_post', methods=['POST', 'GET'])
@login_required
def choice_of_post():
    form = ChoiceOfPostForm()
    return render_template('choice_of_post.html',
                           title='Читать статьи',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           form=form)


@app.route('/choice_of_post_<type>', methods=['POST', 'GET'])
@login_required
def choice_of_post_type(type):
    form = ChoiceOfPostForm()
    return redirect(url_for('add',
                            type=type))


@app.route('/add_post_<type>', methods=['POST', 'GET'])
@login_required
def add(type):
    if type == 'Статья':
        form = AddArticleForm()
    elif type == 'История':
        form = AddStoryForm()
    else:
        form = AddReasForm()
    if request.method == 'POST':
        if not check_verify_tags(request.form['tags']):
            flash('Хештеги прописаны неверно! Попробуйте снова',
                  category='error')
        else:
            number = db.add_post(current_user, request, form, type)

            flash(f'{type} №{number} опубликована',
                  category='success')
    return render_template('add.html',
                           title='Добавить публикацию',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           form=form,
                           type=type,
                           isinstance=isinstance,
                           AddStoryForm=AddStoryForm)


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    if current_user.is_authenticated:
        return redirect(url_for('profile',
                                name=current_user.get_name()))

    def change_menu_pass():
        nonlocal check_verify_pass, menu_password
        for i in range(len(menu_password)):
            menu_password[i][1] = check_verify_pass[i]

    form = RegistrationForm()
    title = 'Авторизация пользователя'
    check_verify_pass = [True] * 5

    menu_password = db.get_menu_password()
    for i in range(len(menu_password)):
        print(menu_password, i)
        menu_password[i] = [menu_password[i], check_verify_pass[i]]

    if request.method == 'POST':
        set_symbols_name, names = db.get_symb_name(request)

        check_verify_pass = [
            request.form['password1'] != request.form['password2'],
            len(request.form['password1']) <= 3,
            check_login(set_symbols_name)[0],
            len(set(request.form['password1'])) <= 2,
            check_login(set_symbols_name)[1],
        ]
        change_menu_pass()

        if request.form['name'] in [i[0] for i in names]:
            flash('Попробуйте другой логин. Этот логин уже занят',
                  category='error')

        elif request.form['password1'] != request.form['password2']:
            flash('Пароли не совпадают. Попробуйте снова',
                  category='error')

        elif len(request.form['password1']) <= 3:
            flash('Длина пароля - не менее 4 смиволов',
                  category='error')

        elif check_login(set_symbols_name)[0]:
            flash('В логине используется запрещенные символы (' + check_login(set_symbols_name)[2] + ')',
                  category='error')

        elif check_login(set_symbols_name)[1]:
            flash('В логине не используется обязательный символ - латинская буква любого регистра',
                  category='error')

        elif ((request.form['radio'] == 'Номер телефона' and not check_phone_number(request.form['info']))
              or (request.form['radio'] == 'Электронная почта' and not check_mail(request.form['info']))):
            flash('Неверно введен номер телефона / электронная почта',
                  category='error')

        elif len(set(request.form['password1'])) <= 2:
            flash('Слишком простой пароль. Используйте различные символы',
                  category='error')

        else:
            result = db.add_user(request, form)

            db.update_data_user(request.form['name'], result['avatar'])
            result = db.find_user(request.form['name'])

            checkbox = True if 'checkbox' in request.form else False
            userlogin = UserLogin().create(result)
            login_user(userlogin, remember=checkbox)

            return redirect(url_for('profile',
                                    name=request.form['name']))

    return render_template('reg.html',
                           links_header=db.get_info_menu_right(current_user),
                           form=form,
                           title=title,
                           links_header_text=db.get_info_menu_left(),
                           menu_password=menu_password,
                           check_ver_pass=check_verify_pass)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile',
                                name=current_user.get_name()))
    form = LoginForm()
    title = 'Вход в систему'
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        result = db.find_user(name)

        if not result or not check_password_hash(result['password'], password):
            flash('Неправильно набран логин / пароль. Попробуйте снова',
                  category='error')
        else:
            checkbox = True if 'checkbox' in request.form else False
            userlogin = UserLogin().create(result)
            login_user(userlogin, remember=checkbox)

            db.update_data_user(name, result['avatar'])

            return redirect(request.args.get('next')
                            or url_for('profile',
                                       name=name))

    return render_template('login.html',
                           title=title,
                           form=form,
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left())


# обработчики страниц для зарегистрированных пользователей
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        return redirect(url_for('index'))


@app.route('/profile/<name>', methods=['GET', 'POST'])
@login_required
def profile(name):
    title = 'Страница - ' + name
    return render_template('index.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=title,
                           links_header_text=db.get_info_menu_left(),
                           cnt_users=db.cnt_users()['cnt'] - (db.cnt_users()['cnt'] % 10),
                           cnt_subjs=db.cnt_subjs()['cnt'])


@app.route('/profile/<name>/page', methods=['GET', 'POST'])
@login_required
def profile_page(name):
    db.profile_menu()
    title = 'Профиль - ' + name
    return render_template('profile.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=title,
                           menu=db.profile_menu(),
                           links_header_text=db.get_info_menu_left(),
                           form_exit=ExitForm(),
                           redirect=redirect,
                           url_for=url_for,
                           range=range,
                           form_avatar=AvatarForm(),
                           info=db.get_info_profile_page(current_user)[0],
                           none=None,
                           strptime=dt.datetime.strptime)


@app.route('/profile/<name>/change_avatar', methods=['POST', 'GET'])
@login_required
def change_avatar(name):
    form = AvatarForm()
    if request.method == 'POST':
        if request.form.get('radio') is None:
            if 'file' not in request.files:
                flash('Ошибка чтения файла!', category='error')
                return redirect(request.url)
            file = request.files['file']
            if not file.filename:
                flash('Нельзя установить пустый аватар!', category='error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(os.path.abspath(app.config['UPLOAD_FOLDER']), filename))
                db.update_avatar(AVATAR_URL + filename, current_user.get_name())
                return redirect(url_for('download_avatar', name=filename))
            flash('Некорректный формат файла!', category='error')
            return redirect(request.url)
        else:
            session['avatar'] = request.form['radio'][8:-4]
            db.update_avatar(request.form['radio'], current_user.get_name())
        return redirect(url_for('profile_page',
                                name=name))

    return render_template('profile_avatar.html',
                           links_header=db.get_info_menu_right(current_user),
                           title='Изменение аватара',
                           menu=db.profile_menu(),
                           links_header_text=db.get_info_menu_left(),
                           form_exit=ExitForm(),
                           range=range,
                           form=form,
                           info=db.get_info_profile_page(current_user)[0],
                           none=None,
                           strptime=dt.datetime.strptime)


@app.route('/download_<name>', methods=['POST', 'GET'])
@login_required
def download_avatar(name):
    send_from_directory(app.config["UPLOAD_FOLDER"], name)
    return redirect(url_for('profile_page', name=current_user.get_name()))


@app.route('/profile/<name>/settings', methods=['POST', 'GET'])
@login_required
def settings(name):
    return render_template('profile_settings.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=f'Настройки',
                           menu=db.profile_menu(),
                           links_header_text=db.get_info_menu_left(),
                           form_exit=ExitForm(),
                           info=db.find_user(current_user.get_name()),
                           form_email=ChangeEmailForm(),
                           form_number=ChangeNumberForm(),
                           form_fio=ChangeFioForm(),
                           form_about_me=ChangeAboutMeForm(),
                           none=None,
                           bool=bool,
                           session=session)


@app.route('/add_email', methods=['POST', 'GET'])
@login_required
def add_email():
    form = ChangeEmailForm()
    if request.method == 'POST' and form.validate_on_submit():
        res = check_verify_info('email', request.form.get('email'))
        if res[0]:
            db.add_data_user('email', request.form['email'], current_user)
            success_flash('email')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
        else:
            flash_msgs('email', res[1], 'error')
    session['type_change_data'] = 'email'
    flash('Неккорректная почта!', category='error')
    return redirect(url_for('settings',
                            name=current_user.get_name()))


@app.route('/add_number', methods=['POST', 'GET'])
@login_required
def add_number():
    form = ChangeNumberForm()
    if request.method == 'POST' and form.validate_on_submit() and all(
            [i.isdigit() for i in request.form.get('number')]):
        res = check_verify_info('number', request.form.get('number'))
        if res[0]:
            db.add_data_user('number', request.form['number'], current_user)
            success_flash('number')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
        else:
            flash_msgs('number', res[1], 'error')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
    session['type_change_data'] = 'number'
    flash('Некорректный номер телефона!', category='error')
    return redirect(url_for('settings',
                            name=current_user.get_name()))


@app.route('/add_fio', methods=['POST', 'GET'])
@login_required
def add_fio():
    form = ChangeFioForm()
    if request.method == 'POST' and form.validate_on_submit():
        print([request.form['sur'], request.form['first'], request.form['last']])
        res = check_verify_info('fio', [request.form['sur'], request.form['first'], request.form['last']])
        if res[0]:
            db.add_data_user('fio', [request.form['sur'], request.form['first'], request.form['last']], current_user)
            success_flash('fio')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
        else:
            flash_msgs('fio', res[1], 'error')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
    session['type_change_data'] = 'fio'
    return redirect(url_for('settings',
                            name=current_user.get_name()))


@app.route('/add_about_me', methods=['POST', 'GET'])
@login_required
def add_about_me():
    form = ChangeAboutMeForm()
    if request.method == 'POST' and form.validate_on_submit():
        db.add_data_user('about_me', request.form['about_me'], current_user)
        success_flash('about_me')
        return redirect(url_for('settings',
                                name=current_user.get_name()))


@app.route('/profile/<name>/change_password1', methods=['POST', 'GET'])
@login_required
def change_password1(name):
    form = ChangePasswordForm1()
    if request.method == 'POST':
        if check_password_hash(current_user.get_psw(), request.form['old_password']):
            return redirect(url_for('change_password2',
                                    name=current_user.get_name()))
        else:
            flash('Неверно введен пароль!', category='error')
    return render_template('profile_change_psw1.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=f'Изменение пароля',
                           links_header_text=db.get_info_menu_left(),
                           form=form,
                           session=session)


@app.route('/profile/<name>/change_password2', methods=['POST', 'GET'])
@login_required
def change_password2(name):
    form = ChangePasswordForm2()
    if request.method == 'POST':
        res = check_verify_info('password', request.form.get('password'))
        if res[0]:
            db.add_data_user('password', generate_password_hash(request.form['password']), current_user)
            success_flash('password')
            return redirect(url_for('settings',
                                    name=current_user.get_name()))
        else:
            flash_msgs(res[1], 'error')
    return render_template('profile_change_psw2.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=f'Изменение пароля',
                           links_header_text=db.get_info_menu_left(),
                           form=form)


@app.route('/profile/<name>/posts', methods=['POST', 'GET'])
@login_required
def posts(name):
    return render_template('profile_posts.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=f'Добавить статью',
                           menu=db.profile_menu(),
                           links_header_text=db.get_info_menu_left(),
                           form_exit=ExitForm(),
                           form=SearchForm(),
                           posts=db.find_posts,
                           range=range,
                           len=len,
                           str=str,
                           types_of_posts=db.get_types_of_posts(current_user),
                           types_morph=[morph.parse(i['type'])[0].inflect({'plur'}).word.capitalize() for i in
                                        db.get_types_of_posts(current_user)] if db.get_types_of_posts(
                               current_user) else False,
                           morph=morph,
                           smiles=db.get_smiles(),
                           current_user=current_user)


@app.route('/profile/<name>/friends', methods=['POST', 'GET'])
@login_required
def friends(name):
    form = AnswerRequestFriendForm()
    form_dlt = DeleteFriendForm()
    return render_template('profile_friends.html',
                           links_header=db.get_info_menu_right(current_user),
                           title=f'Друзья',
                           menu=db.profile_menu(),
                           links_header_text=db.get_info_menu_left(),
                           form_exit=ExitForm(),
                           none=None,
                           friends=db.get_friends(current_user),
                           len=len,
                           cnt_friends=db.get_cnt_friends(current_user.get_id()),
                           cnt_request_friends=db.get_cnt_request_friends(current_user.get_id()),
                           request_friends=db.get_request_friend(current_user.get_id()),
                           form=form,
                           form_dlt=form_dlt)


@app.route('/profile/<name>/support', methods=['GET', 'POST'])
@login_required
def profile_support(name):
    requests = db.vyvod_support_req(current_user)

    return render_template('profile_support.html',
                           title='Мессенджер с поддержкой',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           menu=db.profile_menu(),
                           requests=requests,
                           form_exit=ExitForm(),
                           none=None,
                           len=len)


@app.route('/profile/<name>/achievements', methods=['GET', 'POST'])
@login_required
def profile_achievements(name):
    form = GetPrizeAchieForm()
    return render_template('profile_achie.html',
                           title='Достижения',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           menu=db.profile_menu(),
                           achies=db.get_achies(current_user),
                           compl_achies=db.get_compl_achies(current_user),
                           form_exit=ExitForm(),
                           progress=db.get_progress_achies,
                           current_user=current_user,
                           form=form,
                           cnt_money=db.cnt_money(current_user),
                           cnt_all_money=db.cnt_all_money())


@app.route('/find_friends', methods=['POST', 'GET'])
@login_required
def find_friends():
    form = AddFriendForm()
    return render_template('find_friends.html',
                           title='Найти друзей',
                           links_header=db.get_info_menu_right(current_user),
                           links_header_text=db.get_info_menu_left(),
                           prop_friends=db.get_cnt_prop_friends(current_user),
                           len=len,
                           none=None,
                           form=form)


@app.route('/request-friend-<receiver>', methods=['POST', 'GET'])
@login_required
def request_friend(receiver):
    if request.method == 'POST':
        db.add_request_friend(current_user.get_id(), receiver)
        return redirect(url_for('find_friends'))


@app.route('/agree_request_<id>', methods=['POST', 'GET'])
@login_required
def agree_request(id):
    if request.method == 'POST':
        db.add_friend(id)
        return redirect(url_for('friends', name=current_user.get_name()))


@app.route('/against_request_<id>', methods=['POST', 'GET'])
@login_required
def against_request(id):
    if request.method == 'POST':
        db.delete_request_friend(id)
        return redirect(url_for('friends', name=current_user.get_name()))


@app.route('/delete_friend_<id>', methods=['POST', 'GET'])
@login_required
def delete_friend(id):
    if request.method == 'POST':
        db.delete_friend(id)
        return redirect(url_for('friends', name=current_user.get_name()))


@app.route('/add_compl_achie_<id>', methods=['GET', 'POST'])
@login_required
def add_compl_achie(id):
    if request.method == 'POST':
        db.add_compl_achie(id, current_user)
        return redirect(url_for('profile_achievements', name=current_user.get_name()))


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 2 ** 20
    app.run(debug=True)
