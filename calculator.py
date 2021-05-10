from tkinter import *
import webbrowser


class ButtonObject:
    def __init__(self, frame, out, font=None, width=3, bd=7, pady=3, padx=3,
                 relief="raised"):
        self.frame = frame
        self.out = out
        self.font = font
        self.width = width
        self.bd = bd
        self.pady = pady
        self.padx = padx
        self.relief = relief

    def num(self, text=None, num=None, row=None, column=None, fg='black',
            foo=None):
        Button(self.frame, text=text, font=self.font, width=self.width,
               relief=self.relief, command=lambda: foo(self.out, num),
               bd=self.bd, fg=fg).grid(row=row, column=column, pady=self.pady,
                                       padx=self.padx)


def main():

    def popup(event):
        menu1 = Menu(tearoff=False, font="Arial 12")
        menu1.add_command(label="Copy", command=copy)
        menu1.post(event.x_root, event.y_root)

    def copy():
        root.clipboard_clear()
        root.clipboard_append(out.get())

    def about(event):
        menu2 = Menu(tearoff=False, font="Arial 12")
        menu2.add_radiobutton(label="Pin on",
                              command=lambda: root.attributes("-topmost", True))
        menu2.add_radiobutton(label="Pin off",
                              command=lambda: root.attributes("-topmost", False))
        menu2.add_separator()
        menu2.add_command(label="About", command=dialog)
        menu2.post(event.x_root, event.y_root)

    def dialog():
        global aboutflag

        def destroy_about_window():
            global aboutflag
            win.destroy()
            aboutflag = False

        def callback(blank=None):
            webbrowser.open_new(r"https://github.com/chicory-ru/Simple-calculator")
            destroy_about_window()

        if not aboutflag:
            win = Toplevel(bg="light gray", bd=7, relief="ridge")  # About.
            win.geometry(f"280x170+{650}+{400}")
            win.title("About")
            win.minsize(width=250, height=110)
            win.resizable(width=False, height=False)
            win.attributes("-topmost", True)
            win.overrideredirect(True)
            ok = Button(win, text='OK', font="Arial 12",
                        command=destroy_about_window, width=9, bd=3)
            ok.pack(side=BOTTOM, padx=10, pady=10)
            version = Label(win, text="Simple calculator v.1.0", font="Arial 14",
                            bg="light gray")
            version.pack(padx=9, pady=9)
            link = Label(win, text="https://github.com...", fg="blue",
                         cursor="hand2", font="Arial 14", bg="light gray")
            link.pack(padx=7, pady=7)
            link.bind("<Button-1>", callback)
            aboutflag = True

    root = Tk()
    root.title("Simple calculator")
    root.minsize(width=250, height=300)
    root.resizable(width=False, height=False)

    frame = Frame(root, bd=7,  relief="ridge", bg="light gray")
    frame.pack()
    frame.bind('<Button-3>', about)

    out = Entry(frame, width=12, font="Arial 21", justify=RIGHT, bd=7, bg='blue',
                fg='dark blue')
    out.bind('<Button-3>', popup)
    out.grid(row=0, column=0, columnspan=3, sticky=N+S+W+E, pady=9, padx=3)
    out.insert(0, "0")
    out.config(state="readonly")
    
    # Create buttons.
    bo = ButtonObject(frame, out, "Arial 19")
    bo.num('1', '1', 1, 0, foo=output)
    bo.num('2', '2', 1, 1, foo=output)
    bo.num('3', '3', 1, 2, foo=output)
    bo.num('4', '4', 2, 0, foo=output)
    bo.num('5', '5', 2, 1, foo=output)
    bo.num('6', '6', 2, 2, foo=output)
    bo.num('7', '7', 3, 0, foo=output)
    bo.num('8', '8', 3, 1, foo=output)
    bo.num('9', '9', 3, 2, foo=output)
    bo.num('0', '0', 4, 0, foo=output)
    bo.num(".", "period", 4, 1, foo=output)
    bo.num("=", "Return", 4, 2, 'brown', foo=equally)
    bo.num("÷", "slash", 1, 3, 'brown', foo=count)
    bo.num("×", "asterisk", 2, 3, 'brown', foo=count)
    bo.num("-", "minus", 3, 3, 'brown', foo=count)
    bo.num("+", "plus", 4, 3, 'brown', foo=count)
    bo.num(text="C", row=0, column=3, fg='red', foo=clear)
    
    # Bind keyboard keys. Simultaneously to Linux and Windows
    def num(event):
        key = event.keysym
        if key in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'period',
                   'KP_1', 'KP_2', 'KP_3', 'KP_4', 'KP_5', 'KP_6', 'KP_7',
                   'KP_8', 'KP_9', 'KP_0', 'KP_Decimal'}:
            key = key.replace("KP_", "")
            if key == 'Decimal':
                key = 'period'
            output(out, key)
        elif key == 'plus' or key == 'KP_Add':
            count(out, 'plus')
        elif key == 'asterisk' or key == 'KP_Multiply':
            count(out, 'asterisk')
        elif key == 'minus' or key == 'KP_Subtract':
            count(out, 'minus')
        elif key == 'slash' or key == 'KP_Divide':
            count(out, 'slash')
        elif key == 'Return' or key == 'KP_Enter':
            equally(out, 'Return')
        elif key == 'Delete' or key == 'Escape':
            clear(out, key)
    root.bind_all('<KeyPress>', num)

    root.mainloop()


def output(out, text):
    global countflag
    global firstdigit
    out.config(state=NORMAL)
    if out.get() == "Error":
        out.config(state="readonly")
        return
    if text == "period":
        text = "."
    if (out['bg'] == 'black' or out['bg'] == 'gray' or out['bg']
                  == 'green' or out['bg'] == 'yellow') and not countflag:
        out.delete(0, "end")
        if text == "0":
            # out.config(bg='blue')
            out.insert(0, "0")
            out.config(state="readonly")
            return
        if text == ".":
            if firstdigit != '0':
                print(end='0')      # Console calculator.
            out.insert(0, "0")
        countflag = True
    if out['bg'] == 'blue':  # The "bg" parameter is used as a flag.
        if firstdigit == '0' and text == '.':
            print(end='0')         # Console calculator.
        out.config(bg='red')
        if text == "0":
            out.config(bg='blue')
            out.config(state="readonly")
            return
        if text != ".":
            out.delete(0, "end")
    if text == "." and out.get().find(".") != -1 or len(out.get()) > 10:
        out.config(state="readonly")
        return
    value = out.get() + text
    print(end=text)         # Console calculator.
    out.delete(0, "end")
    out.insert(0, value)
    out.config(state="readonly")


def clear(out, blank=None):  # Return the flags to their original position.
    global firstdigit
    global countflag
    out.config(state=NORMAL)
    if out.get() != '0':
        print(end=('\r' + 'Clear' + ' ' * 21 + '\n'))  # Console calculator.
    out.config(bg='blue')
    out.delete(0, "end")
    out.insert(0, "0")
    out.config(state="readonly")
    firstdigit = '0'
    countflag = False


def count(out, sign):
    global firstdigit
    global countflag
    out.config(state=NORMAL)
    if out.get() == "Error":
        countflag = False
        out.config(state="readonly")
        return
    if firstdigit != '0':
        print(end='')  # Console calculator.
        equally(out, sign)
        count(out, sign)
        out.config(state="readonly")
        return
    else:
        firstdigit = out.get()
    if sign == "plus":
        out.config(bg='black')
        print(end=' + ')     # Console calculator.
    elif sign == "minus":
        out.config(bg='gray')
        print(end=' - ')     # Console calculator.
    elif sign == "asterisk":
        out.config(bg='green')
        print(end=' × ')     # Console calculator.
    elif sign == "slash":
        out.config(bg='yellow')
        print(end=" / ")     # Console calculator.
    out.config(state="readonly")


def equally(out, blank=None):
    global countflag
    global firstdigit
    out.config(state=NORMAL)
    if out['bg'] == 'black':
        result = float(firstdigit) + float(out.get())
    elif out['bg'] == 'gray':
        result = float(firstdigit) - float(out.get())
    elif out['bg'] == 'green':
        result = float(firstdigit) * float(out.get())
    elif out['bg'] == 'yellow':
        if float_to_string(float(out.get())) == "0":
            # Division by zero.
            # I create an overflow to trigger the error just below.
            result = 1000000000000
        else:
            result = float(firstdigit) / float(out.get())
    else:
        out.config(state="readonly")
        return
    # I round up to the capacity of the output.
    result = round(float(result), 11 - len(str(int(result)))) 
    # We restrict the output to the capacity of the visible part of the field.
    if len(str(int(result))) > 11:  
        out.delete(0, "end")
        out.insert(0, "Error")
        out.config(bg='blue')
    else:
        out.delete(0, "end")
        out.insert(0, float_to_string(result))
        firstdigit = '0'
        out.config(bg='blue')
    print(end=(' = ' + out.get()) + '\n')  # Console calculator.
    countflag = False
    out.config(state="readonly")


def float_to_string(num):
    return ('%i' if num == int(num) else '%s') % num


if __name__ == "__main__":
    countflag = False
    firstdigit = '0'
    aboutflag = False
    main()
