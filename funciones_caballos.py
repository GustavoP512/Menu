import datos_caballos as dc
from clases_juego import Caballo
from os import system
from time import sleep
import pygame
from button import Button
import sys
import tkinter as tk
from tkinter import messagebox


def text_info(mensaje):
    root=tk.Tk()
    root.withdraw()
    messagebox.showinfo('Mensaje', mensaje)
    

def text_emerge(mensaje):
    root=tk.Tk()
    root.withdraw()

    messagebox.showerror('Error', mensaje)
    root.destroy()

def mostrar_caballos(caballos, screen):
    system('cls')
    font=pygame.font.Font("fonts/Race Sport.ttf", 25)
    black=(0, 0, 0)
    x=250
    y=90
    
    list_button=Button(None, (250, 30), 'Lista de Caballos', font, black, None)
    list_button.update(screen)

    for c in caballos.values():
        texto=f'({c.etiqueta}) {c} --> {c.cuotas_saltos_velocidad[0]:.2f}'
        button_carrera=Button(None, (x, y), texto, font, black, None)
        button_carrera.update(screen)
        y+=60

def generar_caballos(cantidad):
    return {str(i + 1): Caballo(dc.nombre_genero(), dc.peso(), dc.edad(), dc.altura(), dc.cuota_saltos_velocidad(), i + 1)
            for i in range(cantidad)}


def desarrollar_carrera(caballos, ha_terminado=False):
    system('cls')
    for c in caballos.values():
        print(f'CABALLO #{c.etiqueta}  ' + ' '.join(' ' if i != c.posicion else '*' for i in range(50)) + '\n')
        c.correr() if not ha_terminado else None
    sleep(1)

def carrera(usuario, screen):
    caballos=None
    caballo_apuesta=[]
    comenzar_carrera=ha_apostado=False
    white=(255, 255, 255)
    black=(0, 0, 0)
    color=(255, 0, 0)
    base_font = pygame.font.Font(None, 32) 
    font=pygame.font.Font("fonts/Race Sport.ttf", 30)
    font2=pygame.font.Font("fonts/Race Sport.ttf", 15)

    def modalidad_menu():
        nonlocal caballos
        font=pygame.font.Font("fonts/Race Sport.ttf", 50)
        font2=pygame.font.Font("fonts/Race Sport.ttf", 35)
        f_color=(0, 0, 0)

        while True:
         title=font.render("Carrera de Caballos", True, f_color)
         title_rect=title.get_rect(center=(512, 50))

         screen.fill(white)
         screen.blit(title, title_rect)
         mouse_menu=pygame.mouse.get_pos()

         modalidad_2=Button(image=None, pos=(512, 250), text_input= "Modalidad: 2 Caballos", font=font2, base_color=f_color, hovering_color=None)
         modalidad_2.update(screen)

         modalidad_4=Button(image=None, pos=(512, 450), text_input= "Modalidad: 4 Caballos", font=font2, base_color=f_color, hovering_color=None)
         modalidad_4.update(screen)

         modalidad_8=Button(image=None, pos=(512, 650), text_input= "Modalidad: 8 Caballos", font=font2, base_color=f_color, hovering_color=None)
         modalidad_8.update(screen)

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

        color_active = color
        color_passive = black
        color2 = color_passive 
        active = False
        user_text=''
        input_rect = pygame.Rect(180, 600, 150, 30) 

        while not comenzar_carrera:

            mouse_menu= pygame.mouse.get_pos()
            screen.fill(white)

            datos_button=Button(None, (255, 560), 'Ingrese numero del caballo para ver datos: ', font2, black, None)
            datos_button.update(screen)

            button_carrera=Button(None, (800, 200), "Iniciar carrera", font, black, None)
            button_carrera.update(screen)

            button_apuesta=Button(None, (800, 300), "Realizar apuesta", font, black, None)
            button_apuesta.update(screen)

            button_saldo=Button(None, (512, 740), usuario.mostrar_saldo(), font, black, None)
            button_saldo.update(screen)

            back_button=Button(None, (910, 740), 'Back', font, black, None)
            back_button.update(screen)


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
                            usuario.saldo+=caballo_apuesta[1]
                            caballo_apuesta.clear()
                            ha_apostado= not ha_apostado
                            modalidad_menu()

                    if button_carrera.checkForInput(mouse_menu):
                        if not ha_apostado:
                            text_emerge('Debe realizar una apuesta para proceder a la carrera')
                        else: None

                    if button_apuesta.checkForInput(mouse_menu):
                        if not ha_apostado:
                            menu_apuesta()
                        else: text_emerge(F'Ya ha realizado una apuesta, {caballo_apuesta[1]}$ por caballo #{caballo_apuesta[0]}')

                    if input_rect.collidepoint(event.pos):
                        active=True
                    else: active=False
            
                if event.type==pygame.KEYDOWN:

                    if active:

                        if event.key == pygame.K_RETURN:
                            opcion=user_text
                            user_text = ''

                            if opcion in caballos:

                                menu_datos2(caballos[opcion].obtener_datos(), opcion)
                    
                            else: text_emerge('Error, no se encuentra ese caballo.')
                        
                        elif event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1] 
                
                        else: user_text += event.unicode
            
            if active:
                color2=color_active
            else:
                color2=color_passive
        
            pygame.draw.rect(screen, color2, input_rect) 

            text_surface = base_font.render(user_text, True, (255, 255, 255)) 

            screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))


            pygame.display.flip()
    

    def menu_datos2(text, opcion):
       while True:
           mouse_datos=pygame.mouse.get_pos()
           screen.fill(white)
           x=512
           y=150

           title=Button(None, (512, 50), f'DATOS DEL CABALLO #{opcion}', font, black, None)
           title.update(screen)
           back_button=Button(None, (900, 700), 'Back', font, black, None)
           back_button.update(screen)

           for data in text:
                horse_button=Button(None, (x, y), data, font, black, None)
                horse_button.update(screen)
                y+=75
            
           for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_datos):
                        menu_carrera()
            
           pygame.display.flip()

    def menu_apuesta():
        nonlocal ha_apostado, caballo_apuesta

        font2=pygame.font.Font("fonts/Race Sport.ttf", 20)
        base_font = pygame.font.Font(None, 32) 
        user_text = user_text2 ='' 
        color=(255, 0, 0)
        input_rect = pygame.Rect(700, 300, 140, 32)
        inpunt_rect2= pygame.Rect(700, 500, 140, 32) 
        color_active = color
        color_passive = black
        color2 = color_passive
        monto=apuesta=0
        cont1=cont2=False
        caballo=''

        while True:
            screen.fill(white)
            mostrar_caballos(caballos, screen)
            apuesta_button=Button(None, (750, 250), 'Ingrese el caballo a apostar:', font2, black, None)
            apuesta_button.update(screen)
            apuesta_button2=Button(None, (750, 450), 'Ingrese el monto de su apuesta:', font2, black, None)
            apuesta_button2.update(screen)
            
            

            for event in pygame.event.get():
               if event.type==pygame.QUIT:
                 pygame.quit()
                 sys.exit()
                
               if event.type==pygame.MOUSEBUTTONDOWN:
                 if input_rect.collidepoint(event.pos): 
                    active = True
                 else: active = False

                 if inpunt_rect2.collidepoint(event.pos):
                    active2 = True
                 else: active2 = False
                
               if event.type==pygame.KEYDOWN:
                   if active:
                      
                      if event.key == pygame.K_RETURN:
                         
                         if user_text in caballos:
                             if not cont1:
                                 caballo=user_text
                                 text_info(F'Ha apostado por el caballo #{caballo}')
                                 cont1= not cont1
                             else: text_info(F'Ya ha realizado una apuesta por el caballo #{caballo}' )
                         else:
                            text_emerge('Error, ingrese un caballo valido.')
                            user_text = ''
                     

                      elif event.key == pygame.K_BACKSPACE:
                          user_text = user_text[:-1] 
                
                      else: user_text += event.unicode

                   elif active2:
                     
                     if event.key == pygame.K_RETURN:
                        monto=user_text2
                        monto= 0 if not monto.isnumeric() else float(monto)

                        if monto > 100 and monto < usuario.saldo:
                            if not cont2:
                              apuesta = usuario.apostar(monto)
                              text_info(F'Ha apostado {apuesta}')
                              cont2= not cont2
                            else: text_info(F'Ya ha realizado una apuesta de {apuesta}$')
                            
                        else:
                            text_emerge('Error, ingrese un monto valido.')
                            user_text2= ''

                    
                     elif event.key == pygame.K_BACKSPACE:
                         user_text2 = user_text2[:-1] 
                    
                     else: user_text2 += event.unicode
         
          
            pygame.draw.rect(screen, color2, input_rect)
            pygame.draw.rect(screen, color2, inpunt_rect2)

            text_surface = base_font.render(user_text, True, (255, 255, 255))
            text_surface2 = base_font.render(user_text2, True, (255, 255, 255))

            screen.blit(text_surface, (input_rect.x+5, input_rect.y+5)) 
            screen.blit(text_surface2, (inpunt_rect2.x+5, inpunt_rect2.y+5))

            if ((apuesta > 100) and (caballo in caballos)):
               caballo_apuesta.extend([caballo, apuesta])
               text_info(F'Apuesta realizada con exito, {caballo_apuesta[1]}$ por caballo #{caballo_apuesta[0]}')
               ha_apostado=True
               menu_carrera()
            
            pygame.display.flip()

    
    modalidad_menu()
