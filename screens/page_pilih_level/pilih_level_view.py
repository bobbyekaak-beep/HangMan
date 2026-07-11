import tkinter as tk

WIN_W = 400
WIN_H = 700

CARD_H = 150
CARD_GAP = 12

LEVELS = [
    {
        "key": "easy",
        "title": "EASY",
        "desc": "Level mudah untuk pemula.",
        "block": "#8BC34A",
        "border": "#A5D6A7",
        "bg": "#F8FCF5",
        "text": "#558B2F",
    },
    {
        "key": "medium",
        "title": "MEDIUM",
        "desc": "Level menantang untuk\nmengasah kemampuan.",
        "block": "#F5B942",
        "border": "#FFE082",
        "bg": "#FFFDF5",
        "text": "#F09819",
    },
    {
        "key": "hard",
        "title": "HARD",
        "desc": "Level sulit hanya untuk\nyang hebat.",
        "block": "#E9564B",
        "border": "#FFAB9E",
        "bg": "#FFF7F6",
        "text": "#E53935",
    },
]


def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    # kotak dengan sudut membulat
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def left_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    # sudut kiri membulat, sisi kanan lurus
    points = [
        x1 + r, y1, x2, y1, x2, y1, x2, y2, x2, y2,
        x1 + r, y2, x1, y2, x1, y2 - r, x1, y1 + r, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def gambar_daun(canvas, cx, cy, size, warna):
    pts = [cx, cy - size, cx + size * 0.65, cy, cx, cy + size, cx - size * 0.65, cy]
    canvas.create_polygon(pts, smooth=True, fill=warna, outline="")
    canvas.create_line(cx, cy - size * 0.75, cx, cy + size * 0.75, fill="white", width=1)


def gambar_gunung(canvas, cx, cy, size, warna_tua, warna_muda):
    canvas.create_polygon(
        cx - size, cy + size * 0.6, cx - size * 0.1, cy - size * 0.25, cx + size * 0.5, cy + size * 0.6,
        fill=warna_muda, outline=""
    )
    canvas.create_polygon(
        cx - size * 0.45, cy + size * 0.6, cx + size * 0.15, cy - size * 0.65, cx + size, cy + size * 0.6,
        fill=warna_tua, outline=""
    )


def gambar_mahkota(canvas, cx, cy, size, warna):
    canvas.create_rectangle(cx - size, cy + size * 0.25, cx + size, cy + size * 0.65, fill=warna, outline="")
    canvas.create_polygon(
        cx - size, cy + size * 0.3,
        cx - size * 0.6, cy - size * 0.45,
        cx - size * 0.2, cy,
        cx, cy - size * 0.65,
        cx + size * 0.2, cy,
        cx + size * 0.6, cy - size * 0.45,
        cx + size, cy + size * 0.3,
        fill=warna, outline=""
    )
    for px, py in [(cx - size * 0.6, cy - size * 0.45), (cx, cy - size * 0.65), (cx + size * 0.6, cy - size * 0.45)]:
        canvas.create_oval(px - 4, py - 4, px + 4, py + 4, fill="#FFD54F", outline="")


def gambar_piala(canvas, cx, cy, size, warna):
    canvas.create_rectangle(cx - size * 0.15, cy + size * 0.3, cx + size * 0.15, cy + size * 0.6, fill=warna, outline="")
    canvas.create_rectangle(cx - size * 0.4, cy + size * 0.6, cx + size * 0.4, cy + size * 0.75, fill=warna, outline="")
    canvas.create_oval(cx - size * 0.4, cy - size * 0.5, cx + size * 0.4, cy + size * 0.3, fill=warna, outline="")
    canvas.create_arc(cx - size * 0.7, cy - size * 0.35, cx - size * 0.35, cy + size * 0.05,
                       start=90, extent=180, style="arc", outline=warna, width=2)
    canvas.create_arc(cx + size * 0.35, cy - size * 0.35, cx + size * 0.7, cy + size * 0.05,
                       start=-90, extent=180, style="arc", outline=warna, width=2)


def gambar_kilau(canvas, cx, cy, size, warna):
    canvas.create_polygon(
        cx, cy - size, cx + size * 0.25, cy - size * 0.25,
        cx + size, cy, cx + size * 0.25, cy + size * 0.25,
        cx, cy + size, cx - size * 0.25, cy + size * 0.25,
        cx - size, cy, cx - size * 0.25, cy - size * 0.25,
        smooth=False, fill=warna, outline=""
    )


class PilihLevelApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white", width=WIN_W, height=WIN_H)
        self.controller = controller
        self.pack_propagate(False)

        content = tk.Frame(self, bg="white")
        content.pack(expand=True)

        back_btn = tk.Button(
            self, text="←", font=("Segoe UI", 20), bg="white", fg="#757575",
            bd=0, activebackground="white", activeforeground="#757575",
            cursor="hand2", padx=6, pady=2, command=self.kembali
        )
        back_btn.place(x=15, y=15)

        self.buat_header(content)
        self.buat_kartu_level(content)
        self.buat_footer(content)

    def buat_header(self, parent):
        header = tk.Frame(parent, bg="white", width=WIN_W - 30)
        header.pack(fill="x", pady=(0, 8))

        tk.Label(header, text="PILIH LEVEL", bg="white", fg="#1C2A3A",
                 font=("Segoe UI", 18, "bold")).pack()

        divider = tk.Canvas(parent, width=150, height=14, bg="white", highlightthickness=0)
        divider.pack(pady=(0, 6))
        divider.create_line(10, 7, 60, 7, fill="#8BC34A", width=2)
        divider.create_oval(70, 4, 76, 10, fill="#8BC34A", outline="")
        divider.create_line(86, 7, 140, 7, fill="#8BC34A", width=2)

    def kembali(self):
        self.controller.go_back()

    def buat_kartu_level(self, parent):
        tinggi_canvas = 3 * CARD_H + 2 * CARD_GAP
        self.cards_canvas = tk.Canvas(parent, width=WIN_W, height=tinggi_canvas, bg="white", highlightthickness=0)
        self.cards_canvas.pack()

        y = 0
        for level in LEVELS:
            self.gambar_kartu(y, level)
            y += CARD_H + CARD_GAP

    def gambar_kartu(self, y, level):
        canvas = self.cards_canvas
        x1, x2 = 20, WIN_W - 20
        y2 = y + CARD_H
        r = 20
        cy = y + CARD_H / 2

        rounded_rect(canvas, x1, y, x2, y2, r, fill=level["bg"], outline=level["border"], width=2)

        block_w = 100
        left_rounded_rect(canvas, x1, y, x1 + block_w, y2, r, fill=level["block"], outline=level["block"])
        canvas.create_polygon(
            x1 + block_w, cy - 20, x1 + block_w + 14, cy, x1 + block_w, cy + 20,
            fill=level["block"], outline=level["block"]
        )

        circ_r = 32
        ccx = x1 + block_w / 2
        canvas.create_oval(ccx - circ_r, cy - circ_r, ccx + circ_r, cy + circ_r, fill="white", outline="")

        if level["key"] == "easy":
            gambar_daun(canvas, ccx, cy, 16, level["text"])
        elif level["key"] == "medium":
            gambar_gunung(canvas, ccx, cy, 18, level["block"], level["border"])
        else:
            gambar_mahkota(canvas, ccx, cy, 16, level["text"])

        text_x = x1 + block_w + 25
        canvas.create_text(text_x, y + 40, text=level["title"], font=("Segoe UI", 17, "bold"),
                            fill=level["text"], anchor="w")
        canvas.create_text(text_x, y + 72, text=level["desc"], font=("Segoe UI", 9),
                            fill="#444444", anchor="w", justify="left")
        canvas.create_text(x2 - 20, cy, text="›", font=("Segoe UI", 22, "bold"), fill=level["text"])

        klik_area = canvas.create_rectangle(x1, y, x2, y2, fill="", outline="")
        canvas.tag_bind(klik_area, "<Button-1>", lambda e, k=level["key"]: self.pilih_level(k))
        canvas.tag_bind(klik_area, "<Enter>", lambda e: canvas.config(cursor="hand2"))
        canvas.tag_bind(klik_area, "<Leave>", lambda e: canvas.config(cursor=""))

    def pilih_level(self, key):
        # sesuaikan nama frame tujuan dengan yang ada di main.py
        self.controller.show_frame("PilihLevelAngka", data={"kesulitan": key})

    def buat_footer(self, parent):
        canvas = tk.Canvas(parent, width=WIN_W, height=70, bg="white", highlightthickness=0)
        canvas.pack(pady=(25, 0))

        x1, x2 = 20, WIN_W - 20
        h = 60
        rounded_rect(canvas, x1, 0, x2, h, 18, fill="#F2F2F2", outline="")

        gambar_piala(canvas, x1 + 30, h / 2, 14, "#F5B942")
        canvas.create_line(x1 + 55, 12, x1 + 55, h - 12, fill="#CFCFCF", width=1)
        canvas.create_text(x1 + 70, h / 2, text="Semakin tinggi level, semakin seru\ntantangannya!",
                            font=("Segoe UI", 8), fill="#333333", anchor="w", justify="left")
        gambar_kilau(canvas, x2 - 20, h / 2, 7, "#4CAF50")


class _ControllerTiruan:
    # controller tiruan untuk uji coba mandiri
    def __init__(self, root):
        self.root = root

    def go_back(self):
        print("Tombol kembali ditekan")

    def show_frame(self, nama_frame, data=None):
        print(f"Pindah ke frame: {nama_frame}, data: {data}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pilih Level")
    root.geometry(f"{WIN_W}x{WIN_H}")
    root.resizable(False, False)

    controller = _ControllerTiruan(root)
    frame = PilihLevelApp(root, controller)
    frame.pack(fill="both", expand=True)

    root.mainloop()