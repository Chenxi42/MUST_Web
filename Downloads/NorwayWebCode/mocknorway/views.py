from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.http import HttpResponseRedirect
from django.urls import reverse
# from datastream.forms import HistoricalForm
# from datastream.forms import TraveltimeForm
import datetime
from time import time, sleep
from django.contrib.auth.decorators import login_required
# import mysql.connector
# from mysql.connector import Error
import pandas as pd
import re


# Create your views here.

# Homepage. Simply creates static homepage according to template
def index(request):
    return render(request, 'index.html')
def contact(request):
    return render(request, 'contact.html')

#This displays real-time message data
@login_required
def message(request):
    # This code pulls real-time message data from the server
    # Establishing a connection to the database
    try:
        # connects to the mySQL database running loabally
        connection = mysql.connector.connect(host='localhost',
                                            database='sensors',
                                            user='root',
                                            password='Star*lab12345')
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    cursor = connection.cursor()

    # Grabs the most recent message row for message1
    sql_command = "SELECT * FROM message1 ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(sql_command)
    ans1 = cursor.fetchall()

    # grabs the most recent message row for message 2
    sql_command = "SELECT * FROM message2 ORDER BY timestamp DESC LIMIT 1"
    cursor.execute(sql_command)
    ans2 = cursor.fetchall()
    
    # used to filter out everything that's not a number or decimal point
    non_decimal = re.compile(r'[^\d.]+')

    # Iterates through the message1 data
    # produces list m1 with all numbers stored in indexes
    for i in ans1:
        m1 = str(i).split(', ')
        currentIndex = 0
        for j in m1:
            m1[currentIndex] = non_decimal.sub('', j)
            currentIndex = currentIndex + 1

    # Iterates through the message2 data
    # produces list m2 with all numbers stored in indexes
    for a in ans2:
        m2 = str(a).split(', ')
        currentIndex = 0
        for b in m2:
            m2[currentIndex] = non_decimal.sub('', b)
            currentIndex = currentIndex + 1

    # This part of the method assembles all of the variables to go out
    context = {
        'year1' : m1[0][1:],
        'month1' : m1[1],
        'day1' : m1[2],
        'hour1' : m1[3],
        'minute1' : m1[4],
        'second1' : m1[5],
        'c11' : m1[6],
        'c12' : m1[7],
        'c13' : m1[8],
        'c14' : m1[9],
        'c15' : m1[10],
        'c16' : m1[11],

        'year2' : m2[0][1:],
        'month2' : m2[1],
        'day2' : m2[2],
        'hour2' : m2[3],
        'minute2' : m2[4],
        'second2' : m2[5],
        'c21' : m2[6],
        'c22' : m2[7],
        'c23' : m2[8],
        'c24' : m2[9],
        'c25' : m2[10],
        'c26' : m2[11],
    }
    
    return render(request, 'message.html', context=context)

# this creates a form for the user to enter a date and time
# it will redirect the user to a page displaying message data from said date and time
@login_required
def historical008(request):
    # If this is a request, process the data
    if request.method == 'POST':
        form = HistoricalForm(request.POST)

        # Check if valid:
        if form.is_valid():
            # Process the data to get the date that we need.

            # Store the start date from the form as a datetime object
            datereq1 = form.cleaned_data['start_date']
            # save individual variables to session
            request.session['startyear'] = datereq1.strftime("%Y")
            request.session['startmonth'] = datereq1.strftime("%m")
            request.session['startday'] = datereq1.strftime("%d")
            request.session['starthour'] = datereq1.strftime("%H")
            request.session['startminute'] = datereq1.strftime("%M")
            request.session['startsecond'] = datereq1.strftime("%S")
            # Store the end date from the form as a datetime object
            datereq2 = form.cleaned_data['end_date']
            request.session['endyear'] = datereq2.strftime("%Y")
            request.session['endmonth'] = datereq2.strftime("%m")
            request.session['endday'] = datereq2.strftime("%d")
            request.session['endhour'] = datereq2.strftime("%H")
            request.session['endminute'] = datereq2.strftime("%M")
            request.session['endsecond'] = datereq2.strftime("%S")

            # figure out which type of sensor data to call
            whichsensor = form.cleaned_data['which_sensor']
            request.session['sensor'] = whichsensor
            return HttpResponseRedirect('histview008/')
    # if this is a GET, create the default form
    else:
        default_date = datetime.date.today()
        form = HistoricalForm(initial={'message_date': default_date})

    context = {
        'sensornum': '008',
        'form': form,
    }

    return render(request, 'historical.html', context=context)

# this method displays historical data based on start and end time info stored in session
# it connects to the server
# it then makes a query based on the numbers pulled from session
# it then takes the results of the query and copies it to a pandas dataframe
# the dataframe is a table that is then returned
@login_required
def histview008(request):
    # connect to the MySQL database:
    try:
        # connects to the mySQL database running loabally
        connection = mysql.connector.connect(host='localhost',
                                            database='sensors',
                                            user='root',
                                            password='Star*lab12345')
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    cursor = connection.cursor()

    # Make a query...
    # query varies based on which sensor is selected
    if request.session.get('sensor') == 'detection':
        sql_command = "SELECT * FROM detection008 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'macaddress':
        sql_command = "SELECT * FROM macaddress008 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'environment':
        sql_command = "SELECT * FROM environment008 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'traveltime':
        sql_command = "SELECT * FROM traveltimes WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"

    SQL_Query = pd.read_sql_query(sql_command, connection)
    df = pd.DataFrame(SQL_Query)

    response = HttpResponse()
    response.write("""<!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Norway Project Sensors</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
            <!-- Add additional CSS in static file -->
            
            <link rel="stylesheet" href="{% static 'css/styles.css' %}">
            </head>
            <body>
            <div class="container-fluid">
                <div class="row">
                <div class="col-sm-2">
                    <ul class="sidebar-nav">
                    <a href="javascript:history.back()">Go Back</a>
                    </ul>
                </div>""")
    response.write("""<div class="col-sm-10 "> <h1> Historical Data From Sensor 008 </h1>""")

    response.write(df.to_html())
    response.write("""	  </div>
                </div>
            </div>
            </body>
            </html>""")
    return response 
    return render(request, 'histview.html', context=context)

# this creates a form for the user to enter a date and time
# it will redirect the user to a page displaying message data from said date and time
@login_required
def historical009(request):
    # If this is a request, process the data
    if request.method == 'POST':
        form = HistoricalForm(request.POST)

        # Check if valid:
        if form.is_valid():
            # Process the data to get the date that we need.

            # Store the start date from the form as a datetime object
            datereq1 = form.cleaned_data['start_date']
            # save individual variables to session
            request.session['startyear'] = datereq1.strftime("%Y")
            request.session['startmonth'] = datereq1.strftime("%m")
            request.session['startday'] = datereq1.strftime("%d")
            request.session['starthour'] = datereq1.strftime("%H")
            request.session['startminute'] = datereq1.strftime("%M")
            request.session['startsecond'] = datereq1.strftime("%S")
            # Store the end date from the form as a datetime object
            datereq2 = form.cleaned_data['end_date']
            request.session['endyear'] = datereq2.strftime("%Y")
            request.session['endmonth'] = datereq2.strftime("%m")
            request.session['endday'] = datereq2.strftime("%d")
            request.session['endhour'] = datereq2.strftime("%H")
            request.session['endminute'] = datereq2.strftime("%M")
            request.session['endsecond'] = datereq2.strftime("%S")

            # figure out which type of sensor data to call
            whichsensor = form.cleaned_data['which_sensor']
            request.session['sensor'] = whichsensor
            return HttpResponseRedirect('histview009/')
    # if this is a GET, create the default form
    else:
        default_date = datetime.date.today()
        form = HistoricalForm(initial={'message_date': default_date})

    context = {
        'sensornum': '009',
        'form': form,
    }

    return render(request, 'historical.html', context=context)

# this method displays historical data based on start and end time info stored in session
# it connects to the server
# it then makes a query based on the numbers pulled from session
# it then takes the results of the query and copies it to a pandas dataframe
# the dataframe is a table that is then returned
@login_required
def histview009(request):
    # connect to the MySQL database:
    try:
        # connects to the mySQL database running loabally
        connection = mysql.connector.connect(host='localhost',
                                            database='sensors',
                                            user='root',
                                            password='Star*lab12345')
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    cursor = connection.cursor()

    # Make a query...
    # query varies based on which sensor is selected
    if request.session.get('sensor') == 'detection':
        sql_command = "SELECT * FROM detection009 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'macaddress':
        sql_command = "SELECT * FROM macaddress009 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'environment':
        sql_command = "SELECT * FROM environment009 WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"
    elif request.session.get('sensor') == 'traveltime':
        sql_command = "SELECT * FROM traveltimes WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"

    SQL_Query = pd.read_sql_query(sql_command, connection)
    df = pd.DataFrame(SQL_Query)

    response = HttpResponse()
    response.write("""<!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Norway Project Sensors</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
            <!-- Add additional CSS in static file -->
            
            <link rel="stylesheet" href="{% static 'css/styles.css' %}">
            </head>
            <body>
            <div class="container-fluid">
                <div class="row">
                <div class="col-sm-2">
                    <ul class="sidebar-nav">
                    <a href="javascript:history.back()">Go Back</a>
                    </ul>
                </div>""")
    response.write("""<div class="col-sm-10 "> <h1> Historical Data From Sensor 009 </h1>""")

    response.write(df.to_html())
    response.write("""	  </div>
                </div>
            </div>
            </body>
            </html>""")
    return response 
    return render(request, 'histview.html', context=context)

@login_required
def image(request):
    # this code pulls the filepath of the most recent image
    # Establishing a connection to the database
    try:
        # connects to the mySQL database running loabally
        connection = mysql.connector.connect(host='localhost',
                                            database='sensors',
                                            user='root',
                                            password='Star*lab12345')
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

#    cursor = connection.cursor()
    # image1 data as well as image2 data

 #   sql_command = "SELECT photo FROM image1 ORDER BY timestamp DESC LIMIT 1"
  #  cursor.execute(sql_command)
   # ans1 = cursor.fetchall()

 #   sql_command = "SELECT photo FROM image2 ORDER BY timestamp DESC LIMIT 1"
 #   cursor.execute(sql_command)
 #   ans2 = cursor.fetchall()
 #   non_decimal = re.compile(r'[^\d.]+')

  #  as1 = str(ans1)
  #  as2 = str(ans2)

 #   image1 = as1[3:-4]
 #   image2 = as2[3:-4]


    # this part assembles the variables to go out
    context = {
  #      'image1' : image1,
  #      'image2' : image2,
    }

    return render(request, 'image.html', context=context)
    
# this creates a form for the user to enter a date and time
# it will redirect the user to a page displaying message data from said date and time
@login_required
def traveltime(request):
    # If this is a request, process the data
    if request.method == 'POST':
        form = TraveltimeForm(request.POST)

        # Check if valid:
        if form.is_valid():
            # Process the data to get the date that we need.

            # Store the start date from the form as a datetime object
            datereq1 = form.cleaned_data['start_date']
            # save individual variables to session
            request.session['startyear'] = datereq1.strftime("%Y")
            request.session['startmonth'] = datereq1.strftime("%m")
            request.session['startday'] = datereq1.strftime("%d")
            request.session['starthour'] = datereq1.strftime("%H")
            request.session['startminute'] = datereq1.strftime("%M")
            request.session['startsecond'] = datereq1.strftime("%S")
            # Store the end date from the form as a datetime object
            datereq2 = form.cleaned_data['end_date']
            request.session['endyear'] = datereq2.strftime("%Y")
            request.session['endmonth'] = datereq2.strftime("%m")
            request.session['endday'] = datereq2.strftime("%d")
            request.session['endhour'] = datereq2.strftime("%H")
            request.session['endminute'] = datereq2.strftime("%M")
            request.session['endsecond'] = datereq2.strftime("%S")

            return HttpResponseRedirect('travelview/')
    # if this is a GET, create the default form
    else:
        default_date = datetime.date.today()
        form = TraveltimeForm(initial={'message_date': default_date})

    context = {
        'form': form,
    }

    return render(request, 'traveltime.html', context=context)

@login_required
def travelview(request):
    # connect to the MySQL database:
    try:
        # connects to the mySQL database running loabally
        connection = mysql.connector.connect(host='localhost',
                                            database='sensors',
                                            user='root',
                                            password='Star*lab12345')
    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    cursor = connection.cursor()

    # Make a query...
    sql_command = "SELECT * FROM traveltimes WHERE timestamp BETWEEN '" + request.session.get('startyear') + '-' + request.session.get('startmonth') + '-' + request.session.get('startday') + ' ' + request.session.get('starthour') + ':' + request.session.get('startminute') + ':' + request.session.get('startsecond') + "' AND '" + request.session.get('endyear') + '-' + request.session.get('endmonth') + '-' + request.session.get('endday') + ' ' + request.session.get('endhour') + ':' + request.session.get('endminute') + ':' + request.session.get('endsecond') + "'"

    SQL_Query = pd.read_sql_query(sql_command, connection)
    df = pd.DataFrame(SQL_Query)

    response = HttpResponse()
    response.write("""<!DOCTYPE html>
            <html lang="en">
            <head>
            <title>Norway Project Sensors</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">
            <!-- Add additional CSS in static file -->
            
            <link rel="stylesheet" href="{% static 'css/styles.css' %}">
            </head>
            <body>
            <div class="container-fluid">
                <div class="row">
                <div class="col-sm-2">
                    <ul class="sidebar-nav">
                    <a href="javascript:history.back()">Go Back</a>
                    </ul>
                </div>""")
    response.write("""<div class="col-sm-10 "> <h1> Historical Data From Sensor 009 </h1>""")

    response.write(df.to_html())
    response.write("""	  </div>
                </div>
            </div>
            </body>
            </html>""")
    return response 
    return render(request, 'histview.html', context=context)