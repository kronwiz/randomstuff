import tkinter
from PIL import Image, ImageTk

IMG_STORE = {}

# create the tcl interpreter
tk = tkinter.Tk()

def pyimage(*args):
    subcmd = args[0]
    if subcmd == "create":
        imgtype = args[1]  # image type now is ignored
        if args[2] == "-file":
            filename = args[3]
            image = Image.open(filename)
            tkimg = ImageTk.PhotoImage(image)

        else:
            data = args[3]
            tkimg = ImageTk.PhotoImage(data = data)

        tkimg_name = str(tkimg)
        IMG_STORE[tkimg_name] = (image, tkimg)
        return tkimg_name

tk.createcommand("pyimage", pyimage)

def main():
    fin = open("edi_embedded.tcl", "r")
    try:
        edi_tcl = fin.read()
    finally:
        fin.close()

    res = tk.eval(edi_tcl)


if __name__ == '__main__':
    main()



# define a python function
##def pycommand(*args):
##    print "pycommand args:", ", ".join(args)
##
### register it as a tcl command:
##tcl_command_name = "pycommand"
##python_function = pycommand
##cmd = tcl.createcommand(tcl_command_name, python_function)
##
### call it, and print the results:
##result = tcl.eval("pycommand one two three")
##print "tcl result:", result
