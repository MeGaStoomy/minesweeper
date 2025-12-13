import tkinter as tk

main = tk.Tk()
frame = tk.Frame(main)

def svgPhotoImage(file_path_name):
        from PIL import Image,ImageTk
        import rsvg,cairo 
        svg = rsvg.Handle(file=file_path_name)
        width, height = svg.get_dimension_data()[:2]
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width), int(height))
        context = cairo.Context(surface)
        #context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
        svg.render_cairo(context)
        tk_image=ImageTk.PhotoImage('RGBA')
        image=Image.frombuffer('RGBA',(width,height),surface.get_data(),'raw','BGRA',0,1)
        tk_image.paste(image)
        return(tk_image)
        
tk_image = svgPhotoImage(r'images/closed.svg')
frame.configure(image=tk_image)
