from flask import flash

from flask_app.config.mysqlconnections import connectToMySQL

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    db = 'login_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls,data):
        query = 'select * from users where email = %(email)s;'
        results = connectToMySQL('login_schema').query_db(query,data)

        if len(results) < 1:
            return False

        return User(results[0])


    @classmethod
    def get_by_id(cls,data):
        query = 'select * from users where id = %(id)s;'
        results = connectToMySQL('login_schema').query_db(query,data)

        if len(results) < 1:
            return False

        return User(results[0])


    @classmethod
    def create(cls,data):
        query = 'insert into users (first_name, last_name, email, password, created_at, updated_at) values (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());'
        
        return connectToMySQL('login_schema').query_db(query,data)


    @staticmethod
    def register_valid(post_data):
        is_valid = True

        if len(post_data['first_name']) < 2:
            flash('First Name must be at least 2 characters.')
            is_valid = False

        if len(post_data['last_name']) < 2:
            flash('Last Name must be at least 2 characters.')
            is_valid = False

        if not EMAIL_REGEX.match(post_data['email']): 
            flash("Invalid email address!")
            is_valid = False
        else:
            user = User.get_by_email({'email': post_data['email']})
            if user:
                flash('Email is already in use.')
                is_valid = False

        if len(post_data['password']) < 8:
            flash('Password must be at least 8 characters.')
            is_valid = False 

        if post_data['password'] != post_data['confirm_password']:
            flash('Password does not match.')
            is_valid = False

        return is_valid

    
    @staticmethod
    def login_valid(post_data):
        pass