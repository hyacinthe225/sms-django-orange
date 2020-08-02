from django.shortcuts import *
from django.contrib.auth.models import User
import requests
import json
# from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
# from rest_framework.decorators import api_view, renderer_classes
from django.http import JsonResponse
from sendsms.forms import *
from sendsms.models import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from sendsms.forms import SignUpForm
from django.utils.crypto import get_random_string
from django.db.models import Count
from django.core.exceptions import ValidationError

def loginView(request):
	return render(request, 'registration/login.html')

def registerView(request):
	return render(request, 'registration/register.html')

def home(request):
    my_form = RawSmsForm()
    headers = {'Authorization': 'Bearer' + ' ' + 'ADdceqecfncdq1pG5ZVwUYaNim12', 'Content-Type': 'application/json' }
    sub = False
    address = str(request.POST.get('address'))
    address = address.split(",") 
    message = request.POST.get('message')
    for address in address:
        if request.method=="POST":
            if len(address)<8 :
                messages.error(request, "Un ou plusieurs SMS n'ont pas été envoyés car le  numéro doit être un nombre à 8 chiffres ")
            else:
                
                my_form = RawSmsForm(request.POST)
                if my_form.is_valid():

                    data = {
                        "outboundSMSMessageRequest":{ 
                            "address":"tel:+225" +  address, 
                            "senderAddress":"tel:+22577552217", 
                            "outboundSMSTextMessage":{ 
                            "message": message 
                                    } 
                                } 
                            }
                    api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B22577552217/requests"
                    response = requests.post( api_url, json=data, headers=headers)
                    if response.status_code == 201:
                        sub = True
                        Sms.objects.create(**my_form.cleaned_data)
                    else:

                        messages.error(request, 'ERREUR SURVENUE ! , VEUILLEZ CORRIGER LES NUMEROS ET RESSAYEZ SVP')

    context = {
            # 'info':info['partnerId'],
            'my_form':my_form,
            'sub':sub,
    }
    return render(request, 'index.html', context)



def csvgroup(request):
    sub = False
    if request.method =='POST':
        csv_file = request.FILES
        csv_file = csv_file['file']
        try:
            if not csv.name.endswith('.csv'):
                messages.error(request, " LE FICHIER N'EST PAS DE TYPE CSV")
            else:

                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                    created = Groupe.objects.update_or_create(
                    groupe=column[0],
                    nom=column[1],
                    numeros=column[2],)
                if  created:
                            sub = True
                csvreader = csv.reader(file)
            # Do whatever checks you want here
            # Raise ValidationError if checks fail
        except csv.Error:
            raise ValidationError('Failed to parse the CSV file')


        
                
    context = {
        'sub':sub
    }
    return render(request, 'csvgroup.html', context )

def statistiques(request):
    info = Sms.objects.all()
    context = {
        'info':info
    }
    return render (request, 'statistiques.html', context)


def signup(request):
    address = "tel:+225" + str(request.POST.get('username'))
    if request.method == 'POST':
        headers = {'Authorization': 'Bearer' + ' ' + 'ADdceqecfncdq1pG5ZVwUYaNim12', 'Content-Type': 'application/json' }
        form = SignUpForm(request.POST)
        vcode = get_random_string(4,'0123456789')
        if form.is_valid():
            user = form.save()
            # user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.vcode = vcode
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            data = {
                "outboundSMSMessageRequest":{ 
                    "address": address, 
                    "senderAddress":"tel:+22577552217", 
                    "outboundSMSTextMessage":{ 
                    "message": "Bienvenue sur HSMS, votre code de validation est :  "  + vcode 
                            } 
                        } 
                    }
            api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B22577552217/requests"
            response = requests.post( api_url, json=data, headers=headers)
            return redirect('/verif')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def confirm_tel(request):
    verif =  False
    code_user = request.POST.get('code_user')
    info = Profile.objects.get(user_id=request.user.id)
    vcode = info.vcode
    form = VerifForm()
    if request.method == 'POST' :
        if code_user == vcode :
            form = VerifForm(request.POST)
            if form.is_valid():
                form.save()
                verif = True
                return redirect('/')
            else:
                form = VerifForm()
        else :
            return redirect('/verif')

    return render(request, 'confirm_tel.html', {'form': form, 'verif':verif,})

def liste(request):
    form = ListeForm()
    info = Liste.objects.all()

    if request.method == 'POST':
        form =ListeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Groupe créé avec success ")
            form = ListeForm()
        else:
            form = ListeForm()
    return render(request, 'liste.html',  {'form': form, 'info':info} )


def sendcsv(request):
    sub = False
    choix = Groupe.objects.values('groupe').annotate(dcount=Count('groupe'))
    headers = {'Authorization': 'Bearer' + ' ' + 'ADdceqecfncdq1pG5ZVwUYaNim12', 'Content-Type': 'application/json' }
    if request.method =='POST':
        form =CsvForm(request.POST)
        choix = request.POST.get('groupe')
        message = str(request.POST.get('message'))
        groupe = Groupe.objects.filter(groupe=choix)
        for groupe in groupe :
            address = groupe.numeros
            message = message.replace("$", groupe.nom)
            data = {
                "outboundSMSMessageRequest":{ 
                    "address":"tel:+225" +  address, 
                    "senderAddress":"tel:+22577552217", 
                    "outboundSMSTextMessage":{ 
                    "message": message 
                            } 
                        } 
                    }
            api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B22577552217/requests"
            response = requests.post( api_url, json=data, headers=headers)
            if response.status_code == 201:
                created = Sms.objects.create(
                address=address,
                message=message,)
                sub = True
            else:

                messages.error(request, 'ERREUR SURVENUE ! , VEUILLEZ RESSAYEZ SVP')

    context = {
       'sub':sub,
       'choix':choix
    
    }
    return render(request, 'sendcsv.html', context)

def sendliste(request):
    liste = Liste.objects.all()
    address = str(request.POST.get('liste'))
    address = address.split(",") 
    message = request.POST.get('message')
    headers = {'Authorization': 'Bearer' + ' ' + 'ADdceqecfncdq1pG5ZVwUYaNim12', 'Content-Type': 'application/json' }
    form = SendlisteForm()
    if request.method =='POST':
        form = SendlisteForm(request.POST)
        if form.is_valid():
            for address in address:
                
                data = {
                    "outboundSMSMessageRequest":{ 
                    "address":"tel:+225" +  address, 
                    "senderAddress":"tel:+22577552217", 
                    "outboundSMSTextMessage":{ 
                    "message": message 
                            } 
                        } 
                }
                api_url = "https://api.orange.com/smsmessaging/v1/outbound/tel%3A%2B22577552217/requests"
                response = requests.post( api_url, json=data, headers=headers)
                if response.status_code == 201:
                    created = Sms.objects.create(
                    address=address,
                    message=message,)
                else:

                    messages.error(request, 'ERREUR SURVENUE ! , VEUILLEZ CORRIGER LES NUMEROS ET RESSAYEZ SVP')


    context ={
        'form':form,
        'liste':liste,
    }
    return render(request, 'sendlist.html', context)



# info = requests.get('https://api.orange.com/sms/admin/v1/contracts', headers=headers).json()
# info = json.loads(info)