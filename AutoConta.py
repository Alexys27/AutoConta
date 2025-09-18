import os
import re
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox, simpledialog
from generare_procuri import DocumentProcessor

class AutoContaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoConta")
        self.geometry("600x250")

        self.processor = DocumentProcessor()
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        # Tab Generare Procuri
        tab_procura = ttk.Frame(notebook)
        notebook.add(tab_procura, text="Generare Procuri")

        # Input path (folder)
        tk.Label(tab_procura, text="Folder intrare:").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.input_path_entry = tk.Entry(tab_procura, width=50)
        self.input_path_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(tab_procura, text="Alege folder", command=self.browse_input_folder).grid(row=0, column=2, padx=5, pady=10)

        # Output path (folder)
        tk.Label(tab_procura, text="Folder ieșire:").grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.output_path_entry = tk.Entry(tab_procura, width=50)
        self.output_path_entry.grid(row=2, column=1, padx=10, pady=10)
        tk.Button(tab_procura, text="Alege folder", command=self.browse_output_folder).grid(row=2, column=2, padx=5, pady=10)

        # Buton generare
        generate_button = tk.Button(tab_procura, text="Generează Procură", command=self.generate_procura_gui, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"))
        generate_button.grid(row=3, column=1, pady=20)

    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_path_entry.delete(0, tk.END)
            self.input_path_entry.insert(0, folder_selected)

    def browse_template_file(self):
        file_selected = filedialog.askopenfilename(filetypes=[("Documente Word", "*.docx")])
        if file_selected:
            self.template_path_entry.delete(0, tk.END)
            self.template_path_entry.insert(0, file_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_path_entry.delete(0, tk.END)
            self.output_path_entry.insert(0, folder_selected)

    def prompt_missing_fields_gui(self, context: dict, required_fields: list) -> dict:
        """
        Deschide o fereastră de input pentru câmpurile lipsă și returnează dict-ul completat.
        Validare CNP și CUI.
        """
        missing_fields = [f for f in required_fields if f not in context or not context[f]]
        if not missing_fields:
            return context

        popup = tk.Toplevel(self)
        popup.title("Completează câmpurile lipsă")
        entries = {}

        for i, field in enumerate(missing_fields):
            tk.Label(popup, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(popup, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[field] = entry

        def submit():
            valid = True
            for field, entry in entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showwarning("Atenție", f"Câmpul '{field}' este obligatoriu!")
                    valid = False
                    break
                if field == "CNP" and not re.fullmatch(r"\d{13}", value):
                    messagebox.showerror("Eroare", "CNP-ul trebuie să aibă exact 13 cifre!")
                    valid = False
                    break
                if field == "CUI":
                    cui_clean = value.upper().replace("RO", "")
                    if not re.fullmatch(r"\d{2,10}", cui_clean):
                        messagebox.showerror("Eroare", "CUI-ul trebuie să fie între 2 și 10 cifre (RO optional)!")
                        valid = False
                        break
                context[field] = value
            if valid:
                popup.destroy()

        tk.Button(popup, text="Salvează", command=submit).grid(row=len(missing_fields), column=0, columnspan=2, pady=15)
        popup.grab_set()
        self.wait_window(popup)
        return context

    def generate_procura_gui(self):
        input_dir = self.input_path_entry.get()
        template_path = "IMPUTERNICIRE_model_ro_eng.docx"
        output_folder = self.output_path_entry.get()

        if not input_dir or not template_path or not output_folder:
            messagebox.showwarning("Atenție", "Completează toate câmpurile!")
            return

        # Creează calea fișierului de ieșire (nume automat)
        output_path = os.path.join(output_folder, f"PROCURA_GENERATA_{os.path.split(input_dir)[1]}.docx")
        os.makedirs(output_folder, exist_ok=True)

        try:
            # Procesează fișierele și extrage datele
            all_data = {}
            for file_path in Path(input_dir).iterdir():
                if file_path.is_file() and file_path.suffix.lower() in self.processor.supported_extensions:
                    text = self.processor.read_file(str(file_path))
                    extracted = self.processor.extract_data(text)
                    for k, v in extracted.items():
                        all_data.setdefault(k, []).append(v)

            if not all_data:
                messagebox.showwarning("Atenție", "Nu s-au găsit date în niciun fișier.")
                return

            # Folosește prima valoare găsită pentru fiecare câmp
            context = {k: v[0] for k, v in all_data.items()}

            # Completează câmpurile lipsă folosind metoda GUI
            required_fields = list(self.processor.patterns.keys())
            context = self.prompt_missing_fields_gui(context, required_fields)

            # Generează procura
            self.processor.generate_procura(template_path, output_path, context)
            messagebox.showinfo("Succes", f"Procura a fost generată la:\n{output_path}")

        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare:\n{e}")


if __name__ == "__main__":
    app = AutoContaApp()
    app.mainloop()
