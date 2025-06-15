from tkinter import Button, Label, messagebox
import random
import settings
import ctypes
import sys

class Polje:
    all = []
    cell_count = settings.BROJ_POLJA
    broj_polja = None

    def __init__(self, x, y, jeste_mina=False):
        self.jeste_mina = jeste_mina
        self.jeste_otvoreno = False
        self.zastavica = False
        self.polje_dugme = None
        self.x = x
        self.y = y

        Polje.all.append(self)

    def create_polje_dugme(self, location):
        dugme = Button(
            location,
            width=4, height=2,
            font=('Arial', 14, 'bold'),
            relief='raised',
            bd=3,
            bg='SystemButtonFace'
        )
        dugme.bind('<Button-1>', self.lijevi_klik)
        dugme.bind('<Button-3>', self.desni_klik)
        self.polje_dugme = dugme

    @staticmethod
    def labela_brojača_polja(location):
        labela = Label(
            location,
            bg='gray',
            fg='white',
            text=f"PREOSTALA POLJA:{Polje.cell_count}",
            font=("Arial", 15)
        )
        Polje.broj_polja = labela

    def lijevi_klik(self, event):
        if self.jeste_mina:
            self.pokazi_minu()
        else:
            if self.broj_mina_u_okolini == 0:
                for objekat_polja in self.okolna_polja:
                    objekat_polja.pokazi_polje()
            self.pokazi_polje()

            if Polje.cell_count == settings.BR_MINA:
                ctypes.windll.user32.MessageBoxW(0, 'Čestitam, pobijedili ste!', 'WIN', 1)

            self.polje_dugme.unbind('<Button-1>')
            self.polje_dugme.unbind('<Button-3>')

    def pokazi_minu(self):
        for polje in Polje.all:
            if polje.jeste_mina:
                polje.polje_dugme.configure(
                    text='🚩',
                    bg='yellow',
                    fg='black',
                    disabledforeground='black',
                    state='disabled'
                )
        messagebox.showinfo("KRAJ", "Kliknuli ste na minu! GAME OVER!")
        sys.exit()

    def polja_po_osama(self, x, y):
        for polje in Polje.all:
            if polje.x == x and polje.y == y:
                return polje

    @property
    def okolna_polja(self):
        o_polja = [
            self.polja_po_osama(self.x - 1, self.y - 1),
            self.polja_po_osama(self.x - 1, self.y),
            self.polja_po_osama(self.x - 1, self.y + 1),
            self.polja_po_osama(self.x, self.y - 1),
            self.polja_po_osama(self.x + 1, self.y - 1),
            self.polja_po_osama(self.x + 1, self.y),
            self.polja_po_osama(self.x + 1, self.y + 1),
            self.polja_po_osama(self.x, self.y + 1)
        ]
        return [polje for polje in o_polja if polje is not None]

    @property
    def broj_mina_u_okolini(self):
        br = 0
        for polje in self.okolna_polja:
            if polje.jeste_mina:
                br += 1
        return br

    def pokazi_polje(self):
        if not self.jeste_otvoreno:
            Polje.cell_count -= 1
            broj = self.broj_mina_u_okolini
            if broj >= 0:
                self.polje_dugme.configure(
                    text=str(broj),
                    fg=self.boja_za_broj(broj),
                    bg='lightgray',
                    relief='sunken'
                )
            else:
                self.polje_dugme.configure(
                    text='',
                    bg='lightgray',
                    relief='sunken'
                )

            if Polje.broj_polja:
                Polje.broj_polja.configure(
                    bg='gray',
                    fg='white',
                    text=f"⏳ PREOSTALA POLJA: {Polje.cell_count}",
                    font=('Arial', 14, 'bold'),
                    pady=20
                )

            self.polje_dugme.configure(bg='SystemButtonFace')
            self.jeste_otvoreno = True

    def desni_klik(self, event):
        if not self.zastavica:
            self.polje_dugme.configure(
                text='🚩',
                bg='green'
            )
            self.zastavica = True
        else:
            self.polje_dugme.configure(
                text='',
                bg='SystemButtonFace',
            )
            self.zastavica = False

    @staticmethod
    def biraj_bomba_polja():
        mina_polja = random.sample(
            Polje.all, settings.BR_MINA
        )
        for odabrano_polje in mina_polja:
            odabrano_polje.jeste_mina = True

    def __repr__(self):
        return f"Polje({self.x}, {self.y})"

    def boja_za_broj(self, broj):
        boje = {
            0: 'magenta',
            1: 'blue',
            2: 'green',
            3: 'red',
            4: 'navy',
            5: 'maroon',
            6: 'turquoise',
            7: 'black',
            8: 'gray'
        }
        return boje.get(broj, 'black')
