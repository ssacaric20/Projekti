import math
import time

# meowmeowmeowmeowmeowmeow

class Notakto:
    def __init__(self):
        self.ploce = [[[' ' for red in range(3)] for stupac in range(3)] for br_ploca in range(3)]
        self.pune_ploce = [False, False, False] 
        self.aktivne_ploce = {0,1,2}

    def print_ploce(self):
        for i in self.aktivne_ploce:
            print(f"Board {i + 1}:")
            print("   1   2   3 ")
            print("  " + "-" * 13)
            for red_index, red in enumerate(self.ploce[i]):
                print(f"{red_index + 1} | " + " | ".join(red) + " |")  
                print("  " + "-" * 13)
            print("\n")

# meowmeowmeowmeowmeowmeow
    
    def popunjena(self, ploca):
        return all(cell != ' ' for red in ploca for cell in red)

    def gubitak(self, ploca):
        for i in range(3):
            if ploca[i][0] == ploca[i][1] == ploca[i][2] == 'X' or ploca[0][i] == ploca[1][i] == ploca[2][i] == 'X':
                return True
        if ploca[0][0] == ploca[1][1] == ploca[2][2] == 'X' or ploca[0][2] == ploca[1][1] == ploca[2][0] == 'X':
            return True
        return False

# meowmeowmeowmeowmeowmeow

    def mogucnosti(self, ploca_index):
        potezi = []
        for i in range(3):
            for j in range(3):
                if self.ploce[ploca_index][i][j] == ' ':
                    potezi.append((i, j))
        return potezi

    def potez(self, ploca_index, red, stupac):
        if self.ploce[ploca_index][red][stupac] == ' ':
            self.ploce[ploca_index][red][stupac] = 'X'
            return True
        return False
    
    def undo(self, ploca_index, red, stupac):
        self.ploce[ploca_index][red][stupac] = ' '

# meowmeowmeowmeowmeowmeow

    def minimax(self, ploca_index, maksimiziranje):
        if self.gubitak(self.ploce[ploca_index]):
            return 1 if maksimiziranje else -1
        
        if maksimiziranje:
            najbolja_vr = -math.inf
            for (red, stupac) in self.mogucnosti(ploca_index):
                self.potez(ploca_index, red, stupac)
                vr = self.minimax(ploca_index, False)
                self.undo(ploca_index, red, stupac)
                najbolja_vr = max(vr, najbolja_vr)
            return najbolja_vr
        else:
            najbolja_vr = math.inf
            for (red, stupac) in self.mogucnosti(ploca_index):
                self.potez(ploca_index, red, stupac)
                vr = self.minimax(ploca_index, True)
                self.undo(ploca_index, red, stupac)
                najbolja_vr = min(vr, najbolja_vr)
            return najbolja_vr
    
    def najbolji_potez(self):
        najbolja_vr = math.inf
        najbolji_potez = None
        best_ploca = None
        
        for ploca_index in range(3):
            if self.pune_ploce[ploca_index]: 
                continue
            for (red, stupac) in self.mogucnosti(ploca_index):
                self.potez(ploca_index, red, stupac)
                vr = self.minimax(ploca_index, True)
                self.undo(ploca_index, red, stupac)
                if vr < najbolja_vr:
                    najbolja_vr = vr
                    najbolji_potez = (red, stupac)
                    best_ploca = ploca_index
        return best_ploca, najbolji_potez
   
# meowmeowmeowmeowmeowmeow
    
    def azuriraj_aktivne_ploce(self, ploca_index):
        if self.gubitak(self.ploce[ploca_index]):
            self.aktivne_ploce.remove(ploca_index)
            self.pune_ploce[ploca_index] = True
            if not all(self.pune_ploce):
                print(f"Ploca {ploca_index + 1} je mrtva i nece se vise prikazivati.\n")
                time.sleep(1)

# meowmeowmeowmeowmeowmeow

    def zaigrajmo(self):
        print("Bokic!! ovo je Notakto, varijacija na igru krizic-kruzic~")
        print("Oba igraca koriste 'X', a cilj je *izbjeci* da se popuni 3 za redom.")
        print("Dakle, ako na ploci dobijete 3 za redom, gubite!")
        print("Takodjer se igra preko tri ploce, a ne samo na jednoj :)\n")
        time.sleep(2)
        
        while not all(self.pune_ploce):
            self.print_ploce()
            igrac_na_potezu = 'igrac'
            
            try:
                ploca_index = int(input("Ploca na kojoj zelite napraviti potez (1-3): ")) - 1
                if not (0 <= ploca_index < len(self.pune_ploce)):
                    print("Ploca ne postoji. Molimo unesite broj između 1 i 3.")
                    time.sleep(2)
                    continue
                if self.pune_ploce[ploca_index]:
                    print("Ta ploca je vec ispunjena, biraj neku drugu!")
                    time.sleep(2)
                    continue
                    
                red = int(input("Zeljeni red (1-3): ")) - 1 
                stupac = int(input("Zeljeni stupac(1-3): ")) - 1
                if not (0 <= red < 3) or not (0 <= stupac < 3):
                    print("Uneseni red ili stupac su izvan opsega. Molimo unesite broj između 1 i 3.")
                    time.sleep(2)
                    continue
                    
                if not self.potez(ploca_index, red, stupac):
                    print("To polje je vec ispunjeno :( biraj ponovno!!!")
                    time.sleep(2)
                    continue

            except ValueError:
                print("Neispravan unos.")
                time.sleep(2)
                continue
            
            if self.gubitak(self.ploce[ploca_index]):
                self.print_ploce()
                print(f"Izgubili ste na ploci {ploca_index + 1}! Napravili ste 3 za redom!\n")
                self.azuriraj_aktivne_ploce(ploca_index)
                time.sleep(1)
            
            ai_ploca, ai_potez = self.najbolji_potez()
            if ai_potez:
                print("\nSada je AI na potezu...")
                igrac_na_potezu = 'ai'
                time.sleep(2)
                self.potez(ai_ploca, ai_potez[0], ai_potez[1])
                print(f"AI bira plocu {ai_ploca + 1}, i postavlja X na polje ({ai_potez[0] + 1}, {ai_potez[1] + 1})\n")

                if self.gubitak(self.ploce[ai_ploca]):
                    self.print_ploce()
                    print(f"Yay! AI je izgubio na ploci {ai_ploca + 1}!")
                    self.azuriraj_aktivne_ploce(ai_ploca)
                    time.sleep(1)
        
        print("Kraj! Sve ploce su popunjene.")
        if igrac_na_potezu == 'igrac':
            print("Igrac je napravio zadnji potez - AI pobjedjuje ! >:)\n")
        else:
            print("AI je napravio zadnji potez - Igrac pobjedjuje! :)\n")

Notakto().zaigrajmo()