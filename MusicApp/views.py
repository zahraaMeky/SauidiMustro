import threading
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as logoutUser
from django.contrib.auth.decorators import login_required
from zoomus import ZoomClient
import schedule
import time
import webbrowser
# Create your views here.
def Home(request):
    testimonialsList=[]
    teachers=teacher.objects.all()
    testimonials=Testimonial.objects.all()
    blogs = Blog.objects.all()
    for testimonial in testimonials:
        user=  testimonial.user
        print("testimonial user",user,testimonial.message)
        fetchUser =CustomUser.objects.filter(username=user)
        for fuser in fetchUser:
            testimonialsList.append({"name":fuser.Full_name,"img":fuser.Photo,"message":testimonial.message})
    first_item_list = [testimonialsList[0]]
    testimonialsList.pop(0)
    context={"teachers":teachers,'testimonials':testimonialsList,"first_item_list":first_item_list,"blogs":blogs}
    return render(request,"pages/index.html",context)

def signUp_User(request):
    usertype = ""
    Pfile_url =""
    if request.method == "POST":
        print('request.method',request.POST.get("username"))
        username = request.POST.get("username")
        name = request.POST.get("name")
        print('username,type',username)
        phone =request.POST.get('phone')
        if 'pimg' in  request.FILES:
            photo =request.FILES['pimg']
            pfss = FileSystemStorage()
            pfile = pfss.save(photo.name,photo)
            Pfile_url = pfss.url(pfile)
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        checkuser=CustomUser.objects.filter(username=username).exists()
        if(checkuser == False):
         if password1 == password2:
                try:
                    user = CustomUser.objects.create_user(Full_name=name,phone_no=phone,username=username,password=password1,Photo=Pfile_url)
                    user.save()
                    print("user")
                    messages.success(request, 'تم التسجيل بنجاح.')
                    return redirect('login')
                except Exception as e:
                    print(f"Save failed: {e}")
         else:messages.error(request, 'كلمة المرور متطابقة')
        else:
              messages.error(request, 'المستخدم موجود')
    return render (request,'user/signupuser.html')

def Login(request):
    if request.method == "POST":
        userN = request.POST.get("username")
        password=request.POST.get('password')
        print('login userN',userN,password)
        user = authenticate(username=userN,password=password)
        print('login user',user)
        if user:
            userID = user.id
            auth_login(request,user)
            return redirect('/user/')
         
        else:
          messages.error(request,'المستخدم غير موجود')
    return render (request, 'user/login.html')

@login_required(login_url='/login/') 
def Logout (request):
    logoutUser(request)
    return redirect('/login/')

@login_required(login_url='/login/') 
def UserPage(request):
    courses = []
    courseType=""
    current_user = request.user
    if current_user is not None:
        current_userId = current_user.id
        photo =current_user.Photo
        username=current_user.username
        phone_no=current_user.phone_no
        Full_name = current_user.Full_name   
        reservedCourses = Booking.objects.filter(user=current_user)
        for c in reservedCourses:
           course_id = c.course
           fetchCourses = Course.objects.filter(name=course_id)
           print("fetchCourses",course_id)
           for course in fetchCourses:
                ctype =course.type
                if ctype == "arabic":courseType="مــوسيقي عربيــة"
                if ctype == "forign":courseType="مــوسيقي غربيــة"
                teacher= course.teacher
                print("teacher",teacher)
                courses.append({"name":course.name,"description":course.description,"img":course.img,
                                "price":course.price,"type":courseType,"teacher":teacher})
        print("courses",courses)
        context={
        "userphoto":photo,
        "userusername":username,
        "userfullName":Full_name,
        "userphone_no":phone_no,
        "courses":courses
    }
    return render (request, 'user/UserPage.html',context)

def CoursesPage(request,type):
    fetch_Courses=Course.objects.filter(type=type)
    return render (request, 'pages/courses.html',context={"courses":fetch_Courses})

@login_required(login_url='/login/') 
def BookingCorses(request,id):
    current_user = request.user
    if current_user is not None:
        fetchCouse = Course.objects.get(id=id)
        bookedCoursers = Booking.objects.filter(user=current_user,course=fetchCouse).exists()
        if bookedCoursers == False:
                    book = Booking(user=current_user,course=fetchCouse)
                    book.save()
        else:messages.error(request, 'تم شراء الدورة من قبل')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/login/') 
def addTestimonial(request):
    current_user = request.user
    if current_user is not None:
        if request.method == "POST":
            message = request.POST.get("message")
            fetchTestimonial = Testimonial.objects.filter(user=current_user).exists()
            if fetchTestimonial == False:
                    saveTestimonial = Testimonial(user=current_user,message=message)
                    saveTestimonial.save()
        else:messages.error(request, 'تم التقييم من قبل')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


def ContactPage(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        type = request.POST.get("type")
        user_message = request.POST.get("message")  # Renamed the variable to 'user_message'
        phone = request.POST.get("phone")
        try:
            saveContact = contact(name=name, email=email, subject=subject, type=type, messages=user_message, phone_no=phone)
            saveContact.save()
            messages.success(request, 'تم إستقبــال طلبـك.')
        except Exception as e:
            print(f"Save failed: {e}")
            messages.error(request, 'حدث خطأ')

    return render(request, 'pages/contact.html')




def TeacherPage(request,id):
    teacher_instance = get_object_or_404(teacher,id=id)
    courses = Course.objects.filter(teacher=teacher_instance)
    return render (request, 'pages/teacher.html',context={"teacher":teacher_instance,"Courses":courses})

def blogPage(request,id):
    blog_instance = get_object_or_404(Blog,id=id)
    return render (request, 'pages/blog.html',context={"blog":blog_instance})

# def open_link(link):
#     webbrowser.open(link)

# def open_zoom_meeting(request):
#     open_link('https://us05web.zoom.us/j/81547377094?pwd=UQcLMcKvjEMQcdhAL2lVjZpRAoqoBX.1')
#     return HttpResponse("open zoom")


# schedule.every().wednesday.at("04:35").do(open_zoom_meeting)

# def check_internet_loop():
#     while 1:
#         schedule.run_pending()
#         time.sleep(1)


# threading.Thread(target=check_internet_loop, daemon=True).start()

