from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re


EMAIL_REGEX= re.compile(r'^[a-zA-A0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Picker_upper:
    schema="poop_project"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password= data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # this needs to be a list
        self.puppy_parent_ids= []


    @staticmethod
    def validate_picker_upper(picker_upper):
        is_valid=True
        if len(picker_upper['first_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(picker_upper['first_name']) < 3:
            flash('First name must be atleast 3 characters long.')
            is_valid=False
        if len(picker_upper['last_name']) < 1:
            flash('Last name cannot be blank.')
            is_valid=False
        elif len(picker_upper['last_name']) < 3:
            flash('Last name must be atleast 3 characters long.')
            is_valid=False
        if len(picker_upper['email'])<1:
            flash('Email cannot be blank')
            is_valid=False
        elif len(picker_upper['email']) < 8:
            flash('Email must be atleast 8 characters long')
            is_valid=False
        elif not EMAIL_REGEX.match(picker_upper['email']):
            flash('Invalid email format')
            is_valid=False
        if len(picker_upper['password']) < 1:
            flash('Password cannot be blank.')
            is_valid=False
        elif len(picker_upper['password']) < 8:
            flash('Password must be atleast 8 characters long.')
            is_valid=False
        if len(picker_upper['confirm_password']) < 1:
            flash('Please confirm your password.')
            is_valid=False
        elif picker_upper['password']!=picker_upper['confirm_password']:
            flash("Your passwords do not match.")
            is_valid=False
        return is_valid

    # CREATE
    @classmethod
    def save(cls,data):
        query= "INSERT INTO picker_uppers (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW() );"
        results= connectToMySQL(cls.schema).query_db(query, data)
        return results

    #Do they exist?
    @classmethod
    def get_by_email(cls,email):
        query= "SELECT * FROM picker_uppers WHERE email = %(email)s;"
        results=connectToMySQL(cls.schema).query_db(query, {"email":email})
        if len(results)<1:
            return False
        return cls(results[0])








    
    # Read
    @classmethod
    def get_one(cls,id):
        query = "SELECT first_name FROM picker_uppers WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,{"id":id})
        picker_uppers = []
        for picker_upper in results:
            picker_uppers.append( picker_upper )
        return picker_uppers





    #Validate New picker_upper
    @staticmethod
    def validate_picker_upper(picker_upper):
        is_valid=True
        if len(picker_upper['first_name']) < 1:
            flash('First name cannot be blank.')
            is_valid=False
        elif len(picker_upper['first_name']) < 3:
            flash('First name must be atleast 3 characters long.')
            is_valid=False
        if len(picker_upper['last_name']) < 1:
            flash('Last name cannot be blank.')
            is_valid=False
        elif len(picker_upper['last_name']) < 3:
            flash('Last name must be atleast 3 characters long.')
            is_valid=False
        if len(picker_upper['email'])<1:
            flash('Email cannot be blank')
            is_valid=False
        elif len(picker_upper['email']) < 8:
            flash('Email must be atleast 8 characters long')
            is_valid=False
        elif not EMAIL_REGEX.match(picker_upper['email']):
            flash('Invalid email format')
            is_valid=False
        if len(picker_upper['password']) < 1:
            flash('Password cannot be blank.')
            is_valid=False
        elif len(picker_upper['password']) < 8:
            flash('Password must be atleast 8 characters long.')
            is_valid=False
        if len(picker_upper['confirm_password']) < 1:
            flash('Please confirm your password.')
            is_valid=False
        elif picker_upper['password']!=picker_upper['confirm_password']:
            flash("Your passwords do not match.")
            is_valid=False
        return is_valid

