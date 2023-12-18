#-*- coding: utf-8 -*-
from django import forms
from Soluciones.models import soluciones,paquetes,solucionesConcursos
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class FormularioPaquetes(forms.ModelForm):
    class Meta:
        model=paquetes
        fields =("paqueteCod","paquetePrecio","paqueteDias","paqueteDescr","paquetePerfil")
class Formrespuestas(forms.ModelForm):

    class Meta:
        model = solucionesConcursos
        fields = '__all__'

class Formulario(forms.ModelForm):
    class Meta:
        model = soluciones
        fields =("problemaNumero","problemaProblema","problemaLibro","problemaSolucion","problemaVideo","problemaSolucionadoPor","problemaTema")

class NewUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2')