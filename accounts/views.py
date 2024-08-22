from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse,StreamingHttpResponse,HttpResponseRedirect
import cv2
import numpy as np
from PIL import Image
import os,sys
import time
import datetime
from .models import *
from django.template import RequestContext
from django.utils.datastructures import MultiValueDictKeyError
# Create your views here.

User=get_user_model()

def register(request):
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if (not user_check(username)):
            if(password1==password2 ):
                user=User.objects.create_user(password=password1,username=username,first_name=first_name,last_name=last_name,email=email)
                user.save()
                print("user created")
            
            else:
                print("password is incorrect")
            return redirect('/')
        else:
            print("user is already taken")
            return redirect('register')
            

    else: 
        return render(request,'register.html',{'text':"Register Form"})
def user_check(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


from django.contrib.auth.forms import AuthenticationForm

def login(request):
    
    if request.method=='POST':
        
        form = AuthenticationForm(request,request.POST)
        
        if form.is_valid():
            
            username=request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
        
            if user:
                
                if user.is_student:
                    auth.login(request, user)
                    return redirect('student_dashboard')
                
                if user.is_teacher:
                    auth.login(request, user)
                    return redirect('teacher_dashboard')
    else:
        form = AuthenticationForm()
        return render(request, 'login-new.html',{'form':form,'text':"Login"})
    

student_login_required = user_passes_test(lambda user: user.is_student)

@student_login_required
def student_dashboard(request):
	
	return render(request, 'student/s_dash.html')
	
teacher_login_required = user_passes_test(lambda user: user.is_teacher)

@teacher_login_required
def teacher_dashboard(request):

	return render(request, 'teacher/teacher_dashboard.html')

def logout(request):
    auth.logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('/')

def student_register(request):
    return render(request, 'registration/register_stud.html')

def faceDetection(test_img):
    gray_img=cv2.cvtColor(test_img,cv2.COLOR_BGR2GRAY)#convert color image to grayscale
    face_haar_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')#Load haar classifier
    #faces=face_haar_cascade.detectMultiScale(gray_img,scaleFactor=1.32,minNeighbors=5)#detectMultiScale returns rectangles
    faces = face_haar_cascade.detectMultiScale(
        gray_img,     
        scaleFactor=1.25,
        minNeighbors=3,     
        minSize=(40,40)
        )
    return faces,gray_img
def stream(uid):
    #cap.open("https://192.168.43.1:8080/video")
    cap = cv2.VideoCapture(0)
    userid=uid
    count=0
    while True:
        
        ret,frame=cap.read()# captures frame and returns boolean value and captured image
        faces_detected,gray_img=faceDetection(frame)

        if not ret:
            print("Error: failed to capture image")
            break
        count+=1
        for (x,y,w,h) in faces_detected:
            
            cv2.imwrite('media/TrainingImages/User.'+str(userid)+"."+str(count)+".jpg",gray_img[y:y+h,x:x+h])

            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=2)

        cv2.imwrite('img_sample/stud_face.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('img_sample/stud_face.jpg', 'rb').read() + b'\r\n')
        if (count==50):
            
            break

@login_required
def video_feed(request):
    return StreamingHttpResponse(stream(request.user.id), content_type='multipart/x-mixed-replace; boundary=frame')
    
@login_required
def student_add(request):
	return render(request,'student/video_feed.html',{'message':"Face the Camera"})


recognizer = cv2.face.LBPHFaceRecognizer_create()
detector =cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")

# function to get the images and label data
def traindata(request):
    path='media/TrainingImages'
    def traind(path):

        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)

        return faceSamples,ids

    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    faces,ids =traind(path)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.save('ymlfile/Trainner.yml') # recognizer.save() worked on Mac, but not on Pi
    #recognizer.save(os.path.join(path, ))

    # Print the numer of faces trained and end program
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    return redirect('teacher_dashboard')

def recognition(*args):
    face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades +"haarcascade_frontalface_default.xml")
    recognizer =cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('ymlfile/Trainner.yml')
    cap = cv2.VideoCapture(0)
    id=0
    count=dict()
    present=dict()
    start=dict()
    name=""
    
    t0=time.time()+40
    while time.time()<t0:
        ret,frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
    # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.25,
            minNeighbors=5,
            minSize=(30,30)
        
        ) 
     
        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(225,0,0),2)
            id, conf = recognizer.predict(gray[y:y+h,x:x+w])
            pred=id
            
            if(conf<50):
                name=User.objects.get(pk=id).username
                pred=name
                
                count[pred]=count.get(pred,0)+1
                
                if count[pred]==1:
                    present[pred]=True
                    
                    print(pred,present[pred],count[pred])
                    count[pred]=0
                    cv2.putText(frame,str(name),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 4) 
            else:
                cv2.putText(frame,"Unknown",(x,y+h),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 4)
        cv2.imwrite('img_sample/face.jpg',frame)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + open('img_sample/face.jpg', 'rb').read() + b'\r\n')
    update_attendance(present,args[0],args[1])
    print(args[0],args[1])
    for presents in present:
        print (presents,present[presents])

def update_attendance(present,*args):
    today=datetime.date.today()
    time=datetime.datetime.now()
    periods=args[1]
    subject=args[0]
    for person in present:
        user=User.objects.get(username=person)
        try:
            qs=Attendance.objects.get(user=user,date=today)
        except:
            qs=None
        if qs is None:
            if present[person]==True:
                a=Attendance(date=today,time=time,periods=periods,subject=subject,present=True,attend=user)
                a.save()
            else:
                a=Attendance(date=today,time=time,present=False,attend=user)
                a.save()
        else:
            if(present[person]==True):
                qs.present=True
                qs.save(update_fields=['present'])
    
@login_required
def track(request):
    if request.POST:
        pk_subject=request.POST.getlist('subjects',None)
        period=request.POST.get('period')
        try:
            subject=Subject.objects.get(pk__in=pk_subject).sub_name
            
        except:
            subject=None
        print(subject,period)
    return StreamingHttpResponse(recognition(subject,period), content_type='multipart/x-mixed-replace; boundary=frame')
    
@login_required
def trackstudent(request):
    key=TeacherProfile.objects.get(t_id=(request.user.id))
    options=Subject.objects.filter(sub_id=key).all()
    return render(request,'teacher/track.html',{'options':options,'message':'Take Attendance Portal'})

@login_required
def view_attendance(request):
    try:
        attendance=Attendance.objects.filter(attend=(request.user.id)).all()
    except:
        attendance=None
    return render(request,'student/attendance.html',{'attendance':attendance,'message':"Your Attendance !"})

@login_required
def view_t_attendance(request):
    try:
        attendance=Attendance.objects.all()
    except:
        attendance=None
    return render(request,'teacher/attendance_show.html',{'attendance':attendance,'message':" Attendance Management"})

def edit_attendance(request,id):
    a_id=int(id)
    try:
        attendance=Attendance.objects.get(id=a_id)
    except:
        attendance=None
    if(request.GET.get('status')=='p'):
        attendance.present=True
        attendance.save() 
    else:
        attendance.present=False
        attendance.save()
    return redirect('view_attendance') 

def timetables(request):
    return render(request,'student/timetable.html',{'message':"College Time Table"})
def timetablet(request):
    return render(request,'teacher/timetable.html',{'message':"College Time Table"})

'''def detail(request):
    if request.POST:
        pk_subject=request.POST.getlist('subjects',None)
        period=request.POST.get('period')
        try:
            subject=Subject.objects.get(pk__in=pk_subject).sub_name
        except:
            subject=None
        print(subject,period)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))'''



import cv2
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def camera_feed(request):
    cap = cv2.VideoCapture(0)
    channel_layer = get_channel_layer()

    while True:
        ret, frame = cap.read()
        _, buffer = cv2.imencode('.jpg', frame)
        image_bytes = buffer.tobytes()

        async_to_sync(channel_layer.group_send)(
            'camera_feed_group',
            {
                'type': 'send_camera_feed',
                'image': image_bytes,
            }
        )

from .forms import AttendanceForm
from .models import Attendance
from django.http import JsonResponse
from django.template.loader import render_to_string

def get_edit_form(request,attend_id):

    form_class = AttendanceForm
    form_class.method = 'POST'
    form_class.action = request.path
    instance = Attendance.objects.get(pk=attend_id)

    if request.method == form_class.method:
        form = form_class(request.POST,instance=instance,prefix='form1')
        if form.is_valid():
            form.save()
            return JsonResponse({'message':'Blog Updated successfully..'})
    else:
        form     = form_class(instance=instance,prefix='form1')
        
        html_content = render_to_string('edit_form.html',{'form':form},request)
        return JsonResponse({'html_content': html_content})