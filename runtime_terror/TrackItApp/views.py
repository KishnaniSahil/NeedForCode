from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db import connection
# from pymysql import *
# from pymysql import cursors

# Create your views here.
def show(request):
    cursor=connection.cursor()
    cursor.execute('select * from student where softdelete=0')
    columns=[col[0] for col in cursor.description]
    info=[
        dict(zip(row,columns))
        for row in cursor.fetchall()
    ]
    print(info)
    context={
        'keyinfo':info
    }
    # return HttpResponse('hello world')
    return render(request,'TrackItApp/login.html',context)

# def second(request):
#     return render(request,'TrackItApp/second.html')
def fetch(request):
    username=request.POST['username']
    password=request.POST['password']
    print(username,password)
    cursor=connection.cursor()
    cursor.execute('select * from faculty where fname=%s and f_pwd=%s',(username,password))
    result=cursor.fetchone()
    print(result)
    if result is None:
        return HttpResponse('invalid user')
    else:
        return render(request,'TrackItApp/second.html')

def back(request):
    # return redirect('report')
    return render(request,'TrackItApp/login.html')
    # return HttpResponse('hellooooooo')

def keep(request):
    grade=request.POST.get('standard')
    sname=request.POST.get('sname')
    roll_no=request.POST.get('roll_no')
    print(grade,sname,roll_no)
    cursor=connection.cursor()
    # cursor.execute('select * from student where grade=%s and roll_no=%d',(grade,roll_no))
    cursor.execute('select * from student where grade=%s and roll_no=%s',(grade,roll_no))
    details=cursor.fetchone()
    print(details)

    # (1, 'Aaditya', 'aadityakhetwani@gmail.com', '123', 1, b'\x00', 'D12C', None)

    cursor.execute('select * from activities where roll_no=%s',(roll_no))
    columns=[col[0] for col in cursor.description]
    res=[
        dict(zip(columns,row))
        for row in cursor.fetchall()
    ]
    # [{'act_id': 1, 'roll_no': 1, 'marks': 45, 'attendance': '40', 'extra_curricular': '1,2,6,7'}]
    feedback=''
    if(res[0]['extra_curricular'] is None):
        if (res[0]['marks']>80 and res[0]['marks']<=100):
            if res[0]['attendance']>90:
                feedback='Good excel in studies,need to focus on extra-curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                feedback='Good excel in studies,an average attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                feedback='Good excel in studies,not very regular.Need to focus on extra-curricular activities'
            else:
                feedback='Good excel in studies,poor attendance.Need to focus on extra-curricular activities'

        elif (res[0]['marks']>60 and res[0]['marks']<=80):
            if res[0]['attendance']>90:
                feedback='mediocre marks and quite a regular student.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                feedback='mediocre marks and attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                feedback='mediocre marks,not very regular.Need to focus on extra-curricular activities'
            else:
                feedback='mediocre marks,poor attendance.Need to focus on extra-curricular activities'

        elif (res[0]['marks']>50 and res[0]['marks']<=60):
            if res[0]['attendance']>90:
                feedback='Good marks and attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                feedback='Good marks,average attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                feedback='Good marks and not very regular.Need to focus on extra-curricular activities'
            else:
                feedback='Good marks,poor attendance.Need to focus on extra-curricular activities' 
        elif (res[0]['marks']>35 and res[0]['marks']<=50):
            if res[0]['attendance']>90:
                feedback='Below average,good attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                feedback='Below average marks,average attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                feedback='Below average marks and not very regular.Need to focus on extra-curricular activities'
            else:
                feedback='Below average marks,poor attendance.Need to focus on extra-curricular activities' 
        
        else:
            if res[0]['attendance']>90:
                feedback='Poor academics,good attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                feedback='Poor academics,average attendance.Need to focus on extra-curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                feedback='Poor academics,not very regular.Need to focus on extra-curricular activities'
            else:
                feedback='poor academics and attendance.Need to focus on extra-curricular activities' 
    else:
        skills_known=len(res[0]['extra_curricular'].split(','))
        cursor.execute('select count(*) from extra_curricular')
        count=cursor.fetchone()[0]
        ratio=skills_known/count
        if (res[0]['marks']>80 and res[0]['marks']<=100):
            if res[0]['attendance']>90:
                if ratio>=0.9:
                    feedback='excellent student'  
                elif ratio>=0.7:
                    feedback='Excellent in academics,good attendance and extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Excellent in academics,good attendance little extra_curricular activities'
                else:
                    feedback='Excellent in academics,good attendance,very less extra_curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                if ratio>=0.9:
                    feedback='Excellent in academics,mediocre attendance and extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Excellent in academics,mediocre attendance and extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Excellent in academics,mediocre attendance,little extra_curricular activities'
                else:
                    feedback='Excellent in academics,mediocare attendance,very less extra_curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                if ratio>=0.9:
                    feedback='Excellent in academics,very less attendance and good extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Excellent in academics,very less attendance and extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Excellent in academics,very less attendance,little extra_curricular activities'
                else:
                    feedback='Excellent in academics,very less attendance and extra_curricular activities'
            else:
                if ratio>=0.9:
                    feedback='Excellent in academics,poor attendance and good extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Excellent in academics,poor attendance and extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Excellent in academics,poor attendance,little extra_curricular activities'
                else:
                    feedback='Excellent in academics,poor attendance and extra_curricular activities'
        elif (res[0]['marks']>60 and res[0]['marks']<=80):
            if res[0]['attendance']>90:
                if ratio>=0.9:
                    feedback='mediocre marks,excellent attendance and extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Mediocre marks,excellent attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='mediocre marks,excellent attendance,little extra_curricular activities'
                else:
                    feedback='mediocre marks,excellent attendance,very less extra_curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                if ratio>=0.9:
                    feedback='Mediocre marks and attendance.Excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Mediocre marks, attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Mediocre marks and attendance,little extra_curricular activities'
                else:
                    feedback='Mediocre marks and attendance,very less extra_curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                if ratio>=0.9:
                    feedback='Mediocre marks,very less attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='mediocre marks,very less attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='mediocre marks,very less attendance,little extra_curricular activities'
                else:
                    feedback='mediocre marks,very less attendance and extra_curricular activities'
            else:
                if ratio>=0.9:
                    feedback='mediocre marks,poor attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='mediocre marks,poor attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='mediocre marks,poor attendance,little extra_curricular activities'
                else:
                    feedback='mediocre marks,poor attendance and extra_curricular activities'
        elif (res[0]['marks']>50 and res[0]['marks']<=60):

            if res[0]['attendance']>90:
                if ratio>=0.9:
                    feedback='Good marks,excellent attendance and extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Good marks,excellent attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Good marks,excellent attendance,little extra_curricular activities'
                else:
                    feedback='Good marks,excellent attendance,very less extra_curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                if ratio>=0.9:
                    feedback='Good marks and attendance.Excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Good marks, attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Good marks and attendance,little extra_curricular activities'
                else:
                    feedback='Good marks and attendance,very less extra_curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                if ratio>=0.9:
                    feedback='Good marks,very less attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Good marks,very less attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Good marks,very less attendance,little extra_curricular activities'
                else:
                    feedback='Good marks,very less attendance and extra_curricular activities'
            else:
                if ratio>=0.9:
                    feedback='Good marks,poor attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Good marks,poor attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Good marks,poor attendance,little extra_curricular activities'
                else:
                    feedback='Good marks,poor attendance and extra_curricular activities'
        elif (res[0]['marks']>35 and res[0]['marks']<=50):
            if res[0]['attendance']>90:
                if ratio>=0.9:
                    feedback='Below average marks,excellent attendance and extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Below average mark,excellent attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Below average mark,excellent attendance,little extra_curricular activities'
                else:
                    feedback='Below average mark,excellent attendance,very less extra_curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                if ratio>=0.9:
                    feedback='Below average mark and attendance.Excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Below average mark,mediocre attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Below average mark and attendance,little extra_curricular activities'
                else:
                    feedback='Below average mark and attendance,very less extra_curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                if ratio>=0.9:
                    feedback='Below average mark,very less attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Below average mark,very less attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Below average marks,very less attendance,little extra_curricular activities'
                else:
                    feedback='Below average mark,very less attendance and extra_curricular activities'
            else:
                if ratio>=0.9:
                    feedback='Below average mark,poor attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='Below average mark,poor attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='Below average mark,poor attendance,little extra_curricular activities'
                else:
                    feedback='Below average mark,poor attendance and extra_curricular activities'
        else:
            if res[0]['attendance']>90:
                if ratio>=0.9:
                    feedback='Poor marks,excellent attendance and extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='poor marks,excellent attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='poor mark,excellent attendance,little extra_curricular activities'
                else:
                    feedback='poor mark,excellent attendance,very less extra_curricular activities'
            elif res[0]['attendance']>70 and res[0]['attendance']<=90:
                if ratio>=0.9:
                    feedback='poor mark and attendance.Excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='poor mark,mediocre attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='poor mark and attendance,little extra_curricular activities'
                else:
                    feedback='poor mark and attendance,very less extra_curricular activities'
            elif res[0]['attendance']>50 and res[0]['attendance']<=70:
                if ratio>=0.9:
                    feedback='poor mark,very less attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='poor mark,very less attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='poor marks,very less attendance,little extra_curricular activities'
                else:
                    feedback='poor mark,very less attendance and extra_curricular activities'
            else:
                if ratio>=0.9:
                    feedback='poor mark,poor attendance and excellent extra_curricular activities'  
                elif ratio>=0.7:
                    feedback='poor mark,poor attendance and good extra_curricular activities'
                elif ratio<=0.5:
                    feedback='poor mark,poor attendance,little extra_curricular activities'
                else:
                    feedback='poor mark,poor attendance and extra_curricular activities'
 
    attendance=res[0]['attendance']
    marks=res[0]['marks']
    print(feedback)
    # return HttpResponse('hello world')
    context={
        'keyfeedback':feedback,
        'keydetails':details,
        'keyres':res,
        'keyattendance':attendance,
        'keymarks':marks,
        'keyratio':ratio*100,
        'keyname':details[1],
    }
    return render(request,'TrackItApp/third.html',context)

    
