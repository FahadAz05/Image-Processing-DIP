import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def stretch(img, a, b):
    # Compute the histogram stretch
    return np.clip((img - np.min(img)) * ((b - a) / (np.max(img) - np.min(img))) + a, 0, 255).astype(np.uint8)

def shrink(img, a, b):
    # Compute the histogram shrinkage
    return np.clip((img - np.min(img)) * ((b - a) / (np.max(img) - np.min(img))) + a, a, b).astype(np.uint8)

def apply_stretch_shrink(stretch_func):
    # Get the selected image
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    # Load the image
    img = Image.open(file_path)
    img_array = np.array(img)
    
    # Get the stretch/shrink parameters
    a = int(entry_a.get())
    b = int(entry_b.get())
    
    # Apply the stretch/shrink
    result_array = stretch_func(img_array, a, b)
    
    # Convert the result back to an image
    result_img = Image.fromarray(result_array)
    
    # Display the result
    result_img_tk = ImageTk.PhotoImage(result_img)
    label_image.configure(image=result_img_tk)
    label_image.image = result_img_tk

# Create the main window
root = tk.Tk()
root.title("Histogram Stretch/Shrink")

# Create the image display label
label_image = tk.Label(root)
label_image.pack()

# Create the entry fields for stretch/shrink with labels
tk.Label(root, text="Enter value for a (min intensity):").pack()
entry_a = tk.Entry(root)
entry_a.pack()
entry_a.insert(0, "0")  # Default value for a

tk.Label(root, text="Enter value for b (max intensity):").pack()
entry_b = tk.Entry(root)
entry_b.pack()
entry_b.insert(0, "255")  # Default value for b

# Create the apply stretch and shrink buttons
button_stretch = tk.Button(root, text="Apply Stretch", command=lambda: apply_stretch_shrink(stretch))
button_stretch.pack()

button_shrink = tk.Button(root, text="Apply Shrink", command=lambda: apply_stretch_shrink(shrink))
button_shrink.pack()

# Start the GUI loop
root.mainloop()