from http import client
from django.shortcuts import render
from django import forms
from secrets import token_urlsafe
import pymongo

class RForm(forms.Form):
    isbn = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'field'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
    phone = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'field'}))

class CForm(forms.Form):
    res_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'field'}))
    phone = forms.IntegerField( widget=forms.TextInput(attrs={'class': 'field'}))

def homepage(request):
    return render(request, 'home.html')

def show(request):
    conn = pymongo.MongoClient()
    db = conn["library"]
    col = db["all_books"]
    context = col.find()
    data_all = []
    for x in context:
        data_all.append(
            {
                "ISBN": x["ISBN"],
                "name": x["Book_name"],
                "Au": x["Author"],
                "Ct": x["Count"],
                "Bor": x["Borrowed"],
                "Res": x["Reserved"],
                "Av": x["Available"],
            }
        )
    return render(request, "display.html", {"data": data_all})

def request_res(request):
    form = RForm(request.POST)
    if form.is_valid():
            conn = pymongo.MongoClient()
            db = conn["library"]
            col = db["all_books"]
            query1 = { "ISBN" : form.cleaned_data['isbn'] }
            # print(col)
            doc = col.find_one(query1)
            # print(doc,form.cleaned_data['isbn'])
            if doc['Available'] > 0:
                a = doc['Available']-1
                b = doc['Reserved']+1
                col.find_one_and_update({"ISBN": form.cleaned_data['isbn']}, {"$set": {'Available':a, 'Reserved':b}})
                col = db["reserved"]
                id = ''.join([c for c in token_urlsafe(10) if c not in '-_OI0l'])[:5]
                form.cleaned_data["res_id"] = id
                col.insert_one(form.cleaned_data)
                return render(request, 'reserved.html', { "data": id })
            else:
                return(render(request, 'rfailed.html'))
    return render(request, 'request.html', { "form" : RForm() })

def cancel_res(request):
    if request.method == "POST":
        form = CForm(request.POST)
        print(form)
        print(form.is_valid())
        print(form.errors)
        #print(form.cleaned_data)
        if form.is_valid():
                conn = pymongo.MongoClient()
                db = conn["library"]
                col = db["reserved"]
                query1 = { "res_id" : form.cleaned_data['res_id'] }
                doc = col.find_one(query1)
                print(doc)
                if doc:
                    isbn = doc["isbn"]
                    col.delete_one( { 'res_id' : form.cleaned_data['res_id'] } )
                    col = db["all_books"]
                    query1 = { "ISBN" : isbn }
                    doc = col.find_one(query1)
                    a = doc['Available']+1
                    b = doc['Reserved']-1
                    col.find_one_and_update({"ISBN": isbn}, {"$set": {'Available':a, 'Reserved':b}})
                    return(render (request, 'cancelled.html'))
                else:
                    return(render (request, 'cfailed.html'))
    return render(request, 'cancel.html', { "form" : CForm() })

def admin(request):
    return render(request, 'admin.html')