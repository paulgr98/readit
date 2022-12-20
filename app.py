import PySimpleGUI as sg
import sqlite3
import faker
import random
from passlib.hash import pbkdf2_sha256
import asyncpraw
import asyncstdlib as a
import asyncio
import datetime as dt
import config as cfg


class User(object):
    def __init__(self):
        self.id = None
        self.password = None
        self.last_login = None
        self.is_superuser = None
        self.username = None
        self.first_name = None
        self.last_name = None
        self.email = None
        self.is_staff = None
        self.is_active = None
        self.date_joined = None


class ReaditUser(object):
    def __init__(self):
        self.user = User()
        self.about_text = None
        self.avatar_url = None
        self.karma = None


class Subreadit(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.description = None
        self.created_at = None
        self.owner_id = None


class Submission(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.upvotes = None
        self.downvotes = None
        self.image_url = None
        self.created_at = None
        self.author_id = None
        self.subreadit_id = None
        self.text = None


class Comment(object):
    def __init__(self):
        self.id = None
        self.created_at = None
        self.upvotes = None
        self.downvotes = None
        self.submission_id = None
        self.user_id = None
        self.content = None


async def generate_data(file_location):
    with sqlite3.connect(file_location) as conn:
        c = conn.cursor()

        users = generate_users(10)
        add_users_to_db(users, c)
        print("Users added to database")

        subs = ['Polska', 'Polska_wpz', 'okkolegauposledzony', 'ProgrammerHumor']
        subreadits = generate_subreadits(subs)
        add_subreadits_to_db(subreadits, c)
        print("Subreadits added to database")

        submissions = await generate_submissions(100)
        add_submissions_to_db(submissions, c)
        print("Submission added to database")

        comments = generate_n_comments_for_submissions(10, submissions)
        add_comments_to_db(comments, c)
        print("Comments added to database")

        conn.commit()


def generate_users(number_of_users: int) -> list[ReaditUser]:
    gen = faker.Faker()
    rdt_users = []
    start_id = 100
    for i in range(start_id, start_id + number_of_users):
        user = User()
        user.id = i
        user.password = pbkdf2_sha256.hash("password")[1:]
        user.last_login = gen.date_time()
        user.is_superuser = False
        user.first_name = gen.first_name()
        user.last_name = gen.last_name()
        user.username = make_username(user.first_name, user.last_name)
        user.email = user.username + '@gmail.com'
        user.is_staff = False
        user.is_active = True
        user.date_joined = gen.date_time()

        rdt_user = ReaditUser()
        rdt_user.user = user
        rdt_user.about_text = gen.text()
        rdt_user.avatar_url = gen.image_url()
        rdt_user.karma = random.randint(0, 10000)

        rdt_users.append(rdt_user)
    return rdt_users


def make_username(first_name: str, last_name: str) -> str:
    username = ''
    username += first_name[:3].lower()
    username += last_name[:3].lower()
    for _ in range(3):
        username += str(random.randint(0, 9))
    return username


def add_users_to_db(users: list[ReaditUser], cursor: sqlite3.Cursor):
    for user in users:
        command = f"INSERT INTO auth_user VALUES ({user.user.id}, '{user.user.password}', " \
                  f"'{user.user.last_login}', {user.user.is_superuser}, '{user.user.username}', " \
                  f"'{user.user.last_name}', '{user.user.email}', {user.user.is_staff}, " \
                  f"{user.user.is_active}, '{user.user.date_joined}', '{user.user.first_name}')"
        cursor.execute(command)

        command = f"INSERT INTO users_readituser VALUES ({user.user.id}, '{user.avatar_url}'," \
                  f"{user.karma}, {user.user.id}, '{user.about_text}')"
        cursor.execute(command)


def generate_subreadits(subs: list[str]) -> list[Subreadit]:
    gen = faker.Faker()
    subreadits = []
    start_id = 100
    number_of_subreadits = len(subs)
    for i in range(start_id, start_id + number_of_subreadits):
        subreadit = Subreadit()
        subreadit.id = i
        subreadit.name = subs[i - start_id]
        subreadit.description = gen.text()
        subreadit.created_at = gen.date_time()
        subreadit.owner_id = random.randint(100, 109)
        subreadits.append(subreadit)
    return subreadits


def add_subreadits_to_db(subreadits: list[Subreadit], cursor: sqlite3.Cursor):
    for subreadit in subreadits:
        command = f"INSERT INTO subreadits_subreadit VALUES ({subreadit.id}, '{subreadit.name}', " \
                  f"'{subreadit.created_at}', {subreadit.owner_id}, '{subreadit.description}')"
        cursor.execute(command)


async def generate_submissions(number_of_submissions: int):
    submissions = []

    async with asyncpraw.Reddit(client_id=cfg.CLIENT_ID,
                                client_secret=cfg.CLIENT_SECRET,
                                user_agent=cfg.USER_AGENT) as reddit:
        sub = await reddit.subreddit('ProgrammerHumor')
        await sub.load()
        posts = sub.hot(limit=number_of_submissions)

        start_id = 100
        async for i, post in a.enumerate(posts, start=start_id):
            submission = Submission()
            submission.id = i
            submission.title = replace_bad_chars(post.title)
            submission.upvotes = post.score
            submission.downvotes = int(post.score / post.upvote_ratio - post.score)
            submission.image_url = post.url
            submission.created_at = dt.datetime.fromtimestamp(post.created_utc)
            submission.author_id = random.randint(100, 109)
            submission.subreadit_id = 103
            submission.text = replace_bad_chars(post.selftext)

            submissions.append(submission)

    return submissions


def replace_bad_chars(text: str) -> str:
    text = text.replace("'", "")
    text = text.replace('"', "")
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text


def add_submissions_to_db(submissions: list[Submission], cursor: sqlite3.Cursor):
    for submission in submissions:
        command = f"INSERT INTO submissions_submission VALUES ({submission.id}, '{submission.title}', " \
                  f"{submission.upvotes}, {submission.downvotes}, '{submission.image_url}', " \
                  f"'{submission.created_at}', {submission.author_id}, {submission.subreadit_id}, " \
                  f"'{submission.text if submission.text else ' '}')"
        cursor.execute(command)


def generate_n_comments_for_submissions(num_of_comments: int, submissions: list[Submission]) -> list[Comment]:
    gen = faker.Faker()
    comments = []
    comment_id = 100
    for sub in submissions:
        for _ in range(num_of_comments):
            comment = Comment()
            comment.id = comment_id
            comment.created_at = gen.date_time()
            comment.upvotes = random.randint(0, 100)
            comment.downvotes = random.randint(0, 10)
            comment.submission_id = sub.id
            comment.user_id = random.randint(100, 109)
            comment.content = gen.text()

            comments.append(comment)
            comment_id += 1
    return comments


def add_comments_to_db(comments: list[Comment], cursor: sqlite3.Cursor):
    for comment in comments:
        command = f"INSERT INTO comments_comment VALUES ({comment.id}, '{comment.created_at}', " \
                  f"{comment.upvotes}, {comment.downvotes}, {comment.submission_id}, " \
                  f"{comment.user_id}, '{comment.content}')"
        cursor.execute(command)


async def main():
    layout = [[sg.Text("Select the database file: ")],
              [sg.Input(), sg.FileBrowse()],
              [sg.Button("Generate")]]
    window = sg.Window("Readit Data Generator", layout)
    event, values = window.read()
    await generate_data(values[0])
    window.close()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
