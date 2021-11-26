import re
from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from datetime import date
from dateutil.relativedelta import relativedelta

from Estadisticas.models import *
from Jugador.models import Jugador
from .serializers import *


    
class estadisticasJugador(APIView):
    def get(self,request, id_jugador):
        jug = EstadisticasJugador.objects.filter(jugador=id_jugador)
        if len(jug) == 0:
            res = []
        else:
            estadisticas = []
            for j in jug:
                gen = EstadisticasGenerales.objects.get(id = j.estadisticasGenerales.id)
                if j.estadisticasDiversas == None:
                    amarillas,rojas = 0,0
                else:
                    misc = EstadisticasDiversas.objects.get(id = j.estadisticasDiversas.id)
                    amarillas,rojas = misc.amarillas,misc.rojas
                if j.jugador.posicion != "PO":
                    est = Estadisticas(temporada=j.temporada,posicion=j.jugador.posicion, equipo= j.equipo, amarillas= amarillas, rojas= rojas, asistencias_cleanSheet= gen.asistencias, pj= gen.partidosJugados,
                    titular= gen.titular, min = gen.minutosJugados, goles_paradas= gen.goles)
                else:
                    if j.estadisticasPortero == None:
                        paradas, cleanSheet = 0,0
                    else:
                        por = EstadisticasPortero.objects.get(id = j.estadisticasPortero.id)
                        paradas, cleanSheet = por.paradasRecibidos,por.cleanSheet
                    est = Estadisticas(temporada=j.temporada,posicion=j.jugador.posicion, equipo= j.equipo, amarillas= amarillas, rojas= rojas, asistencias_cleanSheet=cleanSheet, pj= gen.partidosJugados,
                    titular= gen.titular, min = gen.minutosJugados, goles_paradas = paradas)
                estadisticas.append(est)
                estadisticas.sort(key = lambda x:x.temporada)    
            serializer = EstadisticasJug(estadisticas, many="True")
            res = serializer.data
        return Response(res)

class notasJugador(APIView):
    def get(self,request, id_jugador):

        def corteNota(corte1,corte2,nota,estadistica):
            if nota > 10:
                nota = 10
            if estadistica <= corte1:
                if nota > 5:
                    nota = 5
            elif estadistica <= corte2 and estadistica > corte1:
                if nota > 8:
                    nota = 8
            return round(nota,1)

        def efectividad_goleadora(jug,posicion):
            tiros,tirosPuerta = 0,0
            goles = 0 
            for j in jug:
                goles += j.estadisticasGenerales.goles
                if j.estadisticasTiros == None:
                    tiros,tirosPuerta = 0,0
                else:
                    tiros += j.estadisticasTiros.tiros
                    tirosPuerta += j.estadisticasTiros.tirosPorteria
            if tiros == 0:
                tiros = 1
            if posicion == "DL":
                efectividad =  35 *(goles/tiros) + 0.1 * goles
            elif posicion == "CC":
                efectividad =  40 *(goles/tiros) + 2*(tirosPuerta/tiros) + 0.1 * goles
            else:
                efectividad =  50 *(goles/tiros) + 2*(tirosPuerta/tiros) + 0.2 * goles
            res = corteNota(50,100,efectividad,tiros)
            if res < 3:
                res = 3
            return res
        
        def tiros(jug,posicion):
            tiros,tirosPuerta = 0,0
            goles = 0
            for j in jug:
                goles += j.estadisticasGenerales.goles
                if j.estadisticasTiros == None:
                    tiros += 0
                    tirosPuerta += 0
                else:
                    tiros += j.estadisticasTiros.tiros
                    tirosPuerta += j.estadisticasTiros.tirosPorteria
            if tiros == 0:
                tiros = 1
            if posicion =="DL":
                estadistica =  12*(tirosPuerta/tiros) + 0.05 * (goles)
            elif posicion == "CC":
                estadistica =  13*(tirosPuerta/tiros) + 0.1 * (goles)
            else:
                estadistica =  15*(tirosPuerta/tiros) + 0.3 * (goles)
            res = corteNota(70,150,estadistica,tiros)
            return res
        
        def pases(jug,posicion):
            pasesCortosBien,pasesCortos,pasesMediosBien,pasesMedios,pasesLargosBien,pasesLargos = 0,0,0,0,0,0
            for j in jug:
                if j.estadisticasPases != None:
                    pasesCortosBien += j.estadisticasPases.pasesCortosEfectivos
                    pasesCortos += j.estadisticasPases.pasesCortos
                    pasesMediosBien += j.estadisticasPases.pasesMediosEfectivos
                    pasesMedios += j.estadisticasPases.pasesMedios
                    pasesLargosBien += j.estadisticasPases.pasesLargosEfectivos
                    pasesLargos += j.estadisticasPases.pasesLargos
                    
            if pasesCortos==0:
                pasesCortos = 1
            if pasesMedios==0:
                pasesMedios = 1
            if pasesLargos==0:
                pasesLargos = 1
            
            if posicion == "DL":
                cortos = 9.25*(pasesCortosBien+pasesMediosBien/pasesCortos+pasesMedios) + 0.0005 * pasesCortos + 0.0005 * pasesMedios
                largos = 10*(pasesLargosBien+0.5*(pasesMediosBien)/pasesLargos +0.5*(pasesMediosBien)) + 0.0015 * pasesLargos + 0.0005 * pasesMedios
            if posicion == "CC":
                cortos = 8.5*(pasesCortosBien+pasesMediosBien/pasesCortos+pasesMedios) + 0.0004 * pasesCortos + 0.0004 * pasesMedios
                largos = 10*(pasesLargosBien+0.5*(pasesMediosBien)/pasesLargos +0.5*(pasesMediosBien)) + 0.001 * pasesLargos + 0.0004 * pasesMedios
            else:
                cortos = 8*(pasesCortosBien+pasesMediosBien/pasesCortos+pasesMedios) + 0.00035 * pasesCortos + 0.00035 * pasesMedios
                largos = 10*(pasesLargosBien+0.5*(pasesMediosBien)/pasesLargos +0.5*(pasesMediosBien)) + 0.001 * pasesLargos + 0.0003 * pasesMedios

            c = corteNota(800,3000,cortos,pasesCortos)
            l = corteNota(400,1000,largos,pasesLargos)
            return c,l

        def entradas(jug):
            entradas,entradasBien = 0,0
            for j in jug:
                if j.estadisticasDefensa != None:
                    entradas += j.estadisticasDefensa.entradas
                    entradasBien += j.estadisticasDefensa.entradasGanadas
            if entradas == 0:
                entradas = 1
            entr = 10*(entradasBien/entradas) + 0.025 * entradas
            res = corteNota(200,600,entr,entradas)
            return res

        def presion(jug):
            presion,presionGanada = 0,0
            for j in jug:
                if j.estadisticasDefensa != None:
                    presion += j.estadisticasDefensa.presion
                    presionGanada += j.estadisticasDefensa.presionGanada
            if presion == 0:
                presion = 1
            pr = 15*(presionGanada/presion) + 0.002 * presion
            res = corteNota(150,400,pr,presion)
            return res

        def para_regates(jug):
            regates,regatesParados = 0,0
            for j in jug:
                if j.estadisticasDefensa != None:
                    regates += j.estadisticasDefensa.intentoRegate
                    regatesParados += j.estadisticasDefensa.regateParado
            if regates == 0:
                regates = 1
            reg = 12 * (regatesParados/regates) + 0.01 * regatesParados
            res = corteNota(50,150,reg,regates)
            return res

        def regates(jug):
            regates,regatesBien = 0,0
            for j in jug:
                if j.estadisticasRegates!=None:
                    regates += j.estadisticasRegates.regates
                    regatesBien += j.estadisticasRegates.regatesCompletados
            if regates == 0:
                regates = 1
            reg = 10 * (regatesBien/regates) + 0.01 * regatesBien
            res = corteNota(40,130,reg,regates)
            return res

        def controles(jug,posicion):
            controles,controlesMal = 0,0
            for j in jug:
                if j.estadisticasRegates != None:
                    controles += j.estadisticasRegates.controles
                    controlesMal += j.estadisticasRegates.controlesFallidos
            controlesMal =100 * controlesMal
            total = controles + controlesMal 
            if total == 0:
                total = 1
            if posicion == "DL":
                ctr = 15*(controles/total) + 0.002 * controles
            elif posicion == "CC":
                ctr = 10*(controles/total) + 0.001 * controles
            else:
                ctr = 10*(controles/total) + 0.0005 * controles
            res = corteNota(800,1700,ctr,controles)
            if res < 3:
                res = 3
            return res

        def balones_aereos(jug):
            ganados, total, minutos,pasesCabeza = 0,0,0,0
            for j in jug:
                minutos += j.estadisticasGenerales.minutosJugados
                if j.estadisticasRegates != None:
                    g = j.estadisticasDiversas.balonesAereosGanados
                    ganados += g
                    total += j.estadisticasDiversas.balonesAereosPerdidos + g
                if j.estadisticasTipoPases != None:
                    pasesCabeza += j.estadisticasTipoPases.pasesCabeza
            if total == 0:
                total = 1
            aereo = 10 * (ganados/total) + 0.01 * ganados + 0.01 * pasesCabeza
            res = corteNota(1000,3000,aereo,minutos)
            if res < 3:
                res = 3
            return res

        def temperamento(jug):
            amarillas, rojas, dobleAmarillas, minutos = 0,0,0,0
            for j in jug:
                minutos += j.estadisticasGenerales.minutosJugados
                if j.estadisticasRegates != None:
  
                    amarillas += j.estadisticasDiversas.amarillas
                    rojas += j.estadisticasDiversas.rojas
                    dobleAmarillas += j.estadisticasDiversas.dobleAmarillas
            temp = 10 - (amarillas * 0.25 - dobleAmarillas * 0.5 - rojas* 0.75) 
            res = corteNota(2000,5000,temp,minutos)
            return res


        def recuperaciones(jug,posicion):
            recuperaciones,minutos = 0,0
            for j in jug:
                minutos += j.estadisticasGenerales.minutosJugados
                if j.estadisticasDiversas== None:
                    recuperaciones += 0
                else:
                    recuperaciones += j.estadisticasDiversas.balonesSueltosRecuperados
                if minutos == 0:
                    minutos=1
                if posicion == "DF":
                    recup = 60*(recuperaciones)/minutos + 0.0005 * recuperaciones
                elif posicion == "CC":
                    recup = 75*(recuperaciones)/minutos + 0.001 * recuperaciones
                else:
                    recup = 85*(recuperaciones)/minutos + 0.003 * recuperaciones
                if recup < 3:
                    recup = 3
                res = corteNota(1000,3000,recup,minutos)
            return res
        
        def portero(jug):
            paradas,tirosRecibidos,golesEncajados,minutos = 0,0,0,0
            for j in jug:
                minutos += j.estadisticasGenerales.minutosJugados
                if j.estadisticasPortero != None:
                    por = j.estadisticasPortero
                    paradas += por.paradasRecibidos
                    tirosRecibidos += por.tirosRecibidos
                    golesEncajados += por.golesRecibidos
            if tirosRecibidos != 0 and minutos != 0 :
                par = 10*(paradas/tirosRecibidos) + 0.001 * paradas
                encj = 8 * (minutos/(golesEncajados*90)) + 0.001 * paradas
                res1 = corteNota(60,180,par,tirosRecibidos)
                res2 = corteNota(1000,3000,encj,minutos)
            else:
                res1,res2 = 0,0
            return res1,res2

        try:    
            jug = EstadisticasJugador.objects.filter(jugador=id_jugador)
            j = Jugador.objects.get(id=id_jugador)
            posicion = j.posicion
            pas = pases(jug,posicion)
            por = portero(jug)
            notas = Notas(efectividad=efectividad_goleadora(jug,posicion),tiros=tiros(jug,posicion),pasesCortos=pas[0],pasesLargos=pas[1],entradas=entradas(jug),presion= presion(jug),
            paraRegates= para_regates(jug),regates=regates(jug),controles=controles(jug,posicion),balonesAereos=balones_aereos(jug),temperamento=temperamento(jug),recuperaciones=recuperaciones(jug,posicion),
            paradas = por[0],sinGoles = por[1])
            serializer = NotasSerializar([notas], many=True)
            res = serializer.data
            return Response(res)
        except:
          return Response({"mensaje":"No existe dicho jugador"},status=status.HTTP_400_BAD_REQUEST)


class caracteristicasJugador(APIView):

    def calcularEdad(self,fecha_nacimiento):
 
        edad = date.today().year - fecha_nacimiento.year
        cumpleanios = fecha_nacimiento + relativedelta(years=edad)
    
        if cumpleanios > date.today():
            edad = edad - 1
    
        return edad

    def get(self,request,id_jugador):

        try:
            lis = []
            jug = EstadisticasJugador.objects.filter(jugador=id_jugador)
            jugador = Jugador.objects.get(id=id_jugador)

            partidosJugados,titular,entraSuplente,goles,minutosJugados,asistencias,distanciaTiros,tirosFalta,penalties,penaltiesMarcados,fueraJuego,tiros_puerta = 0,0,0,0,0,0,0,0,0,0,0,0
            pasesPieDerecho,pasesPieIzquierdo,cornersLanzados,presionAtaque,presionMedio,presionDefensa,recuperaciones,balonesAereosGanados,balonesAereosPerdidos = 0,0,0,0,0,0,0,0,0
            amarillas,rojas,dobleAmarillas,faltasRecibidas,faltasCometidas,golesRecibidos,cleanSheet,penaltiesEncajados,penaltiesParados,penaltiesFalloContraio,penaltiesConcedidos = 0,0,0,0,0,0,0,0,0,0,0
            centros,pasesCortos,pasesCortosEfectivos,reg,controles,entradas,entradasGanadas = 0,0,0,0,0,0,0
                
            for j in jug:

                generales,tiros,diversas,portero,defensa,regates,tipoPase,pases = j.estadisticasGenerales,j.estadisticasTiros,j.estadisticasDiversas,j.estadisticasPortero,j.estadisticasDefensa,j.estadisticasRegates,j.estadisticasTipoPases,j.estadisticasPases
                
                if generales != None:
                    goles += generales.goles
                    partidosJugados += generales.partidosJugados
                    titular += generales.titular
                    entraSuplente += generales.entraSuplente
                    minutosJugados += generales.minutosJugados
                    asistencias += generales.asistencias
                
                if regates != None:
                    reg += regates.regatesCompletados
                    controles += regates.controles

                if tiros != None:
                    distanciaTiros += tiros.distanciaTiros
                    tirosFalta += tiros.tirosFalta
                    penalties += tiros.penalties
                    penaltiesMarcados += tiros.penaltiesMarcados
                    tiros_puerta += tiros.tirosPorteria
                
                if tipoPase != None:
                    pasesPieDerecho += tipoPase.pasesPieDerecho
                    pasesPieIzquierdo += tipoPase.pasesPieIzquierdo
                    cornersLanzados += tipoPase.cornersLanzados
                    centros += tipoPase.centros
                
                if pases != None:
                    pasesCortos += pases.pasesCortos
                    pasesCortosEfectivos += pases.pasesCortosEfectivos

                if defensa != None:
                    presionAtaque += defensa.presionAtaque
                    presionMedio += defensa.presionMedio
                    presionDefensa += defensa.presionDefensa
                    entradas += defensa.entradas
                    entradasGanadas += defensa.entradasGanadas
                    

                if diversas != None:
                    balonesAereosGanados += diversas.balonesAereosGanados
                    balonesAereosPerdidos += diversas.balonesAereosPerdidos
                    amarillas += diversas.amarillas
                    rojas += diversas.rojas
                    dobleAmarillas += diversas.dobleAmarillas
                    faltasRecibidas += diversas.faltasRecibidas
                    faltasCometidas += diversas.faltasCometidas
                    penaltiesConcedidos += diversas.penaltiesConcedidos
                    fueraJuego += diversas.fueraJuego
                    recuperaciones += diversas.balonesSueltosRecuperados

                if portero != None:    
                    golesRecibidos += portero.golesRecibidos
                    cleanSheet += portero.cleanSheet
                    penaltiesEncajados += portero.penaltiesEncajados
                    penaltiesParados += portero.penaltiesParados
                    penaltiesFalloContraio += portero.penaltiesFalladosContrario
            
            if rojas + dobleAmarillas >=4:
                expulsiones = "Expulsado con frecuencia"
                lis.append(expulsiones)
            
            if amarillas >= 15:
                lis.append("Recibe muchas amarillas")

            if asistencias >= 16:
                asistente = "Asistente"
                lis.append(asistente)
            
            if centros >= 200:
                lis.append("Centrador")

            if pasesCortos>=1:
                if jugador.posicion == "CC" and pasesCortos>1800 and pasesCortosEfectivos/pasesCortos >= 0.88:
                    lis.append("Pase al pie")

            if presionDefensa >= 1:
                if jugador.posicion == "DF" and (presionAtaque + 0.5*presionMedio)/(presionDefensa)>= 0.8:
                    lis.append("Ofensivo")
            
            if presionAtaque >= 1:
                if jugador.posicion == "DL" and (presionDefensa + 0.5*presionMedio)/(presionAtaque)>= 0.9:
                    lis.append("Ayuda en defensa")

            if goles >= 20:
                goleador = "Goleador"
                lis.append(goleador)

            if reg >= 150:
                lis.append("Regateador")

            if recuperaciones >= 800:
                lis.append("Recuperaciones")

            if entradas >=1:
                if entradasGanadas/entradas >= 0.7 and entradas >= 150:
                    lis.append("Entradas")
            
            if jugador.posicion == "PO":
                if goles >= 1:
                    lis.append("Portero goleador")
                if pasesCortosEfectivos >= 500 and controles >= 1000:
                    lis.append("Habilidoso con los pies")

            if jugador.altura:
                if jugador.posicion == "PO" and jugador.altura >= 190:
                    alto = "Alto"
                    lis.append(alto)

                if jugador.posicion != "PO" and jugador.altura >= 186:
                    alto = "Alto"
                    lis.append(alto)

            if jugador.fechaDeNacimiento!=None:
                edad = self.calcularEdad(jugador.fechaDeNacimiento)
                if edad >= 33:
                    lis.append("Jugador veterano")
                if edad <= 19 and partidosJugados>=10:
                    lis.append("Joven Promesa")

            if tirosFalta >=15: 
                lis.append("Lanzador de Faltas Cercanas")

            if penalties >= 8:
                lis.append("Lanzador de penalties")

            if penaltiesMarcados >=1:
                if penalties/penaltiesMarcados >= 0.85 and penalties >= 5:
                    lis.append("Especialista desde los 11 metros")

            if cornersLanzados >= 30:
                lis.append("Lanzador de corners")

            if faltasRecibidas >= 130:
                lis.append("Recibe muchas faltas")

            if faltasCometidas >= 150:
                lis.append("Realiza muchas faltas")

            if distanciaTiros >= 26 and goles >= 5 and tiros_puerta >= 30:
                lis.append("Tirador lejano")
            
            if penaltiesConcedidos >= 4:
                lis.append ("Provoca muchos penalties")
            
            if fueraJuego >= 80:
                lis.append ("Cae mucho en fuera de juego")

            if partidosJugados >= 1:
                if jugador.posicion == "PO":
                    if partidosJugados >= 30 and cleanSheet/partidosJugados >= 0.35:
                        lis.append("Portería a cero")
                    if partidosJugados >= 30 and golesRecibidos/partidosJugados <= 1:
                        lis.append("Recibe pocos goles")
                    if partidosJugados >= 30 and golesRecibidos/partidosJugados >= 1.5:
                        lis.append("Recibe muchos goles")

                if titular >= 100 and titular/partidosJugados >= 0.95:
                    titu = "Titular"
                    lis.append(titu)
                if partidosJugados >= 60 and entraSuplente/partidosJugados >= 0.4:
                    revulsivo = "Revulsivo"
                    lis.append(revulsivo)

            penalties_total =  penaltiesEncajados + penaltiesParados + penaltiesFalloContraio
            if penalties_total >=1:
                if penalties_total >= 5 and (2*penaltiesParados + penaltiesFalloContraio)/(penalties_total)>= 0.5:
                    lis.append("Para penalties")

            caracteristicas = Caracteristicas(caracteristicas=lis)
            serializer = CaracteristicasSerializar([caracteristicas],many=True)
            res = serializer.data
            return Response(res)
        except:
           return Response({"mensaje":"No existe dicho jugador"},status=status.HTTP_400_BAD_REQUEST)
