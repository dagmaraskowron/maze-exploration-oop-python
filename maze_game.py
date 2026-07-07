import random

class Przedmiot:
    def __init__(self, id, nazwa, opis):
        self.id = id
        self.nazwa = nazwa
        self.opis = opis

    def sprawdz(self):
        print(f"- {self.nazwa}")
        print(f"   {self.opis}")

class Klucz(Przedmiot):
    def __init__(self, id, nazwa, opis):
        super().__init__(id, nazwa, opis)
        self.id_drzwi = id

    def sprawdz(self):
        super().sprawdz()
        print(f"   Otwiera drzwi #{self.id_drzwi}")

class Skarb(Przedmiot):
    def __init__(self, id, nazwa, opis, wartosc):
        super().__init__(id, nazwa, opis)
        self.wartosc = wartosc

    def sprawdz(self):
        super().sprawdz()
        print(f"   Wartosc: {self.wartosc}")

class Stworzenie:
    def __init__(self, id, nazwa, opis):
        self.id = id
        self.nazwa = nazwa
        self.opis = opis

    def sprawdz(self):
        print(f"- {self.nazwa}")
        print(f"   {self.opis}")

class Zlodziej(Stworzenie):
    def __init__(self, id):
        super().__init__(id, "Zlodziej", "Moze cos ukrasc")

    def ukradnij(self, gracz, przedmiot):
        if przedmiot in gracz.ekwipunek:
            gracz.ekwipunek.remove(przedmiot)
            print(f"Zlodziej ukradl ci przedmiot: {przedmiot.nazwa}")

    def spotkaj_gracza(self, gracz):
        if gracz.ekwipunek:
            przedmioty_kradzione = [e for e in gracz.ekwipunek if isinstance(e, Skarb)]
            if przedmioty_kradzione:
                przedmiot = random.choice(przedmioty_kradzione)
                self.ukradnij(gracz, przedmiot)
        else:
            print("Zlodziej nie znalazl nic do kradziezy.")

class Przejscie:
    def __init__(self, id, nastepna_komnata):
        self.id = id
        self.nastepna_komnata = nastepna_komnata

    def czy_mozna_przejsc(self, gracz):
        return True

class Drzwi(Przejscie):
    def __init__(self, id, poprzednia_komnata, nastepna_komnata):
        super().__init__(id, nastepna_komnata)
        self.poprzednia_komnata = poprzednia_komnata
        if self not in self.nastepna_komnata.przejscia_powrotne:
            self.nastepna_komnata.przejscia_powrotne.add(self)
        self.czy_otwarte = False

    def otworz(self, gracz):
        if self.czy_otwarte:
            print("Drzwi juz sa otwarte.")
            return
        for przedmiot in gracz.ekwipunek:
            if isinstance(przedmiot, Klucz) and przedmiot.id_drzwi == self.id:
                self.czy_otwarte = True
                print("Uzyto klucza do otwarcia drzwi.")
                return
        print("Nie masz odpowiedniego klucza do tych drzwi.")

    def zamknij(self):
        self.czy_otwarte = False

    def czy_mozna_przejsc(self, gracz):
        return self.czy_otwarte

class Komnata:
    def __init__(self, id, nazwa, opis):
        self.id = id
        self.nazwa = nazwa
        self.opis = opis
        self.przejscia = []
        self.przejscia_powrotne = set()
        self.przedmioty = []
        self.stworzenia = []

    def dodaj_przedmiot(self, przedmiot):
        self.przedmioty.append(przedmiot)

    def usun_przedmiot(self, przedmiot):
        if przedmiot in self.przedmioty:
            self.przedmioty.remove(przedmiot)

    def dodaj_stworzenie(self, stworzenie):
        self.stworzenia.append(stworzenie)

    def usun_stworzenie(self, stworzenie):
        if stworzenie in self.stworzenia:
            self.stworzenia.remove(stworzenie)

class Mapa:
    def __init__(self):
        self.id = 1
        self.komnaty = []

    def znajdz_komnate(self, id):
        a = [k for k in self.komnaty if k.id == id]
        return a[0] if a else None

    def wyswietl_mape(self):
        print("\n MAPA LABIRYNTU ")
        for komnata in self.komnaty:
            print(f"\nKomnata #{komnata.id}: {komnata.nazwa}")

            if komnata.przejscia:
                print("  Przejscia:")
                for p in komnata.przejscia:
                    typ = "Drzwi" if isinstance(p, Drzwi) else "Przejscie"
                    status = "(otwarte)" if isinstance(p, Drzwi) and p.czy_otwarte else "(zamkniete)" if isinstance(p, Drzwi) else ""
                    print(f"  - {typ} #{p.id} -> Komnata {p.nastepna_komnata.id} {status}")

            if komnata.przejscia_powrotne:
                print("  Przejścia powrotne:")
                for p in komnata.przejscia_powrotne:
                    typ = "Drzwi" if isinstance(p, Drzwi) else "Przejście"
                    status = "(otwarte)" if isinstance(p, Drzwi) and p.czy_otwarte else "(zamknięte)" if isinstance(p, Drzwi) else ""
                    print(f"  - {typ} #{p.id} <- Komnata {p.poprzednia_komnata.id} {status}")

class Gracz:
    def __init__(self):
        self.id = 0
        self.aktualna_komnata = None
        self.ekwipunek = []

    def przejdz(self, id_przejscia):
        przejscie = [p for p in self.aktualna_komnata.przejscia if p.id == id_przejscia]
        if przejscie:
            if przejscie[0].czy_mozna_przejsc(self):
                self.aktualna_komnata = przejscie[0].nastepna_komnata
                print(f"Przechodzisz do: {self.aktualna_komnata.nazwa}.")

                for s in self.aktualna_komnata.stworzenia:
                    if isinstance(s, Zlodziej):
                        s.spotkaj_gracza(self)
            else:
                if isinstance(przejscie[0], Drzwi):
                    print("Drzwi sa zamkniete.")
                else:
                    print("Nie mozesz przejsc przez to przejscie.")
        else:
            przejscia_powrotne = [p for p in self.aktualna_komnata.przejscia_powrotne if p.id == id_przejscia]
            if przejscia_powrotne:
                if przejscia_powrotne[0].czy_mozna_przejsc(self):
                    self.aktualna_komnata = przejscia_powrotne[0].poprzednia_komnata
                    print(f"Przechodzisz do: {self.aktualna_komnata.nazwa}.")
                else:
                    if isinstance(przejscia_powrotne[0], Drzwi):
                        print("Drzwi sa zamkniete.")
                    else:
                        print("Nie mozesz przejsc przez to przejscie.")
            else:
                print(f"Nie znaleziono przejscia #{id_przejscia}.")

    def otworz_drzwi(self, id_drzwi):
        drzwi = [d for d in self.aktualna_komnata.przejscia + [x for x in self.aktualna_komnata.przejscia_powrotne] if isinstance(d, Drzwi) and d.id == id_drzwi]
        if drzwi:
            drzwi[0].otworz(self)
            if drzwi[0].czy_otwarte:
                print(f"Drzwi #{id_drzwi} otwarte.")
        else:
            print(f"Nie znaleziono drzwi #{id_drzwi}.")

    def zamknij_drzwi(self, id_drzwi):
        drzwi = [d for d in self.aktualna_komnata.przejscia + [x for x in self.aktualna_komnata.przejscia_powrotne] if isinstance(d, Drzwi) and d.id == id_drzwi]
        if drzwi:
            drzwi[0].zamknij()
            print(f"Drzwi #{id_drzwi} zamkniete.")
        else:
            print(f"Nie znaleziono drzwi #{id_drzwi}.")

    def rozejrzyj_sie(self):
        print(f"Jestes w: {self.aktualna_komnata.nazwa}")
        print(self.aktualna_komnata.opis)

        print("Przejscia:")
        for p in self.aktualna_komnata.przejscia:
            print(f"- {'Drzwi' if isinstance(p, Drzwi) else 'Przejscie'} #{p.id}")

        print("Przejscia powrotne:")
        for p in self.aktualna_komnata.przejscia_powrotne:
            print(f"- {'Drzwi' if isinstance(p, Drzwi) else 'Przejscie'} #{p.id}")

        print("Przedmioty:")
        if self.aktualna_komnata.przedmioty:
            for p in self.aktualna_komnata.przedmioty:
                p.sprawdz()
        else:
            print("Brak przedmiotow.")

        print("Stworzenia:")
        if self.aktualna_komnata.stworzenia:
            for s in self.aktualna_komnata.stworzenia:
                s.sprawdz()
        else:
            print("Brak stworzen.")

    def sprawdz_przedmiot(self, id_przedmiotu):
        for x in [p for p in self.ekwipunek if p.id == id_przedmiotu]:
            x.sprawdz()

    def wez(self, przedmiot):
        self.ekwipunek.append(przedmiot)

    def poloz(self, przedmiot):
        if przedmiot in self.ekwipunek:
            self.ekwipunek.remove(przedmiot)
            self.aktualna_komnata.dodaj_przedmiot(przedmiot)
            print(f"Polozono przedmiot: {przedmiot.nazwa}")
        else:
            print("Nie masz takiego przedmiotu.")


class Gra:
    def __init__(self):
        self.id = 1
        self.nazwa = "Gra"
        self.gracz = None
        self.mapa = None
        self.czy_trwa = False

    def generuj_mape(self):
        m = Mapa()
        m.id = 1
        m.komnaty = []

        k1 = Komnata(1, "Komnata 1", "Opis komnaty 1")
        k2 = Komnata(2, "Komnata 2", "Opis komnaty 2")
        k3 = Komnata(3, "Komnata 3", "Opis komnaty 3")
        k4 = Komnata(4, "Komnata 4", "Opis komnaty 4")
        k5 = Komnata(5, "Komnata 5", "Opis komnaty 5")
        k6 = Komnata(6, "Komnata 6", "Opis komnaty 6")
        k7 = Komnata(7, "Komnata 7", "Opis komnaty 7")

        k1.przejscia.append(Drzwi(1, k1, k2))
        k1.przejscia.append(Przejscie(2, k3))
        k3.przejscia.append(Drzwi(3, k3, k4))
        k3.przejscia.append(Przejscie(4, k5))
        k4.przejscia.append(Przejscie(5, k7))
        k5.przejscia.append(Drzwi(6, k5, k4))
        k5.przejscia.append(Przejscie(7, k1))
        k6.przejscia.append(Drzwi(8, k6, k7))
        k6.przejscia.append(Przejscie(9, k1))

        k1.dodaj_przedmiot(Klucz(1, "Klucz 1", "Opis klucza 1"))
        k3.dodaj_przedmiot(Klucz(3, "Klucz 3", "Opis klucza 3"))
        k5.dodaj_przedmiot(Klucz(6, "Klucz 6", "Opis klucza 6"))
        k1.dodaj_przedmiot(Klucz(8, "Klucz 8", "Opis klucza 8"))
        k2.dodaj_przedmiot(Skarb(10, "Skarb 1", "Złoty skarb", 100))
        k4.dodaj_przedmiot(Skarb(11, "Skarb 2", "Srebrny skarb", 50))

        k3.dodaj_stworzenie(Zlodziej(1))
        k5.dodaj_stworzenie(Zlodziej(2))

        m.komnaty = [k1, k2, k3, k4, k5, k6, k7]
        return m

    def przesun_stworzenia(self):
        for komnata in self.mapa.komnaty:
            for stworzenie in komnata.stworzenia[:]:
                mozliwe_przejscia = komnata.przejscia + [x for x in getattr(komnata, "przejscia_powrotne", [])]
                if mozliwe_przejscia and mozliwe_przejscia[0].czy_mozna_przejsc(None) and random.choice([True, False]):
                    przejscie = random.choice(mozliwe_przejscia)
                    nowa_komnata = przejscie.nastepna_komnata
                    komnata.usun_stworzenie(stworzenie)
                    nowa_komnata.dodaj_stworzenie(stworzenie)

    def dostepne_polecenia(self):

        aktualna = self.gracz.aktualna_komnata
        dostepne = []

        dostepne.append("mapa")
        dostepne.append("rozejrzyj sie")
        dostepne.append("koniec")

        klucze_w_komnacie = [k for k in aktualna.przedmioty if isinstance(k, Klucz)]
        skarby_w_komnacie = [s for s in aktualna.przedmioty if isinstance(s, Skarb)]
        if klucze_w_komnacie:
            dostepne.append("wez klucz")
        if skarby_w_komnacie:
            dostepne.append("wez skarb")

        dostepne.append("sprawdz klucze")
        dostepne.append("sprawdz skarby")
        dostepne.append("sprawdz ekwipunek")

        klucze_w_ekwipunku = [k for k in self.gracz.ekwipunek if isinstance(k, Klucz)]
        skarby_w_ekwipunku = [s for s in self.gracz.ekwipunek if isinstance(s, Skarb)]
        if klucze_w_ekwipunku:
            dostepne.append("poloz klucz")
        if skarby_w_ekwipunku:
            dostepne.append("poloz skarb")

        wszystkie_przejscia = aktualna.przejscia + [x for x in getattr(aktualna, "przejscia_powrotne", [])]
        for p in wszystkie_przejscia:
            if isinstance(p, Drzwi):
                if not p.czy_otwarte:
                    dostepne.append(f"otworz drzwi {p.id}")
                else:
                    dostepne.append(f"zamknij drzwi {p.id}")
                if p.czy_mozna_przejsc(None):
                    dostepne.append(f"przejdz drzwi {p.id}")
            else:
                dostepne.append(f"przejdz przejscie {p.id}")

        return dostepne

    def rozpocznij(self):
        self.czy_trwa = True
        self.mapa = self.generuj_mape()
        self.gracz = Gracz()
        self.gracz.aktualna_komnata = self.mapa.znajdz_komnate(1)

        while self.czy_trwa:
            dostepne = self.dostepne_polecenia()
            print("\nDostępne polecenia:")
            for a, b in enumerate(dostepne, start=1):
                print(f"{a}. {b}")
            wybor = input("Wybierz polecenie - numer lub pełne polecenie: ").strip()

            if wybor.isdigit():
                numer = int(wybor)
                if 1 <= numer <= len(dostepne):
                    polecenie = dostepne[numer - 1]
                else:
                    print("Niepoprawny numer polecenia")
                    continue
            else:
                polecenie = wybor

            self.przetworz_polecenie(polecenie)
            self.przesun_stworzenia()

    def przetworz_polecenie(self, polecenie):
        polecenie = polecenie.strip().lower()
        sp = polecenie.split()
        polecenie_poprawne = False

        if len(sp) == 1:
            if sp[0] == "koniec":
                self.zakoncz()
                polecenie_poprawne = True
            elif sp[0] == "mapa":
                self.mapa.wyswietl_mape()
                polecenie_poprawne = True
        elif len(sp) == 2:
            if sp[0] == "rozejrzyj" and sp[1] == "sie":
                self.gracz.rozejrzyj_sie()
                polecenie_poprawne = True
            elif sp[0] == "wez":
                p = sp[1]
                if p == "klucz":
                    polecenie_poprawne = True
                    klucze_w_komnacie = [k for k in self.gracz.aktualna_komnata.przedmioty if isinstance(k, Klucz)]
                    if klucze_w_komnacie:
                        self.gracz.wez(klucze_w_komnacie[0])
                        self.gracz.aktualna_komnata.usun_przedmiot(klucze_w_komnacie[0])
                        print(f"Wzięto klucz {klucze_w_komnacie[0].nazwa}")
                    else:
                        print("Nie ma klucza w tej komnacie.")
                elif p == "skarb":
                    polecenie_poprawne = True
                    skarby_w_komnacie = [k for k in self.gracz.aktualna_komnata.przedmioty if isinstance(k, Skarb)]
                    if skarby_w_komnacie:
                        self.gracz.wez(skarby_w_komnacie[0])
                        self.gracz.aktualna_komnata.usun_przedmiot(skarby_w_komnacie[0])
                        print(f"Wzięto skarb {skarby_w_komnacie[0].nazwa}")
                    else:
                        print("Nie ma skarbu w tej komnacie.")
            elif sp[0] == "sprawdz":
                if sp[1] == "klucze":
                    polecenie_poprawne = True
                    klucze_w_ekwipunku = [k for k in self.gracz.ekwipunek + self.gracz.aktualna_komnata.przedmioty if isinstance(k, Klucz)]
                    if klucze_w_ekwipunku:
                        for k in klucze_w_ekwipunku:
                            self.gracz.sprawdz_przedmiot(k.id)
                    else:
                        print("Nie masz kluczy")
                elif sp[1] == "skarby":
                    polecenie_poprawne = True
                    skarby_w_ekwipunku = [k for k in self.gracz.ekwipunek + self.gracz.aktualna_komnata.przedmioty if isinstance(k, Skarb)]
                    if skarby_w_ekwipunku:
                        for k in skarby_w_ekwipunku:
                            self.gracz.sprawdz_przedmiot(k.id)
                    else:
                        print("Nie masz skarbów")
                elif sp[1] == "ekwipunek":
                    polecenie_poprawne = True
                    if self.gracz.ekwipunek:
                        print("Ekwipunek:")
                        for p in self.gracz.ekwipunek:
                            p.sprawdz()
                    else:
                        print("Ekwipunek jest pusty.")
            elif sp[0] == "poloz":
                p = sp[1]
                if p == "klucz":
                    polecenie_poprawne = True
                    klucze_w_ekwipunku = [k for k in self.gracz.ekwipunek if isinstance(k, Klucz)]
                    if klucze_w_ekwipunku:
                        self.gracz.poloz(klucze_w_ekwipunku[0])
                    else:
                        print("Nie masz klucza.")
                elif p == "skarb":
                    polecenie_poprawne = True
                    skarby_w_ekwipunku = [k for k in self.gracz.ekwipunek if isinstance(k, Skarb)]
                    if skarby_w_ekwipunku:
                        self.gracz.poloz(skarby_w_ekwipunku[0])
                    else:
                        print("Nie masz skarbu.")

        elif len(sp) == 3:
            if sp[0] == "otworz" and sp[1] == "drzwi":
                polecenie_poprawne = True
                self.gracz.otworz_drzwi(int(sp[2]))
            elif sp[0] == "zamknij" and sp[1] == "drzwi":
                polecenie_poprawne = True
                self.gracz.zamknij_drzwi(int(sp[2]))
            elif sp[0] == "przejdz":
                if sp[1] == "drzwi" or sp[1] == "przejscie":
                    polecenie_poprawne = True
                    self.gracz.przejdz(int(sp[2]))

        if not polecenie_poprawne:
            print("Niepoprawne polecenie.")
            print("Poprawne polecenia:")
            print("  mapa")
            print("  rozejrzyj sie")
            print("  wez <przedmiot>")
            print("  sprawdz klucze")
            print("  sprawdz skarby")
            print("  sprawdz ekwipunek")
            print("  poloz <przedmiot>")
            print("  otworz drzwi <n>")
            print("  zamknij drzwi <n>")
            print("  przejdz <drzwi/przejscie> <n>")
            print("  koniec")

    def zakoncz(self):
        self.czy_trwa = False
        print("Gra zakonczona.")


if __name__ == "__main__":
    g = Gra()
    g.rozpocznij()
