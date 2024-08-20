import sqlite3 as sql
from random import *

import pymorphy3
from flask import *
from werkzeug.security import *
from pprint import *


def get_name_for_seen_post(type, seen):
    if seen == 100:
        return f"Успех и слава в {morph.parse(type)[0].inflect({'loct', 'plur'}).word}!"
    return f"Первые просмотры в {morph.parse(type)[0].inflect({'loct', 'plur'}).word}!"


def get_name_for_friends(friends):
    if friends == 1:
        return f'Первое знакомство!'
    if friends == 5:
        return f'Дружелюбность поражает!'
    return f'Дружелюбка покоряет сервер!'


def get_name_for_reactions(reactions):
    if reactions == 1:
        return 'Первая реакция!'
    if reactions == 30:
        return 'Произвести впечатление на читателей!'
    return 'Отклики не желают останавливаться!'


morph = pymorphy3.MorphAnalyzer()

DATABASE = "C:\\Users\\User\\OneDrive\\Рабочий стол\\Flask\\Start_project\\static\\db\\database.db"
IMG = '/static/images/'
SMILES = IMG + 'smiles/'
BG_POST = IMG + 'bg_post/'
ACHIE = IMG + 'achies/'

links_header = [
    {
        'text': 'Обратная связь',
        'url': '/support',
        'img_url': f'{IMG}support.png',
        'class': 'support_link',
    },
    {
        'text': 'Регистрация',
        'url': '/reg',
        'img_url': f'{IMG}registration.png',
        'class': 'reg_link',
    },
    {
        'text': 'Войти',
        'url': '/login',
        'img_url': f'{IMG}login.png',
        'class': 'login_link',
    }
]

links_header_logged = [
    {
        'text': 'Обратная связь',
        'url': '/support',
        'img_url': f'{IMG}support.png',
        'class': 'support_link',
    },
    {
        'text': '',
        'url': '',
        'img_url': '',
        'class': 'profile_link',
    },
]

links_header_text = [
    {
        'text': 'Добавить публикацию',
        'url': '/choice_of_post',
        'class': 'text_link_header',
    },
    {
        'text': 'Читать публикации',
        'url': '/read',
        'class': 'text_link_header',
    },
    {
        'text': 'Найти друзей',
        'url': '/find_friends',
        'class': 'text_link_header',
    },
]

criteries = [
    'Пароли должны совпадать',
    'Длина пароля - не менее 4 символов',
    'Символы пароля - латинские буквы, цифры и нижнее подчеркивание',
    'В пароле должно быть 3 уникальных символа',
    'Обязательный символ в логине - латинская буква'
]

links_profile_page = [
    {
        'text': 'Страница',
        'url': 'page',
        'img_url': f'{IMG}profile.png',
        'class': 'page_link',
    },
    {
        'text': 'Публикации',
        'url': 'posts',
        'img_url': f'{IMG}posts.png',
        'class': 'posts_link',
    },
    {
        'text': 'Достижения',
        'url': 'achievements',
        'img_url': f'{IMG}achie.png',
        'class': 'achie_link',
    },
    {
        'text': 'Настройки',
        'url': 'settings',
        'img_url': f'{IMG}settings.png',
        'class': 'settings_link',
    },
    {
        'text': 'Друзья',
        'url': 'friends',
        'img_url': f'{IMG}my_friends.png',
        'class': 'friends_link',
    },
    {
        'text': 'Поддержка',
        'url': 'support',
        'img_url': f'{IMG}support.png',
        'class': 'support_link_menu',
    },
    {
        'text': 'Выйти',
        'url': '/',
        'img_url': f'{IMG}leave_to_account.png',
        'class': 'exit_link',
    },
]

subjects_of_posts = {
    'Авиация': f'{BG_POST}aviation.jpg',
    'Информационные технологии': f'{BG_POST}it.jpg',
    'Кулинария': f'{BG_POST}cook.jpg',
    'Медицина': f'{BG_POST}medicina.jpg',
    'Наука': f'{BG_POST}science.jpg',
    'Недвижимость': f'{BG_POST}real_estate.jpg',
    'Образование': f'{BG_POST}education.jpg',
    'Политика': f'{BG_POST}politic.jpg',
    'Природа': f'{BG_POST}priroda.jpg',
    'Промышленность': f'{BG_POST}industry.jpg',
    'Развлечения': f'{BG_POST}funny.jpg',
    'Философия': f'{BG_POST}filosophia.jpg',
    'Финансы': f'{BG_POST}money.png',
    'Музыка': f'{BG_POST}music.png',
    'Другое': f'{BG_POST}other.jpg',
}

subjects_of_support = [
    'Проблема с авторизацией',
    'Недоступно чтение статей',
    'Проблема с добавлением статьи',
    'Другое'
]

menu_filter = [
    {
        'name': 'Темы статей',
        'class': 'filter_subjects'
    },
    {
        'name': 'Хештеги',
        'class': 'filter_tags'
    },
    {
        'name': 'Тип',
        'class': 'filter_types'
    }
]

links_smiles = [
    f'{SMILES}love_laugh.png',
    f'{SMILES}laugh.png',
    f'{SMILES}shock.png',
    f'{SMILES}laugh_cry.png',
    f'{SMILES}cry.png',
    f'{SMILES}angry.png',
    f'{SMILES}terrible.png',
]

img_type_of_post = {
    'Статья': f'{IMG}article.png',
    'История': f'{IMG}story.png',
    'Сообщение': f'{IMG}rassujd.png'
}

achies = []
for ind in (1, 5):
    achies.extend([
        {
            'desc': f"Добавить {ind} {morph.parse('публикация')[0].inflect({'accs'}).make_agree_with_number(ind).word} на тему {subj}",
            'price': (1, 5).index(ind) + 1,
            'name': f"Первый шаг в теме {subj}!" if (1, 5).index(
                ind) == 0 else f"Талантливый писатель в теме {subj}!",
            'img': ACHIE + 'add_post.png',
            'points': ind
        } for subj in subjects_of_posts
    ])
for ind in (1, 5):
    achies.extend([
        {
            'desc': f"Опубликовать 1 {morph.parse(type)[0].inflect({'accs'}).word}" if (1, 5).index(ind) == 0
            else f"Опубликовать 5 {morph.parse(type)[0].make_agree_with_number(5).word}",
            'price': (1, 5).index(ind) + 1,
            'name': f"Первый шаг в {morph.parse(type)[0].inflect({'loct', 'plur'}).word}!" if (1, 5).index(ind) == 0
            else f"Талантливый писатель в {morph.parse(type)[0].inflect({'loct', 'plur'}).word}!",
            'img': ACHIE + 'add_post.png',
            'points': ind
        } for type in img_type_of_post
    ])
for seen in (10, 100):
    achies.extend([
        {
            'desc': f"Набрать {seen} просмотров на {morph.parse(type)[0].inflect({'loct'}).word}",
            'price': (10, 100).index(seen) + 1,
            'name': get_name_for_seen_post(type, seen),
            'img': ACHIE + 'seen.png',
            'points': seen
        } for type in img_type_of_post
    ])
for friends in (1, 5, 20):
    achies.extend([
        {
            'desc': f"Познакомиться с {friends} {morph.parse('друг')[0].inflect({'ablt'}).make_agree_with_number(friends).word}",
            'price': (1, 5, 20).index(friends) + 1,
            'name': get_name_for_friends(friends),
            'img': ACHIE + 'friends.png',
            'points': friends
        }
    ])
for reactions in (1, 10, 30):
    achies.extend([
        {
            'desc': f"Получить {reactions} {morph.parse('реакция')[0].inflect({'accs'}).make_agree_with_number(friends).word}",
            'price': (1, 10, 30).index(reactions) + 1,
            'name': get_name_for_reactions(reactions),
            'img': ACHIE + 'reactions.png',
            'points': reactions
        }
    ])


class DB:
    def __init__(self):
        with sql.connect(DATABASE, check_same_thread=False) as self.connect:
            self.connect.row_factory = sql.Row
            self.cursor = self.connect.cursor()
            self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu (
            text VARCHAR(80) NOT NULL,
            url VARCHAR(80) NOT NULL,
            img_url VARCHAR(80) NOT NULL,
            class VARCHAR(80) NOT NULL
            )
            ''')
        self.connect.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_logged (
            text VARCHAR(80) NOT NULL,
            url VARCHAR(80) NOT NULL,
            img_url VARCHAR(80) NOT NULL,
            class VARCHAR(80) NOT NULL
            )
            ''')
        self.connect.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS menu_text (
            text VARCHAR(80) NOT NULL,
            url VARCHAR(80) NOT NULL,
            class VARCHAR(80) NOT NULL
            )
            ''')
        self.connect.commit()

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_profile (
                text VARCHAR(80) NOT NULL,
                url VARCHAR(80) NOT NULL,
                img_url VARCHAR(80) NOT NULL,
                class VARCHAR(80) NOT NULL
                )
                ''')
        self.connect.commit()

        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS menu_password (
                text VARCHAR(140) NOT NULL
                )
                ''')
        self.connect.commit()

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                type VARCHAR(20) NOT NULL,
                bg VARCHAR(80) DEFAULT NULL,
                user_id BIGINT NOT NULL,
                subject VARCHAR(30) DEFAULT NULL,
                header VARCHAR(35) NOT NULL,
                text TEXT NOT NULL,
                time_of_read VARCHAR(60) NOT NULL,
                tags VARCHAR(1024),
                datetime DATETIME NOT NULL,
                img_type VARCHAR(80) NOT NULL,
                love_laugh BIGINT DEFAULT 0,
                laugh BIGINT DEFAULT 0,
                shock BIGINT DEFAULT 0,
                laugh_cry BIGINT DEFAULT 0,
                cry BIGINT DEFAULT 0,
                angry BIGINT DEFAULT 0,
                terrible BIGINT DEFAULT 0,
                seen BIGINT DEFAULT 0,
                
                CONSTRAINT owner_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
                )
                """)
        self.connect.commit()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(20) NOT NULL,
                        password VARCHAR(30) NOT NULL,
                        avatar VARCHAR(80) NOT NULL,
                        add_info VARCHAR(120) NOT NULL,
                        type_info VARCHAR(30) NOT NULL,
                        email VARCHAR(100),
                        number VARCHAR(13),
                        date DATETIME NOT NULL,
                        first_name VARCHAR(50),
                        surname VARCHAR(60),
                        last_name VARCHAR(60),
                        about_me TEXT,
                        coins TINYINT DEFAULT 0
                        )
                        """)
        self.connect.commit()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS answer_messages (
                        id INTEGER PRIMARY KEY,
                        message TEXT NOT NULL
                        )
                        """)
        self.connect.commit()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS inbox_messages (
                        id INTEGER PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        subject VARCHAR(50) NOT NULL,
                        message TEXT NOT NULL,
                        logged TINYINT DEFAULT 1
                        )
                        """)
        self.connect.commit()

        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS subjects_of_posts (
                    name VARCHAR(50) NOT NULL
                    )
                    """)
        self.connect.commit()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS subjects_of_support (
                            name VARCHAR(50) NOT NULL
                            )
                            """)
        self.connect.commit()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS menu_filter (
                            name VARCHAR(50) NOT NULL,
                            class VARCHAR(50) NOT NULL
                            )
                            """)
        self.connect.commit()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS smiles (
                            link VARCHAR(80) NOT NULL
                            )
                            """)
        self.connect.commit()

        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS reactions (
                            user_id BIGINT NOT NULL,
                            post_id BIGINT NOT NULL,
                            reaction VARCHAR(20) NOT NULL,
                            datetime DATETIME NOT NULL,
                            
                            CONSTRAINT post_id_fk FOREIGN KEY (post_id) REFERENCES posts (id),
                            CONSTRAINT owner_rc_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
                            )
                            """)
        self.connect.commit()

        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS achies (
                           id INTEGER PRIMARY KEY,
                           name VARCHAR(60) NOT NULL,
                           desc VARCHAR(120) NOT NULL,
                           price TINYINT NOT NULL,
                           img VARCHAR(100) NOT NULL,
                           points INTEGER NOT NULL
                           )
                           """)
        self.connect.commit()

        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS compl_achies (
                           achie_id INTEGER NOT NULL,
                           user_id INTEGER NOT NULL,
                           
                           CONSTRAINT achie_id_fk FOREIGN KEY (achie_id) REFERENCES achies (id)
                           )
                           """)
        self.connect.commit()

        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS views (
                           user_id BIGINT NOT NULL,
                           post_id BIGINT NOT NULL,
                           
                           CONSTRAINT post_views_id_fk FOREIGN KEY (post_id) REFERENCES posts (id),
                            CONSTRAINT user_seen_id_fk FOREIGN KEY (user_id) REFERENCES users (id)
                           )
                           """)
        self.connect.commit()

        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS friends (
                           id INTEGER PRIMARY KEY,
                           id1 BIGINT NOT NULL,
                           id2 BIGINT NOT NULL,
                           
                           CONSTRAINT friends_id_fk FOREIGN KEY (id1, id2) REFERENCES users (id, id)
                           )
                           """)
        self.connect.commit()

        self.cursor.execute("""
                           CREATE TABLE IF NOT EXISTS request_friends (
                           id INTEGER PRIMARY KEY,
                           sender BIGINT NOT NULL,
                           receiver BIGINT NOT NULL,
                           
                           CONSTRAINT users_req_fr_id_fk FOREIGN KEY (sender, receiver) REFERENCES users (id, id)
                           )
                           """)
        self.connect.commit()

        self.paste_data()

    def paste_data(self):
        self.cursor.execute('SELECT * FROM menu')
        check_empty = self.cursor.fetchall()
        if not check_empty:
            for link in links_header:
                self.cursor.execute(f'''INSERT INTO menu (text, url, img_url, class) VALUES
                                    ("{link["text"]}", "{link["url"]}", "{link["img_url"]}", "{link["class"]}")''')
                self.connect.commit()
            for link in links_header_logged:
                self.cursor.execute(f'''INSERT INTO menu_logged (text, url, img_url, class) VALUES
                                    ("{link["text"]}", "{link["url"]}", "{link["img_url"]}", "{link["class"]}")''')
                self.connect.commit()
            for link in links_header_text:
                self.cursor.execute(f'''INSERT INTO menu_text (text, url, class) VALUES
                                    ("{link["text"]}", "{link["url"]}", "{link["class"]}")''')
                self.connect.commit()
            for link in criteries:
                self.cursor.execute(f'INSERT INTO menu_password (text) VALUES ("{link}")')
                self.connect.commit()
            for link in links_profile_page:
                self.cursor.execute(f'''INSERT INTO menu_profile (text, url, img_url, class) VALUES
                                    ("{link["text"]}", "{link["url"]}", "{link["img_url"]}", "{link["class"]}")''')
                self.connect.commit()
            for link in subjects_of_support:
                self.cursor.execute(f'INSERT INTO subjects_of_support (name) VALUES ("{link}")')
                self.connect.commit()
            for link in menu_filter:
                self.cursor.execute(f'''INSERT INTO menu_filter (name, class) VALUES
                                    ("{link["name"]}", "{link["class"]}")''')
                self.connect.commit()
            for link in links_smiles:
                self.cursor.execute(f'INSERT INTO smiles (link) VALUES'
                                    f' ("{link}")')
                self.connect.commit()
            for link in subjects_of_posts:
                self.cursor.execute(f'INSERT INTO subjects_of_posts (name) VALUES'
                                    f' ("{link}")')
                self.connect.commit()
            for link in achies:
                self.cursor.execute(f'INSERT INTO achies (name, desc, price, img, points) VALUES'
                                    f' ("{link["name"]}", "{link["desc"]}", {link["price"]}, "{link["img"]}", "{link["points"]}")')
                self.connect.commit()

    def check_header_of_post(self, header):
        if not header:
            self.cursor.execute('SELECT MAX(id) FROM posts')
            res = self.cursor.fetchone()
            if not res or res[0] is None:
                return 'Статья №1'
            return f'Статья №{res[0] + 1}'
        return header

    def get_subjs_support(self):
        self.cursor.execute('SELECT name FROM subjects_of_support')
        return [(i['Name'], i['Name']) for i in self.cursor.fetchall()]

    def get_subjs(self):
        self.cursor.execute(f'SELECT name FROM subjects_of_posts')
        return [(i['name'], i['name']) for i in self.cursor.fetchall()]

    def get_info_menu_right(self, current_user):
        if current_user.is_authenticated:
            self.cursor.execute('SELECT * FROM menu_logged')
            res = self.cursor.fetchall()
            return res
        self.cursor.execute('SELECT * FROM menu')
        res = self.cursor.fetchall()
        return res

    def get_info_menu_left(self):
        self.cursor.execute('SELECT * FROM menu_text')
        res = self.cursor.fetchall()
        return res

    def update_data_user(self, name, avatar):
        self.cursor.execute(f'''UPDATE menu_logged 
                                    SET text = ?, url = ?, img_url = ? 
                                    WHERE class = ?''',
                            (name, f'/profile/{name}/page',
                             f'{avatar}',
                             'profile_link'))

        self.cursor.execute(f'''UPDATE menu_logged 
                                    SET url = ? 
                                    WHERE class = ?''',
                            (f'/profile/{name}',
                             'main_page_link'))
        self.connect.commit()

    def update_avatar(self, avatar, login):
        print(avatar, login)
        self.cursor.execute(f'''UPDATE menu_logged 
                                    SET img_url = ? 
                                    WHERE class = ?''',
                            (f'{avatar}',
                             'profile_link'))
        self.connect.commit()

        self.cursor.execute('''UPDATE users 
                                    SET avatar = ? 
                                    WHERE name = ?''',
                            (avatar,
                             login))
        self.connect.commit()

    def profile_menu(self):
        self.cursor.execute('SELECT * FROM menu_profile')
        return self.cursor.fetchall()

    def post_support_req(self, request_form):
        if 'name' in request_form:
            self.cursor.execute(f'''INSERT INTO inbox_messages (name, subject, message) 
                                   VALUES ("{request_form["name"]}", 
                                   "{request_form["subject"]}", 
                                   "{request_form["message"]}")''')
        else:
            self.cursor.execute(f'''INSERT INTO inbox_messages (name, subject, message, logged)
                                   VALUES ("{request_form["nickname"]}", 
                                   "{request_form["subject"]}", 
                                   "{request_form["message"]}", 
                                   0)''')
        self.connect.commit()
        self.cursor.execute('SELECT COUNT() FROM inbox_messages')
        return len(self.cursor.fetchall())

    def add_post(self, current_user, request, form, type):
        if type != 'История':
            self.cursor.execute(f'''INSERT INTO posts (type, bg, user_id, subject, header, text, time_of_read, tags,
                                    datetime, img_type) 
                                    VALUES ("{type}",
                                    "{self.get_bg_post(request.form["subject"])}", 
                                    "{current_user.get_id()}", 
                                    "{request.form["subject"]}", 
                                    "{self.check_header_of_post(request.form["header"])}",
                                    "{request.form["text"]}",
                                    "{self.get_timeread(request.form["text"])}",
                                    "{request.form["tags"]}", 
                                    "{form.date}", 
                                    "{img_type_of_post[type]}")''')

        else:
            self.cursor.execute(f'''INSERT INTO posts (type, bg, user_id, header, text, time_of_read, tags, 
                                    datetime, img_type) 
                                    VALUES ("{type}", 
                                    "{BG_POST + "story.jpg"}",
                                    "{current_user.get_id()}", 
                                    "{self.check_header_of_post(request.form["header"])}",
                                    "{request.form["text"]}",
                                    "{self.get_timeread(request.form["text"])}",
                                    "{request.form["tags"]}", 
                                    "{form.date}", 
                                    "{img_type_of_post[type]}")''')
        self.connect.commit()

        self.cursor.execute('SELECT MAX(id) FROM posts')
        return self.cursor.fetchone()[0]

    def get_menu_password(self):
        self.cursor.execute('SELECT * FROM menu_password')
        return self.cursor.fetchall()

    def get_symb_name(self, request):
        self.cursor.execute('SELECT name FROM users')
        names = self.cursor.fetchall()
        return set([symb for symb in request.form['name']]), names

    def add_user(self, request, form):
        add_info = {
            'Электронная почта': 'email',
            'Номер телефона': 'number'
        }
        self.cursor.execute(f'''
                            INSERT INTO users (name, password, avatar, add_info, type_info, {add_info[request.form["radio"]]}, date) 
                            VALUES 
                            (?, ?, ?, ?, ?, ?, ?)
                            ''', (request.form["name"],
                                  generate_password_hash(request.form["password1"]),
                                  url_for('static', filename=f'images/avatar{randint(1, 4)}.png'),
                                  request.form['info'],
                                  request.form['radio'],
                                  request.form['info'],
                                  form.date))
        self.connect.commit()

        self.cursor.execute(f'''SELECT avatar 
                                FROM users 
                                WHERE name = "{request.form["name"]}"''')
        return self.cursor.fetchone()

    def find_posts(self, type, current_user):
        print('111', type)
        self.cursor.execute(f'''SELECT *
                            FROM posts
                            WHERE user_id = {current_user.get_id()}
                            AND type = "{type}"''')
        res = self.cursor.fetchall()
        print(res, '----')
        return res

    def vyvod_support_req(self, current_user):
        self.cursor.execute(f"""SELECT inbox_messages.id, Subject, inbox_messages.message, answer_messages.message
                               FROM inbox_messages
                               FULL JOIN answer_messages ON inbox_messages.id = answer_messages.id
                               WHERE inbox_messages.name LIKE '{current_user.get_name()}'""")
        return self.cursor.fetchall()

    def find_user(self, name):
        self.cursor.execute(f"""SELECT *
                                FROM users 
                                WHERE name = '{name}' 
                                """)
        return self.cursor.fetchone()

    def get_info_profile_page(self, current_user):
        self.cursor.execute(f'''SELECT *
                                FROM users
                                WHERE name = "{current_user.get_name()}"''')
        info = self.cursor.fetchall()[0]
        return info, info['id']

    def get_info_user(self, user_id):
        self.cursor.execute(f"""SELECT *
                                FROM users
                                WHERE id = {user_id}""")
        return self.cursor.fetchone()

    def get_menu_filter(self):
        self.cursor.execute('SELECT * FROM menu_filter')
        return self.cursor.fetchall()

    def get_tags(self):
        self.cursor.execute("""SELECT DISTINCT tags
                            FROM posts""")

        tags_lst = list(map(lambda x: x[0].split(), self.cursor.fetchall()))
        res = []
        for tags in tags_lst:
            for tag in tags:
                if tag not in res:
                    self.cursor.execute(f'SELECT COUNT(tags) FROM posts WHERE tags LIKE "%{tag}%"')
                    res.append((tag, f'{tag} ({self.cursor.fetchone()[0]})'))
        return res

    def get_subjects_filter(self):
        res = []
        for subj in subjects_of_posts:
            self.cursor.execute(f'SELECT COUNT(subject) FROM posts WHERE subject LIKE "%{subj}%"')
            cnt = self.cursor.fetchone()
            if cnt and cnt[0] > 0:
                res.append((subj, f'{subj} ({cnt[0]})'))
        return res

    def filter_posts(self, session, current_user, search):
        if session.get('req', False):
            req = session['req']
            del session['req']
            self.cursor.execute(req)
            return self.cursor.fetchall(), req

        flag = False
        flag2 = False
        request = 'SELECT * FROM posts'

        if search:
            if flag:
                request += f' AND (id LIKE "%{search}%" OR header LIKE "%{search}%")'
            else:
                request += f' WHERE (id LIKE "%{search}%" OR header LIKE "%{search}%")'
            flag = True
            if session['order'] == 'new':
                request += ' ORDER BY datetime DESC'
            else:
                request += ' ORDER BY datetime ASC'
            self.cursor.execute(request)

        elif search == '':
            request += ' WHERE (id LIKE "" OR header LIKE "")'
            if session['order'] == 'new':
                request += ' ORDER BY datetime DESC'
            else:
                request += ' ORDER BY datetime ASC'
            self.cursor.execute(request)

        else:
            if 'all_choices' not in session or not session['all_choices']:
                if 'tags' not in session:
                    session['tags'] = '%'
                if not session['tags']:
                    request += ' WHERE tags is NULL'
                    flag = True

                if 'subjs' not in session:
                    session['subjs'] = '%'
                if not session['subjs']:
                    if flag:
                        request += ' AND subject IS NULL'
                    else:
                        request += ' WHERE subject IS NULL'
                    flag = True

                if 'types' not in session:
                    session['types'] = '%'
                if not session['types']:
                    if flag:
                        request += ' AND type IS NULL'
                    else:
                        request += ' WHERE type IS NULL'
                    flag = True

                if session['tags'] not in ('%', ''):
                    if type(session['tags']) == list:
                        for tag in session['tags']:
                            if flag:
                                if flag2:
                                    request += f' OR tags LIKE "%{tag}%"'
                                else:
                                    request += f' AND (tags LIKE "%{tag}%"'
                            else:
                                request += f' WHERE (tags LIKE "%{tag}%"'
                            flag2 = True
                            flag = True
                    else:
                        if flag:
                            request += f' AND tags LIKE "%{session["tags"]}%"'
                        else:
                            request += f' WHERE tags LIKE "%{session["tags"]}%"'
                        flag = True
                if flag2:
                    request += ')'
                if session['subjs'] not in ('%', ''):
                    if flag:
                        if type(session['subjs']) == list:
                            request += f' AND subject IN {tuple(session["subjs"])}'
                        else:
                            request += f' AND subject LIKE "{session["subjs"]}"'
                    else:
                        if type(session['subjs']) == list:
                            request += f' WHERE subject IN {tuple(session["subjs"])}'
                        else:
                            request += f' WHERE subject LIKE "{session["subjs"]}"'
                    flag = True
                if session['tags'] not in ('%', ''):
                    if flag:
                        if type(session['types']) == list:
                            request += f' AND type IN {tuple(session["types"])}'
                        else:
                            request += f' AND type LIKE "{session["types"]}"'
                    else:
                        if type(session['types']) == list:
                            request += f' WHERE type IN {tuple(session["types"])}'
                        else:
                            request += f' WHERE type LIKE "{session["types"]}"'
            if 'with_user' not in session or not session['with_user']:
                if current_user.is_authenticated:
                    if flag:
                        request += ' AND'
                    else:
                        request += ' WHERE'
                    if session['order'] == 'new':
                        order = ' ORDER BY datetime DESC'
                    else:
                        order = ' ORDER BY datetime ASC'
                    request = f'{request} user_id != {current_user.get_id()}{order}'
                    self.cursor.execute(request)
                else:
                    if session['order'] == 'new':
                        request += ' ORDER BY datetime DESC'
                    else:
                        request += ' ORDER BY datetime ASC'
                    print(request)
                    self.cursor.execute(request)
            else:
                if session['order'] == 'new':
                    request += ' ORDER BY datetime DESC'
                else:
                    request += ' ORDER BY datetime ASC'
                print(request)
                self.cursor.execute(request)

        return self.cursor.fetchall(), request

    def get_bg_post(self, subject):
        return subjects_of_posts[subject]

    def get_types_of_post(self):
        self.cursor.execute('SELECT DISTINCT type FROM posts')
        types = self.cursor.fetchall()
        res = []
        for type in types:
            self.cursor.execute(f'SELECT COUNT(type) FROM posts WHERE type = "{type[0]}"')
            res.append((type[0], f'{type[0]} ({self.cursor.fetchone()[0]})'))
        return res

    def get_types_of_posts(self, current_user):
        self.cursor.execute(f'SELECT DISTINCT type FROM POSTS WHERE user_id = {current_user.get_id()}')
        return self.cursor.fetchall()

    def get_timeread(self, text):
        cnt_min = len(text.split()) // 150 + 1
        minute = morph.parse('минута')[0]
        minute = minute.make_agree_with_number(cnt_min).word
        return f'{cnt_min} {minute}'

    def get_smiles(self):
        self.cursor.execute('SELECT * FROM smiles')
        return self.cursor.fetchall()

    def add_smile(self, field, post_id, current_user, user_id):
        if current_user.is_authenticated:
            self.cursor.execute(
                f'SELECT COUNT(*) as cnt FROM reactions WHERE user_id = {current_user.get_id()} AND post_id = {post_id}')
            res1 = self.cursor.fetchone()['cnt']
            if res1 == 0 and user_id != current_user.get_id():
                self.cursor.execute(f'UPDATE posts SET {field} = {field} + 1 WHERE id = "{post_id}"')
                self.connect.commit()

                self.cursor.execute(f'''INSERT INTO reactions (user_id, post_id, reaction)
                                        VALUES ("{current_user.get_id()}", {post_id}, "{field}")''')
                self.connect.commit()
                return False
            if res1 == 0:
                return 'Нельзя поставить реакцию себе!'
            return 'Установлен лимит на 1 реакцию!'
        return 'Необходимо зарегистрироваться!'

    def get_count_posts(self):
        self.cursor.execute('SELECT COUNT(*) FROM POSTS')
        return self.cursor.fetchone()[0]

    def get_own_posts(self, current_user):
        if not current_user is None:
            self.cursor.execute(f'SELECT COUNT(*) as cnt FROM posts WHERE user_id = "{current_user.get_id()}"')
            return self.cursor.fetchone()['cnt']
        return 0

    def find_post(self, id):
        self.cursor.execute(f'SELECT * FROM posts WHERE id = "{id}"')
        return self.cursor.fetchone()

    def update_info_user(self, info, type, current_user):
        self.cursor.execute(f'UPDATE users SET {type} = {info} WHERE id = "{current_user.get_id()}"')
        self.connect.commit()

    def add_data_user(self, type, value, current_user):
        if type == 'fio':
            self.cursor.execute(
                f"""UPDATE users SET first_name = '{value[1]}', surname = '{value[0]}', last_name = '{value[2]}'
                                           WHERE id = {current_user.get_id()}
                       """)
        else:
            self.cursor.execute(f"""UPDATE users SET {type} = '{value}'
                                WHERE id = {current_user.get_id()}
            """)
        self.connect.commit()

    def check_unical_value(self, data, current_user):
        if data != 'fio':
            self.cursor.execute(f'SELECT {data} FROM users WHERE id = "{current_user.get_id()}"')
            return self.cursor.fetchone()[0]
        self.cursor.execute(f'SELECT surname, first_name, last_name FROM users WHERE id = "{current_user.get_id()}"')
        res = self.cursor.fetchall()[0]
        return res

    def get_compl_achies(self, current_user):
        self.cursor.execute(f"""SELECT achies.*
                             FROM achies
                             LEFT JOIN compl_achies ON achies.id = compl_achies.achie_id
                             WHERE compl_achies.user_id = '{current_user.get_id()}'""")
        return self.cursor.fetchall()

    def get_achies(self, current_user):
        self.cursor.execute(f"""SELECT achies.*
                            FROM achies
                            LEFT JOIN compl_achies ON achies.id = compl_achies.achie_id
                            WHERE compl_achies.user_id IS NULL""")
        return self.cursor.fetchall()

    def get_owner_post(self, id):
        print(id)
        self.cursor.execute(f'''SELECT user_id 
                            FROM posts 
                            WHERE id = "{id}"''')
        return self.cursor.fetchone()['user_id']

    def update_views(self, id):
        self.cursor.execute(f'''UPDATE posts
                            SET seen = seen + 1
                            WHERE id = "{id}"''')
        self.connect.commit()

    def get_user(self, id):
        self.cursor.execute(f'SELECT name FROM users WHERE id = "{id}"')
        return self.cursor.fetchone()['name']

    def add_views(self, user_id, post_id, current_user):
        if current_user.is_authenticated:
            self.cursor.execute(f'''INSERT INTO views (user_id, post_id)
                                VALUES ({user_id}, {post_id})''')
            self.connect.commit()
        return None

    def check_is_been_views(self, user_id, post_id):
        self.cursor.execute(f'''SELECT COUNT(*) as cnt FROM views
                            WHERE user_id = "{user_id}" 
                            AND post_id = "{post_id}"''')
        return self.cursor.fetchone()['cnt']

    def get_progress_achies(self, achie_id, current_user):
        types_of_post = {
            0: 'Статья',
            1: 'История',
            2: 'Сообщение'
        }
        if achie_id in range(1, len(subjects_of_posts) * 2 + 1):
            self.cursor.execute(f'''SELECT COUNT(*)
                                FROM posts
                                WHERE user_id = "{current_user.get_id()}"''')

        if 27 <= achie_id <= 32:
            self.cursor.execute(f'''SELECT COUNT(*)
                                FROM posts
                                WHERE user_id = "{current_user.get_id()}"
                                AND type = "{types_of_post[achie_id % 3]}"''')

        if 33 <= achie_id <= 41:
            self.cursor.execute(f"""SELECT seen
                                FROM POSTS
                                WHERE type = '{types_of_post[achie_id % 3]}'""")

        if 42 <= achie_id <= 44:
            self.cursor.execute(f'''SELECT COUNT(*) FROM friends
            WHERE (id1 = {current_user.get_id()} OR id2 = {current_user.get_id()})''')

        else:
            self.cursor.execute(f'''SELECT COUNT(*)
                                FROM reactions
                                JOIN posts ON reactions.post_id = posts.id
                                WHERE posts.user_id = "{current_user.get_id()}"''')
        return self.cursor.fetchone()[0]

    def add_compl_achie(self, achie_id, current_user):
        self.cursor.execute(f"INSERT INTO compl_achies (achie_id, user_id) VALUES ({achie_id}, {current_user.get_id()})")
        self.connect.commit()

        self.cursor.execute(f'SELECT price FROM achies WHERE id = {achie_id}')
        price = self.cursor.fetchone()['price']

        self.cursor.execute(f"""UPDATE users
                            SET coins = coins + {price}
                            WHERE id = {current_user.get_id()}""")

    def get_friends(self, current_user):
        self.cursor.execute(f"""SELECT users.*, friends.id as frship_id FROM friends
                            JOIN users ON users.id IN (id1, id2)
                            WHERE users.id != {current_user.get_id()}
                            AND (id1 = {current_user.get_id()} OR id2 = {current_user.get_id()})""")
        return self.cursor.fetchall()

    def get_prop_friends(self, cnt_friends, current_user):
        res = []
        for friend_id in range(1, cnt_friends + 1):
            if friend_id != int(current_user.get_id()):
                print(friend_id)
                self.cursor.execute(f"""SELECT id1 FROM friends
                                    WHERE id1 IN ({current_user.get_id()}, {friend_id})
                                    AND id2 IN ({current_user.get_id()}, {friend_id})""")
                res1 = self.cursor.fetchone()
                self.cursor.execute(f"""SELECT sender FROM request_friends
                                WHERE sender IN ({current_user.get_id()}, {friend_id})
                                AND receiver IN ({current_user.get_id()}, {friend_id})""")
                res2 = self.cursor.fetchone()
                if res1 is None and res2 is None:
                    self.cursor.execute(f"SELECT users.* FROM users WHERE id = {friend_id}")
                    res.append(self.cursor.fetchone())
        return res

    def get_cnt_prop_friends(self, current_user):
        self.cursor.execute("SELECT MAX(id) as mx FROM users")
        return self.get_prop_friends(self.cursor.fetchone()['mx'], current_user)

    def add_request_friend(self, sender, receiver):
        self.cursor.execute(f'INSERT INTO request_friends (sender, receiver) VALUES ({sender}, {receiver})')
        self.connect.commit()

    def get_request_friend(self, receiver):
        self.cursor.execute(f'''SELECT users.*, request_friends.id as request_id FROM request_friends
                            JOIN users ON sender = users.id
                            WHERE receiver = {receiver}''')
        return self.cursor.fetchall()

    def get_cnt_friends(self, id):
        self.cursor.execute(f"SELECT COUNT(*) as cnt FROM friends WHERE id1 = {id} OR id2 = {id}")
        return self.cursor.fetchone()['cnt']

    def get_cnt_request_friends(self, id):
        self.cursor.execute(f'''SELECT COUNT(*) as cnt FROM request_friends
                            WHERE receiver = {id}''')
        return self.cursor.fetchone()['cnt']

    def add_friend(self, id):
        print(id)
        self.cursor.execute(f'SELECT * FROM request_friends WHERE id = {id}')
        res = self.cursor.fetchone()
        print(id)
        id1, id2 = res['sender'], res['receiver']

        self.delete_request_friend(id)

        self.cursor.execute(f'INSERT INTO friends (id1, id2) VALUES ({id1}, {id2})')
        self.connect.commit()

    def delete_request_friend(self, id):
        self.cursor.execute(f'DELETE FROM request_friends WHERE id = {id}')
        self.connect.commit()

    def delete_friend(self, id):
        self.cursor.execute(f'DELETE FROM friends WHERE id = {id}')
        self.connect.commit()
        return None

    def cnt_users(self):
        self.cursor.execute('SELECT COUNT(name) as cnt FROM users')
        return self.cursor.fetchone()

    def cnt_subjs(self):
        self.cursor.execute('SELECT COUNT(*) as cnt FROM subjects_of_posts')
        return self.cursor.fetchone()

    def cnt_money(self, current_user):
        self.cursor.execute(f'SELECT coins FROM users WHERE id = {current_user.get_id()}')
        return self.cursor.fetchone()['coins']

    def cnt_all_money(self):
        self.cursor.execute('SELECT SUM(price) as cnt FROM achies')
        return self.cursor.fetchone()['cnt']

