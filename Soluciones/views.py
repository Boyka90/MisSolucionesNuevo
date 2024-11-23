from django.shortcuts import render,redirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from Soluciones.models import correoValidacion,libros, soluciones, paquetes,tematicas,UsuarioPaq,QRPago,perfil,ProblemaPaq,User, comentarios
from Soluciones.forms import Formulario,FormularioPaquetes,NewUserForm,Formrespuestas
from django.db.models import Count,Sum
from django.views.generic import ListView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.urls import reverse_lazy
import random
from django.contrib.auth.views import  LogoutView
from django.contrib import messages
from django.contrib.auth.models import User,Group
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from MisSoluciones.settings import EMAIL_HOST_USER
from enzona_api.enzona_business_payment import enzona_business_payment
import datetime as fecha
from django.contrib.auth.decorators import login_required
import json,threading,time
from django.core.exceptions import PermissionDenied

from pdf2image import convert_from_path








"""Integracion con Enzona"""

def Pago_Enzona(merchant_uuid,description_payment,currency,shipping,discount,tip,lst_products,merchant_op_id,invoice_number,return_url,cancel_url,terminal_id):
    pay = Payments(
    merchant_uuid=merchant_uuid,
    description_payment= description_payment,
    currency=currency,
    shipping=shipping,
    discount=discount,
    tip=tip,
    lst_products=lst_products,
    merchant_op_id= merchant_op_id,
    invoice_number=invoice_number,
    return_url= return_url,
    cancel_url=cancel_url,
    terminal_id=terminal_id
)

    response = ebp.create_payments(payment=pay.get_payment())
    transaction_uuid = response.transaction_uuid()
    link_confirm = response.link_confirm()
def group_required(*group_names,login_url):
   """Requires user membership in at least one of the groups passed in."""

   def in_groups(u):

       gente = User.objects.filter(groups__name__in=['profesores'])
       lista = []
       for i in gente:
           lista.append(i.id)
       estas=u.id in lista

       if u.is_authenticated and estas==True:

               return True
       return False
   return user_passes_test(in_groups,login_url)



def revisadoo(request):
    libro=request.GET.get('libro', None)
    problema=request.GET.get('problema', None)
    obse=request.GET.get('Obs', None)
    estado=request.GET.get('revi', None)
    soluciones.objects.filter(problemaLibro = libros.objects.get(titulo=libro), problemaNumero=problema).update(problemaRev= estado,problemaObs=obse)
    data={"s":"Registro guardado"}
    return JsonResponse(data)

def contactanos(request):
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    perfiles=perfil.objects.all()
    configurar=completarPlantilla(request)
    configurar["mispaquetes"]=paquetesUsu
    configurar["novalida"]="none"
    return render(request,"contactanos.html" ,configurar)
@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')
class ListaLibros(ListView):
    template_name = "libros_list.html"
    model = libros

    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        configuracion=completarPlantilla(self.request)
        context=super(ListaLibros,self).get_context_data(**kwargs)
        context.update(configuracion)
        return context
@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')

class TematicasAct(UpdateView):
    template_name = "tematicas_Actua.html"
    success_url = reverse_lazy('listatemas')
    model = tematicas
    fields = '__all__'



    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        configurar = completarPlantilla(self.request)
        context=super(TematicasAct,self).get_context_data(**kwargs)
        context.update(configurar)
        return context
@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')

class librosAct(UpdateView):
    template_name = "libro_Actua.html"
    success_url = reverse_lazy('listalibros')
    model = libros
    fields = '__all__'



    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        configurar = completarPlantilla(self.request)
        context=super(librosAct,self).get_context_data(**kwargs)
        context.update(configurar)
        return context
@method_decorator(group_required('profesores', login_url='/error/'), name='dispatch')



class Tematicas(ListView):
        template_name = "tematicas_list.html"
        model = tematicas



        def get_context_data(self, **kwargs):
            perfiles = perfil.objects.values()
            configurar = completarPlantilla(self.request)
            context = super(Tematicas, self).get_context_data(**kwargs)
            context.update(configurar)
            return context
@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')

class CreaTemas(CreateView):


    model = tematicas
    template_name = "temas_form.html"
    success_url = reverse_lazy('listatemas')
    fields = "__all__"



    def get_context_data(self,**kwargs):

        perfiles = perfil.objects.values()
        context=super(CreaTemas,self).get_context_data(**kwargs)
        context.update({'novalida':'none','perfiles':perfiles})
        return context

@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')
class CreaLibro(CreateView):
    model = libros
    template_name = "libros_form.html"
    success_url = reverse_lazy('listalibros')
    fields = "__all__"
    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        context=super(CreaLibro,self).get_context_data(**kwargs)
        context.update({'novalida':'none','perfiles':perfiles})
        return context

@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')
class BorraLibro(DeleteView):
    model = libros
    success_url = reverse_lazy('listalibros')
    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        context=super(BorraLibro,self).get_context_data(**kwargs)
        context.update({'novalida':'none','perfiles':perfiles})
        return context
@method_decorator(group_required('profesores',login_url='/error/'), name='dispatch')
class BorraTemas(DeleteView):
    model = tematicas
    success_url = reverse_lazy('listatemas')
    def get_context_data(self,**kwargs):
        perfiles = perfil.objects.values()
        context=super(BorraTemas,self).get_context_data(**kwargs)
        context.update({'novalida':'none','perfiles':perfiles})
        return context
def vencimiento():
    QActivos= UsuarioPaq.objects.select_related().filter(activo=True)
    while True:
        for h in QActivos:
            fechaVence=h.fechaPago+fecha.timedelta(days=h.paqueteMio.paqueteDias)
            if fechaVence<fecha.date.today():
                UsuarioPaq.objects.filter(id=h.id).update(vencido=True,activo=False)
        time.sleep(60)

#hilo=threading.Thread(target=vencimiento())
#hilo.start()

def registroCodigo(request):

    if request.method == 'POST':
        formulario = NewUserForm(data=request.POST)

        valida=correoValidacion.objects.filter(correo=request.session["correosesion"],codigo=request.POST.get("codigo"))
        if valida.exists():
            user = User.objects.create_user(username=valida[0].usuario, first_name=valida[0].Apellido1,last_name=valida[0].Apellido2,email=valida[0].correo, password=valida[0].clave, )
            user=authenticate(username=valida[0].usuario,password=valida[0].clave)
            login(request, user)
            return redirect('index')
        else:
            return redirect('registro')
    return render(request, 'RegistroCodigo.html')

def team(request):
    data=completarPlantilla(request)
    return render(request, 'team.html',data)
def promociones(request):
    data = completarPlantilla(request)
    m = 3;
    return render(request, 'promociones.html',data)
def enviacorreo(Asunto,comentario,correo,origen):

        if origen=='contactanos':
            email =  EmailMessage(Asunto,comentario,EMAIL_HOST_USER,[correo])
            email.send()

def enviacorreoValidar(request):
        print("enviando...")

def Modalvirtual(request):
        asignatura= request.GET.get('asignatura', None)
        data={'msj':"asignatura"}
        return JsonResponse(data)

def Buscatemasxperfil(request):
    libro=request.GET.get('perfil', None)
    temas=tematicas.objects.select_related("perfilId").filter(perfilId__nombrePerfil=libro)
    lista=[]
    for u in temas:
        lista.append(u.temaNombre)


    data= {'temas':list(lista)}
    return JsonResponse(data)





def LPaquetes(request,miperfil): #OK
    perfiles=perfil.objects.values()
    gente = User.objects.filter(groups__name__in=['profesores'])
    listaProfe = []
    for i in gente:
        listaProfe.append(i.id)
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, vencido=False,activo=True)
    paquete=paquetes.objects.select_related('paquetePerfil').filter(paquetePerfil__nombrePerfil=miperfil)
    datos={'listaProfe':listaProfe,'au': request.user.is_authenticated,'perfil':miperfil,'novalida':"none","paquetes":paquete,'perfiles':perfiles,'mispaquetes':paquetesUsu,'estilo':"display:none"}


    return render(request, 'listarPaquetes.html',datos )

def Milogin(request):

    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                form = AuthenticationForm()
                configuracion=completarPlantilla(request)


                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request,"login.html",{"form": form})

def logout(request): #OK
    request.session.flush()
    return redirect('/')

def registro(request): #OK
    data = {'form': NewUserForm(), 'msj': 'Ha ocurrido un problema, Intentelo nuevamente'}
    if request.method == 'POST':

        codigo = random.randint(10000, 20000)
        correo=request.POST.get('email')
        clave1 = request.POST.get('password1')
        clave2 = request.POST.get('password2')
        usuario1=request.POST.get('username')
        apellido1=request.POST.get('first_name')
        apellido2= request.POST.get('last_name')
        request.session["correosesion"]=correo
        valida=correoValidacion.objects.filter(correo=request.session["correosesion"]).exists()
        if clave1==clave2 and valida==False:
            try:
                email = EmailMessage('Registro a MisSoluciones', 'Su código de Validacion es {0}'.format(codigo), EMAIL_HOST_USER,[correo])
                email.send()
                correoValidacion.objects.create(correo=correo, codigo=codigo, validado=False,clave=clave1, usuario=usuario1,Apellido1=apellido1,Apellido2=apellido2)

                return redirect('registroCodigo')
            except:
                return render(request, "registro.html", data)
    return render(request, "registro.html", data)

def terminos(request):

    return render(request,"terminos.html",completarPlantilla(request))

def verPaquetes(request,codigo): #ok
    paquetes = ProblemaPaq.objects.select_related('problemaID', 'paqueteID').filter(paqueteID__paqueteCod=codigo)
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, vencido=False)
    configuracion=completarPlantilla(request)
    configuracion['novalida']='none'
    configuracion['paquetes'] = paquetes
    configuracion['mispaquetes'] = paquetesUsu
    configuracion['estilo'] = "display:none"
    return render(request,"verPaquetes.html" ,configuracion)
@login_required(login_url='/login/') #OK
def mipkt(request,pkt):
    request.session["pkt"]=pkt
    gente = User.objects.filter(groups__name__in=['profesores'])
    listaProfe = []
    for i in gente:
        listaProfe.append(i.id)
    perfiles1=perfil.objects.all()
    paquetesUsu = UsuarioPaq.objects.filter(usuario=request.user.id, paqueteMio=paquetes.objects.get(paqueteCod=pkt))
    if len(paquetesUsu) !=0 :
        problemas=ProblemaPaq.objects.select_related("paqueteID","problemaID").filter(paqueteID__paqueteCod=pkt)
        mispaquetes= UsuarioPaq.objects.filter(usuario=request.user.id, activo=True)
        configura=completarPlantilla(request)
        configura['pkt']=pkt
        configura['problemas'] = problemas
        configura['mispaquetes'] = mispaquetes
        configura['listaProfe'] = listaProfe

        return render(request, "verMiPKT.html", configura)
    else:
        redirect('index')







def TranferMovil(request,pkt,usuario):
    usuario=request.GET.get("usuario")
    paquete=request.GET.get("paquete")
    codigo='{0}Z{1}'.format(paquete,usuario)
    negocio="TTAAMM"
    lista1=[codigo,negocio]
    contact1 = dict(
        first_name='John',
        last_name='Doe',
        first_name_reading='jAAn',
        last_name_reading='dOH',
        tel='+41769998877',
        email='j.doe@company.com',
        url='http://www.company.com',

    )
    data={'verificado':'ok','sms':"Tranccion Realizada",'qr':contact1 }
    return render(request,'transfermovil.html',data)
def historial(request):
    lista=[]
    paquetesComprados=UsuarioPaq.objects.filter(usuario=request.user.id)
    for u in paquetesComprados:
        valor='Codigo:{0}, comprado:{1}, Activo:{2}'.format(u.paqueteMio.paqueteCod, u.fechaIni,u.activo)
        lista.append(valor)

    data={'s':list(lista)}
    return JsonResponse(data)
def concur(request):
    concursosActivos=concursos.objects.filter(activo=True)
    config=completarPlantilla(request)

    config["concursos"]=concursosActivos

    return render(request,'concursos.html',config)
def registrodeConcur(request):
    codigo = request.GET.get('codigoC', None)

    UsuarioConcurso.objects.create(usuario=User.objects.get(id=request.user.id),concur=concursos.objects.get(Codigonombre=codigo))
    data={'t':'Usuario Inscrito'}
    return JsonResponse(data)
def MuestraConcu(request):
    concu1=UsuarioConcurso.objects.select_related('concur').get(usuario=request.user.id)
    figura=concursos.objects.get(Codigonombre=concu1.concur.Codigonombre)
    confi=completarPlantilla(request)
    confi['figura']=figura.problema
    confi['form'] = Formrespuestas()

    return render(request,'MuestraConcurso.html', confi)
def verifConcur(request):


    if UsuarioConcurso.objects.filter(usuario=request.user.id).exists():
        concu=UsuarioConcurso.objects.select_related('concur').get(usuario=request.user.id)

        data={'hacer':'algo', 'msj':'Usted esta inscrito en el concurso {0}'.format(concu.concur.Codigonombre)}
    else:
        data={'hacer':'nada'}

    return JsonResponse(data)

def consultar(request):
    solucionesTabla=soluciones.objects.select_related("problemaLibro")
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False)
    gente = User.objects.filter(groups__name__in=['profesores'])
    perfiles=perfil.objects.all()
    vpaq= paquetes.objects.all()
    listaProfe = []
    for i in gente:
        listaProfe.append(i.id)
    return render(request,'busquedas.html',{'listaProfe': listaProfe,'novalida': 'none','au': request.user.is_authenticated,'data':solucionesTabla, 'perfiles':perfiles, 'vpaq':vpaq, 'mispaquetes':paquetesUsu})

def problema(request,libro):
    id=libros.objects.get(titulo=libro)
    problemas=soluciones.objects.filter(problemaLibro=id)
    problemas10=soluciones.objects.filter(problemaLibro=id)[:2]
    arbol={}
    for y in problemas:

        arbol[y.problemaTema.temaNombre]=[]
    for v in problemas:
        arbol[v.problemaTema.temaNombre].append(v.problemaNumero)
    data={'libro':libro, 'problemas':problemas,'arbol':arbol,'tamara':problemas10}
    return render(request,"problema.html", data)

@login_required(login_url='/login/')
def versolucion(request,libro, numero):

    dic=completarPlantilla(request)
    id=libros.objects.get(titulo=libro)
    solucion=soluciones.objects.select_related().get(problemaLibro=id, problemaNumero=numero)
    mispaquetes=UsuarioPaq.objects.select_related('paqueteMio').filter(usuario=request.user.id)
    dic["solucion"]=solucion
    dic["pkt"] = request.session["pkt"]

    return render(request,"versolucion.html", dic)


def versolucionProfe(request,libro, numero):

    dic=completarPlantilla(request)
    id=libros.objects.get(titulo=libro)
    solucion=soluciones.objects.select_related().get(problemaLibro=id, problemaNumero=numero)



    dic["solucion"]=solucion

    return render(request,"versolucionProf.html", dic)


def compraPKT(request): #OK

    lista=request.GET.getlist('lista[]', None)
    UnPKT=request.GET.get('paquete', None)

    fuenteDePago=request.GET.get('fuenteDePago', None)
    transacion=request.GET.get('Transac', None)
    usuarioID = int(request.user.id)
    fecha1 = fecha.date.today()
    lista1=[]
    utilizados=[]
    print(transacion)
    if fuenteDePago=="Carrito":
        for y in lista:
            if y not in lista1 and y != '':
                lista1.append(y)

        for  u in lista1:
            puede = UsuarioPaq.objects.filter(usuario=usuarioID, paqueteMio=paquetes.objects.get(paqueteCod=u),activo=True)

            if len(puede)==0:
                UsuarioPaq.objects.create(usuario=usuarioID, fechaIni=fecha1,paqueteMio=paquetes.objects.get(paqueteCod=u), activo=True)

            else:
                utilizados.append(u)
        data={'utilizados':list(utilizados),'sms':"1transacion"}
    if fuenteDePago=="NoCarrito":
       puede = UsuarioPaq.objects.filter(usuario=usuarioID, paqueteMio=paquetes.objects.get(paqueteCod=UnPKT),activo=True)
       if len(puede)==0:
            UsuarioPaq.objects.create(usuario=usuarioID, fechaIni=fecha1,paqueteMio=paquetes.objects.get(paqueteCod=UnPKT), activo=False, transac=transacion)
            data={'sms':"Ha Adquirido un paquete mediante la Transacción {0}".format(transacion)}



    return JsonResponse(data)

def borrarPaquetes(request):
    paquete=request.GET.get("paquete")
    paquetes.objects.get(paqueteCod=paquete).delete()
    Listapaquetes=paquetes.objects.all()
    lista=[]
    for y in Listapaquetes:
        lista.append(y.paqueteCod)
    sms="hghjjg"
    data={"listapaquetes":list(lista),"smg":sms}
    return JsonResponse(data)
def borraPa(request):
    valor=request.GET.get("paquete")

    try:
        UsuarioPaq.objects.select_related('paqueteMio').filter(paqueteMio__paqueteCod=valor).delete()
        tema="El registro ha sido eliminado."
        tipo=2
        data = {'sms': tema,'tipo':tipo}
    except:
        tema="Ha ocurrido un error"
        tipo=1
        data = {'sms': tema,'tipo':tipo}

    return JsonResponse(data)

def getProblemas(request):
    problemas = request.GET.get('problemas', None)
    ProblS=soluciones.objects.filter(problemaPkt=paquetes.objects.get(paqueteCod=problemas))

    lista=[]
    for u in ProblS:
        lista.append(u.problemaNumero)

    problemasLista=[]
    while len(lista) >3:
         pice = lista[:3]
         problemasLista.append(pice)
         lista   = lista[3:]
         problemasLista.append(lista)

    a=json.dumps(problemasLista)

    data = {'problemas': a}

    return JsonResponse(data)

def BuscaTransaccion(request):

    transaccion=request.GET.get("transac",None)
    try:
        buscarTransa=UsuarioPaq.objects.get(transac=transaccion)
    except:
        buscarTransa=""

    if buscarTransa !="":
        data= {'SMS':"Transaccíon,{1}, es Valida,el valor de la misma es {0}".format(buscarTransa.paqueteMio.paquetePrecio,transaccion ), 'estado':'ok'}
        return JsonResponse(data)

    else:
        data= {'SMS':"No Existe esa Transaccíon,{0}",'estado':'Nok'}
        return JsonResponse(data)

def ActivarTransaccion(request):

    transaccion=request.GET.get("transac",None)
    activar=UsuarioPaq.objects.filter(transac=transaccion).update(activo=True)


    data= {'SMS':transaccion,'estado':'Nok', "act":activar1}
    return JsonResponse(data)
def index(request):
    gente = User.objects.filter(groups__name__in=['profesores'])
    var = True
    listaProfe = []
    for i in gente:
        listaProfe.append(i.id)
    orden={}

    pket=""
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False,activo=True)

    perfiles=perfil.objects.values()
    vpaq= paquetes.objects.all()
    temas=tematicas.objects.all()
    if  not request.user.is_staff:
        admin="pointer-events:none;cursor:default"
    if  not request.user.is_authenticated:
        pket="pointer-events:none;cursor:default"
    u=soluciones.objects.select_related("problemaLibro").values('problemaLibro',"problemaLibro__titulo").annotate(num_books=Count('problemaLibro'))
    cadena=""
    for hh in u:
        cadena=cadena+""+hh["problemaLibro__titulo"]+"("+str(hh["num_books"])+")"+","+""
    total=soluciones.objects.count()
    for i in range(0,len(u)):
        libro=libros.objects.get(id=int(u[i]['problemaLibro']))
        orden[libro.titulo]=u[i]['num_books']

    return render(request,"index.html", { "problXLibro":cadena,"var":var,"listaProfe":listaProfe,'novalida':'none','perfiles':perfiles,'mispaquetes':paquetesUsu,'libros':orden,'total':total,'estilo':"display:none","pket":pket, "vpaq": vpaq,"temas":temas,'au':request.user.is_authenticated})

def completarPlantilla(request):
    gente = User.objects.filter(groups__name__in=['profesores'])
    listaProfe= []
    for i in gente:
        listaProfe.append(i.id)
    paquetesUsu=UsuarioPaq.objects.filter(usuario=request.user.id,vencido=False,activo=True)
    perfiles=perfil.objects.values()
    vpaq= paquetes.objects.all()
    temas=tematicas.objects.all()
    librosT=libros.objects.all()
    configura={'listaProfe':listaProfe,'au':request.user.is_authenticated,'novalida':'none','perfiles':perfiles,'mispaquetes':paquetesUsu,'libros':librosT, "temas":temas}
    return configura
def getPaquetes(request):
    perfil=request.GET.get('perfil', None)

    paquetes1=paquetes.objects.select_related('paquetePerfil').filter(paquetePerfil__nombrePerfil=perfil)
    lista=[]
    for h in paquetes1:
        lista.append('{0}, {2} de {1}'.format(h.paqueteCod,h.paqueteDescr,h.paqueteCant))
    data= {'paquetes':list(lista)}
    return JsonResponse(data)

def getDetalles(request):
    cadena=request.GET.get('CodigoP', None).split(',')

    paquetes1=paquetes.objects.values().get(paqueteCod=cadena[0])

    lista=[]
    for h in paquetes1.keys():
       lista.append(paquetes1[h])

    data= {'paquetes':list(lista)}
    return JsonResponse(data)
def contac(request):
    nombre=request.POST.get("nombre")
    correo=request.POST.get("email")
    tipo=request.POST.get("subject")
    comentario=request.POST.get("message")
    if request.user.is_authenticated:
        usuario=User.objects.get(id=request.user.id)
        comentarios.objects.create(nombre=nombre,usuario=usuario,correo=correo,tipo=tipo,comentario=comentario)
    data=completarPlantilla(request)
    if request.method=="POST":
        correo='misoluciones22@yandex.com'
        enviacorreo(tipo,comentario,correo,'contactanos')

    return render(request,"contactanos.html",data)
def poblarPaquetes(request):

    problemas=request.GET.getlist('problemas[]', None)


    paquete=request.GET.get('paquete', None)
    a = paquetes.objects.get(paqueteCod=paquete)
    CantidadProbl=a.paqueteCant
    for u in problemas:
        ProblemaPaq.objects.create(problemaID=soluciones.objects.get(problemaNumero=u),paqueteID=paquetes.objects.get(paqueteCod=paquete))
        CantidadProbl+=1
    paquetes.objects.filter(paqueteCod=paquete).update(paqueteCant=CantidadProbl)
    data={'t':problemas}
    return JsonResponse(data)

#@login_required(login_url='/login/')
def Tuerror(request):
    mensaje={"mensaje":"lalalalal"}

    configuracion=completarPlantilla(request)
    configuracion["mensaje"]="Usted no tiene permiso para entrar a esta sección"
    return render(request,"404.html",configuracion)
@group_required('profesores',login_url='/error/')
def formaPket(request):
    data=completarPlantilla(request)
    formularioPaquetes = FormularioPaquetes()
    data = completarPlantilla(request)
    data['formularioPaquetes'] = formularioPaquetes
    data['paquetes'] = paquetes.objects.all()
    if request.method == "POST":
        form = FormularioPaquetes(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.paqueteCreador = request.user
            post.save()

    else:
        form = FormularioPaquetes()
    return render(request,"FormaPKT.html",data)
def BuscaProblemas(request):
    libro=request.GET.get('libro', None)
    temas=request.GET.get('temas', None)
    problemas1=soluciones.objects.select_related("problemaLibro","problemaTema").filter(problemaLibro__titulo=libro,problemaTema__temaNombre=temas)
    lista=[]
    for u in problemas1:
        if u.problemaNumero not in lista:
            lista.append(u.problemaNumero)

    data= {'problemas':list(lista)}

    return JsonResponse(data)
def BuscaTemasxLibros(request):
    libro=request.GET.get('libro', None)
    temas=soluciones.objects.select_related("problemaLibro","problemaTema").filter(problemaLibro__titulo=libro)
    lista=[]
    for u in temas:
        if u.problemaTema.temaNombre not in lista:
            lista.append(u.problemaTema.temaNombre)


    data= {'temas':list(lista)}
    return JsonResponse(data)
def Muestraproblemas(request):
    pro=request.GET.getlist('problemas[]',None)
    problemas=soluciones.objects.filter(problemaNumero__in=pro)
    lista=[]
    for h in problemas:
        lista.append(h.problemaProblema.url)

    data= {'temas':list(lista)}
    return JsonResponse(data)
@group_required('profesores',login_url='/login/')
def cargar(request): #agrega libros
   configuracion=completarPlantilla(request)

   libros1=libros.objects.all()
   perfiles=perfil.objects.all()

   configuracion['formulario']=Formulario()
   configuracion['libros'] = libros1
   configuracion['novalida'] = "none"
   configuracion['perfiles'] = perfiles
   if request.method=="POST":

       formulario=Formulario(data=request.POST, files=request.FILES)
       if formulario.is_valid():
           formulario.save()
           configuracion["mensaje"]="Todo OK"
       else:
           configuracion["formulario"]=formulario
   return render(request, "cargar.html" ,configuracion)

def formaPketNoTrabaja(request):
    formularioPaquetes=FormularioPaquetes()
    data=completarPlantilla(request)
    data['formularioPaquetes']=formularioPaquetes
    data['paquetes']=paquetes.objects.all()
    if request.method == "POST":
        form = FormularioPaquetes(request.POST)
        if form.is_valid():

            post = form.save(commit=False)
            post.paqueteCreador = request.user
            post.save()

    else:
        form = FormularioPaquetes()


    return render(request,"FormaPKT.html",data)
def Creacodigo(request):
    Cod1=request.user.username
    Cod2=request.user.first_name
    Cod3=request.user.last_name

    fecha1=fecha.datetime.now()

    codigo=str(Cod1[0].upper())+str(Cod2[0].upper())+str(Cod3[0].upper())+str(fecha1.year)+str(fecha1.month)+str(fecha1.day)+str(fecha1.hour)+str(fecha1.minute)

    data= {'codigo':codigo}
    return JsonResponse(data)


def home(request):
    cofig=completarPlantilla(request)
    return render(request, 'home.html',cofig)

def salasChat(request, room):
    username = request.GET.get('username')
    room_details = salas.objects.get(salanombre=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })
def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    clave = request.POST['password']
    gente = User.objects.filter(groups__name__in=['profesores'])
    lista = []
    for i in gente:
        lista.append(i.id)
    profe = request.user.id in lista
    if salas.objects.filter(salanombre=room, clave=clave).exists():
        return redirect('/' + room + '/?username=' + username)
    if salas.objects.filter(salanombre=room, clave=clave).exists()==False and profe==True:
        new_room = salas.objects.create(salanombre=room,clave=clave)
        new_room.save()
        return redirect('/' + room + '/?username=' + username)
def getMessages(request, room):
    room_details = salas.objects.get(salanombre=room)
    messages = mensajes.objects.filter(sala=room_details.id)

    return JsonResponse({"messages":list(messages.values())})

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = mensajes.objects.create(mensaje=message, usuario=username, sala=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')


def donativo(request):
        return render(request,'donativo.html')

def cargo(request):
        redirect('Gracias')

def gracias(request):
        render(request,'garcias.html')
