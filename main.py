
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import qrcode
from PIL import Image, ImageTk
import win32clipboard
import io

class QRGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("520x610")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F0")

        self.qr_image = None
        self.qr_photo = None

        self.canvas = tk.Canvas(
            root,
            bg="#F5F5F0",
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scroll_frame = tk.Frame(
            self.canvas,
            bg="#F5F5F0"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scroll_frame,
            anchor="nw",
            width=520
        )

        self.scroll_frame.bind("<Configure>", self.update_scroll)
        self.canvas.bind("<Configure>", self.resize_canvas)
        self.canvas.bind_all("<MouseWheel>", self.mouse_scroll)

        self.build_ui()

    def update_scroll(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def resize_canvas(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def mouse_scroll(self, event):
        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def build_ui(self):
        header = tk.Frame(self.scroll_frame, bg="#F5F5F0")
        header.pack(fill="x", padx=35, pady=(30, 22))

        tk.Label(
            header,
            text="QR Code Generator",
            font=("Segoe UI", 23, "bold"),
            bg="#F5F5F0",
            fg="#252A28"
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Create and save your own QR codes.",
            font=("Segoe UI", 10),
            bg="#F5F5F0",
            fg="#858B87"
        ).pack(anchor="w", pady=(5, 0))

        input_card = tk.Frame(
            self.scroll_frame,
            bg="#FFFFFF",
            highlightbackground="#E5E8E4",
            highlightthickness=1
        )
        input_card.pack(fill="x", padx=35, pady=(0, 18))

        tk.Label(
            input_card,
            text="ENTER TEXT OR URL",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#858B87"
        ).pack(anchor="w", padx=18, pady=(16, 8))

        self.input_field = tk.Entry(
            input_card,
            font=("Segoe UI", 11),
            bg="#FAFAF8",
            fg="#252A28",
            insertbackground="#52796F",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E5E8E4",
            highlightcolor="#52796F"
        )
        self.input_field.pack(fill="x", padx=18, ipady=11)

        tk.Button(
            input_card,
            text="Generate QR Code",
            font=("Segoe UI", 10, "bold"),
            bg="#52796F",
            fg="#FFFFFF",
            activebackground="#405F56",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.generate,
            pady=11
        ).pack(fill="x", padx=18, pady=17)

        preview_card = tk.Frame(
            self.scroll_frame,
            bg="#FFFFFF",
            highlightbackground="#E5E8E4",
            highlightthickness=1
        )
        preview_card.pack(fill="both", expand=True, padx=35, pady=(0, 15))

        tk.Label(
            preview_card,
            text="QR CODE PREVIEW",
            font=("Segoe UI", 9, "bold"),
            bg="#FFFFFF",
            fg="#858B87"
        ).pack(anchor="w", padx=18, pady=(15, 8))

        self.preview = tk.Label(
            preview_card,
            text="Your QR code will appear here",
            font=("Segoe UI", 10),
            bg="#FAFAF8",
            fg="#858B87",
            width=30,
            height=12
        )
        self.preview.pack(pady=10)

        self.status = tk.Label(
            preview_card,
            text="No QR code generated",
            font=("Segoe UI", 9),
            bg="#FFFFFF",
            fg="#858B87"
        )
        self.status.pack(pady=(5, 12))

        self.save_button = tk.Button(
            preview_card,
            text="Save QR Code",
            font=("Segoe UI", 10, "bold"),
            bg="#52796F",
            fg="#FFFFFF",
            activebackground="#405F56",
            activeforeground="#FFFFFF",
            relief="flat",
            cursor="hand2",
            command=self.save,
            state="disabled",
            pady=10
        )
        self.save_button.pack(fill="x", padx=18, pady=(0, 8))

        self.copy_button = tk.Button(
            preview_card,
            text="Copy QR Code",
            font=("Segoe UI", 10, "bold"),
            bg="#FFFFFF",
            fg="#52796F",
            activebackground="#E6EFEA",
            activeforeground="#405F56",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#E5E8E4",
            cursor="hand2",
            command=self.copy,
            state="disabled",
            pady=10
        )
        self.copy_button.pack(fill="x", padx=18, pady=(0, 17))

        tk.Button(
            self.scroll_frame,
            text="Clear",
            font=("Segoe UI", 9),
            bg="#F5F5F0",
            fg="#858B87",
            activebackground="#F5F5F0",
            relief="flat",
            cursor="hand2",
            command=self.clear
        ).pack(pady=(0, 15))

    def generate(self):
        content = self.input_field.get().strip()

        if not content:
            messagebox.showwarning(
                "Empty Input",
                "Please enter some text or a URL."
            )
            return

        try:
            self.qr_image = qrcode.make(
                content,
                box_size=10,
                border=4
            )

            preview_image = self.qr_image.resize(
                (220, 220),
                Image.Resampling.NEAREST
            )

            self.qr_photo = ImageTk.PhotoImage(preview_image)

            self.preview.configure(
                image=self.qr_photo,
                text="",
                width=220,
                height=220
            )

            self.status.configure(
                text="QR code generated successfully.",
                fg="#52796F"
            )

            self.save_button.configure(state="normal")
            self.copy_button.configure(state="normal")

        except Exception as error:
            messagebox.showerror(
                "Generation Error",
                str(error)
            )

    def save(self):
        if self.qr_image is None:
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qr_code.png"
        )

        if path:
            try:
                self.qr_image.save(path)
                self.status.configure(
                    text="QR code saved successfully.",
                    fg="#52796F"
                )
            except Exception as error:
                messagebox.showerror(
                    "Save Error",
                    str(error)
                )

    def copy(self):
        if self.qr_image is None:
            return

        clipboard_open = False

        try:
            image = self.qr_image.convert("RGB")

            output = io.BytesIO()
            image.save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            clipboard_open = True

            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(
                win32clipboard.CF_DIB,
                data
            )

            win32clipboard.CloseClipboard()
            clipboard_open = False

            self.status.configure(
                text="QR code copied to clipboard.",
                fg="#52796F"
            )

        except Exception as error:
            if clipboard_open:
                win32clipboard.CloseClipboard()

            messagebox.showerror(
                "Copy Error",
                str(error)
            )

    def clear(self):
        self.input_field.delete(0, tk.END)

        self.qr_image = None
        self.qr_photo = None

        self.preview.configure(
            image="",
            text="Your QR code will appear here",
            width=30,
            height=12
        )

        self.status.configure(
            text="No QR code generated",
            fg="#858B87"
        )

        self.save_button.configure(state="disabled")
        self.copy_button.configure(state="disabled")


root = tk.Tk()
app = QRGenerator(root)
root.mainloop()
