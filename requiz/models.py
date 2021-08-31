from django.db import models
import bcrypt
import re

email_reg = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class KidUserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}        
        user_emails = KidUser.objects.filter(email = postData['email'])
        if len(postData['first_name']) == 0:
            errors['blank_first'] = "First name cannot be blank"
        if len(postData['first_name']) < 2:
            errors['short_first'] = "First name must 2 letters or more"
        if len(postData['last_name']) == 0:
            errors['blank_last'] = "Last name cannot be blank"
        if len(postData['last_name']) < 2:
            errors['short_last'] = "Last name must 2 letters or more"
        if len(postData['email']) == 0:
            errors['blank_email'] = "Email is required"
        if not email_reg.match(postData['email']):
            errors['not_email'] = "Not a valid email"
        if user_emails:
            errors['user_email'] = "Email already in use"
        if len(postData['password']) == 0:
            errors['blank_pass'] = "Password is required"
        if len(postData['pw_conf']) < 6:
            errors['password'] = "Password must be 6 characters or more"
        if postData['password'] != postData['pw_conf']:
            errors['confirm'] = "Passwords do not match"
        return errors

    def log_val(self, postData):
        errors = {}
        user_emails = KidUser.objects.filter(email = postData['email'])
        if len(postData['email']) == 0:
            errors['blank_email'] = "Email is required"
        if not email_reg.match(postData['email']):
            errors['email'] = "Invalid email address"
        if not user_emails:
            errors['exist_email'] = "Email does not exist"
        if len(postData['password']) < 6:
            errors['password'] = "Password must be at least 6 characters"
        if bcrypt.checkpw(postData['password'].encode(), user_emails[0].password.encode()):
            print('password match')
        else:
            errors['bad_password'] = "Email and password do not match"
        return errors
        

class KidUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = KidUserManager()

class AdultUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.BooleanField()
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = AdultUserManager()

class Query(models.Model):
    question = models.CharField(max_length=200, null=True)
    op1 = models.CharField(max_length=200, null=True)
    op2 = models.CharField(max_length=200, null=True)
    op3 = models.CharField(max_length=200, null=True)
    op4 = models.CharField(max_length=200, null=True)
    ans = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.question

# Create your models here.

class Question(models.Model):
    question = models.CharField(max_length=200, null=True)
    answer = models.CharField(max_length=200, null=True)
    option = models.ForeignKey(Option, related_name="")

    def __str__(self):
        return self.question, self.answer

class Option(models.Model):
    option = models.CharField(max_length=200, null=True)
