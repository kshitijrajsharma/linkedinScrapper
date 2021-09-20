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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import *
from django.shortcuts import redirect

@login_required(login_url="/login/")
def index(request):
    userid=request.user.id
    userprofile = Profile.objects.get_or_create(user=int(userid))

    context = {'segment': 'index','profile':userprofile}
    

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dashboard(request):
    userid=request.user.id
    userins=User.objects.get(id=userid)
    userprofile = Profile.objects.get_or_create(user=userins)
    usernewprofile=Profile.objects.get(user=userid)
    

    context = {'profile':usernewprofile,'taskform':scrapperprofileForm,'profilecount':scrapperprofile.objects.all().count()}
    

    html_template = loader.get_template('dashboard.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def databasetable(request):
    
    userid=request.user.id
    profiledata=scrapperprofile.objects.all()
    usernewprofile=Profile.objects.filter(user=userid)
    context = {'profile': usernewprofile,'profiledata': profiledata,'taskform':scrapperprofileForm}
    html_template = loader.get_template('databasetable.html')
    return HttpResponse(html_template.render(context, request))
    # except template.TemplateDoesNotExist:

    #     html_template = loader.get_template('page-404.html')
    #     return HttpResponse(html_template.render(context, request))

    # except:
    #     html_template = loader.get_template('page-500.html')
    #     return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def pages(request):
    userid=request.user.id
    usernewprofile=Profile.objects.filter(user=userid)

    context = {'profile': usernewprofile}

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

@login_required(login_url="/login/")
def tableview(request):
    userid=request.user.id
    usernewprofile=Profile.objects.filter(user=userid)

    tabledata = scrapperprofile.objects.all()
    context = {'userdata': tabledata,'profile': usernewprofile}

    html_template = loader.get_template('tables-bootstrap-tables.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def scrapperpost(request):
    if request.method == 'POST':
        postForm = scrapperprofileForm(request.POST, request.FILES)
        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            user = User.objects.get(pk=request.user.id)
            post_form.added_by = user
            mtest = post_form.save()
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors)
@login_required(login_url="/login/")
def delete(request,id):
    instance=scrapperprofile.objects.get(id=id)
    instance.delete()
    
    userid=request.user.id
    profiledata=scrapperprofile.objects.all()
    usernewprofile=Profile.objects.filter(user=userid)
    context = {'profile': usernewprofile,'profiledata': profiledata,'taskform':scrapperprofileForm}
    html_template = loader.get_template('databasetable.html')
    return HttpResponse(html_template.render(context, request))
        



# @login_required(login_url="/login/")
# def PersonUpdateView(request):
#     userid=request.user.id
#     userprofile = Profile.objects.get(user=int(userid))
#     form = PersonForm(instance=userprofile)

#     #tabledata = scrapperprofile.objects.all()
#     context = {'form': form}

#     html_template = loader.get_template('settings.html')
#     return HttpResponse(html_template.render(context, request))

class PersonUpdateView(UpdateView):
    model = Profile
    form_class = PersonForm
    template_name = 'settings.html'
    success_url= '/' 
    # def form_valid(self,request, form):
    #     userid=request.user.id
    #     candidate = form.save(commit=False)
    #     candidate.user = int(userid)  # use your own profile here
    #     candidate.save()
    #     return HttpResponseRedirect(self.get_success_url())



@login_required(login_url="/login/")
def scrapperapi(request,id):
    print(id)
    scrapper = scrapperprofile.objects.get(id=id)
    url=scrapper.profilelink
    if scrapper.scrapped_status != True:

        print(request.user.id)
        userid=request.user.id
        requestuser= Profile.objects.get(user=int(userid))
        email=requestuser.Linkedin_Email
        password= requestuser.password
        if email == None:
            return redirect('home')
        browser  = webdriver.Chrome()
        browser.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

        #Enter login info:
        elementID = browser.find_element_by_id('username')
        elementID.send_keys(email)

        elementID = browser.find_element_by_id('password')
        elementID.send_keys(password)
        #Note: replace the keys "username" and "password" with your LinkedIn login info
        elementID.submit()

        # Main scrapping 
        
        urltoscrap="https://www.linkedin.com/in/"+url
        #This is for contact
        contact=urltoscrap
        print(contact)
        
        browser.get(urltoscrap)

        time.sleep(5)#sleep_between_interactions
        
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)#sleep_between_interactions
    
        browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(5)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            browser.find_element_by_class_name("pv-skills-section__additional-skills").click()
        except:
            pass
        src = browser.page_source
        soup = BeautifulSoup(src, 'html.parser')
        education = soup.find_all(id='education-section')

        
        profile = soup.find_all(class_ ="pv-text-details__left-panel mr5")
        currentpost = soup.find_all(class_ ="text-body-medium break-words")
    
        profilepost=""
        for x in currentpost:
            profilepost=x.text
        profilepost=profilepost.strip()
        newlist=profilepost.split()
        profilepost=" ".join(newlist)
    
        print(profilepost)
        
        Experience_post=""
        location=""
        
        for x in profile:
            for y in x.findAll('h1'):
                name=y.text
            
            count=0
            for y in x.findAll('span'):
        
                if(count==3):
                    location=y.text
                count=count+1
            
        print(name)
        name=name.strip()
        location=location.strip()
        newlist=location.split()
        location=" ".join(newlist)
        print(location)
        

        Education_text=""
    #     print(education)
        for x in education:
            for y in x.findAll('h3'):
                #print (y.text)
                Education_text=Education_text+y.text+","
            count=0
            for y in x.findAll('p'):
                if (count==0):
                    #print (y.text)
                    Education_text=Education_text+y.text+","
        Education_text=Education_text.strip()
        newlist=Education_text.split()
        Education_text=" ".join(newlist)
        print(Education_text)
        
        
        skills = soup.find_all(class_ ="pv-skill-category-entity__name-text t-16 t-black t-bold")
        count=0
        skillstext=""
    # print(skills)
        for x in skills:
            count=count+1
            x.text.strip()
            skillstext=skillstext+x.text+","
                
        skillstext=skillstext.strip()
        newlist=skillstext.split()
        skillstext=" ".join(newlist)
        print(skillstext)
        
        interests = soup.find_all(class_ ="pv-entity__summary-title-text")
        intereststext=""
        for x in interests:
            intereststext=intereststext+x.text+","
        intereststext=intereststext.strip()
        newlist=intereststext.split()
        intereststext=" ".join(newlist)
        print(intereststext)
        data = [contact, name, location, profilepost,Education_text,skillstext,intereststext]
        print(data)
        scrapper.Contact=contact
        scrapper.name=name
        scrapper.location=location
        scrapper.Education=Education_text
        scrapper.Skills=skillstext
        scrapper.Interest=intereststext
        scrapper.Description=profilepost
        scrapper.scrapped_status=True

        scrapper.save()

    tabledata = scrapperprofile.objects.all()
    context = {'userdata': tabledata}

    html_template = loader.get_template('tables-bootstrap-tables.html')
    return HttpResponse(html_template.render(context, request))

    

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