from django.db import models

class Course(models.Model):
	number = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=50)

class Student(models.Model):
	eid = models.CharField(max_length=10, primary_key=True)
	password = models.CharField(max_length=32)

class Professor(models.Model):
	eid = models.CharField(max_length=10, primary_key=True)
	password = models.CharField(max_length=32)
	courses = models.ManyToManyField(Course)

class TA(models.Model):
	eid = models.CharField(max_length=10, primary_key=True)
	password = models.CharField(max_length=32)
	courses = models.ManyToManyField(Course)

class Question(models.Model):
	eid = models.ForeignKey(Student, on_delete=models.CASCADE)
	time = models.DateTimeField('time added')
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
	professor = models.ForeignKey(Professor, on_delete=models.SET_NULL, null=True)
	assignment = models.CharField(max_length=20)
	question = models.TextField(max_length=200)



