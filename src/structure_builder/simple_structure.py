from fpdf import FPDF

class CVBuilder(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(10, 10, 10)
        self.add_page()
        self.set_font("Helvetica", size=11)

        self.gutter = 8
        self.col_w = (self.epw - self.gutter) / 2

    # =========================
    # OUTILS DE STYLE
    # =========================
    def h1(self, text):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        self.set_font("Helvetica", size=11)

    def h2(self, text):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", size=11)

    def paragraph(self, text):
        self.multi_cell(0, 5, text)
        self.ln(2)

    # =========================
    # COLONNE UNIQUE
    # =========================
    # def draw_column(self, x, y, w, title, text):
    #     # Position de départ
    #     self.set_xy(x, y)

    #     # Dessine le cadre de la colonne
    #     self.rect(x, y, w, 40)

    #     self.set_font("Helvetica", "B", 12)
    #     self.cell(w, 6, title, new_x="LEFT", new_y="NEXT")

    #     self.set_font("Helvetica", size=11)
    #     self.multi_cell(w, 5, text)

    #     return self.get_y()
    
    def draw_column(self, x, y, w, title, text):
        self.set_xy(x, y)

        self.set_font("Helvetica", "B", 12)
        self.cell(w, 6, title, new_x="LEFT", new_y="NEXT")

        self.set_font("Helvetica", size=11)
        self.multi_cell(w, 5, text)

        return self.get_y()

    # =========================
    # DEUX COLONNES ROBUSTES
    # =========================
    # def two_columns(self, left_title, left_text, right_title, right_text):
    #     y = self.get_y()

    #     left_x = self.l_margin
    #     right_x = self.l_margin + self.col_w + self.gutter

    #     print("left_x =", left_x)
    #     print("right_x =", right_x)
    #     print("col_w =", self.col_w)

    #     left_bottom = self.draw_column(left_x, y, self.col_w, left_title, left_text)
    #     right_bottom = self.draw_column(right_x, y, self.col_w, right_title, right_text)

    #     self.set_y(max(left_bottom, right_bottom) + 5)

    def two_columns(self, left_title, left_text, right_title, right_text):
        y = self.get_y()

        left_bottom = self.draw_column(
            self.l_margin,
            y,
            self.col_w,
            left_title,
            left_text,
        )

        right_bottom = self.draw_column(
            self.l_margin + self.col_w + self.gutter,
            y,
            self.col_w,
            right_title,
            right_text,
        )

        self.set_y(max(left_bottom, right_bottom) + 5)

    # =========================
    # OUTILS DE MISE EN PAGE
    # =========================
    def spacer(self, height=5):
        """Ajoute un espace vertical."""
        self.ln(height)


    def hr(
        self,
        color=(0, 120, 220),
        thickness=0.5,
        margin=0,
        space_before=2,
        space_after=4,
    ):
        self.ln(space_before)

        y = self.get_y()

        self.set_draw_color(*color)
        self.set_line_width(thickness)

        self.line(
            self.l_margin + margin,
            y,
            self.w - self.r_margin - margin,
            y,
        )

        self.ln(space_after)

    def dotted_hr(self):
        y = self.get_y()

        self.set_draw_color(180)

        x = self.l_margin

        while x < self.w - self.r_margin:
            self.line(x, y, x + 1.5, y)
            x += 3

        self.ln(4)

    def color_bar(self, color=(40, 120, 220), height=2):
        self.set_fill_color(*color)

        self.rect(
            self.l_margin,
            self.get_y(),
            self.epw,
            height,
            "F",
        )

        self.ln(height + 3)

    def section(self, title):
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")

        self.hr()

        self.set_font("Helvetica", "", 11)

    def centered_paragraph(self, text, width=None):
        if width is None:
            width = self.epw

        self.multi_cell(
            width,
            5,
            text,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        self.ln(2)

    
    def center_text(self, text, size=12, bold=False, height=8, color=(0, 0, 0)):
        if bold:
            self.set_font("Helvetica", "B", size)
        else:
            self.set_font("Helvetica", "", size)

        # Définition de la couleur du texte
        self.set_text_color(*color)

        self.cell(
            0,
            height,
            text,
            align="C",
            new_x="LMARGIN",
            new_y="NEXT"
        )

        # Remettre la couleur par défaut (noir)
        self.set_text_color(0, 0, 0)


    def bullet_list(self, items, width=None, bullet=""):
        if width is None:
            width = self.epw

        self.set_font("Helvetica", "", 11)

        for item in items:
            self.multi_cell(
                width,
                5,
                f"{bullet} {item}",
                align="L",
                new_x="LMARGIN",
                new_y="NEXT"
            )

        self.ln(2)