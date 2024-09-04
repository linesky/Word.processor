import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from PIL import Image, ImageDraw, ImageFont
#pip install pillow
class TextToBitmapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Bitmap App")
        self.root.geometry("800x600")
        self.root.configure(bg='black')

        # Criar área de texto com barras de rolagem
        self.text_area = tk.Text(root, wrap='word', bg='black', fg='white', insertbackground='white', font=('Arial', 12))
        self.text_area.pack(expand=True, fill='both')

        # Adiciona barras de rolagem
        scrollbar = Scrollbar(self.text_area)
        scrollbar.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_area.yview)

        # Criar botões
        self.save_text_button = tk.Button(root, text="Save Text", command=self.save_text)
        self.save_text_button.pack(side='left', padx=5, pady=5)

        self.save_bitmap_button = tk.Button(root, text="Save Bitmap", command=self.save_bitmap)
        self.save_bitmap_button.pack(side='left', padx=5, pady=5)

        self.load_text_button = tk.Button(root, text="Load Text File", command=self.load_text)
        self.load_text_button.pack(side='left', padx=5, pady=5)

        self.draw_button = tk.Button(root, text="Draw", command=self.draw_text)
        self.draw_button.pack(side='left', padx=5, pady=5)

        # Inicializa o bitmap (imagem)
        self.bitmap_width, self.bitmap_height = 2480, 3508  # Tamanho A4 em pixels a 300 DPI
        self.bitmap = Image.new('RGB', (self.bitmap_width, self.bitmap_height), 'black')
        self.draw = ImageDraw.Draw(self.bitmap)

    def save_text(self):
        text = self.text_area.get("1.0", 'end-1c')
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)
            messagebox.showinfo("Success", "Text saved successfully.")

    def save_bitmap(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("Bitmap Files", "*.bmp")])
        if file_path:
            self.bitmap.save(file_path)
            messagebox.showinfo("Success", "Bitmap saved successfully.")

    def load_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, file.read())

    def draw_text(self):
        self.bitmap = Image.new('RGB', (self.bitmap_width, self.bitmap_height), 'black')
        self.draw = ImageDraw.Draw(self.bitmap)
        text = self.text_area.get("1.0", 'end-1c')
        lines = text.split('\n')
        y_position = 50

        for line in lines:
            if line.startswith('#'):
                try:
                    font_size = int(line[1:3])
                    content = line[3:]
                    font = ImageFont.truetype("arial.ttf", font_size)
                    self.draw.text((50, y_position), content, font=font, fill="white")
                    y_position += font_size + 10
                except ValueError:
                    continue

        self.bitmap.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToBitmapApp(root)
    root.mainloop()

