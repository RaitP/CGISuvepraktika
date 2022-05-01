# vajalikud impordid
from bs4 import BeautifulSoup
import requests
import datetime
from tkinter import *

# definitsioon ööpikkus, saab sisendiks päeva ja dokumendi
# definitsioon tagasatab öö pikkuse
def ööpikkus(kuupäev,doc):
    # dokumiendist otsikase vajalik html-i lause, mis sisaldab vajalikku infot
    # valisin lauseks, mida otsin, päeva pikkuse
    kell = doc.select("#as-monthsun > tbody > tr:nth-child("+ kuupäev +") > td.c.tr.sep-l")
    # muudan saadud tulemuse sõneks, et seal hõlpsamini infot saada
    kell = str(kell)
    # valin vajailku osa sõnest (päeva pikkuse) 
    päevapikkus = kell[(len(kell)-14):-len('</td> ')]
    # jagan kella kolmeks tunnid minutid sekundid
    osad = päevapikkus.split(":")
    # teen viin kogu kella sekundi kujule
    päevapikkus = int(osad[0])*60*60 + int(osad[1])*60 + int(osad[2])
    # lahutan 24h ehk 86400 sekundist päevakestvuse aja ja saan öö pikkuse
    ööpikkus = 86400 - päevapikkus
    # viin öö pikkuse sekundid paremini loetavale kujule (tunnid:minutid:sekundid)
    vastus = str(datetime.timedelta(seconds=ööpikkus))
    # tagastan öö pikkuse
    return vastus

# definitsioon astroniimilineKoidik, saab sisendiks päeva ja dokumendi
# definitsioon tagasatab astroniimilise koidiku alguse
def astroniimilineKoidik(kuupäev,doc):
    # dokumiendist otsikase vajalik html-i lause, mis sisaldab vajalikku infot
    # valisin lauseks, mida otsin, astronoomilse kodiku alguse
    koidik = doc.select("#as-monthsun > tbody > tr:nth-child("+ kuupäev +") > td:nth-child(6)")
    # muudan saadud tulemuse sõneks, et seal hõlpsamini infot saada
    kell = str(koidik)
    # valin vajailku osa sõnest (astronoomilise koidiku alguse) 
    vastus = kell[(len(kell)-11):-len('</td> ')]
    # tagastan vastuse
    return vastus

# definitsioon astroniimilineKoidikLõpp, saab sisendiks päeva ja dokumendi
# definitsioon tagasatab astroniimilise koidiku lõpu
def astronoomiliseKoidikuLõpp(kuupäev,doc):
    # dokumiendist otsikase vajalik html-i lause, mis sisaldab vajalikku infot
    # valisin lauseks, mida otsin, astronoomilse kodiku lõppu
    koidikuLõpp = doc.select("#as-monthsun > tbody > tr:nth-child("+ kuupäev +") > td:nth-child(7)")
    # muudan saadud tulemuse sõneks, et seal hõlpsamini infot saada
    kell = str(koidikuLõpp)
    # valin vajailku osa sõnest (astronoomilise koidiku lõpu) 
    vastus = kell[(len(kell)-11):-len('</td> ')]
    # tagastan vastuse
    return vastus

# definitsioon astroniimilineKoidik, ei saa sisendeid
# definitsioon väljastab GUI-le soovitud andmed
def sisestus():
    # viin kordinaadid sobivasse kujusse ja muudan sõneks, et saada vajalik info veebilehelt
    kordinaat = str(kordinaadidLatitude.get()) + "," + str(kordinaadidLongitude.get())

    # lisan url-ile vajalikud andmed: kordinaadid, kuu ja aasta, mille saan GUI-st
    url = "https://www.timeanddate.com/sun/@" + kordinaat + "?month=" + str(kuu.get()) + "&year=" + str(aasta.get())
    # saan url-i lehe koodi
    result = requests.get(url)
    # muudan selle html-i põhiseks
    doc = BeautifulSoup(result.text, "html.parser")

    # väljastan vastuse GUI-s
    ööPikkusOn = Label(text="Öö pikkus on")
    vastusPikkus = Label(text=ööpikkus(str(päev.get()), doc))
    ööPikkusOn.grid(row=4,column=0)
    vastusPikkus.grid(row=4,column=1)

    koidikAlgus = Label(text="Astronoomiline koidik algab kell")
    vastusAlgus = Label(text = astroniimilineKoidik(str(päev.get()), doc))
    koidikAlgus.grid(row=5,column=0)
    vastusAlgus.grid(row=5,column=1)

    koidikLõpp = Label(text="Astronoomiline koidik lõppeb kell")
    vastusLõpp = Label(text = astronoomiliseKoidikuLõpp(str(päev.get()), doc))
    koidikLõpp.grid(row=6,column=0)
    vastusLõpp.grid(row=6,column=1)

# loon akna
aken = Tk()

# lisan aknale kordinaadi sisestuse
kordinaadiSisestus = Label(text="Sisestage kordinaadid ", font=50)
kordinaadiSisestus.grid(row=0,column=0)
kordinaadidLatitude = Entry()
kordinaadidLatitude.grid(row=0,column=1)
kordinaadidLongitude = Entry()
kordinaadidLongitude.grid(row=0,column=2)

# lisan aknale kuupäeva sisestuse
aastaSisestus = Label(text="aasta", font=50)
kuuSisestus = Label(text="kuu", font=50)
päevaSisestus = Label(text="päev", font=50)
aastaSisestus.grid(row=1,column=1)
kuuSisestus.grid(row=1,column=2)
päevaSisestus.grid(row=1,column=3)
kuupäevaSisestus = Label(text="Sisestage kuupäev ", font=50)
kuupäevaSisestus.grid(row=2,column=0)
aasta = Entry()
aasta.grid(row=2,column=1)
kuu = Entry()
kuu.grid(row=2,column=2)
päev = Entry()
päev.grid(row=2,column=3)

# lisan aknale nupu, mis edastaks saadud andmed sisestus definitsiooni
edasta = Button(aken, text="Edasta", command=sisestus)
edasta.grid(row=3,column=3)
aken.mainloop()

# Autor: Rait Pommer
