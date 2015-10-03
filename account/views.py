# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from file_read import read
from django.template import Template, Context
#from django.shortcuts import render
import MySQLdb as msdb
import time
#Email
from django.core.mail import send_mail
from models import Computer,Complaint,Lab,CommonComplaints,Printers,Scanners

ranges=[]  #Global variable for range query
global error
error=  ''

construct_complaint=[]
class CompList(object):
    def __init__ (self, computer):
        self.computer = computer

class ComplaintTypes(object):
    def __init__ (self, name):
        self.name=name

class PrinterList(object):
    def __init__ (self, dead_stock_no,toner_date,status,pc_name,cost,mfg_desc):
        self.dead_stock_no=dead_stock_no
        self.toner_date=toner_date
        self.status=status
        self.pc_name=pc_name
        self.cost=cost
        self.mfg_desc=mfg_desc

class ScannerList(object):
    def __init__ (self, dead_stock_no,mfg_desc,status,pc_name,cost):
        self.dead_stock_no=dead_stock_no
        self.status=status
        self.pc_name=pc_name
        self.cost=cost
        self.mfg_desc=mfg_desc


class Result (object):
    def __init__ (self, computer,deadStock,ip,status,description,processor,ram,hdd,graphics,cost):
        self.status = status
        self.computer = computer
        self.ip=ip
        self.deadStock=deadStock
        self.description=description
        self.processor=processor
        self.ram=ram
        self.hdd=hdd
        self.graphics=graphics
        self.cost=cost

class Labs(object):
    def __init__(self,lab,location,pcs,printers,scanners,com_devices,com_cost,ups,ups_cost,incharge,assistant,made,solved,cost):
        self.lab = lab
        self.pcs = pcs
        self.printers = printers
        self.scanners = scanners
        self.cost = cost
        self.location=location
        self.com_devices=com_devices
        self.com_cost=com_cost
        self.ups=ups
        self.ups_cost=ups_cost
        self.incharge=incharge
        self.assistant=assistant
        self.made=made
        self.solved=solved

class ComplaintList(object):
    def __init__(self,complaint_id,lab,computer_name,date,status,complaint):
        self.lab=lab
        self.computer_name=computer_name
        self.complaint_id=complaint_id
        self.date=date
        self.status=status
        self.complaint=complaint
#End of Declaration Section**************************

def connect():
    conn=msdb.connect('mysql.server','kedark7893','apurva','kedark7893$clrms')
    return conn


def love(request):
    code = read('/home/kedark7893/clrms/templates/love.html')
    t= Template(code)
    c = Context()
    return HttpResponse(t.render(c))


#Login Related Views**********************************************************
def home(request):
    code = read('/home/kedark7893/clrms/templates/login.html')
    t= Template(code)
    c = Context()
    request.session.clear()
    return HttpResponse(t.render(c))


def login_check(request):
    global error
    conn = connect()
    cur = conn.cursor()
    uname= request.POST['uname']
    password = request.POST['password']

    cur.execute("select password from account_account where username = '%s'"%uname)
    for row in cur.fetchall():
        if row[0] == password:
            request.session['user'] = uname
            conn.close()
            return HttpResponseRedirect('http://kedark7893.pythonanywhere.com/welcome')

    error = 'Wrong Password'
    conn.close()
    code = read('/home/kedark7893/clrms/templates/login.html')
    t= Template(code)
    c = Context({'error': error})
    return HttpResponse(t.render(c))

#Sign up Related Views**********************************************************
def signup_check(request):
    conn = connect()
    cur = conn.cursor()
    uname= request.POST['uname']
    password = request.POST['password']
    try:
        unumber=int(uname.rstrip('@mitcoe.ac.in'))
    except Exception as e:
        error='Use valid ERP number for username'
        conn.close()
        code = read('/home/kedark7893/clrms/templates/login.html')
        t= Template(code)
        c = Context({'error': error})
        return HttpResponse(t.render(c))


    if uname.find('@mitcoe.ac.in') !=-1 or uname.find('@mitcoe.edu.in') !=-1 :

        try:
            cur.execute("insert into account_account values('%s','%s')"%(uname,password))
            error = 'Signup successful'
            conn.commit ()
            conn.close()
            #code = read('/home/kedark7893/clrms/templates/welcome.html')
            #t= Template(code)
            #c = Context({'error': error})
            request.session['user'] = uname
            return HttpResponseRedirect("http://kedark7893.pythonanywhere.com/welcome")
        except msdb.IntegrityError:
            error = 'Username already exists'
            conn.close()
            code = read('/home/kedark7893/clrms/templates/login.html')
            t= Template(code)
            c = Context({'error': error})
            return HttpResponse(t.render(c))
    else:
        error='Use valid ERP number for username'
        conn.close()
        code = read('/home/kedark7893/clrms/templates/login.html')
        t= Template(code)
        c = Context({'error': error})
        return HttpResponse(t.render(c))

def welcome(request):
    global error
    try:
        u=request.session['user']
        conn = connect()
        cur = conn.cursor()

        cur.execute ("select * from account_lab")
        results=[]
        for row in cur.fetchall ():
            results.append (Labs (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))


        code = read('/home/kedark7893/clrms/templates/welcome.html')
        t= Template(code)
        c = Context({'user':u,'results': results})
        conn.close()
        return HttpResponse(t.render(c))
    except Exception as e:
        error='Please login first!'
        code = read('/home/kedark7893/clrms/templates/login.html')
        t= Template(code)
        c = Context({'error': error})
        return HttpResponse(t.render(c))

#Lab Table Related Views******************************************************
def Dlab(request):
    lab=request.GET['name']
    code = read('/home/kedark7893/clrms/templates/dlab.html')
    t= Template(code)
    conn = connect()
    cur = conn.cursor()

    #if lab_choice==1:
    try:
        cur.execute ("select computer_name,dead_stock_no,ip_address,status,description,processor,ram,hdd,graphics,cost from account_computer where lab_id=(select id from account_lab where name='%s')"%lab)
        results = []
        for row in cur.fetchall ():
            if row[3]=="ON":
                results.append (Result (row[0],row[1],row[2],"Working",row[4],row[5],row[6],row[7],row[8],row[9]))
            else:
                results.append (Result (row[0],row[1],row[2],"Not Working",row[4],row[5],row[6],row[7],row[8],row[9]))
        cur.execute ("select dead_stock_no,toner_date,status,computer_id,cost,mfg_desc from account_printers where lab_id=(select id from account_lab where name='%s')"%lab)
        printers = []
        for row in cur.fetchall ():
            c=Computer.objects.get(id=row[3])
            printers.append (PrinterList (row[0],row[1],row[2],c.computer_name,row[4],row[5]))

        cur.execute ("select dead_stock_no,mfg_desc,status,computer_id,cost from account_scanners where lab_id=(select id from account_lab where name='%s')"%lab)
        scanner = []
        for row in cur.fetchall ():
            c=Computer.objects.get(id=row[3])
            scanner.append (ScannerList (row[0],row[1],row[2],c.computer_name,row[4]))

        total_cost=0
        cur.execute("select sum(cost) from account_computer where lab_id=(select id from account_lab where name='%s') and cost_flag=1"%lab)
        try:
            total_cost=total_cost+int(cur.fetchone()[0])
        except Exception as e:
            total_cost=total_cost+0
        cur.execute("select sum(cost) from account_printers where lab_id=(select id from account_lab where name='%s' and cost_flag=1)"%lab)
        try:
            total_cost=total_cost+int(cur.fetchone()[0])
        except Exception as e:
            total_cost=total_cost+0
        cur.execute("select sum(cost) from account_scanners where lab_id=(select id from account_lab where name='%s' and cost_flag=1)"%lab)
        try:
            total_cost=total_cost+int(cur.fetchone()[0])
        except Exception as e:
            total_cost=total_cost+0
        cur.execute ("select * from account_lab where name='%s'"%lab)
        labDetails=[]
        for row in cur.fetchall ():
            labDetails.append (Labs (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))
            total_cost=total_cost+row[7]+row[9]

        lab_cost_update=Lab.objects.get(name=lab)
        lab_cost_update.cost=total_cost
        lab_cost_update.save()
        c = Context({'results': results,'printers':printers,'name':lab,'details':labDetails,'cost':total_cost,'scanners':scanner})
        conn.close()
        return HttpResponse(t.render(c))
    except Exception as e:
        code = read('/home/kedark7893/clrms/templates/404.html')
        t= Template(code)
        c = Context({})
        return HttpResponse(t.render(c))

def overview(request):
    code = read('/home/kedark7893/clrms/templates/overview.html')
    t= Template(code)
    conn = connect()
    cur = conn.cursor()

    cur.execute ("select computer_name,dead_stock_no,ip_address,status,description,processor,ram,hdd,graphics,cost from account_computer")
    results = []
    for row in cur.fetchall ():
        if row[3]=="ON":
            results.append (Result (row[0],row[1],row[2],"Working",row[4],row[5],row[6],row[7],row[8],row[9]))
        else:
            results.append (Result (row[0],row[1],row[2],"Not Working",row[4],row[5],row[6],row[7],row[8],row[9]))

    cur.execute ("select dead_stock_no,toner_date,status,computer_id,cost,mfg_desc from account_printers")
    printers = []
    for row in cur.fetchall ():
        c=Computer.objects.get(id=row[3])
        printers.append (PrinterList (row[0],row[1],row[2],c.computer_name,row[4],row[5]))

    cur.execute ("select dead_stock_no,mfg_desc,status,computer_id,cost from account_scanners")
    scanner = []
    for row in cur.fetchall ():
        c=Computer.objects.get(id=row[3])
        scanner.append (ScannerList (row[0],row[1],row[2],c.computer_name,row[4]))

    total_cost=0
    cur.execute("select sum(cost) from account_computer")
    total_cost=total_cost+int(cur.fetchone()[0])
    cur.execute("select sum(cost) from account_printers")
    try:
        total_cost=total_cost+int(cur.fetchone()[0])
    except Exception as e:
        total_cost=total_cost+0
    cur.execute("select sum(cost) from account_scanners")
    try:
        total_cost=total_cost+int(cur.fetchone()[0])
    except Exception as e:
        total_cost=total_cost+0

    cur.execute ("select * from account_lab")
    labDetails=[]
    for row in cur.fetchall ():
        labDetails.append (Labs (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))
        total_cost=total_cost+row[7]+row[9]

    c = Context({'results': results,'printers':printers,'details':labDetails,'cost':total_cost,'scanners':scanner})
    conn.close()
    return HttpResponse(t.render(c))

#----------Search View------------------------------------------

def search(request):
    return
'''    code = read('/home/kedark7893/clrms/templates/searchresults.html')
    t= Template(code)
    search=request.GET['SearchString']
    conn=connect()
    cur=conn.cursor()

    try:
        cur.execute("select * from account_computer where dead_stock_no like '% "+ search +"%'")
        res=cur.fetchone()

    except Exception as e:
        try:
            cur.execute("select * from account_printers where dead_stock_no like '% "+ search +"%'")
            res=cur.fetchone()
        except Exception as e:
            try:
                cur.execute("select * from account_scanners where dead_stock_no like '% "+ search +"%'")
                res=cur.fetchone()
            except Exception as e:
                res="Sorry, No matching Results were found!"
    c=Context({'searchresults':res})

    return HttpResponse(t.render(c))

'''
#Complaint Releated Views**********************************************************
def complaint(request):
    try:
        u=request.session['user']
        code = read('/home/kedark7893/clrms/templates/complaint.html')
        t= Template(code)
        c = Context({'user':u})
        return HttpResponse(t.render(c))
    except Exception as e:
        error='Please login first!'
        code = read('/home/kedark7893/clrms/templates/login.html')
        t= Template(code)
        c = Context({'error': error})
        return HttpResponse(t.render(c))


def LabSelect(request):
    u=request.session['user']
    conn = connect()
    cur = conn.cursor()
    cur.execute ("select * from account_lab")
    results=[]
    for row in cur.fetchall ():
            results.append (Labs (row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))
    code = read('/home/kedark7893/clrms/templates/LabSelect.html')
    t= Template(code)
    c = Context({'results': results,'user':u})
    conn.close()
    return HttpResponse(t.render(c))

def ComplaintForm(request):
    u=request.session['user']
    lab=request.POST['selection']
    request.session['lab'] = lab
    conn = connect()
    cur = conn.cursor()
    cur.execute ("select id from account_lab where name='%s'"%lab)
    for row in cur.fetchall ():
            lab=int(row[0])
    cur.execute ("select computer_name from account_computer where lab_id=%d"%lab)
    results=[]
    for row in cur.fetchall ():
            results.append (CompList (row[0]))
    cur.execute ("select name from account_complainttype")
    complaint_types=[]
    for row in cur.fetchall ():
            complaint_types.append (ComplaintTypes (row[0]))

    conn.close()
    code = read('/home/kedark7893/clrms/templates/ComplaintForm.html')
    t= Template(code)
    c = Context({'result':results,'user':u,'complaint_types':complaint_types})
    return HttpResponse(t.render(c))

def complaint_final(request):
    u=request.session['user']
    type_of_complaint=request.POST['type_of_complaint']
    computer=request.POST['selection']
    request.session['computer']=computer
    request.session['type_of_complaint']=type_of_complaint

    if type_of_complaint == "Hardware" or type_of_complaint=="Software":
        var = "software"
    else:
        var = "other"

    conn = connect()
    cur = conn.cursor()
    cur.execute ("select * from account_commoncomplaints where complaint_type_id=(select id from account_complainttype where name='%s')"%type_of_complaint)
    complaint_types=[]
    for row in cur.fetchall ():
       complaint_types.append (ComplaintTypes (row[2]))

    conn.close()
    code = read('/home/kedark7893/clrms/templates/ComplaintFinal.html')
    t= Template(code)
    c = Context({'user':u,'complaint_types':complaint_types, 'var':var})
    return HttpResponse(t.render(c))


def complaint_send(request):

    u=request.session['user']
    lab_name=request.session['lab']
    description=request.POST['describe']
    computer=request.session['computer']
    type_of_complaint=request.session['type_of_complaint']
    if type_of_complaint == "Hardware" or type_of_complaint=="Software":
        selected= request.POST['selection']
    else:
        selected="other"

    construct_complaint=[]
    conn = connect()
    cur = conn.cursor()
    cur.execute ("select dead_stock_no,ip_address,mac_address from account_computer where computer_name='%s'"%computer)
    for row in cur.fetchall ():
       construct_complaint.append (row[0])
       construct_complaint.append (row[1])
       construct_complaint.append (row[2])


    #Update Logic------------------------------

    comp=Computer.objects.get(computer_name=computer)
    l=Lab.objects.get(name=lab_name)
    l.complaints_made=l.complaints_made+1
    incharge=l.incharge
    assistant=l.assistant
    l.save()

    if type_of_complaint == "Software" or type_of_complaint== "Hardware":
        fatal=CommonComplaints.objects.get(complaint=selected)
        if 'Printer' in fatal.complaint:
            p=Printers.objects.get(computer=comp.id)
            p.complaints_made=p.complaints_made+1
            p.status='OFF'
            p.save()
        if 'Scanner' in fatal.complaint:
            s=Scanners.objects.get(computer=comp.id)
            s.complaints_made=s.complaints_made+1
            s.status='OFF'
            s.save()
        complaint_update=Complaint(lab=l,computer_name=comp,complaint=CommonComplaints.objects.get(complaint=selected),\
        date=time.strftime("%Y-%m-%d"),status='Pending')
        complaint_update.save()
        if fatal.critical == 1:
            comp.status='OFF'
    comp.complaints_made=comp.complaints_made+1
    comp.description=comp.description+':\nCompalint'+selected+'  '+description
    comp.save()




    mailContent= '\nlab:'+lab_name+ '\nComputer: ' + computer+'\nType:'+type_of_complaint+'\nComplaint:'+selected+ '\n'+ description +\
    '\nDeadStock No.:'+ str(construct_complaint[0])+'\nIP:'+ str(construct_complaint[1])+'\nMAC:'+ \
    str(construct_complaint[2]) + '\n' \
    + '\n\n\nThis is an auto-generated email from our website.'

    send_mail('Complaint from:' + u, mailContent, 'clrms.mitcoe@gmail.com',[incharge,assistant], fail_silently=False)

    return HttpResponseRedirect('http://kedark7893.pythonanywhere.com/Thank-You')

def thank_you(request):
    return HttpResponse("<h1>Thank You!<a href='/welcome' target='_top'>Back to Welcome Page!</a></h1>")

#-------------------UPDATE AFTER COMPLAINT IS RESOLVED-----------------------------

def update(request):
    code = read('/home/kedark7893/clrms/templates/update.html')
    t= Template(code)
    c = Context()
    conn = connect()
    cur = conn.cursor()
    cur.execute ("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint where status='pending'")
    complaints = []
    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        complaints.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))

    c = Context({'complaints':complaints})
    conn.close()
    return HttpResponse(t.render(c))


def update_comp(request):
    complaintId=request.GET['complaint_ID']
    c=Complaint.objects.get(id=complaintId)
    comp=Computer.objects.get(id=c.computer_name_id)
    c.status='Solved'
    fatal=CommonComplaints.objects.get(id=c.complaint_id)
    if fatal.critical==1:
        comp.status='ON'

    if 'Printer' in fatal.complaint:
        p=Printers.objects.get(computer=comp.id)
        p.complaints_resolved=p.complaints_resolved+1
        p.status='ON'
        p.save()
    if 'Scanner' in fatal.complaint:
        s=Scanners.objects.get(computer=comp.id)
        s.complaints_resolved=s.complaints_resolved+1
        s.status='ON'
        s.save()
    comp.complaints_resolved=comp.complaints_resolved+1
    comp.description=comp.description.split(":")[0]
    comp.save()
    c.save()
    l=Lab.objects.get(id=c.lab_id)
    l.complaints_resolved=l.complaints_resolved+1
    l.save()
    return HttpResponseRedirect('http://kedark7893.pythonanywhere.com/admin/update')


#----------------------------------------------------------------------------------------
#---------------------------Stats related views------------------------------------------
#----------------------------------------------------------------------------------------

def stats(request):

    code = read('/home/kedark7893/clrms/templates/stats.html')
    t= Template(code)
    conn = connect()
    cur = conn.cursor()
    cur.execute ("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint")
    complaints = []
    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        complaints.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))

    cur.execute ("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint where date=CURDATE()")
    daily = []
    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        daily.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))


    cur.execute ("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint")
    hardware = []
    software=[]
    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        if complaint.complaint_type_id==1:
            hardware.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))
        else:
            software.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))

    cur.execute ("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint where status='pending'")
    pending = []
    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        pending.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))

    cur.execute("select computer_name_id from account_complaint group by computer_name_id limit 1;")
    mfc=Computer.objects.get(id=row[2])
    cur.execute("select complaint_id from account_complaint group by complaint_id order by count(*) desc limit 1;")
    mfctype=cur.fetchone()[0]
    mfctype=CommonComplaints.objects.get(id=mfctype)
    c = Context({'complaints':complaints,'daily':daily,'hardware':hardware,'software':software,'pending':pending,\
    'mfc':mfc.computer_name,'mfctype':mfctype,'range':ranges})

    conn.close()


    return HttpResponse(t.render(c))


#-----Range Query for Complaints Table----------------------

def range(request):
    del ranges[:]
    conn=connect()
    cur=conn.cursor()
    start_date=request.POST['d1']
    end_date=request.POST['d2']
    cur.execute("select id,lab_id,computer_name_id,date,status,complaint_id from account_complaint where date between '" + start_date +"' and '"+end_date+"'")

    for row in cur.fetchall ():
        l=Lab.objects.get(id=row[1])
        c=Computer.objects.get(id=row[2])
        complaint=CommonComplaints.objects.get(id=row[5])
        ranges.append (ComplaintList (row[0],l.name,c.computer_name,row[3],row[4],complaint.complaint))

    #return HttpResponse("Start date:--- " + start_date +" End Date:--- "+ end_date)
    return HttpResponseRedirect("/stats")