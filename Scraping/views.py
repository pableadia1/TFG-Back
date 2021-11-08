#encoding:utf-8
from django.shortcuts import render
from bs4 import BeautifulSoup

from Equipo.models import Equipo
from Jugador.models import Jugador
from Estadisticas.models import *
from Liga.models import Liga

import requests
import lxml
import datetime

def obtenerTabla(tab):
    res = None
    if tab != None:
        res = tab.find("tbody").find_all("tr")
        if len(res) > 4:
            res = res[-4:]
    return res

def Zeros(estadistica):
    if estadistica == "":
        estadistica = "0"
    if "." in estadistica:
        estadistica = float(estadistica)
    else:
        estadistica = int(estadistica)
    return estadistica

def yardMetrosDec(yard):
    conv = float(yard) * 0.9144
    sep = str(conv).split(".")
    res = sep[0]+"."+sep[1][0]
    return str(res)

def yardMetros(yard):
    conv = float(yard) * 0.9144
    res = str(conv).split(".")[0]
    return str(res)
    

def demarcaciones(dem):
    res = []
    if "(" in dem:
        dem = dem.split("(")[1]
        dem = dem.split(",")[0].split("-")
        for d in dem:
            d = d.split(")")
            res.append(d[0])
    return res

def generales(s1):
        lisGenerales = []
        generales = s1.find("div", id=["all_stats_standard"])
        if generales != None:
            gen = generales.find("tbody").find_all("tr")
            if len(gen) > 4:
                gen = gen[-4:]
            for g in gen:
                gn = g.find_all("td")
                if len(g) == 32:
                    temporada = g.find("th").text
                    equipo = gn[1].text
                    pj = Zeros(gn[5].text)
                    titular = Zeros(gn[6].text)
                    m = gn[7].text
                    minm = Zeros(m.replace(",",""))
                    goles = Zeros(gn[9].text)
                    asistencias = Zeros(gn[10].text)
                    t =(temporada,equipo,int(pj),int(titular),int(minm),int(goles),int(asistencias))
                    lisGenerales.append(t)
        return lisGenerales

def tiros(s1):
    lisTiros = []
    tiros = s1.find("div", id=["all_stats_shooting"])
    if tiros != None:
        tiros = tiros.find("tbody").find_all("tr")
        if len(tiros) > 4:
            tiros = tiros[-4:]
        for t in tiros:
            t = t.find_all("td")
            if len(t) == 24:
                disparos = Zeros(t[7].text)
                dispararosPuerta = Zeros(t[8].text)
                distanciaTiros = yardMetrosDec(Zeros(t[14].text))
                tirosFalta = Zeros(t[15].text)
                penal = Zeros(t[16].text)
                penalMarcados = Zeros(t[17].text)
                tup =(int(disparos),int(dispararosPuerta),float(distanciaTiros),int(tirosFalta),int(penal),int(penalMarcados))
                lisTiros.append(tup)
    return lisTiros

def pases(s1):
    lisPases = []
    pases = s1.find("div", id=["all_stats_passing"])
    if pases != None:
        pases = pases.find("tbody").find_all("tr")
        if len(pases) > 4:
            pases = pases[-4:]
        for p in pases:
            d = p.find_all("td")
            if len(d) == 29:
                distanciaTotal = yardMetros(Zeros(d[9].text))
                pasesCortosBien = Zeros(d[11].text)
                pasesCortos = Zeros(d[12].text)
                pasesMedioBien = Zeros(d[14].text)
                pasesMedio = Zeros(d[15].text)
                pasesLargosBien = Zeros(d[17].text)
                pasesLargos = Zeros(d[18].text)
                t = (int(distanciaTotal), int(pasesCortosBien), int(pasesCortos), int(pasesMedioBien), int(pasesMedio), int(pasesLargosBien), int(pasesLargos))
                lisPases.append(t)
    return lisPases

def tipoPase(s1):
    lisTipoPase = []
    tipoPases=s1.find("div", id=["all_stats_passing_types"])
    if tipoPases != None:
        tipoPases = tipoPases.find("tbody").find_all("tr")
        if len(tipoPases) > 4:
            tipoPases = tipoPases[-4:]
        for tp in tipoPases:
            d = tp.find_all("td")
            if len(d) == 32:
                conPresion = Zeros(d[11].text)
                centros = Zeros(d[13].text)
                corners = Zeros(d[14].text)
                paseSuelo = Zeros(d[18].text)
                paseBajo = Zeros(d[19].text)
                paseAlto = Zeros(d[20].text)
                paseDercha = Zeros(d[22].text)
                paseIzquierda = Zeros(d[21].text)
                paseCabeza = Zeros(d[23].text)
                paseFueraJuego = Zeros(d[27].text)
                paseFueraCampo = Zeros(d[28].text)
                t = (int(conPresion),int(centros),int(corners),int(paseSuelo),int(paseBajo),int(paseAlto),int(paseDercha),int(paseIzquierda),
                int(paseCabeza),int(paseFueraCampo),int(paseFueraJuego))
                lisTipoPase.append(t)
    return lisTipoPase

def defensa(s1):
    lisDefensa = []
    defensa = s1.find("div", id=["all_stats_defense"])
    if defensa != None:
        defensa = defensa.find("tbody").find_all("tr")
        if len(defensa) > 4:
            defensa = defensa[-4:]
        for df in defensa:
            d = df.find_all("td")
            if len(d) == 30:
                tackles = Zeros(d[6].text)
                tacklesBien = Zeros(d[7].text)
                tacklesDef = Zeros(d[8].text)
                tacklesMed = Zeros(d[9].text)
                tackesAtq = Zeros(d[10].text)
                regates = Zeros(d[12].text)
                regatesTackleados = Zeros(d[11].text)
                presion = Zeros(d[15].text)
                presionBien = Zeros(d[16].text)
                presionDef = Zeros(d[18].text)
                presionMed = Zeros(d[19].text)
                presionAtq = Zeros(d[20].text)
                t = (int(tackles),int(tacklesBien),int(tacklesDef),int(tacklesMed),int(tackesAtq),int(regates),int(regatesTackleados),
                int(presion), int(presionBien),int(presionDef),int(presionMed),int(presionAtq))
                lisDefensa.append(t)
    return lisDefensa

def posesion(s1):
    lisPosesion = []
    posesion = s1.find("div", id=["all_stats_possession"])
    if posesion != None:
        poss = posesion.find("tbody").find_all("tr")
        if len(poss) > 4:
            poss = poss[-4:]
        for ps in poss: 
            p = ps.find_all("td")  
            if len(p) == 31:                
                toques = Zeros(p[6].text)
                toqDefPen = Zeros(p[7].text)
                toqDef = Zeros(p[8].text)
                toqMed = Zeros(p[9].text)
                toqAtq = Zeros(p[10].text)
                toqAtqPen = Zeros(p[11].text)
                dribbles = Zeros(p[14].text)
                dribblesBien = Zeros(p[13].text)
                controles = Zeros(p[18].text)
                distanciaRecorrida = Zeros(yardMetros(p[19].text))
                controlMal = Zeros(p[24].text)
                blancoRecepcion = Zeros(p[26].text)
                recepcionBuena = Zeros(p[27].text)
                t = (toques,toqDefPen,toqDef,toqMed,toqAtq,toqAtqPen, dribbles,dribblesBien,controles,distanciaRecorrida,controlMal,blancoRecepcion,recepcionBuena)
                lisPosesion.append(t)
    return lisPosesion
def misc(s1):
    lisMisc = []
    misc = s1.find("div", id=["all_stats_misc"])
    if misc != None:
        misc = misc.find("tbody").find_all("tr")
        if len(misc) > 4:
            misc = misc[-4:]   
        for m in misc:
            d = m.find_all("td")
            if len(d) == 23:
                amarillas = Zeros(d[6].text)
                rojas = Zeros(d[7].text)
                dobleAmarilla = Zeros(d[8].text)
                faltasCometidas = Zeros(d[9].text)
                faltasRecibidas = Zeros(d[10].text)
                fueraJuego = Zeros(d[11].text)
                penalConcedido = Zeros(d[16].text)
                balonesSueltosRecuperados = Zeros(d[18].text)
                if len(d) < 22:
                    cabezaGanados = "0"
                    cabezaPerdidos = "0"
                else:
                    cabezaGanados = Zeros(d[19].text)
                    cabezaPerdidos = Zeros(d[20].text)
                t=(amarillas,rojas,dobleAmarilla,faltasCometidas,faltasRecibidas,fueraJuego,penalConcedido,balonesSueltosRecuperados,cabezaGanados,cabezaPerdidos)
                lisMisc.append(t)
    return lisMisc

def portero(s1):
    lisPortero = []
    portero = s1.find("div", id=["all_stats_keeper"])
    if portero != None:
        portero = portero.find("tbody").find_all("tr")
        if len(portero) > 4:
            portero = portero[-4:] 
        for p in portero:
            d = p.find_all("td")
            if len(d) == 25:
                golesContra = Zeros(d[9].text)
                dispararosPuertaContra = Zeros(d[11].text)
                dispararosParados = Zeros(d[12].text)
                porteria0 = Zeros(d[17].text)
                penalesMetidos = Zeros(d[20].text)
                penalesParados = Zeros(d[21].text)
                penalesFallados =  Zeros(d[22].text)                
                t=(golesContra,dispararosPuertaContra,dispararosParados,porteria0,penalesMetidos,penalesParados,penalesFallados)
                lisPortero.append(t)
    return lisPortero

def creacion(s1):
    lisCreacion = []
    creacion = s1.find("div", id=["all_stats_gca"])
    if creacion != None:
        creacion = creacion.find("tbody").find_all("tr")
        if len(creacion) > 4:
            creacion = creacion[-4:]
        for c in creacion:
            d = c.find_all("td")
            if len(d) == 23:
                pasesGol = Zeros(d[16].text)
                pasesMuertosGol = Zeros(d[17].text)
                t=(int(pasesGol),int(pasesMuertosGol))
                lisCreacion.append(t)
    return lisCreacion

def tempJuego(s1):
    lisTempJuego = []
    tempJuego = s1.find("div", id=["all_stats_playing_time"])
    if tempJuego != None:
        temp = tempJuego.find("tbody").find_all("tr")
        if len(temp) > 4:
            temp = temp[-4:]
        for t in temp:
            t = t.find_all("td")
            if len(t) == 28:
                completos= Zeros(t[12].text)
                suplente= Zeros(t[13].text)
                tup = (int(completos),int(suplente))
                lisTempJuego.append(tup)
    return lisTempJuego

def estadisticasGenerales(lisGenerales,lisTempJuego,jug):
    if len(lisGenerales)!= 0:
        lisEstd = []
        for l,l1 in zip(lisGenerales, lisTempJuego):
            generales = EstadisticasGenerales.objects.create(partidosJugados= l[2], titular=l[3], partidosCompletos=l1[0],
            entraSuplente=l1[1], goles=l[5], minutosJugados= l[4], asistencias=l[6])
            generales.save()
            tabEstadistica = EstadisticasJugador.objects.create(temporada=l[0], equipo=l[1], jugador=jug, estadisticasGenerales=generales)
            lisEstd.append(tabEstadistica)
        return lisEstd

def estadisticasCreacion(lisCreacion,lisEstd):
    estadistica = []
    if len(lisCreacion) != 0 and len(lisEstd)!= 0:
        lisCr = []       
        for l in lisCreacion:
            crea = EstadisticasCreacion.objects.create(pasesGol= l[0], pasesMuertosGol= l[1])
            crea.save()
            lisCr.append(crea)
        for es,cr in  zip(lisEstd,lisCr):
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasCreacion = cr
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasDefensa(lisDefensa, lisEstd):
    estadistica = []
    if len(lisDefensa) != 0 and len(lisEstd)!= 0:
        lisDef = []
        for l in lisDefensa:
            df = EstadisticasDefensa.objects.create(entradas= l[0], entradasAtaque= l[4], entradasMedio= l[3], entradasDefensa= l[2], entradasGanadas=l[1], presion= l[7]
            , presionAtaque= l[11],presionMedio=l[10], presionGanada=l[8], presionDefensa=l[9], intentoRegate=l[5], regateParado=l[6])
            lisDef.append(df)
            df.save()
        for es,df in  zip(lisEstd,lisDef): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasDefensa = df
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasMisc(lisMisc, lisEstd):
    estadistica = []
    if len(lisMisc) != 0 and len(lisEstd)!= 0:
        lisM = []
        for l in lisMisc:
            m = EstadisticasDiversas.objects.create(balonesAereosGanados= l[8],balonesAereosPerdidos= l[9],amarillas= l[0],balonesSueltosRecuperados= l[7],
            dobleAmarillas= l[2],faltasCometidas= l[3],faltasRecibidas= l[4],fueraJuego= l[5],penaltiesConcedidos= l[6],rojas= l[1])
            lisM.append(m)
            m.save()
        for es,m in  zip(lisEstd,lisM): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasDiversas = m
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasTiros(lisTiros, lisEstd):
    estadistica = []
    if len(lisTiros) != 0 and len(lisEstd)!= 0:
        lisTir = []
        for l in lisTiros:
            tir = EstadisticasTiros.objects.create(distanciaTiros= l[2],penalties= l[4],penaltiesMarcados= l[5], tiros= l[0],tirosFalta= l[3], tirosPorteria= l[1])
            lisTir.append(tir)
            tir.save()
        for es,t in  zip(lisEstd,lisTir): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasTiros = t
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasPortero(lisPortero, lisEstd):
    estadistica = []   
    if len(lisPortero) != 0 and lisEstd != None :
        lisPor = []
        for l in lisPortero:
            por = EstadisticasPortero.objects.create(tirosRecibidos= l[1],cleanSheet= l[3],golesRecibidos= l[0],paradasRecibidos= l[2],
            penaltiesEncajados= l[4],penaltiesFalladosContrario= l[6],penaltiesParados= l[5])
            lisPor.append(por)
            por.save()
        for es,p in  zip(lisEstd,lisPor): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasPortero = p
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasPases(lisPases, lisEstd):
    estadistica = []   
    if len(lisPases) != 0 and len(lisEstd)!= 0:
        lisPas = []
        for l in lisPases:
            pas = EstadisticasPases.objects.create(distanciaPases= l[0],pasesCortos= l[2],pasesCortosEfectivos= l[1],pasesLargos= l[6],
            pasesLargosEfectivos= l[5],pasesMedios= l[4],pasesMediosEfectivos= l[3])
            lisPas.append(pas)
            pas.save()
        for es,p in  zip(lisEstd,lisPas): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasPases = p
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasTipoPase(lisTipoPase, lisEstd):
    estadistica = []   
    if len(lisTipoPase) != 0 and len(lisEstd)!= 0:
        lisTipPas = []
        for l in lisTipoPase:
            tip = EstadisticasTipoPases.objects.create(centros= l[1],conPresion= l[0],cornersLanzados= l[2],paseAlto= l[5],paseBajo= l[4],pasesCabeza= l[8],
            pasesFueraCampo= l[10],pasesFueraJuego= l[9],pasesPieDerecho= l[6],pasesPieIzquierdo= l[7],paseSuelo= l[3])
            lisTipPas.append(tip)
            tip.save()
        for es,p in  zip(lisEstd,lisTipPas): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasTipoPases = p
            estadistica.append(res)
            est.save()
    return estadistica

def estadisticasPosesion(lisPosesion, lisEstd):
    estadistica = []   
    if len(lisPosesion) != 0 and len(lisEstd)!= 0:
        lisPos = []
        for l in lisPosesion:
            pos = EstadisticasRegates.objects.create(balonTocadoAreaPenaltyContr= l[5],balonTocadoAreaPenaltyPropia= l[1],balonTocadoAtaque= l[4],balonTocadoDefensa= l[2]
            ,balonTocadoMedio= l[3],controles= l[8],controlesFallidos= l[10],distanciaPosesion= l[9],pasesObjetivo= l[11],pasesRecibidos= l[12],regates= l[6],regatesCompletados= l[7])
            lisPos.append(pos)
            pos.save()
        for es,p in  zip(lisEstd,lisPos): 
            est = EstadisticasJugador.objects.get(jugador=es.jugador, temporada=es.temporada, id=es.id) 
            res = est.estadisticasRegates = p
            estadistica.append(res)
            est.save()
    return estadistica
    
    
### datos Liga ###
def obtenerLiga(url,url2):
    nl = url.find("h1").string.strip()
    nombreLiga = nl[23:]
    imagen = url.find("div", class_=["media-item logo loader"]).img["src"]
    img = requests.get(imagen)
    nombreImagen = nombreLiga + ".jpg"
    with open("img/ligas/" + nombreImagen, 'wb') as imagen:
        imagen.write(img.content)
    pais = url.find_all("a")[1].text

    tabla = url2.find_all("tr")
    tabla = tabla[1:]

    lg = Liga.objects.create(logo=nombreImagen,nombre=nombreLiga,pais=pais)
    return(tabla,lg)
    
### datos Equipo ###   
def obtenerEquipos(tabla,lg):
    cabezera = "https://fbref.com"
    lis = []
    eqp = []
    for t in tabla:
        res = t.find_all("td")
        r = res[0]
        nombreEquipo = r.find("a").text
        linkEquipo = r.a["href"]
        pjEquipo = int(res[1].text)
        victorias = int(res[2].text)
        empates = int(res[3].text)
        derrotas = int(res[4].text)
        gf = int(res[5].text)
        gc = int(res[6].text)
        ptos = res[8].text
        link = cabezera+linkEquipo      
        r = requests.get(link).text
        r = r[:190000]
        soup = BeautifulSoup(r,"lxml")
        s = soup.find("tbody").find_all("tr")
        escudo = soup.find("div",class_=["media-item"]).img["src"]
        img = requests.get(escudo)
        nombreImagen = nombreEquipo + ".jpg"
        with open("img/equipos/" + nombreImagen, 'wb') as imagen:
            imagen.write(img.content)
        equipo = Equipo.objects.create(nombre=nombreEquipo,derrotas=derrotas, empates= empates , victorias = victorias, puntos= ptos,
        escudo= nombreImagen, golesFavor=gf, golesContra=gc, partidosJugados=pjEquipo,liga=lg)
        lis.append(s)
        eqp.append(equipo)
    return(lis,eqp)

### datos Jugador ###

def datosJugador(res,eqp):
    cabezera = "https://fbref.com"   
    d = res.find_all("td")
    linkJugador = res.find("th").a["href"]
    link = cabezera+linkJugador
    r = requests.get(link).text
    s = BeautifulSoup(r,"lxml").find("div",  id="meta")
    s1 = BeautifulSoup(r, "lxml")
    nombre = s.find("h1").find("span").text
    if s.find("div", class_=["media-item"]) == None:
        nombreImagen = "sinFoto.jpg"
    else:
        fotoJugador = s.img["src"]
        img = requests.get(fotoJugador)
        nombreImagen = nombre + ".jpg"
        with open("img/jugadores/"+ nombreImagen, 'wb') as imagen:
            imagen.write(img.content)
        
    datos = s.find_all("p")
    r = datos[0].text
    pie = "Ambos"
    if "Posición" in r:
        nombreCompleto = nombre
        d1 = datos[0].text.split(":")
        if "Pie" in d1[1]:
            posicion = d1[1][:-16].split("(")[0][:3].replace(" ","")
            dem = d1[1][:-16]
            dem = demarcaciones(dem)
        else:
            posicion = d1[1].split("(")[0][:3].replace(" ","")
            dem = d1[1][:-16]
            dem = demarcaciones(str(dem))
        if len(d1) == 3:
            if "%" in d1[2]: 
                pie = d1[2].split("%")[1][1:-1]
            else:
                pie = d1[2][1:]
        alt = s.find("span", itemprop="height")
        if alt != None:
            altura = alt.text[:-2]
        pess = s.find("span", itemprop="weight")
        if pess != None:
            peso = pess.text[:-2]
        fechaNacimiento = datos[2].find("span")
        if fechaNacimiento != None:
            fechaNacimiento=fechaNacimiento.get("data-birth")
        nacionalidad = s.a.text
    else:
        nombreCompleto = datos[0].text
        d1 = datos[1].text.split(":")
        if len(d1) <= 1:
            d1 = datos[2].text.split(":")
        if "Pie" in d1[1]:
            posicion = d1[1][:-16].split("(")[0][:3].replace(" ","")
            dem = d1[1][:-16]
            dem = demarcaciones(dem)
        else:
            posicion = d1[1].split("(")[0][:3].replace(" ","")
            dem = d1[1][:-16]
            dem = demarcaciones(dem)
        if len(d1) == 3:
            if "%" in d1[2]: 
                pie = d1[2].split("%")[1][1:-1]
            else:
                pie = d1[2][1:]
        alt = s.find("span", itemprop="height")
        if alt != None:
            altura = alt.text[:-2]
        pess = s.find("span", itemprop="weight")
        if pess != None:
            peso = pess.text[:-2]
        fechaNacimiento = datos[3].find("span")
        if fechaNacimiento != None:
            fechaNacimiento=fechaNacimiento.get("data-birth")
        nacionalidad = s.a.text

    if fechaNacimiento != None:
        fn = fechaNacimiento.split("-")
        fn = datetime.date(int(fn[0]),int(fn[1]),int(fn[2]))
        jug = Jugador.objects.create(nombre=nombre , nombreCompleto=nombreCompleto, nacionalidad= nacionalidad, fechaDeNacimiento = fn, 
        altura= altura, peso=peso, pie=pie, posicion = posicion, equipoActual=eqp, foto=nombreImagen, demarcaciones= dem)
    
    return (jug,s1)

def obtenerJugador(s,eqp):      
    for res in s:
        jugador = datosJugador(res,eqp)

        gen = generales(jugador[1])
        tp = tempJuego(jugador[1])
        cr = creacion(jugador[1])
        tir = tiros(jugador[1])
        tpa = tipoPase(jugador[1])
        pas = pases(jugador[1])
        por = portero(jugador[1])
        mis = misc(jugador[1])
        pos = posesion(jugador[1])
        defn = defensa(jugador[1])
        
### estadisticas Jugador ###

        estGen = estadisticasGenerales(gen,tp,jugador[0])
        estPor = estadisticasPortero(por,estGen)
        estDef = estadisticasDefensa(defn,estGen)
        estCreacion = estadisticasCreacion(cr,estGen)
        estMisc = estadisticasMisc(mis,estGen)
        estPas = estadisticasPases(pas,estGen)
        estPos = estadisticasPosesion(pos,estGen)
        estTP = estadisticasTipoPase(tpa,estGen)
        estTiros = estadisticasTiros(tir,estGen)
    

ligas = ["/12/La-Liga-Stats","/9/Premier-League-Stats","/13/Ligue-1-Stats","/11/Serie-A-Stats","/20/Bundesliga-Stats"]

def ScrappingLiga(urlLiga):
    Liga.objects.all().delete()
    res = requests.get(urlLiga).text
    r1 = res[:100000]
    s1 = BeautifulSoup(r1, "lxml").find("div", class_=["comps"])
    r = res[:180000]
    s = BeautifulSoup(r, "lxml").find("table", class_=["stats_table sortable min_width"])
    liga = obtenerLiga(s1,s)
    equipos = obtenerEquipos(liga[0],liga[1])
    for tabla,eq in zip(equipos[0],equipos[1]):
        jugadores = obtenerJugador(tabla,eq)

def Scrapeo(ligas):
    linkEstadisticas = "https://fbref.com/es/comps"
    for l in ligas:
        link = linkEstadisticas+l
        ScrappingLiga(link)

def cargar(request):   
    Scrapeo(["/12/La-Liga-Stats"])
