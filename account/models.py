from django.db import models
from django.contrib import admin

class account (models.Model):
    username = models.CharField (max_length= 30, primary_key=True)
    password = models.CharField (max_length= 30)

class Lab(models.Model):
    name= models.CharField (max_length= 30)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    location=models.CharField(max_length=20)
    no_of_computer=models.IntegerField()
    no_of_printers=models.IntegerField()
    no_of_scanners=models.IntegerField()
    no_of_comm_devices=models.IntegerField()
    comm_devices_cost=models.IntegerField()
    no_of_ups=models.IntegerField()
    ups_cost=models.IntegerField()
    incharge=models.EmailField()
    assistant=models.EmailField()
    complaints_made=models.IntegerField()
    complaints_resolved=models.IntegerField()
    cost=models.IntegerField()




class Computer(models.Model):
    STATUS_CHOICES = (
        ('ON', 'Working'),
        ('OFF', 'Not Working'),
    )
    COST_CHOICES = (
        ('1', 'Consider'),
        ('0', 'Don\'t Consider'),
    )
    OS_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    def __str__(self):              # __unicode__ on Python 2
        return self.computer_name

    lab= models.ForeignKey(Lab,related_name='Computer_lab')
    computer_name= models.CharField(max_length=15)
    dead_stock_no=models.CharField(max_length=35)
    ip_address=models.CharField(max_length=20)
    mac_address=models.CharField(max_length=25)
    complaints_made=models.IntegerField()
    complaints_resolved=models.IntegerField()
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
    description=models.CharField(max_length=300)
    processor=models.CharField(max_length=50)
    ram=models.CharField(max_length=7)
    hdd=models.CharField(max_length=10)
    graphics=models.CharField(max_length=50)
    cost=models.IntegerField()
    cost_flag=models.CharField(max_length=20,choices=COST_CHOICES)

class ComplaintType(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):              # __unicode__ on Python 2
        return self.name

class CommonComplaints(models.Model):
    COMPLAINT_CHOICES=(
        ('RAM','RAM crashed'),
        ('Input Device','Keyboard/Mouse not found'),
        ('Printer SW Error','Printer not working or not installed'),
        ('Printer HW Error','Printer toner empty'),
        ('OS Error','Ubuntu/Windows not Installed'),
        ('SW Error','Required software not Installed'),
        )
    def __str__(self):              # __unicode__ on Python 2
        return self.complaint

    complaint_type= models.ForeignKey(ComplaintType)
    complaint=models.CharField(max_length=50)
    complaints_made=models.IntegerField()
    complaints_resolved=models.IntegerField()
    critical=models.IntegerField()


class Complaint(models.Model):
    STATUS_CHOICES=(
        ('SOLVED','Solved'),
        ('PENDING','Pending'),
        )
    lab= models.ForeignKey(Lab)
    computer_name=models.ForeignKey(Computer)
    complaint=models.ForeignKey(CommonComplaints,related_name='complaint_commoncomplaint')
    date=models.DateField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES)

class Printers(models.Model):
    COST_CHOICES = (
        ('1', 'Consider'),
        ('0', 'Don\'t Consider'),
    )

    STATUS_CHOICES = (
        ('ON', 'Working'),
        ('OFF', 'Not Working'),
    )
    lab= models.ForeignKey(Lab,related_name='printer_lab')
    computer=models.ForeignKey(Computer,related_name='printer_computer')
    dead_stock_no=models.CharField(max_length=35)
    mfg_desc=models.CharField(max_length=50)
    toner_date=models.DateField()
    cost=models.IntegerField()
    complaints_made=models.IntegerField()
    complaints_resolved=models.IntegerField()
    status= models.CharField(max_length=3, choices=STATUS_CHOICES)
    cost_flag=models.CharField(max_length=20,choices=COST_CHOICES)

class Scanners(models.Model):
    COST_CHOICES = (
        ('1', 'Consider'),
        ('0', 'Don\'t Consider'),
    )

    STATUS_CHOICES = (
        ('ON', 'Working'),
        ('OFF', 'Not Working'),
    )
    lab= models.ForeignKey(Lab,related_name='scanner_lab')
    computer=models.ForeignKey(Computer,related_name='scanner_computer')
    dead_stock_no=models.CharField(max_length=35)
    mfg_desc=models.CharField(max_length=50)
    cost=models.IntegerField()
    complaints_made=models.IntegerField()
    complaints_resolved=models.IntegerField()
    status= models.CharField(max_length=3, choices=STATUS_CHOICES)
    cost_flag=models.CharField(max_length=20,choices=COST_CHOICES)


admin.site.register (account)
admin.site.register (Computer)
admin.site.register (Lab)
admin.site.register (CommonComplaints)
admin.site.register (ComplaintType)
admin.site.register (Complaint)
admin.site.register (Printers)
admin.site.register (Scanners)