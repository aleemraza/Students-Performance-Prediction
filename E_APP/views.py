import pickle
import sklearn
import pandas as pd 
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.http import HttpResponseBadRequest
from .models import StudentResults
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from . labelEncoder import encode
from . prediction import predict

# Create your views here.


@login_required(login_url='login')
def deshboard(request):
    user = request.user
    total_entries = StudentResults.objects.filter(user=user).count()
    students = StudentResults.objects.filter(user=user)
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    return render(request, 'dashboard.html' , {"total_entries":total_entries,"students":students,"user_image":user_image, 'usernames':usernames, 
                                               'useremail':useremail})
def testdata (request):
    user = request.user
    total_entries = StudentResults.objects.filter(user=user).count()
    students = StudentResults.objects.filter(user=user)
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    return render(request , 'testdata.html' , {"total_entries":total_entries,"students":students,"user_image":user_image, 'usernames':usernames, 
                                               'useremail':useremail})
def delete_user(request,pk):
    user = StudentResults.objects.filter(pk=pk)
    user.delete()
    return redirect('dashboard')


def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        image=request.FILES.get('image')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:
            user=User.objects.create_user(uname,email,pass1)
            user.save()
            profile = UserProfile.objects.create(user=user, image=image)
            profile.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None and user.is_active:
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")
    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

student_information = [
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "num_of_prev_attempts",
    "is_banked",
    "code_module_x",
    "code_presentation_x",
    "code_module_y",
    "code_presentation_y"]
student_information_decoded = [
    "gender",
    "region",
    "highest_education",
    "imd_band",
    "age_band",
    "num_of_prev_attempts",
    "is_banked",
    "code_module_x",
    "code_presentation_x",
    "code_module_y",
    "code_presentation_y"]
def home (request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    error = None
    gender = ['Select Gender',
              'Female',
              'Male']

    region = ['Select Region',
              'East Anglian Region',
              'East Midlands Region',
              'London Region',
              'North Region',
              'North Western Region',
              'Scotland',
              'South Region',
              'South East Region',
              'West Midlands Region',
              'Wales',
              'Yorkshire Region']

    highest_education = ['Select Highest Education',
                         'No Formal Qualification',
                         'Lower Than A Level',
                         'A Level or Equivalent',
                         'Higher Education Qualification',
                         'Post Graduation Qualification']

    imd_band = ['Select IMD Band',
                '0-10%',
                '10-20%',
                '20-30%',
                '30-40%',
                '40-50%',
                '50-60%',
                '60-70%',
                '70-80%',
                '80-90%',
                '90-100%'
                ]

    age_band = ['Select Age Group',
                '0-35',
                '35-55',
                '55>=']

    num_of_prev_attempts = ['Select Number Of Previous Attempts',
                            0,
                            1,
                            2,
                            3,
                            4,
                            5,
                            6]

    is_banked = ['Select Semester',
                 0,
                 1]

    code_module_x = ['Select First Module',
                     'AAA',
                     'BBB',
                     'CCC',
                     'DDD',
                     'EEE',
                     'FFF',
                     'GGG']

    code_presentation_x = ['Select Semester (First Module)',
                           '2013B',
                           '2013J',
                           '2014B',
                           '2014J']

    code_module_y = ['Select Second Module',
                     'AAA',
                     'BBB',
                     'CCC',
                     'DDD',
                     'EEE',
                     'FFF',
                     'GGG']

    code_presentation_y = ['Select Semester (Module Second)',
                           '2013B',
                           '2013J',
                           '2014B',
                           '2014J']
    
    if request.method == 'POST':
      student_information_decoded[0] = request.POST.get('gender')

      Gender =  student_information[0] = encode(request.POST.get('gender'))
      
      student_information_decoded[1] = request.POST.get('region')
      
      Region =  student_information[1] = encode(request.POST.get('region'))
      
      student_information_decoded[2] = request.POST.get('highest_education')
      
      HighestEducation =  student_information[2] = encode(request.POST.get('highest_education'))
      
      student_information_decoded[3] = request.POST.get('imd_band')
      
      IMDBand =  student_information[3] = encode(request.POST.get('imd_band'))
      
      student_information_decoded[4] = request.POST.get('age_band')
      
      AgeGroup =  student_information[4] = encode(request.POST.get('age_band'))
      
      student_information_decoded[5] = request.POST.get('num_of_prev_attempts')
      
      NumberOfPreviousAttempts =   student_information[5] = encode(request.POST.get('num_of_prev_attempts'))
      
      student_information_decoded[6] = request.POST.get('is_banked')
      
      Semester =  student_information[6] = encode(request.POST.get('is_banked'))
      
      student_information_decoded[7] = request.POST.get('code_module_x')
      
      FirstModule = student_information[7] = encode(request.POST.get('code_module_x'))
      
      student_information_decoded[8] = request.POST.get('code_presentation_x')
      
      SemesterFirstModule =   student_information[8] = encode(request.POST.get('code_presentation_x'))
      
      student_information_decoded[9] = request.POST.get('code_module_y')
      
      SecondModule =   student_information[9]= encode(request.POST.get('code_module_y'))
      
      student_information_decoded[10] = request.POST.get('code_presentation_y')
      
      SemesterSecondModule =   student_information[10] = encode(request.POST.get('code_presentation_y'))   
      print(student_information)
      print("Student details: {}".format(student_information))
      return redirect('results')  
    return render(request, 'home.html',{"user_image": user_image , 'usernames':usernames, 
                                               'useremail':useremail ,'error': error, 'gender': gender, 'region': region,
                                                   'highest_education': highest_education, 'imd_band': imd_band,
                                                   'age_band': age_band, 'num_of_prev_attempts': num_of_prev_attempts,
                                                   'is_banked': is_banked, 'code_module_x': code_module_x,
                                                   'code_presentation_x': code_presentation_x, 'code_module_y': code_module_y,
                                                   'code_presentation_y': code_presentation_y, 'title': 'Questionnaire'})
def results(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    #print("Student details: {}".format(student_information))
    # student = np.array(student_information)
    # pred_result = predict('decision-tree', student_information)
    pred_result, accuracy = predict(student_information)
    #print("Prediction: {}".format(pred_result))

    if pred_result == 'Fail' or pred_result == 'Withdrawn':
        pred_result = 'Pass'
        message = 'Great! You can still work hard and get Distinction!'
    elif pred_result == 'Fail':
        message = 'Don\'t be demotivated. You can change the prediction if you start working hard from now!'
    elif pred_result == 'Distinction':
        message = 'Well Done!'

    #print("Message: {}".format(message))
    accuracy = round(accuracy * 100, 2)
    print("Accuracy: {}".format(accuracy))
    try:
        save = StudentResults.objects.create(user=user, results=pred_result , gender = student_information_decoded[0], region=student_information_decoded[1], 
                                          highest_education = student_information_decoded[2],imd_band = student_information_decoded[3],
                         age_band = student_information_decoded[4],  num_of_prev_attempts = student_information_decoded[5], is_banked =student_information_decoded[6], 
                         code_module_x = student_information_decoded[7],code_presentation_x = student_information_decoded[8], code_module_y = student_information_decoded[9], 
                         code_presentation_y = student_information_decoded[10])
    except Exception as e:
        print("Failed to save the student data to DB:", str(e))
    save = None  # Set save to None if an exception occurs  

    return render(request ,'results.html', {'results': results, 'student':accuracy, 'pred_result':pred_result, 'save':save ,  'message':message , "user_image": user_image , 'usernames':usernames, 
                                               'useremail':useremail})
def about(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    return render(request , 'about.html',{"user_image": user_image , 'usernames':usernames, 
                                               'useremail':useremail})
def contact(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user) if hasattr(user, 'userprofile') else None
    user_image = user_profile.image if user_profile else None
    user_data = User.objects.get(username=user.username, is_superuser=False)  # Assuming username is unique
    usernames = user_data.username
    useremail = user_data.email
    return render(request , 'contact.html',{"user_image": user_image , 'usernames':usernames, 
                                               'useremail':useremail})
