from random import*
from time import*
from math import*
from copy import*
import sys, termios

#variables globales
matriz_2048 = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#-----------------------------------------------------------------------
matrizjug1=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
matrizjug2=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
#-----------------------------------------------------------------------
matriz_ceros, matrizPasada, matrizPasada2, historial_tableros, historial_movimientos, puntajesAltos = [],[],[],[],[],[]
baseColor=17
mov,ultimaPartida,ultimoPunteo="","",""
Punteo, punteoTemp=0,0
#-----------------------------------------------------------------------
jugador1=0
jugador2=0
historial_movimientos1=[]
historial_movimientos2=[]
pedirnombre=""
pedirnombre2=""
#------------------------------------------------------------------------
#es un procedimiento que imprime la matriz 2048, no necesita argumentos
def print_matriz():
  global matriz_ceros
  print('\x1bc')
  print("\t  Mejor Punteo:",puntajesAltos[0])
  print("Movimientos: {:^5}\tPuntos: {:^6}".format(len(historial_movimientos), Punteo))
  print("\t┌────┬────┬────┬────┐")
  for fila in matriz_2048:
    print("\t",end="")
    for val in fila:
      if val==0:
        val=" "
        print ("│ ",val, end=" ")
      else:
        color=3*(int(log2(val)))+baseColor
        print('│\033[48;5;{}m{:^4}\033[0;0m'.format(color,val), end="")
    print("│\n\t├────┼────┼────┼────┤")
  print ("\033[A         \033[A")
  print("\t└────┴────┴────┴────┘")
  historial_tableros.append(deepcopy(matriz_2048))
  matriz_ceros=[]

def print_historial():
  vel=TomarValor("Velocidad de reproduccion: ")
  contador=0
  totalMov=len(historial_movimientos)
  historial_movimientos.append("")
  for tablero in historial_tableros:
    try:
      sleep(1.5/int(vel))
    except:
      if contador==0: print("valor no valido, utilizando velocidad estandar...")
      sleep(1.5)
    print("\x1bc\n\t movimientos:",contador,"/",totalMov)
    print("\t┌────┬─ ∘°❉°∘ ─┬────┐")
    for fila in tablero:
      print("\t",end="")
      for val in fila:
        if val==0:
          val=" "
          print ("│ ",val, end=" ")
        else:
          color=3*(int(log2(val)))+baseColor
          print('│\033[38;5;{}m{:^4}\033[0;0m'.format(color,val), end="")
      print("│\n\t├────┼────┼────┼────┤")
    print ("\033[A         \033[A")
    print("\t└────┴────┴────┴────┘")
    if contador==0:pass
    else:print("\t {:^20}".format(historial_movimientos[contador-1]))
    contador+=1
  historial_movimientos.pop()
  sleep(4)
  print('\x1bc')
  
#busca un numero y actualiza la matriz ceros con la lista de los numeros
def buscar(num):
  contadorFila=0
  contadorPos=0
  for fila in matriz_2048:
    for val in fila:
      val=int(round(val,0))
      matriz_2048[contadorFila][contadorPos]=val
      if val==num:
        pos=[contadorFila,contadorPos]
        matriz_ceros.append(pos)
      contadorPos+=1
    contadorPos=0
    contadorFila+=1
  if len(matriz_ceros)==0: ver_si_perdio()

def nuevo_num():
  #Mando a llamar el ver_si_perdio() cuando se llene el tablero
  random=randint(0,len(matriz_ceros)-1)
  if randint(1,8) <= 2: num_random = 4
  else: num_random = 2
  matriz_2048[matriz_ceros[random][0]][matriz_ceros[random][1]]=num_random  

def ver_si_perdio():
  try:
    contadorFila=0
    contadorPos=0
    for fila in matriz_2048:
      izquierda=1
      arriba=1
      for val in fila:
        try:
          derecha=matriz_2048[contadorFila][contadorPos+1]
          # print("\tA la derecha:",derecha,end="")
        except:
          derecha=1
        try:
          if contadorPos-1>=0:
            izquierda=matriz_2048[contadorFila][contadorPos-1]
            # print("\tA la izquierda:",izquierda,end="")
        except:
          None
        try:
          if contadorFila-1>=0:
            arriba=matriz_2048[contadorFila-1][contadorPos]
            # print("\tArriba:",arriba,end="")
        except:
          None
        try:
          abajo=matriz_2048[contadorFila+1][contadorPos]
          # print("\tAbajo:",abajo,end="")
        except:
          abajo=1
        # print ("\n",val,"en la pos",contadorFila,contadorPos)
        # print("\t\tValores junto: ",izquierda,derecha,arriba,abajo,"\n")
        if val==izquierda or val==derecha or val==arriba or val==abajo:
          # print("HAY POSIBILIDAD\n\n")
          raise Exception()
        contadorPos+=1
      contadorPos=0
      contadorFila+=1
  except:
    None
  else:
    raise Exception()

def mover(direccion,orientazion):
  global Punteo
  comb=False
  if orientazion=="vertical":
    direccionCicloV=direccion
    direccionV=direccion
    if direccion<0: 
      indiceV1=2 
      indiceV2=direccionV
    else:
      indiceV1=direccionV
      indiceV2=4
    indiceH1=0
    indiceH2=4
    direccionH=0
    direccionCicloH=1
  if orientazion=="horizontal":
    direccionCicloH=direccion
    direccionH=direccion
    if direccion<0: 
      indiceH1=2 
      indiceH2=direccionH
    else:
      indiceH1=direccionH
      indiceH2=4
    indiceV1=0
    indiceV2=4
    direccionV=0
    direccionCicloV=1
  for fila in range(indiceV1,indiceV2,direccionCicloV):
    for columna in range(indiceH1,indiceH2,direccionCicloH):
      actual=matriz_2048[fila][columna]
      anterior=matriz_2048[fila-direccionV][columna-direccionH]
      # print("actual:",actual,"comparado con:",anterior)
      if actual==0: pass
      elif actual==anterior:
        Punteo+=int(actual*2)
        if Punteo>int(puntajesAltos[0]):
          puntajesAltos[0]=Punteo
        anterior+=actual+(2*columna+3*fila+5)/111
        actual=0
        matriz_2048[fila][columna]=actual
        matriz_2048[fila-direccionV][columna-direccionH]=anterior
        if anterior>=2048:
          buscar(0)
          print_matriz()
          raise TypeError("!!!GANASTE!!!")
        comb=True
      elif anterior==0:
        # print("se mueve pero no match")
        anterior+=actual
        actual=0
        matriz_2048[fila][columna]=actual
        matriz_2048[fila-direccionV][columna-direccionH]=anterior
        comb=True
    if comb==True: mover(direccion, orientazion)
    comb=False

def TomarValor(frase):
  print(frase)
  datosArchivo = sys.stdin.fileno()
  valoresOriginales = termios.tcgetattr(datosArchivo)
  
  nuevosVal = termios.tcgetattr(datosArchivo)
  nuevosVal[3] = nuevosVal[3] & ~termios.ICANON
  nuevosVal[6][termios.VMIN] = 1
  nuevosVal[6][termios.VTIME] = 0
  
  try:
    termios.tcsetattr(datosArchivo, termios.TCSAFLUSH, nuevosVal)
    tecla=sys.stdin.read(1)
    print ("\n\033[A                             \033[A")
    
    if tecla == "\x1b": 
      tecla += sys.stdin.read(2)
      if   tecla == "\x1b[A": return "w"
      elif tecla == "\x1b[B": return "s"
      elif tecla == "\x1b[C": return "d"
      elif tecla == "\x1b[D": return "a"
      
    else:                     return tecla.lower()
  finally:
    termios.tcsetattr(datosArchivo, termios.TCSAFLUSH, valoresOriginales)
  
def movimiento():
  global matriz_2048, matrizPasada, mov, ultimaPartida, ultimoPunteo, Punteo, punteoTemp
  while True:
    mov=TomarValor("Ingrese un movimiento (w/a/s/d)")
    print ("\n\033[2A                                   \033[A")
    if   mov == "w" or mov=="8":
      punteoTemp=Punteo
      mover(1,"vertical")
      buscar(0)    
      if matrizPasada==matriz_2048: None
      else:  
        historial_movimientos.append("Hacia arriba")
        break
    elif mov == "s" or mov=="2":
      punteoTemp=Punteo
      mover(-1,"vertical")
      buscar(0)    
      if matrizPasada==matriz_2048: None
      else:  
        historial_movimientos.append("Hacia abajo")
        break
    elif mov == "a" or mov=="4":
      punteoTemp=Punteo
      mover(1,"horizontal")
      buscar(0)    
      if matrizPasada==matriz_2048: None
      else:  
        historial_movimientos.append("Hacia la izquierda")
        break
    elif mov == "d" or mov=="6":
      punteoTemp=Punteo
      mover(-1,"horizontal")
      buscar(0)    
      if matrizPasada==matriz_2048: None
      else:  
        historial_movimientos.append("Hacia la derecha")
        break
    elif mov=="q":
      print("Seguro quieres salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="g":
      ultimaPartida=deepcopy(matriz_2048)
      print("Guardar y salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        ultimoPunteo=Punteo
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="e":
      Punteo=punteoTemp
      historial_movimientos.append("Retoceder movimiento") 
      buscar(0)    
      break

def recopilador():
  global puntajesAltos, ultimaPartida, ultimoPunteo
  lineas=[]
  archivo=open("ValoresImportantes.txt")
  for linea in archivo:
    lineas.append(linea.strip())
  puntajesAltos=[lineas[1],lineas[2],lineas[3]]
  ultimaPartida=lineas[-2].strip()
  ultimoPunteo=lineas[-1]

def juego_2048():
  print('\033[?25l', end="")
  try:
    global matrizPasada, matrizPasada2, matriz_2048
    recopilador()
    buscar(0)
    nuevo_num()
    nuevo_num()
    print_matriz()
    while True:
      matrizPasada2=deepcopy(matrizPasada)
      matrizPasada=deepcopy(matriz_2048)
      movimiento()
      nuevo_num()
      print_matriz()
      if mov=="e":
        historial_tableros.pop()
        print(matrizPasada2)
        matriz_2048=deepcopy(matrizPasada2)
        print_matriz()
  except TypeError as stopper:
    print(stopper)
    
  except:
    print("\n\nSe acabo el juego! :(\n\n")
    if len(historial_movimientos)>3:
      print("Deseas ver una reproduccion de la partida? y/n")
      while True:
          confirmacion=TomarValor("\033[A")
          if confirmacion=="y":
            print_historial()
            break
          elif confirmacion=="n":
            break
    print("Saliendo...")
    for i in range(0,3):
      if Punteo>int(puntajesAltos[i]):
       puntajesAltos.insert(i, Punteo)
       puntajesAltos.pop()
       break
      elif Punteo==int(puntajesAltos[i]):
        break
    sleep(2.5)
    print("\x1bc")

def guardar():
  global puntajesAltos, ultimaPartida, ultimoPunteo
  archivo=open("ValoresImportantes.txt", "w")
  archivo.write("Tres mejores puntuaciones:\n")
  for linea in puntajesAltos:
    archivo.write(str(linea)+"\n")
  archivo.write("\nContinuar partida:\n")
  archivo.write(str(ultimaPartida)+"\n")
  archivo.write(str(ultimoPunteo))
  archivo.close()


#----------------Funciones para el jugador vs jugador--------------------
#----------------------------Jugador1------------------------------------
def print_matrizjug1():
  global matriz_ceros
  global matrizjug1
  global pedirnombre
  print('\x1bc')
  print("\t\t\t",pedirnombre)
  print("\t  Mejor Punteo:",puntajesAltos[0])
  print("Movimientos: {:^5}\tPuntos: {:^6}".format(len(historial_movimientos1), jugador1))
  print("\t┌────┬────┬────┬────┐")
  for fila in matrizjug1:
    print("\t",end="")
    for val in fila:
      if val==0:
        val=" "
        print ("│ ",val, end=" ")
      else:
        color=3*(int(log2(val)))+baseColor
        print('│\033[48;5;{}m{:^4}\033[0;0m'.format(color,val), end="")
    print("│\n\t├────┼────┼────┼────┤")
  print ("\033[A         \033[A")
  print("\t└────┴────┴────┴────┘")
  historial_tableros.append(deepcopy(matrizjug1))
  matriz_ceros=[]

def buscar1(num):
  contadorFila=0
  contadorPos=0
  for fila in matrizjug1:
    for val in fila:
      val=int(round(val,0))
      matrizjug1[contadorFila][contadorPos]=val
      if val==num:
        pos=[contadorFila,contadorPos]
        matriz_ceros.append(pos)
      contadorPos+=1
    contadorPos=0
    contadorFila+=1
  if len(matriz_ceros)==0: ver_si_perdio1()

def nuevo_num1():
  random=randint(0,len(matriz_ceros)-1)
  if randint(1,8) <= 2: num_random = 4
  else: num_random = 2
  matrizjug1[matriz_ceros[random][0]][matriz_ceros[random][1]]=num_random  

def ver_si_perdio1():
  try:
    contadorFila=0
    contadorPos=0
    for fila in matrizjug1:
      izquierda=1
      arriba=1
      for val in fila:
        try:
          derecha=matrizjug1[contadorFila][contadorPos+1]
        except:
          derecha=1
        try:
          if contadorPos-1>=0:
            izquierda=matrizjug1[contadorFila][contadorPos-1]
        except:
          None
        try:
          if contadorFila-1>=0:
            arriba=matrizjug1[contadorFila-1][contadorPos]
        except:
          None
        try:
          abajo=matrizjug1[contadorFila+1][contadorPos]
        except:
          abajo=1
        if val==izquierda or val==derecha or val==arriba or val==abajo:
          raise Exception()
        contadorPos+=1
      contadorPos=0
      contadorFila+=1
  except:
    None
  else:
    raise Exception()

def mover1(direccion,orientazion):
  global jugador1
  comb=False
  if orientazion=="vertical":
    direccionCicloV=direccion
    direccionV=direccion
    if direccion<0: 
      indiceV1=2 
      indiceV2=direccionV
    else:
      indiceV1=direccionV
      indiceV2=4
    indiceH1=0
    indiceH2=4
    direccionH=0
    direccionCicloH=1
  elif orientazion=="horizontal":
    direccionCicloH=direccion
    direccionH=direccion
    if direccion<0: 
      indiceH1=2 
      indiceH2=direccionH
    else:
      indiceH1=direccionH
      indiceH2=4
    indiceV1=0
    indiceV2=4
    direccionV=0
    direccionCicloV=1
  for fila in range(indiceV1,indiceV2,direccionCicloV):
    for columna in range(indiceH1,indiceH2,direccionCicloH):
      actual=matrizjug1[fila][columna]
      anterior=matrizjug1[fila-direccionV][columna-direccionH]
      if actual==0: pass
      elif actual==anterior:
        jugador1+=int(actual*2)
        if jugador1>int(puntajesAltos[0]): puntajesAltos[0]=jugador1
        anterior+=actual+(2*columna+3*fila+5)/111
        actual=0
        matrizjug1[fila][columna]=actual
        matrizjug1[fila-direccionV][columna-direccionH]=anterior
        if anterior>=2048:
          buscar1(0)
          print_matrizjug1()
          raise TypeError("!!!GANASTE!!!")
        comb=True
      elif anterior==0:
        anterior+=actual
        actual=0
        matrizjug1[fila][columna]=actual
        matrizjug1[fila-direccionV][columna-direccionH]=anterior
        comb=True
    if comb==True: mover1(direccion, orientazion)
    comb=False

def movimiento1():
  global matrizjug1, matrizPasada, mov, ultimaPartida, ultimoPunteo, jugador1, punteoTemp
  while True:
    mov=TomarValor("Ingrese un movimiento (w/a/s/d)")
    print ("\n\033[2A                                   \033[A")
    if mov == "w" or mov=="8":
      punteoTemp=jugador1
      mover1(1,"vertical")
      buscar1(0)    
      if matrizPasada==matrizjug1: None
      else:  
        historial_movimientos1.append("Hacia arriba")
        break
    elif mov == "s" or mov=="2":
      punteoTemp=jugador1
      mover1(-1,"vertical")
      buscar1(0)    
      if matrizPasada==matrizjug2: None
      else:  
        historial_movimientos1.append("Hacia abajo")
        break
    elif mov == "a" or mov=="4":
      punteoTemp=jugador1
      mover1(1,"horizontal")
      buscar1(0)    
      if matrizPasada==matrizjug1: None
      else:  
        historial_movimientos1.append("Hacia la izquierda")
        break
    elif mov == "d" or mov=="6":
      punteoTemp=jugador1
      mover1(-1,"horizontal")
      buscar1(0)    
      if matrizPasada==matrizjug1: None
      else:  
        historial_movimientos1.append("Hacia la derecha")
        break
    elif mov=="q":
      print("Seguro quieres salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="g":
      ultimaPartida=deepcopy(matrizjug1)
      print("Guardar y salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        ultimoPunteo=jugador1
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="e":
      jugador1=punteoTemp
      historial_movimientos1.append("Retoceder movimiento") 
      buscar1(0)    
      break
#------------------------------------------------------------------------
#---------------------------------jugador2-------------------------------
def print_matrizjug2():
  matriz_ceros=[]
  global matrizjug2
  global pedirnombre2
  print('\x1bc')
  print("\t\t\t",pedirnombre2)
  print("\t  Mejor Punteo:",puntajesAltos[0])
  print("Movimientos: {:^5}\tPuntos: {:^6}".format(len(historial_movimientos2), jugador2))
  print("\t┌────┬────┬────┬────┐")
  for fila in matrizjug2:
    print("\t",end="")
    for val in fila:
      if val==0:
        val=" "
        print ("│ ",val, end=" ")
      else:
        color=3*(int(log2(val)))+baseColor
        print('│\033[48;5;{}m{:^4}\033[0;0m'.format(color,val), end="")
    print("│\n\t├────┼────┼────┼────┤")
  print ("\033[A         \033[A")
  print("\t└────┴────┴────┴────┘")
  historial_tableros.append(deepcopy(matrizjug2))
  matriz_ceros=[]

def buscar2(num):
  global matriz_ceros
  contadorFila=0
  contadorPos=0
  for fila in matrizjug2:
    for val in fila:
      val=int(round(val,0))
      matrizjug2[contadorFila][contadorPos]=val
      if val==num:
        pos=[contadorFila,contadorPos]
        matriz_ceros.append(pos)
      contadorPos+=1
    contadorPos=0
    contadorFila+=1
  if len(matriz_ceros)==0: ver_si_perdio2()

def nuevo_num2():
  random=randint(0,len(matriz_ceros)-1)
  if randint(1,8) <= 2: num_random = 4
  else: num_random = 2
  matrizjug2[matriz_ceros[random][0]][matriz_ceros[random][1]]=num_random  

def ver_si_perdio2():
  try:
    contadorFila=0
    contadorPos=0
    for fila in matrizjug2:
      izquierda=1
      arriba=1
      for val in fila:
        try:
          derecha=matrizjug2[contadorFila][contadorPos+1]
        except:
          derecha=1
        try:
          if contadorPos-1>=0:
            izquierda=matrizjug2[contadorFila][contadorPos-1]
        except:
          None
        try:
          if contadorFila-1>=0:
            arriba=matrizjug2[contadorFila-1][contadorPos]
        except:
          None
        try:
          abajo=matrizjug2[contadorFila+1][contadorPos]
        except:
          abajo=1
        if val==izquierda or val==derecha or val==arriba or val==abajo:
          raise Exception()
        contadorPos+=1
      contadorPos=0
      contadorFila+=1
  except:
    None
  else:
    raise Exception()

def mover2(direccion,orientazion):
  global jugador2
  comb=False
  if orientazion=="vertical":
    direccionCicloV=direccion
    direccionV=direccion
    if direccion<0: 
      indiceV1=2 
      indiceV2=direccionV
    else:
      indiceV1=direccionV
      indiceV2=4
    indiceH1=0
    indiceH2=4
    direccionH=0
    direccionCicloH=1
  if orientazion=="horizontal":
    direccionCicloH=direccion
    direccionH=direccion
    if direccion<0: 
      indiceH1=2 
      indiceH2=direccionH
    else:
      indiceH1=direccionH
      indiceH2=4
    indiceV1=0
    indiceV2=4
    direccionV=0
    direccionCicloV=1
  for fila in range(indiceV1,indiceV2,direccionCicloV):
    for columna in range(indiceH1,indiceH2,direccionCicloH):
      actual=matrizjug2[fila][columna]
      anterior=matrizjug2[fila-direccionV][columna-direccionH]
      if actual==0: pass
      elif actual==anterior:
        jugador2+=int(actual*2)
        if jugador2>int(puntajesAltos[0]):
          puntajesAltos[0]=jugador2
        anterior+=actual+(2*columna+3*fila+5)/111
        actual=0
        matrizjug2[fila][columna]=actual
        matrizjug2[fila-direccionV][columna-direccionH]=anterior
        if anterior>=2048:
          buscar2(0)
          print_matrizjug2()
          raise TypeError("!!!GANASTE!!!")
        comb=True
      elif anterior==0:
        anterior+=actual
        actual=0
        matrizjug2[fila][columna]=actual
        matrizjug2[fila-direccionV][columna-direccionH]=anterior
        comb=True
    if comb==True: mover2(direccion, orientazion)
    comb=False

def movimiento2():
  global matrizjug2, matrizPasada, mov, ultimaPartida, ultimoPunteo, jugador2, punteoTemp
  while True:
    mov=TomarValor("Ingrese un movimiento (w/a/s/d)")
    print ("\n\033[2A                                   \033[A")
    if mov == "w" or mov=="8":
      # print("hacia arriba")
      punteoTemp=jugador2
      mover2(1,"vertical")
      buscar2(0)    
      if matrizPasada==matrizjug2: None
      else:  
        historial_movimientos2.append("Hacia arriba")
        break
    elif mov == "s" or mov=="2":
      # print("hacia abajo")
      punteoTemp=jugador2
      mover2(-1,"vertical")
      buscar2(0)    
      if matrizPasada==matrizjug2: None
      else:  
        historial_movimientos2.append("Hacia abajo")
        break
    elif mov == "a" or mov=="4":
      # print("a la izquierda")
      punteoTemp=jugador2
      mover2(1,"horizontal")
      buscar2(0)    
      if matrizPasada==matrizjug2: None
      else:  
        historial_movimientos2.append("Hacia la izquierda")
        break
    elif mov == "d" or mov=="6":
      # print("a la derecha")
      punteoTemp=jugador2
      mover2(-1,"horizontal")
      buscar2(0)    
      if matrizPasada==matrizjug2: None
      else:  
        historial_movimientos2.append("Hacia la derecha")
        break
    elif mov=="q":
      print("Seguro quieres salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="g":
      ultimaPartida=deepcopy(matrizjug2)
      print("Guardar y salir? y/n")
      while True:
        confirmacion=TomarValor("\033[A")
        ultimoPunteo=jugador2
        if confirmacion=="y":
          raise Exception()
        elif confirmacion=="n":
          print("regresando")
          sleep(0.25)
          print ("\033[A                                   \033[A")
          print ("\033[A                                   \033[A")
          break
    elif mov=="e":
      jugador2=punteoTemp
      historial_movimientos2.append("Retoceder movimiento") 
      buscar(0)    
      break
#------------------------------------------------------------------------
#---------------------------funcion que une ambos jugadores------------
def juegos(x):
  global matrizPasada, matrizPasada2, matrizjug1, matrizjug2
  print('\033[?25l', end="")
  if x==1:
    try:
      recopilador()
      buscar1(0)
      nuevo_num1()
      nuevo_num1()
      print_matrizjug1()
      while True:
        matrizPasada2=deepcopy(matrizPasada)
        matrizPasada=deepcopy(matrizjug1)
        movimiento1()
        nuevo_num1()
        print_matrizjug1()
        if mov=="e":
          historial_tableros.pop()
          print(matrizPasada2)
          matrizjug1=deepcopy(matrizPasada2)
          print_matrizjug1()
    except TypeError as stopper:
      print(stopper)
      
    except:
      print("\n\n\t Se acabo el juego! \n\n")
      
      for i in range(0,3):
        if jugador1>int(puntajesAltos[i]):
         puntajesAltos.insert(i, jugador1)
         puntajesAltos.pop()
         break
        elif jugador1==int(puntajesAltos[i]):
          break
      sleep(2.5)
      print("\x1bc")
  elif x==2:
    try:
      recopilador()
      buscar2(0)
      nuevo_num2()
      nuevo_num2()
      print_matrizjug2()
      while True:
        matrizPasada2=deepcopy(matrizPasada)
        matrizPasada=deepcopy(matrizjug2)
        movimiento2()
        nuevo_num2()
        print_matrizjug2()
        if mov=="e":
          historial_tableros.pop()
          print(matrizPasada2)
          matrizjug2=deepcopy(matrizPasada2)
          print_matrizjug2()
    except TypeError as stopper:
      print(stopper)
    except:
      print("\n\n\t Se acabo el juego! \n\n")
      for i in range(0,3):
        if jugador2>int(puntajesAltos[i]):
         puntajesAltos.insert(i, jugador2)
         puntajesAltos.pop()
         break
        elif jugador2==int(puntajesAltos[i]):
          break
      sleep(2.5)
      print("\x1bc")
#----------------------------------------------------------------------
#-------------------funcion definitiva de dos jugadores----------------
def juego2048dosjugadores(x):
  global jugador1 
  global jugador2
  global pedirnombre
  global pedirnombre2
  print('\033[?25l', end="")
  if x==1:
    juegos(1)
    sleep(1)
    print("\x1bc")
    player="     Turno de "+str(pedirnombre2)
    print()
    for character in player:
      print(character, end="", flush=True)
      sleep(0.1)
    sleep(0.5)
    print('\x1bc')
    juegos(2)
    print()
  elif x==2:
    juegos(2)
    sleep(1)
    print("\x1bc")
    player="     Turno de "+str(pedirnombre)
    print()
    for character in player:
      print(character, end="", flush=True)
      sleep(0.1)
    sleep(0.5)
    print('\x1bc')
    juegos(1)
    print()
  print('\x1bc')
  print()
  if jugador1 > jugador2:
      ganador="     ¡"+str(pedirnombre)+" ha ganado!"
      for charac in ganador:
        print(charac, end="", flush=True)
        sleep(0.2)
      print()
      sleep(0.5)
  elif jugador2 > jugador1:
      ganador2="     ¡"+str(pedirnombre2)+" ha ganado!"
      for chara in ganador2:
        print(chara, end="", flush=True)
        sleep(0.2)
      print()
      sleep(0.5)
  else:
      empate="     ¡Empate!"
      for char in empate:
        print(char, end="", flush=True)
        sleep(0.2)
      print()
      sleep(0.5)
  print()
  print("\t Puntaje "+str(pedirnombre)+":", jugador1)
  print("\t Puntaje "+str(pedirnombre2)+":", jugador2)

#-----------IA----------------------------------------------------------
def fisIA():
  
  # define sus herramientas

  matriz_IA = deepcopy(matriz_2048)
  
  def find_max(matriz):
    max = 0
    max2 = 0
    max3 = 0
    ub_max = [0,0]
    ub_max2 = [0,0]
    ub_max3 = [0,0]
    for columna in range(len(matriz)): 
      for fila in range(len(matriz[columna])):
        if matriz[columna][fila] > max:
          max2 = max
          ub_max2 = ub_max
          max = matriz[columna][fila]
          ub_max = [columna, fila]
          
  
        if (matriz[columna][fila] > max2) and (matriz[columna][fila] <= max) and ([columna,fila] != ub_max):
          max3 = max2
          ub_max3 = ub_max2
          max2 = matriz[columna][fila]
          ub_max2 = [columna, fila]
  
        if matriz[columna][fila] > max3 and matriz[columna][fila] <= max2  and [columna,fila] != ub_max2 and [columna,fila] != ub_max:
          max3 = matriz[columna][fila]
          ub_max3 = [columna, fila]
  
    return (max, ub_max, max2, ub_max2, max3, ub_max3)

  def find_ceros(matriz):
    ceros = 0
    for columna in range(len(matriz)):
      for fila in range(len(matriz[columna])):
        if matriz[columna][fila] == 0: ceros += 1
    return ceros

  def find_total(matriz):
    total = 0
    for columna in matriz:
      for valor in columna:
        total += valor
    return total

  def comparar_lista(objetivo, valores):
    try:
      for valor in valores:
        if objetivo == valor: return True
        raise Exception()
    except: return True
    else: return False
    

  matriz_IA = deepcopy(matriz_2048)

  #define las variables utiles

  def evaluar(matriz_IA):
    find_maximo = find_max(matriz_IA)
    find_cero = find_ceros(matriz_IA)
    max = find_maximo[0]
    ub_max = find_maximo[1]
    max2 = find_maximo[2]
    ub_max2 = find_maximo[3]
    max3 = find_maximo[4]
    ub_max3 = find_maximo[5]
      
    #neuronas
  
    def neurona_proximal():
      dis_ab = sqrt((ub_max[0]-ub_max2[0])**2+(ub_max[1]-ub_max2[1])**2)
  
      dis_bc = sqrt((ub_max2[0]-ub_max3[0])**2+(ub_max2[1]-ub_max3[1])**2)
  
      dis_ac = sqrt((ub_max[0]-ub_max3[0])**2+(ub_max[1]-ub_max3[1])**2)
  
      try: por_ab = 1/dis_ab
      except: None
      try: por_bc = 1/dis_bc
      except: por_bc = 1
      try: por_ac = 1/dis_ac
      except: por_ac = 1
  
      return 0.4*por_ab + 0.4*por_bc + 0.2*por_ac
  
    #print(neurona_proximal(),"opina neurona proxima") 
  
    def neurona_solitaria():
        return find_cero/16
      
    #print(neurona_solitaria(),"opina neurona solitaria")
  
    def neurona_Torres():
      pico = max + max2 + max3
      total = find_total(matriz_IA)
      densidad = pico/total
      return densidad
      
   # print(neurona_Torres(),"opina Torres")
    
    def neurona_antisocial():
      esquinas = [[0,0],[0,3],[3,0],[3,3]]
      centros = [[1,1],[2,2],[2,1],[1,2]]
      if comparar_lista(ub_max,esquinas):
        return 1
      elif coparar_lista(ub_max,centros):
        return 0
      else: return 0.3

    #print(neurona_antisocial(),"opina neurona antisocial")
    
    def neurona_JP():
      try:
        for fila in matriz_IA:
          for val in fila:
            if val >= 2048: raise Exception
      except: return 1
      else: return 0
      
    #print(neurona_JP(),"opina neurona jp")
          

    decision_final = neurona_JP()+0.2*neurona_antisocial() + 0.3*neurona_proximal()+0.4*neurona_solitaria()+0.1*neurona_Torres()

    return decision_final
#---------importamos mover de la funcion principal-----------------------
  def moverIA(direccion,orientazion):
    comb=False
    if orientazion=="vertical":
      direccionCicloV=direccion
      direccionV=direccion
      if direccion<0: 
        indiceV1=2 
        indiceV2=direccionV
      else:
        indiceV1=direccionV
        indiceV2=4
      indiceH1=0
      indiceH2=4
      direccionH=0
      direccionCicloH=1
    if orientazion=="horizontal":
      direccionCicloH=direccion
      direccionH=direccion
      if direccion<0: 
        indiceH1=2 
        indiceH2=direccionH
      else:
        indiceH1=direccionH
        indiceH2=4
      indiceV1=0
      indiceV2=4
      direccionV=0
      direccionCicloV=1
    for fila in range(indiceV1,indiceV2,direccionCicloV):
      for columna in range(indiceH1,indiceH2,direccionCicloH):
        actual=matriz_IA[fila][columna]
        anterior=matriz_IA[fila-direccionV][columna-direccionH]
        if actual==0: pass
        elif actual==anterior:
          anterior+=actual+(2*columna+3*fila+5)/111
          actual=0
          matriz_IA[fila][columna]=actual
          matriz_IA[fila-direccionV][columna-direccionH]=anterior
          comb=True
        elif anterior==0:
          anterior+=actual
          actual=0
          matriz_IA[fila][columna]=actual
          matriz_IA[fila-direccionV][columna-direccionH]=anterior
          comb=True
      if comb==True: moverIA(direccion, orientazion)
      comb=False

  def pulimela(matriz):
    for columna in range(len(matriz)): 
      for fila in range(len(matriz[columna])):
        matriz[columna][fila] = int(round(matriz[columna][fila]))

  #el orden es w,a,s,d
  puntajes = [0,0,0,0]

  moverIA(1,"vertical")
  pulimela(matriz_IA)
  pulimela(matriz_IA)
  puntajes[0] = evaluar(matriz_IA)
 # print_matriz(matriz_IA)
  matriz_IA = deepcopy(matriz_2048)
  #print("en w mi valor es", puntajes[0])

  moverIA(-1,"horizontal")
  pulimela(matriz_IA)
  pulimela(matriz_IA)
  puntajes[1] = evaluar(matriz_IA)
  #print_matriz(matriz_IA)
  matriz_IA = deepcopy(matriz_2048)
# print("en a mi valor es", puntajes[1])

  moverIA(-1,"vertical")
  pulimela(matriz_IA)
  pulimela(matriz_IA)
  puntajes[2] = evaluar(matriz_IA)
 # print_matriz(matriz_IA)
  matriz_IA = deepcopy(matriz_2048)
# print("en s mi valor es", puntajes[2])

  moverIA(1,"horizontal")
  pulimela(matriz_IA)
  pulimela(matriz_IA)
  puntajes[3] = evaluar(matriz_IA)
 # print_matriz(matriz_IA)
  matriz_IA = deepcopy(matriz_2048)
 # print("en d mi valor es", puntajes[3])

  max = 0
  pos = 0
  for i in range(0,4):
    if puntajes[i] > max: 
      max = puntajes[i]
      pos = i
  if pos == 0:
    mover(1,"vertical")
    buscar(0)
    
    
  elif pos == 1:
    mover(-1,"horizontal")
    buscar(0)
    
  elif pos == 2:
    mover(-1,"vertical")
    buscar(0)
    
  elif pos == 3:
    mover(1,"horizontal")
    buscar(0)
#-----------------------------------------------------------------------
def gameplay_fisIA():
  print('\033[?25l', end="")
  try:
    global matriz_2048
    buscar(0)
    nuevo_num()
    nuevo_num()
    print_matriz()
    while True:
      fisIA()
      nuevo_num()
      print_matriz()
      sleep(1)
  except TypeError as stopper:
    print(stopper)
  except:
    print("\n\nLa IA abandona la partida!\n\n")
    print("Saliendo...")
    sleep(1)
    print("\x1bc")
#-----------------------------------------------------------------------
def consola():
  global pedirnombre
  global pedirnombre2
  print('\x1bc')
  print("\t┌───────────────────────────────┐")
  print("\t│                               │")
  print("\t│  Selecciona tu modo de juego  │")
  print("\t│                               │")
  print("\t│      1. Modalidad Normal      │")
  print("\t│      2. Jugador vs Jugador    │")
  print("\t│      3. Jugador vs Maquina    │")
  print("\t│                               │")
  print("\t└───────────────────────────────┘")
  modalidad=int(input("\t >> "))
  if modalidad==1:
    juego_2048()
    guardar()
  elif modalidad==2:
    print()
    pedirnombre=input("\t >> Introduzca nombre del jugador 1: ")
    print()
    pedirnombre2=input("\t >> Introduzca nombre del jugador 2: ")
    ju1=randint(1,2)
    ju2=randint(1,2)
    if ju1>ju2:
      print('\x1bc')
      numero="121212121212121221221212112121212   1"
      comienzo=">>   Comienza "+str(pedirnombre)
      print()
      for character in numero:
        print(">>      ",character, end="\r", flush=True)
        sleep(0.1)
      print()
      print()
      for caracter in comienzo:
        print(caracter, end="", flush=True)
        sleep(0.1)
      sleep(1.5)
      juego2048dosjugadores(1)
    elif ju2>ju1:
      print('\x1bc')
      numero="121212121212121221222121112122121   2"
      comienzo=">>   Comienza "+str(pedirnombre2)
      print()
      for character in numero:
        print(">>      ",character, end="\r", flush=True)
        sleep(0.1)
      print()
      print()
      for caracter in comienzo:
        print(caracter, end="", flush=True)
        sleep(0.1)
      sleep(1.5)
      juego2048dosjugadores(2)
    elif ju1==ju2:
      print('\x1bc')
      numero="121212121212121221221212112212221   1"
      comienzo=">>   Comienza "+str(pedirnombre)
      for character in numero:
        print(">>      ",character, end="\r", flush=True)
        sleep(0.1)
      print()
      print()
      for caracter in comienzo:
        print(caracter, end="", flush=True)
        sleep(0.1)
      sleep(1.5)
      juego2048dosjugadores(1)
  elif modalidad==3:
    print()
    pedirnombre=input("\t >> Introduzca nombre del jugador 1: ")
    print()
    pedirnombre2="fisIA"
    print("\t >> fisIA ")
    ju1=randint(1,2)
    ju2=randint(1,2)
    print('\x1bc')
    comienzo=">>   Comienza "+str(pedirnombre)
    print()
    for caracter in comienzo:
      print(caracter, end="", flush=True)
      sleep(0.1)
    sleep(1.5)
    juegos(1)
    sleep(1)
    print('\x1bc')
    comienzos=">>   Turno de FisIA "
    print()
    for racter in comienzos:
      print(racter, end="", flush=True)
      sleep(0.1)
    print()
    print('\x1bc')
    gameplay_fisIA()
    global jugador1, Punteo
    if jugador1 > Punteo:
      ganador="     ¡"+str(pedirnombre)+" ha ganado!"
      for charac in ganador:
        print(charac, end="", flush=True)
        sleep(0.2)
      print()
      print("\t Puntaje "+str(pedirnombre)+":", jugador1)
      print("\t Puntaje "+str(pedirnombre2)+":", Punteo)
      sleep(0.5)
    elif Punteo > jugador1:
        ganador2="     ¡FisIA"+" ha ganado!"
        for chara in ganador2:
          print(chara, end="", flush=True)
          sleep(0.2)
        print()
        print("\t Puntaje "+str(pedirnombre)+":", jugador1)
        print("\t Puntaje "+str(pedirnombre2)+":", Punteo)
        sleep(0.5)
    else:
        empate="     ¡Empate!"
        for char in empate:
          print(char, end="", flush=True)
          sleep(0.2)
        print()
        print("\t Puntaje "+str(pedirnombre)+":", jugador1)
        print("\t Puntaje "+str(pedirnombre2)+":", Punteo)
        sleep(0.5)
    sleep(1)
consola()
print('\n\033[?25h', end="")