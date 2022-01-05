import pygame
from random import randint

class Hittipeli():

    def __init__(self):
        pygame.init()

        self.lataa_kuvat()

        self.roboleveys = self.robo.get_width()
        self.robokorkeus = self.robo.get_height()
        self.ovileveys = self.ovi.get_width()
        self.ovikorkeus = self.ovi.get_height()
        self.hirvioleveys = self.hirvio.get_width()
        self.hirviokorkeus = self.hirvio.get_height()

        self.fontti = pygame.font.SysFont("helvetica", 24)
        self.naytto = pygame.display.set_mode((1280,960))

        pygame.display.set_caption("hyvä peli")

        self.aloitusnaytto()
        self.uusipeli()
        self.silmukka()
        self.loppu()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["robo", "ovi", "kolikko", "hirvio"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))
        self.robo, self.ovi, self.kolikko, self.hirvio = self.kuvat

    def aloitusnaytto(self):
        # aloitusnäyttö
        aloita = False
        while True:
            if aloita == True:
                return

            self.naytto.fill((42, 0, 42))
            teksti = self.fontti.render('Liikuta robottia nuolinäppäimin ja kerää 10 kolikkoa, jonka jälkeen ovi voittoon aukeaa!', True, (255, 255, 255))
            teksti2 = self.fontti.render('Paina SPACE aloittaaksesi', True, (255, 255, 255))
            self.naytto.blit(teksti, (200, 100))
            self.naytto.blit(teksti2, (200, 200))
            pygame.display.flip()
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE:
                        aloita = True

    def uusipeli(self):
        self.havio = False
        self.voitto = False
        # pelaajan koordinaatit ja liikkeet
        self.x = 0
        self.y = 960 - self.robo.get_height()
        self.vasemmalle = False
        self.oikealle = False
        self.nousu = False

        # kolikot
        self.kolikot = 0
        self.kolikko_x = randint(2,1280-2)
        self.kolikko_y = randint(2,960-2)

        # ovi
        self.ovi_x = 2000
        self.ovi_y = 2000

        # hirviot
        self.hirvio1_x = 1200
        self.hirvio1_y = 200
        self.hirvio2_x = 800
        self.hirvio2_y = 400
        self.hirvio3_x = 400
        self.hirvio3_y = 600
        self.hirvio4_x = 1280/2
        self.hirvio4_y = 100
        self.hirvio1_nopeus = 2
        self.hirvio2_nopeus = 3
        self.hirvio3_nopeus = 4
        self.hirvio4_nopeus = 3

    def hirvioiden_liike(self):
        self.hirvio1_x += self.hirvio1_nopeus
        self.hirvio2_x += self.hirvio2_nopeus
        self.hirvio3_x += self.hirvio3_nopeus
        self.hirvio4_y += self.hirvio4_nopeus

        # reunoihin törmääminen muuttaa suuntaa
        if self.hirvio1_nopeus > 0 and self.hirvio1_x+self.hirvioleveys >= 1280:
            self.hirvio1_nopeus = -self.hirvio1_nopeus
        if self.hirvio2_nopeus > 0 and self.hirvio2_x+self.hirvioleveys >= 1280:
            self.hirvio2_nopeus = -self.hirvio2_nopeus
        if self.hirvio3_nopeus > 0 and self.hirvio3_x+self.hirvioleveys >= 1280:
            self.hirvio3_nopeus = -self.hirvio3_nopeus

        if self.hirvio1_nopeus < 0 and self.hirvio1_x+self.hirvioleveys <= 0:
            self.hirvio1_nopeus = -self.hirvio1_nopeus
        if self.hirvio2_nopeus < 0 and self.hirvio2_x+self.hirvioleveys <= 0:
            self.hirvio2_nopeus = -self.hirvio2_nopeus
        if self.hirvio3_nopeus < 0 and self.hirvio3_x+self.hirvioleveys <= 0:
            self.hirvio3_nopeus = -self.hirvio3_nopeus

        if self.hirvio4_nopeus > 0 and self.hirvio4_y+self.hirviokorkeus >= 960:
            self.hirvio4_nopeus = -self.hirvio4_nopeus
        if self.hirvio4_nopeus < 0 and self.hirvio4_y+self.hirviokorkeus <= 0:
            self.hirvio4_nopeus = -self.hirvio4_nopeus

    def liiku(self):
        if 0 <= self.x and self.vasemmalle:
            self.x -= 2
        if self.x <= 1280 - self.roboleveys and self.oikealle:
            self.x += 2

    def jetpack(self):
        if self.nousu and self.y >= 0:
            self.y -= 2
        if not self.nousu and self.y <= 960-self.robokorkeus:
            self.y += 2

    def robo_saa_kolikon(self):
        if (self.x-self.roboleveys/2 < self.kolikko_x < self.x+self.roboleveys/2) and (self.y-self.robokorkeus/2 < self.kolikko_y < self.y+self.robokorkeus/2):
            self.kolikot += 1
            self.kolikko_x = randint(2,1280-2)
            self.kolikko_y = randint(2,960-2)

    def onko_voittanut(self):
        if self.kolikot == 10:
            self.ovi_x = 1280 - self.ovileveys
            self.ovi_y = 960 - self.ovikorkeus
            if (self.x-self.roboleveys/2 < self.ovi_x < self.x+self.roboleveys/2) and (self.y-self.robokorkeus/2 < self.ovi_y < self.y+self.robokorkeus/2):
                self.voitto = True

    def silmukka(self):
        while True:
            if self.voitto or self.havio:
                return

            self.piirra_naytto()
            self.hirvioiden_liike()
            self.tutki_tapahtumat()
            self.onko_voittanut()
            self.tormays()

    def tormays(self):
        if (self.x-self.roboleveys/3 < self.hirvio1_x < self.x+self.roboleveys/3) and (self.y-self.robokorkeus/3 < self.hirvio1_y < self.y+self.robokorkeus/3):
            self.havio = True
        if (self.x-self.roboleveys/3 < self.hirvio2_x < self.x+self.roboleveys/3) and (self.y-self.robokorkeus/3 < self.hirvio2_y < self.y+self.robokorkeus/3):
            self.havio = True
        if (self.x-self.roboleveys/3 < self.hirvio3_x < self.x+self.roboleveys/3) and (self.y-self.robokorkeus/3 < self.hirvio3_y < self.y+self.robokorkeus/3):
            self.havio = True
        if (self.x-self.roboleveys/3 < self.hirvio4_x < self.x+self.roboleveys/3) and (self.y-self.robokorkeus/3 < self.hirvio4_y < self.y+self.robokorkeus/3):
            self.havio = True

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.nousu = True
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.nousu = False
            
            if tapahtuma.type == pygame.QUIT:
                exit()

        self.liiku()
        self.jetpack()
        self.robo_saa_kolikon()

    def piirra_naytto(self):
        self.naytto.fill((42,0,42))
        self.naytto.blit(self.robo ,(self.x, self.y))
        self.naytto.blit(self.kolikko, (self.kolikko_x, self.kolikko_y))
        self.naytto.blit(self.ovi, (self.ovi_x, self.ovi_y))
        self.naytto.blit(self.hirvio, (self.hirvio1_x,self.hirvio1_y))
        self.naytto.blit(self.hirvio, (self.hirvio2_x,self.hirvio2_y))
        self.naytto.blit(self.hirvio, (self.hirvio3_x,self.hirvio3_y))
        self.naytto.blit(self.hirvio, (self.hirvio4_x,self.hirvio4_y))
        teksti = self.fontti.render("Kolikot: "+str(self.kolikot), True, (255, 255, 255))
        self.naytto.blit(teksti, (2, 2))

        pygame.display.flip()
        
    def loppu(self):
        uusi = False
        pois = False
        if self.voitto:
            while True:
                if uusi:
                    Hittipeli()
                if pois:
                    exit()
                self.naytto.fill((42,0,42))
                voittoteksti = self.fontti.render("Onneksi olkoon, voitit pelin! Paina F2 niin uusi peli alkaa tai ESC niin peli sulkeutuu.", True, (255, 255, 255))
                self.naytto.blit(voittoteksti, (200,100))
                pygame.display.flip()
                for tapahtuma in pygame.event.get():
                    if tapahtuma.type == pygame.KEYDOWN:
                        if tapahtuma.key == pygame.K_F2:
                            uusi = True
                        if tapahtuma.key == pygame.K_ESCAPE:
                            pois = True

        if self.havio:
            while True:
                if uusi:
                    Hittipeli()
                if pois:
                    exit()
                self.naytto.fill((42,0,42))
                havioteksti = self.fontti.render("Hävisit pelin! Paina F2 niin uusi peli alkaa tai ESC niin peli sulkeutuu.", True, (255, 255, 255))
                self.naytto.blit(havioteksti, (200,100))
                pygame.display.flip()
                for tapahtuma in pygame.event.get():
                    if tapahtuma.type == pygame.KEYDOWN:
                        if tapahtuma.key == pygame.K_F2:
                            uusi = True
                        if tapahtuma.key == pygame.K_ESCAPE:
                            pois = True

Hittipeli()