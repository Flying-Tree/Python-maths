#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 13:45:59 2021

@author: Olivier Henry
"""

import tkinter as tk
from math import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
from copy import deepcopy

# =============================================================================
# FUNCTIONS
# =============================================================================

def init():
    global root,polynome,CoefEntries,N,LabelsCoef,polynome_StrVar,barres_fraction,Degre,Degre_label
    root=tk.Tk()
    root.configure(bg=bg_color)
    root.resizable(False,False)
    root.title('Factorisation de polynômes')
    
    CoefEntries=[]
    LabelsCoef=[]
    polynome=[]
    polynome_StrVar=[]
    barres_fraction=[]
    
    Degre_label=tk.Label(root,text='Degré du polynome : ',bg=bg_color)
    N=tk.StringVar()
    Degre=tk.Entry(root,textvar=N,width=10,bg=bg_color)
    Degre.bind('<Return>',updateEntries)
    Degre.bind('<KP_Enter>',updateEntries)
    
    Degre_label.grid(row=0,column=0)
    Degre.grid(row=0,column=1)
    
    root.update_idletasks()     # Pour que les dimensions des objets soient leurs dimensions affichées
    
    root.geometry(str(Degre_label.winfo_width()+Degre.winfo_width()) + 'x' + str(max(Degre.winfo_height(),Degre_label.winfo_height())))

def updateEntries(event):
    global root,LabelsCoef,CoefEntries,N,polynome,polynome_StrVar,barres_fraction,Degre,Degre_label,k
    k=N.get()
    if k!='':
        try:
            k=float(k)    
            if k%1==0 and k>=0:
                k=int(k)
                
                if k>len(CoefEntries)-1:
                    for i in range(len(CoefEntries),k+1):
                        
                        polynome.append(('',''))
                        
                        polynome_StrVar.append((tk.StringVar(),tk.StringVar()))
                        polynome_StrVar[-1][1].set('1')
                        
                        CoefEntries.append((tk.Entry(root,width=10,bg=bg_color,textvar=polynome_StrVar[i][0]),tk.Entry(root,width=10,bg=bg_color,textvar=polynome_StrVar[i][1])))
                        CoefEntries[-1][0].bind('<Return>',updatePolynome)
                        CoefEntries[-1][1].bind('<Return>',updatePolynome)
                        CoefEntries[-1][0].bind('<KP_Enter>',updatePolynome)
                        CoefEntries[-1][1].bind('<KP_Enter>',updatePolynome)
                
                else:
                    for i in range(k+1,len(CoefEntries)):
                        polynome.pop(-1)
                        polynome_StrVar.pop(-1)
                        CoefEntries[-1][0].destroy()
                        CoefEntries[-1][1].destroy()
                        CoefEntries.pop(-1)
                
                for i in range(len(LabelsCoef)):
                    LabelsCoef[0].destroy()
                    LabelsCoef.pop(0)
                    barres_fraction[0].destroy()
                    barres_fraction.pop(0)
                
                for i,x in enumerate(CoefEntries):
                    x[0].grid(row=1+3*i,column=1)
                    x[1].grid(row=3+3*i,column=1)
                    
                    root.update_idletasks()     # Pour que les dimensions des objets soient leurs dimensions affichées
                    
                    LabelsCoef.append(tk.Label(root,text=' Coefficient de degré '+str(i)+' : ',bg=bg_color))
                    barres_fraction.append(tk.Canvas(root,width=x[0].winfo_width(),height=1,bg="black"))
                    
                    LabelsCoef[-1].grid(row=1+3*i,column=0,rowspan=3)
                    barres_fraction[-1].grid(row=2+3*i,column=1)
                
                root.geometry(str(max(Degre_label.winfo_width(),LabelsCoef[0].winfo_width())+max(Degre.winfo_width(),barres_fraction[0].winfo_width())) + 'x' + str(max(Degre.winfo_height(),Degre_label.winfo_height())+(k+1)*(2*CoefEntries[0][0].winfo_height()+barres_fraction[0].winfo_height())))
                
                updatePolynome(None)
                
            else:
                N.set('')
                
                reset_Entries()
        
        except ValueError:
            N.set('')
            
            reset_Entries()
    
    else:
        reset_Entries()

def reset_Entries():
    global root,LabelsCoef,CoefEntries,N,polynome,polynome_StrVar,barres_fraction,Degre,Degre_label
    clear_aff()
    
    polynome=[]
    polynome_StrVar=[]
    
    root.update_idletasks()     # Pour que les dimensions des objets soient leurs dimensions affichées
    root.geometry(str(Degre_label.winfo_width()+Degre.winfo_width()) + 'x' + str(max(Degre.winfo_height(),Degre_label.winfo_height())))
    
    for i in range(len(CoefEntries)):
        CoefEntries[-1][0].destroy()
        CoefEntries[-1][1].destroy()
        CoefEntries.pop(-1)
        LabelsCoef[-1].destroy()
        LabelsCoef.pop(-1)
        barres_fraction[-1].destroy()
        barres_fraction.pop(-1)

def updatePolynome(event):
    global polynome,polynome_StrVar,coef_dom
    invalid=[[True,True] for i in range(len(polynome_StrVar))]
    for i,xStrVar in enumerate(polynome_StrVar):
        try:
            k0=float(xStrVar[0].get())
            if k0%1==0:
                polynome[i]=(int(k0),polynome[i][1])
                invalid[i][0]=False
            else:
                xStrVar[0].set('')
                polynome[i]=(int(k0),'')
        except ValueError:
            for l in xStrVar[0].get():
                if l not in "1234567890-":
                    xStrVar[0].set('')
        
        try:
            k1=float(xStrVar[1].get())
            if k1%1==0:
                polynome[i]=(polynome[i][0],int(k1))
                invalid[i][1]=False
            else:
                xStrVar[1].set('')
                polynome[i]=(polynome[i][0],'')
        except ValueError:
            for l in xStrVar[1].get():
                if l not in "1234567890-":
                    xStrVar[1].set('')
    if invalid==[[False,False] for i in range(len(polynome_StrVar))]:
        coef_dom=(1,1)
        affichage(factorisation_ultime(polynome))
    else:
        clear_aff()

def arrondi(x):
    if x-floor(x)<0.5:
        return floor(x)
    return floor(x)+1

def lcm(liste):
    out=1
    for x in liste:
        out*=arrondi(x/gcd(x,out))
    return out

def p(x,a):
    return sum([(a[i][0]/a[i][1])*x**i for i in range(len(a))])

def Q2Z(a):
    global coef_dom
    l=lcm([x[1] for x in a])
    coef_dom=(coef_dom[0],coef_dom[1]*l)
    return [(arrondi(x[0]*l/x[1]),1) for x in a]

def diviseurs(n):
    out=[]
    for i in range(1,int(sqrt(n))+1):
        if n%i==0:
            out.append(i)
            out.append(arrondi(n/i))
    return out

def racines_evidentes(P):    
    if P[0][0]==0:
        return [(0,1)]
    
    out=[]
        
    if len(P)>3:
        for a in diviseurs(abs(P[0][0])):
            for b in diviseurs(abs(P[-1][0])):
                for sign in (-1,1):
                    a2=arrondi(a/gcd(a,b))
                    b2=arrondi(b/gcd(a,b))
                    if float(p(sign*a2/b2,P))==0.0 and not (sign*a2,b2) in out:
                        out.append((sign*a2,b2))
    return out

def operH(a,c,r):
    out=(c[0]*r[0],c[1]*r[1])                                                      #c×r
    out=(a[0]*out[1]+a[1]*out[0],a[1]*out[1])                                      #a+c×r
    out=(arrondi(out[0]/gcd(out[0],out[1])),arrondi(out[1]/gcd(out[0],out[1])))    #simplifier
    return out

def factoriser(P):
    global coef_dom
    out=[]
    P2=P
    for i,x in enumerate(P2):
        P2[i]=(arrondi(x[0]/gcd(x[0],x[1])),arrondi(x[1]/gcd(x[0],x[1])))      # simplification
    if len(P2)==3:
        coef_dom = (coef_dom[0]*P2[-1][0] , coef_dom[1]*P2[-1][1])
        
        delta=( P2[1][0]**2*P2[2][1]*P2[0][1] - 4*P2[2][0]*P2[0][0]*P2[1][1]**2 , P2[1][1]**2*P2[2][1]*P2[0][1] )  # b²-4ac
        delta=(arrondi(delta[0]/gcd(delta[0],delta[1])),arrondi(delta[1]/gcd(delta[0],delta[1])))         # simplification
        
        out=[ [ (P2[1][0]*P2[2][1] , 2*P2[2][0]*P2[1][1] , delta) , (1,1) ] ]
    elif len(P2)>3:
        for r in racines_evidentes(P):
            out.append([(-r[0],r[1]) , (1,1)])
            p2=[P2[-1]]
            for a in P2[-2:0:-1]:
                p2.insert(0,operH(a,p2[0],r))
            P2=p2
        if len(P2)==1:
            coef_dom=(coef_dom[0]*P2[0][0],coef_dom[1]*P2[0][1])
        elif len(P2)==2:
            coef_dom=(coef_dom[0]*P2[0][0],coef_dom[1]*P2[0][1])
            P2 = [(P2[0][0]*P2[1][1],P2[0][1]*P2[1][0]) , (1,1)]
            P2[0] = (arrondi(P2[0][0]/gcd(P2[0][0],P2[0][1])),arrondi(P2[0][1]/gcd(P2[0][0],P2[0][1])))
            out.append(P2)
        else:
            out.append(P2)
    return out

def factorisation_ultime(P):
    global coef_dom
    if len(P)<=2:
        return [P]
    P2=[P]
    P1=[]
    while P1!=P2:
        P1=P2
        P2=[]
        for p3 in P1:
            if len(p3)>2:
                P2+=factoriser(Q2Z(p3))
            else:
                P2.append(p3)
    
    return P2

def affichage_polynome(Pdvt):
    Pdvt=[(arrondi(a[0]/gcd(a[0],a[1])),arrondi(a[1]/gcd(a[0],a[1]))) for a in Pdvt[::-1]]
    
    tmptxt1=''
    
    xstr=['x']*(len(Pdvt)-1)+['']
    degres=['','']+[str(i) for i in range(len(Pdvt)) if i>1]
    
    for i,a in enumerate(Pdvt):     # simplifier et partir du terme de plus haut degré
        if a[0]*a[1]>0:             # signe devant le coefficient
            tmptxt1+='+'
        elif a[0]*a[1]<0:
            tmptxt1+='-'
        if a[0]!=0:                     # pas de termes nuls
            if abs(a[1])==1 and (abs(a[0])!=1 or i==len(Pdvt)-1):            # pas de fraction pour les entiers ni de coefficients valant ±1
                tmptxt1+=str(abs(a[0]))
            elif abs(a[1])!=1:
                tmptxt1+='\dfrac{'+str(abs(a[0]))+'}{'+str(abs(a[1]))+'}' 
            tmptxt1+=xstr[i] + '^{' + degres[len(Pdvt)-1-i] + '}'                            # éventuel x^k
    
    if tmptxt1[0]=='+':                                              # Ne pas mettre de + après le =
        tmptxt1=tmptxt1[1:]
    
    if '-' in tmptxt1 or '+' in tmptxt1:
        tmptxt1='\left(' + tmptxt1 + '\\right)'
    
    return tmptxt1

def affichage_trinome(p3):
    tmptxt2=''
    for sign in ('-','+'):
        tmptxt2+='\left(x'
        
        if p3[0][2][0]*p3[0][2][1]<0:                                                     # racines complexes car delta<0
            
            if p3[0][0]*p3[0][1]<0:                                                       # signe de Re(r)
                tmptxt2+='-'
            elif p3[0][0]*p3[0][1]>0:
                tmptxt2+='+'
            
            if abs(p3[0][1])==1 and p3[0][0]!=0:                                                         # Re(r) entier
                tmptxt2+=str(abs(p3[0][0]))
            elif abs(p3[0][0])!=0:
                tmptxt2+= '\dfrac{' + str(abs(arrondi(p3[0][0]/gcd(p3[0][0],p3[0][1])))) + '}{' + str(abs(arrondi(p3[0][1]/gcd(p3[0][0],p3[0][1])))) + '}'
            
            tmptxt2+=sign
            
            if arrondi(sqrt(abs(p3[0][2][0])))**2==abs(p3[0][2][0]) and arrondi(sqrt(abs(p3[0][2][1])))**2==abs(p3[0][2][1]):     # Im(r) rationnel
                delta_sqrt=(arrondi(sqrt(abs(p3[0][2][0]))),arrondi(sqrt(abs(p3[0][2][1]))))
                delta_sqrt = (arrondi(delta_sqrt[0]/gcd(delta_sqrt[0],p3[0][1])) , arrondi(delta_sqrt[1]*p3[0][1]/gcd(delta_sqrt[0],p3[0][1])))
                
                if abs(delta_sqrt[1])==1:                                                                                     # Im(r) entier
                    if abs(delta_sqrt[0])==1:
                        tmptxt2+='i\\right)'
                    else:
                        tmptxt2+=str(abs(delta_sqrt[0])) + 'i\\right)'
                    
                else:
                    tmptxt2+='\dfrac{' + str(abs(delta_sqrt[0])) + '}{' + str(abs(delta_sqrt[1])) + '} i\\right)'
            
            else:
                if abs(p3[0][2][1])==1:
                    tmptxt2+='i\sqrt{' + str(abs(p3[0][2][0])) + '}\\right)'
                else:
                    tmptxt2+='i\dfrac{\sqrt{' + str(abs(p3[0][2][0]*p3[0][2][1])) + '}}{' + str(abs(p3[0][2][1])) + '}\\right)'
        
        else:
            if (p3[0][0]-sqrt(p3[0][2][0]/p3[0][2][1])==0.0 and sign=='-') or (p3[0][0]+sqrt(p3[0][2][0]/p3[0][2][1])==0.0 and sign=='+'):  # 0 est une racine
                tmptxt2=tmptxt2[:-7]+'x'
                
            else:
                if arrondi(sqrt(abs(p3[0][2][0])))**2==abs(p3[0][2][0]) and arrondi(sqrt(abs(p3[0][2][1])))**2==abs(p3[0][2][1]):     # r rationnel
                    delta_sqrt=(arrondi(sqrt(abs(p3[0][2][0]))),arrondi(sqrt(abs(p3[0][2][1]))))
                    delta_sqrt = (arrondi(delta_sqrt[0]/gcd(delta_sqrt[0],p3[0][1])) , arrondi(delta_sqrt[1]*p3[0][1]/gcd(delta_sqrt[0],p3[0][1])))
                    if sign=='-':
                        r = (p3[0][0]*delta_sqrt[1]-p3[0][1]*delta_sqrt[0] , p3[0][1]*delta_sqrt[1])
                        r = (arrondi(r[0]/gcd(r[0],r[1])),arrondi(r[1]/gcd(r[0],r[1])))
                    else:
                        r = (p3[0][0]*delta_sqrt[1]+p3[0][1]*delta_sqrt[0] , p3[0][1]*delta_sqrt[1])
                        r = (arrondi(r[0]/gcd(r[0],r[1])),arrondi(r[1]/gcd(r[0],r[1])))
                    
                    if r[0]*r[1]<0:                                                       # signe de r
                        tmptxt2+='-'
                    elif r[0]*r[1]>0:
                        tmptxt2+='+'
                    
                    if abs(r[1])==1 and r[0]!=0:            # r entier
                        tmptxt2+= str(abs(r[0])) + '\\right)'
                    elif r[0]!=0:
                        tmptxt2+= '\dfrac{' + str(abs(r[0])) + '}{' + str(abs(r[1])) + '}\\right)'
                
                else:
                    if p3[0][0]*p3[0][1]<0:                                                       # signe de la partie rationnelle de r
                        tmptxt2+='-'
                    else:
                        tmptxt2+='+'
                    
                    if abs(p3[0][1])==1 and p3[0][0]!=0:                                                         # partie rationnelle de r entière
                        tmptxt2+=str(abs(p3[0][0]))
                    elif abs(p3[0][0])!=0:
                        tmptxt2+= '\dfrac{' + str(arrondi(p3[0][0]/gcd(p3[0][0],p3[0][1]))) + '}{' + str(arrondi(p3[0][1]/gcd(p3[0][0],p3[0][1]))) + '}'
                    
                    tmptxt2+=sign
                    
                    delta=p3[0][2]
                    delta=(delta[0]*delta[1],delta[1]*p3[0][1])
                    if abs(delta[1])==1:
                        tmptxt2+='\sqrt{'+str(abs(delta[0]))+'}\\right)'
                    else:
                        tmptxt2+='\dfrac{\sqrt{'+str(abs(delta[0]))+'}}{'+str(abs(delta[1]))+'}\\right)'
    
    return tmptxt2

def racines_multiples(Pstr):
    Plist = Pstr.split('\left(')
    out=Plist[0]
    for x in Plist[1:]:
        if not x in out:
            if Plist.count(x)>1:
                out+='\left('+x+'^{'+str(Plist.count(x))+'}'
            else:
                out+='\left('+x
    
    # Specific case of 'x' factors, which are all together because 0 is the first tested value in racines_evidentes.
    
    out=out.replace('^{}','')
    
    c=1
    while 'x'*c in out:
        c+=1
    if c>2:
        out=out.replace('x'*(c-1),'x^{'+str(c-1)+'}')
    
    return out

def affichage(Pfact):
    global root,image,k,fig,wx,image,polynome,coef_dom
    
    coef_dom=(arrondi(coef_dom[0]/gcd(coef_dom[0],coef_dom[1])),arrondi(coef_dom[1]/gcd(coef_dom[0],coef_dom[1])))
    
    Pdvt=deepcopy(polynome)
    Pdvt=[(arrondi(a[0]/gcd(a[0],a[1])),arrondi(a[1]/gcd(a[0],a[1]))) for a in Pdvt[::-1]]
    
    try:
        wx.clear()
    except NameError:
        fig=matplotlib.figure.Figure(figsize=(6,1),dpi=100)
        wx=fig.add_subplot(111)
        wx.get_xaxis().set_visible(False)
        wx.get_yaxis().set_visible(False)
        
        image = FigureCanvasTkAgg(fig, master=root)
    
    tmptxt1='P(x)='+affichage_polynome(polynome).replace('\left(','').replace('\\right)','')    # forme développée
    
    tmptxt2='='
    
    ### tmptxt2 soit la factorisation ultime
    
    if Pfact==[polynome]:                               # Au cas où aucune racine n'est trouvée
        tmptxt2='='+affichage_polynome(polynome).replace('\left(','').replace('\\right)','')
        
    else:
        if abs(coef_dom[1])==1 and abs(coef_dom[0])!=1:                             # coefficient dominant entier différent de ±1
            tmptxt2+=str(coef_dom[0]*coef_dom[1])
        elif abs(coef_dom[0])==abs(coef_dom[1])==1 and coef_dom[0]*coef_dom[1]==-1: # valant -1
            tmptxt2+='-'
        elif abs(coef_dom[1])!=1:                                                   # fractionnaire
            tmptxt2+='\dfrac{'+str(coef_dom[0])+'}{'+str(coef_dom[1])+'}'
        
        for p3 in Pfact:
            if len(p3[0])==2:                                                        # racines classiques
                tmptxt2+= affichage_polynome(p3)
            
            else:                                                                    # racines de trinômes
                tmptxt2+= affichage_trinome(p3)
                
    tmptxt2=racines_multiples(tmptxt2)
    ### suite de l'affichage
    
    wx.text(0.05,0.7,'$'+tmptxt1+'$')
    wx.text(0.05,0.2,'$'+tmptxt2+'$')
    
    image._tkcanvas.grid(row=0,column=2,rowspan=3*k+4)
    image.draw()
    
    root.update_idletasks()
    root.geometry(str(image._tkcanvas.winfo_width()+max(Degre_label.winfo_width(),LabelsCoef[0].winfo_width())+max(Degre.winfo_width(),barres_fraction[0].winfo_width())) + "x" + str(max(Degre.winfo_height(),Degre_label.winfo_height())+(k+1)*(2*CoefEntries[0][0].winfo_height()+barres_fraction[0].winfo_height())))

def clear_aff():
    global image
    try:
        image._tkcanvas.grid_forget()
    except NameError:
        return None

# =============================================================================
# VARIABLES
# =============================================================================

bg_color='white'

# =============================================================================
# MAIN
# =============================================================================

init()

root.mainloop()
