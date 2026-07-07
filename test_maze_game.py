import unittest
from maze_game import Klucz, Skarb, Komnata, Drzwi, Przejscie, Gracz, Zlodziej

class TestLabirynt(unittest.TestCase):
    def setUp(self):
        self.k1 = Komnata(1, "Komnata 1", "Opis 1")
        self.k2 = Komnata(2, "Komnata 2", "Opis 2")
        self.klucz = Klucz(1, "Klucz 1", "Opis klucza 1")
        self.skarb = Skarb(2, "Skarb 1", "Opis skarbu 1", 100.0)
        self.drzwi = Drzwi(1, self.k1, self.k2)
        self.przejscie = Przejscie(2, self.k2)
        self.k1.przejscia.append(self.drzwi)
        self.k1.przejscia.append(self.przejscie)
        self.k1.dodaj_przedmiot(self.klucz)
        self.k1.dodaj_przedmiot(self.skarb)
        self.gracz = Gracz()
        self.gracz.aktualna_komnata = self.k1

    def test_wez_klucz(self):
        self.gracz.wez(self.klucz)
        self.assertIn(self.klucz, self.gracz.ekwipunek)

    def test_poloz_klucz(self):
        self.gracz.wez(self.klucz)
        self.gracz.poloz(self.klucz)
        self.assertNotIn(self.klucz, self.gracz.ekwipunek)
        self.assertIn(self.klucz, self.k1.przedmioty)

    def test_otworz_drzwi_z_kluczem(self):
        self.gracz.wez(self.klucz)
        self.gracz.otworz_drzwi(1)
        self.assertTrue(self.drzwi.czy_otwarte)

    def test_otworz_drzwi_bez_klucza(self):
        self.gracz.otworz_drzwi(1)
        self.assertFalse(self.drzwi.czy_otwarte)

    def test_przejdz_przez_otwarte_drzwi(self):
        self.gracz.wez(self.klucz)
        self.gracz.otworz_drzwi(1)
        self.gracz.przejdz(1)
        self.assertEqual(self.gracz.aktualna_komnata, self.k2)

    def test_zlodziej_kradnie(self):
        zlodziej = Zlodziej(1)
        self.k1.dodaj_stworzenie(zlodziej)
        self.gracz.wez(self.skarb)
        zlodziej.spotkaj_gracza(self.gracz)
        self.assertNotIn(self.skarb, self.gracz.ekwipunek)

    def test_zlodziej_nie_kradnie_kluczy(self):
        zlodziej = Zlodziej(1)
        self.k1.dodaj_stworzenie(zlodziej)
        self.gracz.wez(self.klucz)
        zlodziej.spotkaj_gracza(self.gracz)
        self.assertIn(self.klucz, self.gracz.ekwipunek)

    def test_zlodziej_nie_kradnie_gdy_brak(self):
        zlodziej = Zlodziej(1)
        self.k1.dodaj_stworzenie(zlodziej)
        zlodziej.spotkaj_gracza(self.gracz)
        self.assertEqual(len(self.gracz.ekwipunek), 0)

    def test_dodaj_usun_przedmiot(self):
        przedmiot = Klucz(3, "Klucz 3", "Opis klucza 3")
        self.k1.dodaj_przedmiot(przedmiot)
        self.assertIn(przedmiot, self.k1.przedmioty)
        self.k1.usun_przedmiot(przedmiot)
        self.assertNotIn(przedmiot, self.k1.przedmioty)

    def test_dodaj_usun_stworzenie(self):
        zlodziej = Zlodziej(2)
        self.k1.dodaj_stworzenie(zlodziej)
        self.assertIn(zlodziej, self.k1.stworzenia)
        self.k1.usun_stworzenie(zlodziej)
        self.assertNotIn(zlodziej, self.k1.stworzenia)

if __name__ == "__main__":
    unittest.main()
