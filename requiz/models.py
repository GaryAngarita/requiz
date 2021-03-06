from django.db import models
from django.utils.translation import gettext_lazy as _
import bcrypt
import re

from django.db.models.deletion import DO_NOTHING

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

# class Question(models.Model):
#     question = models.CharField(max_length=200, null=True)
#     answer = models.CharField(max_length=200, null=True)

#     def __str__(self):
#         return self.question

# class Option(models.Model):
#     option = models.CharField(max_length=200, null=True)
#     question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)

#     def __str__(self):
#         return self.option


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Quizzes(models.Model):

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = ("Quizzes")
        ordering = ['id']

    category = models.ForeignKey(Category, default=1, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=255, default=_("New Quiz"), verbose_name=_("Quiz Title"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Updated(models.Model):
    date_updated = models.DateTimeField(verbose_name=_("Last Updated"), auto_now=True)

    class Meta:
        abstract = True

class Question(Updated):

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['id']

    SCALE = (
        (0, _('Fundamental')),
        (1, _('Beginner')),
        (2, _('Intermediate')),
        (3, _('Advanced')),
        (4, _('Expert'))
    )

    TYPE = (
        (0, _('Multiple Choice')),
    )
        
    quiz = models.ForeignKey(Quizzes, related_name="question", on_delete=DO_NOTHING)
    technique = models.IntegerField(choices=TYPE, default=0, verbose_name=_("Type of Question"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    difficulty = models.IntegerField(choices=SCALE, default=0, verbose_name=_("Difficulty"))
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False, verbose_name=_("Active Status"))

    def __str__(self):
        return self.title

class Answer(Updated):

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['id']

    question = models.ForeignKey(Question, related_name="answer", on_delete=DO_NOTHING)
    answer_text = models.CharField(max_length=255, verbose_name=_("Answer Text"))
    is_right = models.BooleanField(default=False)
# Create your models here.


