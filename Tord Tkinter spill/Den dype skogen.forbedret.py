#importere alt mulig rart
from random import randint 
from tracemalloc import stop
import time
import tkinter as tk
from tkinter import font as tkfont  # For fontkontroll
from klasser import *
import pygame 

pygame.init()

# Opprett hovedvinduet vi kan se tekstspillet
root = tk.Tk()
root.title("Den Dype Skogen!")
# Opprett en tekstboks
text_box = tk.Text(root, height=30, width=110)
text_box.configure(bg="white", fg="black")
text_box.pack()

#starten til helten.
helt = Helt(navn = "Frank papirhus", health=100, damage=10)
valg1 = 0
from tkinter import font as tkfont  # For fontkontroll

def vis_tekst(tekst, skrifttype=("Times New Roman", 12, "normal")):
    """
    Viser tekst med en spesifisert font.
    """
    valgt_font = tkfont.Font(family=skrifttype[0], size=skrifttype[1], weight=skrifttype[2])
    text_box.configure(font=valgt_font)
    
    # Skriv teksten i bokstav for bokstav for animasjonseffekt
    for bokstav in str(tekst):
        text_box.insert(tk.END, bokstav)
        text_box.see(tk.END)  # Rull til siste linje
        text_box.update()     # Oppdater GUI
        time.sleep(0.04)

def legg_til_knapp(tekst, kommando):
    knapp = tk.Button(root, text=tekst, command=kommando)
    knapp.pack()
    knapp_liste.append(knapp)

def fjern_knapper():
    for knapp in knapp_liste:
        knapp.pack_forget()
    knapp_liste.clear()

def legg_til_musikk(filnavn, volum=1.0):
    """
    Starter bakgrunnsmusikk.
    Parametere:
        filnavn (str): Stien til lydfilen (MP3 eller OGG).
        volum (float): Volumet for musikken (0.0 til 1.0).
    """
    # Initialiser pygame mixer
    pygame.mixer.init()
    # Last inn musikkfil
    pygame.mixer.music.load(filnavn)
    # Sett volum
    pygame.mixer.music.set_volume(volum)
    # Spill av musikk i loop
    pygame.mixer.music.play(-1)  # -1 betyr at musikken looper
    print(f"Spiller av {filnavn} med volum {volum}")
 
def stopp_musikk():
    """
    Stopper bakgrunnsmusikken.
    """
    pygame.mixer.music.stop()
    print("Musikken er stoppet.")

#kappittel 1 (komme seg til hulen!)
def valg_start():
    
    fjern_knapper()
    text_box.delete("1.0", tk.END)
    legg_til_musikk('skog.mp3', 1)
    vis_tekst("KAPITTEL 1.")
    time.sleep(2)
    text_box.delete("1.0", tk.END)
    vis_tekst("""
Med sverdet i hånden hugger du deg gjennom den tette jungelen. Det er mørkt, og vannet sildrer rundt føttene dine. Rustningen henger tung av vann, og trærne stenger for nesten alt sollys. Det har gått flere dager siden du sist så et menneske, og du merker at du snart trenger ly. De kalde nettene har allerede kostet deg flere menn, og du er redd for at du skal bli den neste. Plutselig legger du merke til en liten åpning i fjellet, ikke større enn en telefonkiosk. Den ser kald ut, men kan gi litt ly for vinden.
          """)
    legg_til_knapp("Søk ly i hulen", valg_hule)
    legg_til_knapp("let videre etter et nytt sted", valg_lete)

def valg_hule():
    fjern_knapper()
    vis_tekst("""
Du kryper inn i den lille hulen og prøver å holde på varmen. Sakte mister du følelsen i både ben og armer. Solen har akkurat gått ned, og temperaturen synker stadig. Det går opp for deg at du ikke kan bli her hele natten, men kulden har svekket deg for mye til å finne et nytt sted. Du husker vagt at du passerte en hule tidligere. Kanskje den var én eller to timer tilbake på stien. Dette gir deg et glimt av håp.
            """)
    legg_til_knapp("prøv å finne den andre hulen", valg_lete_etter_hule)
    legg_til_knapp("bli værende(håpe du overlever nattens kulde)", valg_bli_i_hulen)

def valg_lete_etter_hule():
    fjern_knapper()
    vis_tekst("""
Du kjemper deg ut av hulen, beina er svekket av kulden, så du må krabbe. Skogen virker helt ukjent rundt deg, og du blr plutselig usikker på veien. Trærene rundt deg virker nesten levende, og det føles ut som de griper etter deg mens du krabber gjennom skogen. Sakte merker du at varmen returnerer til kroppen, og du får kjempet deg på beina. Kroppen er utmamattet, det eneste som holder deg i gang er adrenalitet. Etter flere timer merker du at hope svinner hend, og du er klar for å gi opp. Samtidig som du faller over av utmattelse ser du omrisse noe langs fjellet. Du bruker dine siste krefter på å krabbe deg inn i hulen, og slukner på sekunde. 
         """)
    legg_til_knapp("trykk for å fortsette spillet", kappitell_2)

def valg_bli_i_hulen():
    fjern_knapper()
    vis_tekst("""
Du blir liggende mens mørket legger seg rundt deg. Du klarer nesten ikke å bevege deg lenger. Gradevis mister du motorikkern i alle kropsdeler. plutselig mister du synet, og et eneste du hører er hjertet ditt som pumper saktere og saktere. Før plutselig det også blir stille.
              
              GAME OVER
              
         """)

def valg_lete():
    fjern_knapper()
    vis_tekst("""
Du går videre, og merker at føttende dine starte å miste følelsen. Plutselig legger det seg en skygge over deg i det solen går ned. I desperasjonens og kuldens øyeblikk husker du en hule, bare noen timer tilbake på stien. Du hadde tidligere valgt å gå forbi på grunn av en grusom lukt som kom fra hulen. lukten kunne minne om et råtnende dyr, men hulen var kanskje den eneste varme muligheten. Skogen var tykkere enn suppe, så det å finne et nytt sted virket vanskelig. 
""")
    legg_til_knapp("prøv å finne hulen du har gått forbi",valg_finne_hulen)
    legg_til_knapp("Lett videre, selv om det er dårlig sikt", valg_klatre)

def valg_klatre():
    fjern_knapper()
    vis_tekst("""
Du går videre. Rundt deg blir skogen tykkere og tykkere. plutselig merker du at du ikke vet hvor du kom fra. trærne rundt deg så både kjente og ukjente ut på samme tid. Du vet ikke om du går i sirkel eller ikke. Hver gang du ser noe som ser litt kjent ut mister du troen på at du noen gang skal finne veien ut. Du merker at beina blir tyngre, og alt følels vanskeligere. Du gjør et siste forsøk ved å klatre opp i et tre, men utmatelsen tar deg på vei opp, og du mister kontrollen over armene. plutselig merker du at du faller, og greinene forsvinner over deg.

            GAME OVER 
""")

def valg_finne_hulen():
    fjern_knapper()
    vis_tekst("""
Du prøver å finne veien tilbake til hulen ved å se etter avkappete greiner og kvister. Det er lenger enn du husker og beina begynner å bli slitene, men plutselig ser du en skygge langs fjellveggen, du kjemper deg bort, og ser en liten hule forann deg. utmattet legger du deg ned, og slukner på sekundet. 
""")
    legg_til_knapp("trykk for å fortsette spillet(Kappitell 2)", kappitell_2)

#Kapitell 2 (kjempe seg gjennom hulen)

def kappitell_2():
    fjern_knapper()
    stopp_musikk()
    legg_til_musikk("hule.mp3",1)
    text_box.delete("1.0", tk.END)
    vis_tekst("KAPITTEL 2.")
    time.sleep(2)
    text_box.delete("1.0", tk.END)
    vis_tekst("""
Du våkner av en forferdelig stank, og når du ser til høyre ser du rett inn i noen enorme øyne. Du spretter tilbake med et skrik og klamrer til veggen. Den er hard og kald. ved beina dine ligger et stor loddent dyr. Det kan minne om en stor katt, men ansiktet er så deformert at du ikke er sikker. På siden av dyret er det et gapende hull med involder og tarmer hengende ut. Det går sakte opp for deg at dyret ikke lenger er en trussel. Når du ser opp merker du at hulen er mye større enn du trodde. I lyset fra morgensolen kan du se langt inn i hulen før den tar en sving til høyre. Det kommer en syngende lyd ut av hulen, og du får veldig lyst til å se hva det er. Du skal bare en liten tur, så du er usikker på om du skal ta med sverdet. Du er fortsatt sliten, så den tynger deg ned mer enn den hjelper.
""")
    legg_til_knapp("Ta med sverdet", sverd_oppplukking)
    legg_til_knapp("La sverdet ligge", uten_sverd)

def sverd_oppplukking():
    fjern_knapper()
    #sverd = Gjenstander("sverd")
    helt.wepons = 10

    vis_tekst("""
Du plukker opp sverdet og kjenner tyngden.
             """)
    legg_til_knapp("Fortsett", uten_sverd)


def uten_sverd():
    fjern_knapper()
    vis_tekst("""
Du går forsiktig inn i hulen, det blir mørkere og mørkere rundt deg. Den syngende lyden skjønner du fort at bare er vinden som blåser gjennom hulen. Når du kommer rundt hjørnet ser du inn i en vegg. Det var ingen ting! I det du kjenner roen bre seg i kroppen, hører du et høyt brak før du kjenner gulvet forsvinne under beina dine. I et par sekunder kjenner du luften fly forbi ørene dine før beina smeller mot bakken. Du ligger et øyeblikk på bakken, før du stavrer deg på beina. du har ingen sjanse til å komme deg tilbake opp. Veggene er høye og bratte rundt deg. forran deg fortsetter hulen dypt innover, i ennen ser du et lite lys. kan det være utgangen?
              """)
    legg_til_knapp("gå mot utgangen", gå_videre)

def gå_videre():
    fjern_knapper()
    vis_tekst("""
Du beveger deg sakte gjennom hulen, både fordi det er mørkt, men også fordi du er usikker på hva du kommer til å finne. Mens du går der i stillheten tenker tilbake på alt som har skjedd. Det var bare drøye 3 måneder siden du hadde forlat London med et fult mannskap, og et av Englands flotteste skip.  Reisen hadde såvidt begynt før de startet å få problemer. På veien over havet til Afrika hadde skipet møtt på et grusomt uvæer, og flere gode menn hadde gått tapt. Når uværet hadde lagt seg fire dager senere hadde skippet blitt dratt langt fra den opprinelige kursen. De neste to månedene gikk forbi uten  at noen så tegn på land. i starten av månede 3 hadde alt av proviant blitt spist opp, og manskapet så værre ut enn noen gang. Når skipet traff land 4 dager senere var det kun 8 igjen....
             """)
    vis_tekst("""
Når du nærmer deg lyset blir du plutselig oppmerksom på en lyd. Mellom lyden av dråper som renner over stein, og skrittende som dunker mellom huleveggene hører du en lyd som kan minne om jern som blir slått mot stein. Lyden vokser høyere jo nærmere du kommer. Du går rundt et siste hjørnet og står plutselig ansikt til ansikt med groteskt vesen. Det kan minne om et menneske, men ikke noe menneske du har sett før. kroppen er dekket i store svarte sår, og huden er tykere enn barken på et tre. til å være så lite ser vesenet imponerende kraftig ut. Øynene er stikkende, og fulle av hat og død. 
              """)
    legg_til_knapp("gjør deg klar til kamp", kamp_lett)
    legg_til_knapp("prøv å løp", valg_løpe)

def valg_løpe():
    fjern_knapper()
    text_box.delete("1.0", tk.END)

    if helt.wepons == 10:
        vis_tekst("""
Du snur deg om, og legger på sprang. Bakken under deg føles ustødig, og sverdet føles tyngre enn noen gang. Du nærmer deg hullet du falt gjennom, men du vet du ikke kan komme deg opp. Plutselig skjenner du at sverdet henger fast i siden av hulen. Med et rykk blir du kastet fremmover, og monsteret hopper over deg. Du prøver å gripe etter sverdet ditt, men orken holder deg nede. Det siste du ser er et sylskarpt sverd som flyr mot deg. 
                
                GAME OVER
            """)
    else:
        vis_tekst("""
Du snur deg om, og legger på sprang. Bakken under deg føles ustødig, men du er lett til beins. Du kommer fort tilbake til deg du falt gjennom taket, men det er fortsatt for langt opp. Det er en annen vei du kan løpe. Det er mørkt, men du forstetter nedover en bratt bakke. Bak deg hører du pusten til monsteret, den høres tung og sliten ut. Veien foran deg blir bare farligere og farligere, på din høyre side ser det en skrent som leder til en sikker død. 
""")
        global valg1
        valg1 = 5
        legg_til_knapp ("prøv å ta orken, han er sliten", kamp_lett)
        legg_til_knapp("orken er sliten, så du kan løpe fra han, men veien er veldig farlig", løpe_langs_skrent)
        

def løpe_langs_skrent():
    fjern_knapper()
    vis_tekst("""
Du løper videre langs kanten, veien blir trngere, og du merker dypet under deg lokke på deg. Bak deg hører du monsteret komme nærmere. Hjertet starter å banke fortere, du prøver å løpe så fort veien lar deg løpe. Veien har nå blitt så tynn at du må gå sidelengs for å ikke falle av. Når du ser bak deg ser du rett inn i de gruomme øynene som stritter mot deg. synet får deg til å skvette så mye at du mister forfestet. Plutselig merker du at du faller. det siste du ser er mørket som omgir deg, og de grufulle hylebene til monsteret...

              GAME OVER 
""")
def kamp_lett():
    stopp_musikk()
    legg_til_musikk("normal kamp musik.mp3",1)
    text_box.delete("1.0", tk.END)
    fjern_knapper()
    vis_tekst("kampen har startet, vær forsiktig")

    def dodge():
        fjern_knapper()
        dodge = randint (0,10)
        if dodge > 5:
            attack = randint(0,helt.damage) + randint(0,helt.wepons)
            vis_tekst("""
Du klarte å smette unna. Monsteret mister balansen. Du har muligheten til å få inn et slag
            """)
            vis_tekst(f"""
Du slår han i ryggen og tar {attack} skade
            """)
            ork.health-= attack
            legg_til_knapp("fortsett",kamp_main)
        else:
            attack = randint(0,ork.damage)
            vis_tekst("""
Du prøver å hoppe unna, men han får tak i deg, og slår deg hardt ned i bakken
                    """)
            vis_tekst(f"""
angrepet tok {attack}skade!
                    """)
            helt.health -= attack
            legg_til_knapp("fortsett",kamp_main)

    def attack():
            fjern_knapper()
            attack = randint(0,helt.damage) + randint(0,helt.wepons)
            vis_tekst(f"""
Du slo han med en skade som tilsvarer {attack}
            """)
            ork.health -= attack
            attack = randint(0,ork.damage)
            vis_tekst(f"""
han slo deg tilbake og tok {attack} liv av deg
                    """)
            helt.health -= attack
            legg_til_knapp("fortsett",kamp_main)
    
    def block():
        fjern_knapper()
        attack = randint(0,ork.damage)-randint(0,10)
        if attack < 0:
            attack = 0
        vis_tekst(f"""
Orken hopper mot deg, og du prøver å blockere det. Du klarer såvidt å blokkere slaget. Orken tar bare {attack} skade av deg
        """)
        helt.health -= attack

        if attack <= 0:
            vis_tekst("""
Siden du parerte perfekt klarer du å få inn et perfekt slag som          
            """)
            legg_til_knapp("fortsett",kamp_main)

        elif attack < 5 and attack >= 0:
            attack = randint(0,(helt.damage+helt.wepons))*1.5
            vis_tekst(f"""
Du slår han ut av balanse, og klarer å få inn ett ekstra bra slag som gjør {attack} skade
            """)
            ork.health -= attack
            legg_til_knapp("fortsett",kamp_main)

        elif attack > 5 and attack < 15:
            attack = randint(0,(helt.damage+helt.wepons))
            vis_tekst(f"""
Du får inn et normalt slag som gjør {attack} skade
            """)
            ork.health -= attack
            legg_til_knapp("fortsett",kamp_main)

        else:
            vis_tekst ("""
Når du blokkerer slaget flyr du ut av balanse. Dette fører til at du ikke får inn et eget slag 
            """)
            legg_til_knapp("fortsett",kamp_main)

    def kamp_main():
        text_box.delete("1.0", tk.END)
        fjern_knapper()
        if ork.health > 0 and helt.health > 0:

            if helt.health > 40:
                vis_tekst(f"""
Du har ganske mye liv {helt.health}, og orken har {ork.health} liv igjen""")
                time.sleep(0.5)
                vis_tekst("""
Orken kommer mot deg igjen!
                        """)
                legg_til_knapp ("prøv å hoppe unna angrepet",dodge)
                legg_til_knapp("angrip han tilbake", attack)
                legg_til_knapp("prøv å blokker slaget", block)
            elif helt.health > 20:
                vis_tekst(f"""
Du begynner å få mindre liv {helt.health}, orken har {ork.health} liv igjen
                          """)
                time.sleep(0.5)
                vis_tekst("""
Orken kommer mot deg igjen!
                        """)
                legg_til_knapp ("prøv å hoppe unna angrepet",dodge)
                legg_til_knapp("angrip han tilbake", attack)
                legg_til_knapp("prøv å blokker slaget", block)
            else:
                vis_tekst(f"""
Vær forsiktig, du har veldig lite liv {helt.health}, orken har {ork.health} liv igjen
                            """)
                time.sleep(0.5)
                vis_tekst("""
Orken kommer mot deg igjen!
                        """)
                legg_til_knapp ("prøv å hoppe unna angrepet",dodge)
                legg_til_knapp("angrip han tilbake", attack) 
                legg_til_knapp("prøv å blokker slaget", block)
        
        elif ork.health > 0 and helt.health <= 0:
            vis_tekst("""
        Med et hardt sverdhugg blir du slått i bakken. Monsteret kommer over deg, og slår deg hardt i hode
                    
                    GAME OVER""")
        
        elif ork.health <= 0 and helt.health > 0:
            vis_tekst("""
Du løper mot han og sparker han hardt i magen. I smerte faller han om på bakken. Før han rekker å reise seg opp, hugger du av han hode
            """)
            legg_til_knapp("gå videre i hulen", kappittel_3)

    if valg1 == 0:
        ork = Vesner("Ork", 50, 20)
    elif valg1 == 5:
        ork = Vesner("ork", 20, 18)
    
    legg_til_knapp("fortsett",kamp_main)

#Kappittel 3!

def kappittel_3():
    text_box.delete("1.0", tk.END)
    stopp_musikk()
    fjern_knapper()
    legg_til_musikk("hulelyder.mp3",1)
    vis_tekst("KAPITTEL 3.")
    time.sleep(2)
    text_box.delete("1.0", tk.END)
    if helt.health > 50:
        vis_tekst("""
Hode til orken ligger livløst på bakken. 
    """)
    else:
        vis_tekst("""
Hode til orken ligger livløst på bakken. Du er fortsatt fanget i hulen. 
    """) 

# Start spillet
knapp_liste = []

vis_tekst("Dette spillet setter alle evnene dine på prøve. Målet er å overleve, og komme seg tilbake til tryghet. Et feil valg kan ende med døden, så du må være forsiktig!")
legg_til_knapp("Trykk her for å starte spillet",valg_start)

# Start GUI-løkken
root.mainloop()