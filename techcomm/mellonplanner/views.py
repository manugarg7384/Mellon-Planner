from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from mellonplanner.models import *
from mellonplanner.backend.sched import getAllSchedules

from django.core.context_processors import csrf

def getschedule(request, index):
    index = int(index)
    context = {}
    if 'schedules' not in request.session:
        context['errors'] = ["Reinput classes or check cookies"]
        return render(request, 'index.html', context)
    if index > len(request.session['schedules']):
        context['errors'] = ['Incorrect page number']
        return render(request, 'index.html', context)
    allListFormatted,unitsList = request.session['schedules'],request.session['units']
    context['schedule'] = allListFormatted[index]

    #context['scheduleCount'] = len(allListFormatted)
    
    context['unitsList'] = enumerate(unitsList)
    context['currentIndex'] = index
    # and finally put pictures in the context dictionary
    return render(request, 'index.html', context)


def getschedules(request):
    

    context = {}
    context.update(csrf(request))
    errors = []
    context['errors'] = errors
    if not 'loc' in request.POST or not request.POST['loc']:
        errors.append('List of classes is required')
    if not 'minunits' in request.POST or not request.POST['minunits']:
        errors.append('Minimum units is required')
    if not 'maxunits' in request.POST or not request.POST['maxunits']:
        errors.append('Maximum units is required')
    semester = request.POST['semester']
    pref = request.POST['preference']
    if(int(semester) == 0):
        context['semester'] = 'Fall'
    elif(int(semester) == 1):
        context['semester'] = 'Spring'
    elif(int(semester) == 2):
        context['semester'] = 'Summer 1/ALL'
    elif(int(semester) == 3):
        context['semester'] = 'Summer 2'       
    if errors:
        return render(request, 'index.html', context)
    if(int(request.POST['minunits']) < 0 or
       (int(request.POST['maxunits']) < int(request.POST['minunits']))):
        errors.append('Invalid units')
    list_of_classes = request.POST['loc'].replace(' ', '').split(",")
    # Should check for validity of classes here, and add errors if any
    # Then call the backend functions
    try:
        print(semester)
        schedules = getAllSchedules(list_of_classes, int(semester),
                                    request.POST['minunits'],
                                    request.POST['maxunits'],
                                    str(pref))

    except Exception:
        context['errors'] += "Something went wrong with course names. May not exist."
        return render(request, 'index.html', context)



    #print(schedules)
    #print(list_of_classes)
    allListFormatted = []
    unitsList = []
    for schedule in schedules:
        listFormatted = []

        schedule1 = schedule
        units = schedule1[0]
        
        classList = schedule1[1]

        for cls in classList:

            listFormatted.extend(convertTimeList(cls[0],cls[1]))
        allListFormatted += [listFormatted]
        unitsList += [units]

    if len(allListFormatted) != 0:
    #print listFormatted
    #('15122 Lec 2 N', 20, [(0, 12.5, 13.5), (1, 10.5, 12.0), (3, 10.5, 12.0)]), ('21127 Lec 2 H', 20, [(0, 14.5, 15.5), (1, 13.5, 14.5), (2, 14.5, 15.5), (3, 13.5, 14.5), (4, 14.5, 15.5)])
        context['schedule'] = allListFormatted[0]

    #context['scheduleCount'] = len(allListFormatted)
    request.session['schedules'],request.session['units'] = allListFormatted,unitsList
    context['unitsList'] = enumerate(unitsList)
    context['currentIndex'] = 0
    # and finally put pictures in the context dictionary
    return render(request, 'index.html', context)

numberToDate = {-1: '2015-02-08T', 0: '2015-02-09T', 1: '2015-02-10T', 2: '2015-02-11T', 3:'2015-02-12T', 4:'2015-02-13T', 5:'2015-02-14T', 6:'2015-02-15T'}



def convertTimeList(klass, l):
    #Test cookie
    
    formattedL = []
    for day,start,end in l:
        #HH:MM:SS
        start = str(start).replace('.5', ':30:00')
        start = start.replace('.0', ':00:00')
        start = start.zfill(8)
        end = str(end).replace('.5', ':30:00')
        end = end.replace('.0', ':00:00')
        end = end.zfill(8)
        formattedL.append({'start':numberToDate[day]+ start , 'end':numberToDate[day]+end, 'title':klass})
    return formattedL



def home(request):
    
    request.session.set_test_cookie()
    # try:
    #     profile = Profile.objects.get(user=request.user)
    # except ObjectDoesNotExist:
    #     return render(request, 'Login_Page.html', {})
    context = {}
    # context.update(csrf(request))
    return render(request, 'index.html', context)
