import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Hesap Makinesi")
        self.root.geometry("600x900")  # Increased window size
        self.root.resizable(True, True)
        self.root.configure(bg='#333333')

        # Create display
        self.display = tk.Entry(root, width=30, font=('Arial', 24), justify='right')  # Increased width and font size
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=15)  # Increased padding

        # Button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', '%', '√', '^',
            '⌫'  # Backspace button added
        ]

        # Create and place buttons
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            if button == 'C':
                tk.Button(root, text=button, width=9, height=3, font=('Arial', 12), command=cmd).grid(row=5,
                                                                                                      column=0)  # Increased button size
            elif button == '⌫':  # Place backspace button
                tk.Button(root, text=button, width=9, height=3, font=('Arial', 12), command=cmd).grid(row=5,
                                                                                                      column=3)  # Increased button size
            else:
                tk.Button(root, text=button, width=9, height=3, font=('Arial', 12), command=cmd).grid(row=row,
                                                                                                      column=col)  # Increased button size
                col += 1
                if col > 3:
                    col = 0
                    row += 1

        self.equation = ""

    def click(self, button):
        if button == '=':
            try:
                self.equation = str(eval(self.equation))
                self.display.delete(0, tk.END)
                self.display.insert(0, self.equation)
            except:
                messagebox.showerror("Hata", "Geçersiz İfade")
                self.equation = ""
                self.display.delete(0, tk.END)
        elif button == 'C':
            self.equation = ""
            self.display.delete(0, tk.END)
        elif button == '⌫':  # Handle backspace
            self.equation = self.equation[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.equation)
        elif button == '%':
            try:
                self.equation = str(float(eval(self.equation)) / 100)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.equation)
            except:
                messagebox.showerror("Hata", "Geçersiz İfade")
                self.equation = ""
                self.display.delete(0, tk.END)
        elif button == '√':
            try:
                self.equation = str(float(eval(self.equation)) ** 0.5)
                self.display.delete(0, tk.END)
                self.display.insert(0, self.equation)
            except:
                messagebox.showerror("Hata", "Geçersiz İfade")
                self.equation = ""
                self.display.delete(0, tk.END)
        elif button == '^':
            self.equation += "**"
            self.display.delete(0, tk.END)
            self.display.insert(0, self.equation)
        else:
            self.equation += button
            self.display.delete(0, tk.END)
            self.display.insert(0, self.equation)


def main():
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
