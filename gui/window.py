import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import fitz

from core.word_finder import search_word


class PDFWordFinderApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("PDF Word Finder")
        self.geometry("1000x700")
        self.minsize(850, 600)

        # ---------- Colors ----------
        self.bg_color = "#F4F7FB"
        self.card_color = "#FFFFFF"
        self.primary_color = "#2563EB"
        self.primary_hover = "#1D4ED8"
        self.text_color = "#172033"
        self.secondary_text = "#64748B"
        self.border_color = "#D9E1EC"
        self.success_color = "#15803D"

        self.configure(bg=self.bg_color)

        self.pdf_path = None

        self.setup_style()
        self.create_widgets()

    # =========================================================
    # STYLE
    # =========================================================

    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "TFrame",
            background=self.bg_color
        )

        style.configure(
            "Card.TFrame",
            background=self.card_color
        )

        style.configure(
            "Title.TLabel",
            background=self.bg_color,
            foreground=self.text_color,
            font=("Segoe UI", 27, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.bg_color,
            foreground=self.secondary_text,
            font=("Segoe UI", 11)
        )

        style.configure(
            "CardTitle.TLabel",
            background=self.card_color,
            foreground=self.text_color,
            font=("Segoe UI", 12, "bold")
        )

        style.configure(
            "Normal.TLabel",
            background=self.card_color,
            foreground=self.secondary_text,
            font=("Segoe UI", 10)
        )

        style.configure(
            "File.TLabel",
            background=self.card_color,
            foreground=self.text_color,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Primary.TButton",
            background=self.primary_color,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(18, 10),
            borderwidth=0
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", self.primary_hover)
            ]
        )

        style.configure(
            "Search.TButton",
            background=self.primary_color,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(20, 9),
            borderwidth=0
        )

        style.map(
            "Search.TButton",
            background=[
                ("active", self.primary_hover)
            ]
        )

        style.configure(
            "TEntry",
            padding=10,
            font=("Segoe UI", 11)
        )

    # =========================================================
    # GUI
    # =========================================================

    def create_widgets(self):

        # ---------- Main container ----------

        main_frame = ttk.Frame(self)
        main_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=30
        )

        # ---------- Header ----------

        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill="x")

        ttk.Label(
            header_frame,
            text="PDF Word Finder",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header_frame,
            text="Search words and phrases across your PDF documents",
            style="Subtitle.TLabel"
        ).pack(
            anchor="w",
            pady=(5, 25)
        )

        # ---------- PDF Card ----------

        pdf_card = ttk.Frame(
            main_frame,
            style="Card.TFrame"
        )

        pdf_card.pack(
            fill="x",
            pady=(0, 18)
        )

        pdf_content = ttk.Frame(
            pdf_card,
            style="Card.TFrame"
        )

        pdf_content.pack(
            fill="x",
            padx=22,
            pady=20
        )

        ttk.Label(
            pdf_content,
            text="PDF DOCUMENT",
            style="CardTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            pdf_content,
            text="Choose a PDF document to search.",
            style="Normal.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 12)
        )

        file_row = ttk.Frame(
            pdf_content,
            style="Card.TFrame"
        )

        file_row.pack(fill="x")

        self.file_label = ttk.Label(
            file_row,
            text="No PDF selected",
            style="File.TLabel"
        )

        self.file_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            file_row,
            text="  Select PDF  ",
            style="Primary.TButton",
            command=self.select_pdf
        ).pack(side="right")

        # ---------- Search Card ----------

        search_card = ttk.Frame(
            main_frame,
            style="Card.TFrame"
        )

        search_card.pack(
            fill="x",
            pady=(0, 18)
        )

        search_content = ttk.Frame(
            search_card,
            style="Card.TFrame"
        )

        search_content.pack(
            fill="x",
            padx=22,
            pady=20
        )

        ttk.Label(
            search_content,
            text="SEARCH DOCUMENT",
            style="CardTitle.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            search_content,
            text="Enter a word or phrase you want to find.",
            style="Normal.TLabel"
        ).pack(
            anchor="w",
            pady=(3, 12)
        )

        search_row = ttk.Frame(
            search_content,
            style="Card.TFrame"
        )

        search_row.pack(fill="x")

        self.search_entry = ttk.Entry(
            search_row
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_pdf()
        )

        ttk.Button(
            search_row,
            text="Search",
            style="Search.TButton",
            command=self.search_pdf
        ).pack(side="right")

        # ---------- Results Header ----------

        result_header = ttk.Frame(
            main_frame
        )

        result_header.pack(
            fill="x",
            pady=(0, 8)
        )

        ttk.Label(
            result_header,
            text="SEARCH RESULTS",
            font=("Segoe UI", 12, "bold"),
            background=self.bg_color,
            foreground=self.text_color
        ).pack(side="left")

        self.result_label = ttk.Label(
            result_header,
            text="Ready to search",
            font=("Segoe UI", 10),
            background=self.bg_color,
            foreground=self.secondary_text
        )

        self.result_label.pack(side="right")

        # ---------- Results Box ----------

        result_frame = tk.Frame(
            main_frame,
            bg=self.card_color,
            highlightbackground=self.border_color,
            highlightthickness=1
        )

        result_frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            result_frame,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.results_text = tk.Text(
            result_frame,
            bg=self.card_color,
            fg=self.text_color,
            font=("Segoe UI", 10),
            relief="flat",
            borderwidth=0,
            padx=18,
            pady=15,
            wrap="word",
            yscrollcommand=scrollbar.set
        )

        self.results_text.pack(
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.results_text.yview
        )

        # ---------- Footer ----------

        footer = ttk.Label(
            main_frame,
            text="PDF Word Finder  •  Built with Python & Tkinter",
            font=("Segoe UI", 9),
            background=self.bg_color,
            foreground=self.secondary_text
        )

        footer.pack(
            anchor="center",
            pady=(12, 0)
        )

    # =========================================================
    # SELECT PDF
    # =========================================================

    def select_pdf(self):

        file_path = filedialog.askopenfilename(
            title="Select PDF",
            filetypes=[
                ("PDF Files", "*.pdf"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        self.pdf_path = file_path

        self.file_label.config(
            text=file_path
        )

        self.result_label.config(
            text="PDF selected"
        )

        self.results_text.delete(
            "1.0",
            tk.END
        )

        self.results_text.insert(
            tk.END,
            "PDF loaded successfully.\n\n"
            "Enter a word or phrase above and click Search."
        )

    # =========================================================
    # SEARCH PDF
    # =========================================================

    def search_pdf(self):

        if not self.pdf_path:

            messagebox.showwarning(
                "No PDF Selected",
                "Please select a PDF document first."
            )

            return

        search_term = self.search_entry.get().strip()

        if not search_term:

            messagebox.showwarning(
                "Empty Search",
                "Please enter a word or phrase to search."
            )

            self.search_entry.focus()

            return

        try:

            total_matches, results = search_word(
                self.pdf_path,
                search_term
            )

            self.results_text.delete(
                "1.0",
                tk.END
            )

            if not results:

                self.result_label.config(
                    text="No matches found"
                )

                self.results_text.insert(
                    tk.END,
                    f'No results found for "{search_term}".\n\n'
                    "Try another word or phrase."
                )

                return

            # Result summary

            pages = [
                str(result["page"])
                for result in results
            ]

            page_text = ", ".join(pages)

            self.result_label.config(
                text=f"{total_matches} match(es) • Page(s): {page_text}",
                foreground=self.success_color
            )

            self.results_text.insert(
                tk.END,
                f'Search results for: "{search_term}"\n\n',
                "heading"
            )

            self.results_text.insert(
                tk.END,
                f"Total matches: {total_matches}\n"
                f"Pages found: {page_text}\n\n"
            )

            self.results_text.insert(
                tk.END,
                "=" * 90 + "\n\n"
            )

            # Individual results

            for result in results:

                self.results_text.insert(
                    tk.END,
                    f"PAGE {result['page']}\n",
                    "page"
                )

                self.results_text.insert(
                    tk.END,
                    f"Matches on this page: {result['count']}\n\n"
                )

                text = result["text"].strip()

                if len(text) > 700:
                    text = text[:700] + "..."

                self.results_text.insert(
                    tk.END,
                    text
                )

                self.results_text.insert(
                    tk.END,
                    "\n\n" + "-" * 90 + "\n\n"
                )

            # Text styling

            self.results_text.tag_config(
                "heading",
                font=("Segoe UI", 12, "bold")
            )

            self.results_text.tag_config(
                "page",
                font=("Segoe UI", 11, "bold")
            )

        except Exception as error:

            messagebox.showerror(
                "Search Error",
                f"Could not search the PDF.\n\n{error}"
            )


if __name__ == "__main__":
    app = PDFWordFinderApp()
    app.mainloop()
