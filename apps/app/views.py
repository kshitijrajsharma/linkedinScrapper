# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from selenium import webdriver
from .models import *
from rest_framework import viewsets
from .serializers import *
from rest_framework.views import APIView
import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.decorators import api_view


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
@api_view(['GET'])
def scrapperprofileview(request):
    queryset = scrapperprofile.objects.all()
    serializer=ScrapperprofileSerializer(queryset, context={"request": request}, many=True)
    return Response({"data":serializer.data})



def scrapperapi(request,id):
    print(id)
    scrapper = scrapperprofile.objects.get(id=id)
    url=scrapper.profilelink
    print(request.user.id)
    userid=request.user.id
    requestuser= Profile.objects.get(user=2)
    email=requestuser.Linkedin_Email
    password= requestuser.password
    browser  = webdriver.Chrome()
    browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    #Enter login info:
    elementID = browser.find_element_by_id('username')
    elementID.send_keys(email)

    elementID = browser.find_element_by_id('password')
    elementID.send_keys(password)
    #Note: replace the keys "username" and "password" with your LinkedIn login info
    elementID.submit()
    urltoscrap="https://www.linkedin.com/in/"+url
    print(urltoscrap)
    browser.get(urltoscrap)
    #Scroll to the end of the page
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)#sleep_between_interactions
    browser.find_element_by_class_name("pv-skills-section__additional-skills").click()

    src = browser.page_source
    soup = BeautifulSoup(src, 'html.parser')
    table = soup.find_all(id='experience-section')
    #experience=soup.find("div", {"id": "experience-section"})
    #print(find_all_id)
    print("*******Experiences **********")
    experiencetopush=""
    for x in table:
        for y in x.findAll('h3'):
            print (y.text)
            experiencetopush=experiencetopush+"\n"+y.text
        for y in x.findAll('span'):
            print (y.text)
            experiencetopush=experiencetopush+"\n"+y.text

    print("\n")
    scrapper.Experience=experiencetopush
    scrapper.save()


    print("*******Education **********")



    education = soup.find_all(id='education-section')
    educationtopush=""

    #experience=soup.find("div", {"id": "experience-section"})
    #print(find_all_id)

    for x in education:
        for y in x.findAll('h3'):
            print (y.text)
            educationtopush=educationtopush+"\n"+y.text
        for y in x.findAll('span'):
            print (y.text)
            educationtopush=educationtopush+"\n"+y.text

    scrapper.Education=educationtopush
    scrapper.save()



    print("*******Skills & endorsements **********")


    #Skills = soup.find_all("div", {"class": "pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view"})
    skills = soup.find_all(class_ ="pv-profile-section pv-skill-categories-section artdeco-card mt4 p5 ember-view")
    skillstring=""
    #experience=soup.find("div", {"id": "experience-section"})
    #print(skills)

    for x in skills:
    
        for y in x.findAll('span'):
            print (y.text)
            skillstring=skillstring+"\n"+y.text
    print("\n")
    scrapper.Skills=skillstring
    scrapper.save()

    print("*******Accomplishmets **********")

    accomplishmets = soup.find_all(class_ ="pv-profile-section pv-accomplishments-section artdeco-card mv4 ember-view")
    accomplishmetstopush=""
    #experience=soup.find("div", {"id": "experience-section"})
    #print(skills)

    for x in accomplishmets:
    
        for y in x.findAll('li'):
            print (y.text)
            accomplishmetstopush=accomplishmetstopush+"\n"+y.text
    print("\n")
    print("*******Interests **********")
    scrapper.Accomplishments=accomplishmetstopush
    scrapper.save()

    Interests = soup.find_all(class_ ="pv-profile-section pv-interests-section artdeco-card mt4 p5 ember-view")
    Intereststopush=""
    #experience=soup.find("div", {"id": "experience-section"})
    #print(skills)

    for x in Interests:
    
        for y in x.findAll('li'):
            print (y.text)
            Intereststopush=Intereststopush+"\n"+y.text
    
    scrapper.Interest=Intereststopush
    scrapper.save()
    return Response(ScrapperprofileSerializer(scrapperprofile.objects.filter(id=id), context={"request": request}, many=True).data)



    
    


@login_required

def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })