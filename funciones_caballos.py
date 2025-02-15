import datos_caballos as dc
from clases_juego import Caballo
from os import system
import pygame
from button import Button
import sys
import funciones_tkinter as tk
from clases_juego import Usuario
from Inputbox import caja

def mostrar_caballos(caballos, screen):
    
    font=pygame.font.Font("fonts/Race Sport.ttf", 28)
    black=(255, 255, 255)
    x=200
    y=125

    frame=Button(pygame.transform.scale(pygame.image.load("images/frame_list.png"), (400, 480)), (200, 280), None, font, black, None)
    list_button=Button(None, (200, 80), 'PARTICIPANTES', font, black, None)
    info_button=Button(pygame.transform.scale(pygame.image.load("images/message.png"), (400, 150)), (200, 620), None, font, black, None)

    for i in [frame, list_button, info_button]:
        i.update(screen)

    for c in caballos.values():
        texto=f'({c.etiqueta}) {c} - {c.cuotas_saltos_velocidad[0]:.2f}'
        button_carrera=Button(None, (x, y), texto, font, black, None)
        button_carrera.update(screen)
        y+=50

def generar_caballos(cantidad):
    return {str(i + 1): Caballo(dc.nombre_genero(), dc.peso(), dc.edad(), dc.altura(), dc.cuota_saltos_velocidad(), i + 1)
            for i in range(cantidad)}


def desarrollar_carrera(caballos, ha_terminado=False):
    system('cls')
    for c in caballos.values():
        print(f'CABALLO #{c.etiqueta}  ' + ' '.join(' ' if i != c.posicion else '*' for i in range(50)) + '\n')
        c.correr() if not ha_terminado else None
    

def carrera(screen):

    user=Usuario(1000)
    caballos=None
    caballo_apuesta=[]
    comenzar_carrera=ha_apostado=False
    fondo=pygame.image.load("images/cielo.jpg")
    black=(0, 0, 0)
    red=(255, 0, 0)
    white=(255, 255, 255)
    font=pygame.font.Font("fonts/Race Sport.ttf", 30)
    font2=pygame.font.Font("fonts/Race Sport.ttf", 15)
    usuario=user


    def modalidad_menu():
        nonlocal caballos
        
        while True:
         mouse_menu=pygame.mouse.get_pos()
         screen.blit(fondo, (0,0))
        
         title=Button(image=pygame.image.load('images/title_game.png'), pos=(640, 90), text_input=None, font=font2, base_color=black, hovering_color=None)
         modalidad_2=Button(image=pygame.image.load('images/horse_2.png'), pos=(640, 200), text_input=None, font=font2, base_color=black, hovering_color=None)
         modalidad_4=Button(image=pygame.image.load('images/horse_4.png'), pos=(640, 375), text_input=None, font=font2, base_color=black, hovering_color=None)
         modalidad_8=Button(image=pygame.image.load('images/horse_8.png'), pos=(640, 550), text_input=None, font=font2, base_color=black, hovering_color=None)
         button_saldo=Button(pygame.image.load('images/saldo_image.png'), (640, 680), f'SALDO: {usuario.mostrar_saldo()}', font, black, None)
          

         for i in [modalidad_2, modalidad_4, modalidad_8, title, button_saldo]:
             i.update(screen)

         for event in pygame.event.get():
            if event.type==pygame.QUIT:
              pygame.quit()
              sys.exit()
            
            elif event.type==pygame.MOUSEBUTTONDOWN:

                if modalidad_2.checkForInput(mouse_menu):
                    caballos=generar_caballos(2)
                    menu_carrera()

                elif modalidad_4.checkForInput(mouse_menu):
                    caballos=generar_caballos(4)
                    menu_carrera()

                elif modalidad_8.checkForInput(mouse_menu):
                    caballos=generar_caballos(8)
                    menu_carrera()

       
         pygame.display.flip()
    

    def menu_carrera():
        nonlocal ha_apostado, caballo_apuesta 

        while not comenzar_carrera:

            screen.blit(fondo, (0,0))
            mouse_menu=pygame.mouse.get_pos()
            
            button_carrera=Button(pygame.transform.scale(pygame.image.load("images/carrera_button.png"), (500, 100)), (900, 250), None, font, black, None)
            button_apuesta=Button(pygame.transform.scale(pygame.image.load("images/apuesta_button.png"), (500, 100)), (900, 400), None, font, black, None)
            button_saldo=Button(pygame.image.load('images/saldo_image.png'), (680, 680), f'SALDO: {usuario.mostrar_saldo()}', font, black, None)
            back_button=Button(pygame.transform.scale(pygame.image.load("images/back_button.png"), (200, 80)), (1180, 675), None, font, black, None)
            
            for i in [button_carrera, button_apuesta, button_saldo, back_button]:
                i.update(screen)

            mostrar_caballos(caballos, screen)
        
            for event in pygame.event.get():

                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==pygame.MOUSEBUTTONDOWN:

                    if back_button.checkForInput(mouse_menu):
                        if not ha_apostado:
                            modalidad_menu()
                        else:
                            respuesta=tk.confirmacion('Ha realizado una apuesta, si sale sera reembolsado ¿desea salir?')
                            if respuesta:
                                usuario.saldo+=caballo_apuesta[1]
                                caballo_apuesta.clear()
                                ha_apostado= not ha_apostado
                                modalidad_menu()
                            

                    if button_carrera.checkForInput(mouse_menu):
                        if not ha_apostado:
                            tk.text_error('Debe realizar una apuesta para proceder a la carrera')
                        else: None

                    if button_apuesta.checkForInput(mouse_menu):
                        if not ha_apostado:
                            menu_apuesta()
                        else: tk.text_info(F'Ya ha realizado una apuesta, {caballo_apuesta[1]}$ por caballo #{caballo_apuesta[0]}')
            
                if event.type==pygame.KEYDOWN:

                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                        opcion=event.unicode

                        if opcion in caballos:
                            menu_datos2(caballos[opcion].obtener_datos(), opcion, 1)
                        
                        else: tk.text_error('Caballo no participante.')
        
            pygame.display.flip()
    

    def menu_datos2(text, opcion, menu):
       while True:
           mouse_datos=pygame.mouse.get_pos()
           screen.blit(fondo, (0, 0))
           x=640
           y=110

           title=Button(pygame.transform.scale(pygame.image.load("images/running_horse.png"), (600, 60)), (640, 35), f"Datos del caballo #{opcion}", font, white, None)
           back_button=Button(pygame.transform.scale(pygame.image.load("images/back_button.png"), (200, 80)), (1180, 675), None, font, black, None)
           
           for i in [title, back_button]:
               i.update(screen)

           for data in text:
                horse_button=Button(pygame.transform.scale(pygame.image.load("images/datos_button.png"), (520, 70)), (x, y), data, font, white, None)
                horse_button.update(screen)
                y+=95
            
           for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_datos):
                        if menu==1:
                            menu_carrera()
                        else: menu_apuesta()      
                
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if menu==1:
                            menu_carrera()
                        else: menu_apuesta() 
                        
            
           pygame.display.flip()

    def menu_apuesta():
        nonlocal ha_apostado, caballo_apuesta
        user_text = user_text2 = caballo = '' 
        input_rect = caja(790, 200, 180, 32, red, black, pygame.font.Font(None, 32), False)
        input_rect2=caja(790, 500, 180, 32, red, black, pygame.font.Font(None, 32), False)
        monto=monto2=0
        cont1=cont2=False

        while True:
            screen.blit(fondo, (0, 0))
            mostrar_caballos(caballos, screen)
            mouse_menu=pygame.mouse.get_pos()

            apuesta_button=Button(pygame.transform.scale(pygame.image.load("images/boton_caballo.png"), (600, 90)), (850, 100), None, font, black, None)
            apuesta_button2=Button(pygame.transform.scale(pygame.image.load("images/boton_monto.png"), (600, 90)), (850, 400),  None, font, black, None)
            back_button=Button(pygame.transform.scale(pygame.image.load("images/back_button.png"), (200, 80)), (1180, 675), None, font, black, None)
            button_saldo=Button(pygame.image.load('images/saldo_image.png'), (680, 680), f'SALDO: {float(usuario.mostrar_saldo())-monto2}', font, black, None)
          
            for i in [apuesta_button, apuesta_button2, back_button, button_saldo]:
                i.update(screen)

            for event in pygame.event.get():
               if event.type==pygame.QUIT:
                 pygame.quit()
                 sys.exit()
                
               if event.type==pygame.MOUSEBUTTONDOWN: 
                 
                 input_rect.activar(event)    
                 input_rect2.activar(event)

                 if back_button.checkForInput(mouse_menu):
                    respuesta=tk.confirmacion('No ha realizado una apuesta, ¿desea salir?')
                    if respuesta:
                        menu_carrera()
                                          
                
               if event.type==pygame.KEYDOWN:
                   if input_rect.active:
                      
                      if event.key == pygame.K_RETURN:
                         
                         if user_text in caballos:
                             if not cont1:
                                 caballo=user_text
                                 tk.text_info(F'Ha elegido al caballo #{caballo}')
                                 user_text= ''
                                 cont1= not cont1
                                 input_rect.active=False
                           
                             else: tk.text_info(F'Ya ha realizado una apuesta por el caballo #{caballo}')
                         
                         else:
                            tk.text_error('Error, ingrese un caballo valido.')
                            pygame.display.set_caption('Speed Horse')
                            user_text = ''
                     

                      elif event.key == pygame.K_BACKSPACE:
                          user_text = user_text[:-1] 
                
                      else: user_text += event.unicode

                   elif input_rect2.active:
                     
                     if event.key == pygame.K_RETURN:
                        monto=user_text2
                        monto= 0 if not monto.isnumeric() else float(monto)

                        if monto > 100 and monto <= usuario.saldo:
                            if not cont2:
                              tk.text_info(F'ha elegido: {monto}$')
                              user_text2= ''
                              monto2=monto
                              cont2= not cont2
                              input_rect2.active=False
                            else: tk.text_info(F'Ya ha realizado una apuesta de {monto2}$')
                            
                        else:
                            tk.text_error('Error, ingrese un monto valido.')
                            user_text2= ''

                    
                     elif event.key == pygame.K_BACKSPACE:
                         user_text2 = user_text2[:-1] 
                    
                     else: user_text2 += event.unicode

                   else:
                       if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8):
                        opcion=event.unicode

                        if opcion in caballos:
                            menu_datos2(caballos[opcion].obtener_datos(), opcion, 2)
                        
                        else: tk.text_error('Caballo no participante.')
            
            
            input_rect.dibujar(screen, user_text)
            input_rect2.dibujar(screen, user_text2)

            for i in [input_rect, input_rect2]:
                i.cambia_color()



            if ((monto2 > 100) and (caballo in caballos)):
               apuesta=usuario.apostar(monto2)
               caballo_apuesta.extend([caballo, apuesta])
               tk.text_info(F'Apuesta realizada con exito, {caballo_apuesta[1]}$ por caballo #{caballo_apuesta[0]}')
               ha_apostado=True
               menu_carrera()
            
            pygame.display.flip()

    
    modalidad_menu()
