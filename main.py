from tkinter import*
import settings
import utilities
from tabla import Polje

root = Tk()
root.configure(bg="gray")
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
root.title('Minesweep igrica')
root.resizable(False,False)


top_frame = Frame(
    root,
    bg='gray', 
    width = settings.WIDTH,
    height = utilities.height_procenat(15)
    )
top_frame.place(x=0,y=0)

game_title = Label(
    top_frame,
    bg='gray',
    fg='black',
    text='💣 MINESWEEPER 💣',
    font=('Arial', 36, 'bold'),
    pady=10
    )
game_title.place(
    x = utilities.width_procenat(25),
    y = 1
)
separator = Frame(
    top_frame,
    bg='black',
    height=2,
    width=settings.WIDTH
    )
separator.place(x=0, y=utilities.height_procenat(12))

left_frame = Frame(
    root,
    bg='gray',
    width = utilities.width_procenat(40),
    height = utilities.height_procenat(75)
    )
left_frame.place(x=0,y=utilities.height_procenat(40))

center_frame = Frame(
    root,
    bg='gray', 
    width = utilities.width_procenat(75),
    height = utilities.height_procenat(75)
    )
center_frame.place(x=utilities.width_procenat(25),y=utilities.height_procenat(25))

for x in range(settings.GRID_SIZE):
    for y in range(settings.GRID_SIZE):
        c = Polje(x, y)
        c.create_polje_dugme(center_frame)

        # --- Izračunavanje početne pozicije da bude centrirano ---
        total_grid_width = settings.GRID_SIZE * settings.CELL_SIZE
        total_grid_height = settings.GRID_SIZE * settings.CELL_SIZE

        start_x = (settings.WIDTH // 2 - total_grid_width) // 2
        start_y = (settings.HEIGHT - utilities.height_procenat(25) - total_grid_height) // 2

        c.polje_dugme.place(
            x=start_x + x * settings.CELL_SIZE,
            y=start_y + y * settings.CELL_SIZE,
            width=settings.CELL_SIZE,
            height=settings.CELL_SIZE
        )
#labela iz klase POLJE
Polje.labela_brojača_polja(left_frame)
Polje.broj_polja.place(x=0, y=0)
Polje.biraj_bomba_polja()


root.mainloop()
