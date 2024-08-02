import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def linear_mapping(img, a, b, c, d):
    # Apply linear mapping equation
    return np.clip((img - a) * ((d - c) / (b - a)) + c, 0, 255).astype(np.uint8)

def non_linear_mapping(img, gamma):
    # Apply non-linear mapping equation (gamma correction)
    return np.clip(255 * (img / 255) ** (1 / gamma), 0, 255).astype(np.uint8)

def apply_mapping():
    # Get the selected image
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    # Load the image
    img = Image.open(file_path)
    img_array = np.array(img)
    
    # Get the mapping parameters
    a = int(entry_a.get())
    b = int(entry_b.get())
    c = int(entry_c.get())
    d = int(entry_d.get())
    gamma = float(entry_gamma.get()) if mapping_var.get() == 2 else 1.0  # Default gamma to 1.0 for linear mapping
    
    # Apply the mapping
    if mapping_var.get() == 1:
        result_array = linear_mapping(img_array, a, b, c, d)
    else:
        result_array = non_linear_mapping(img_array, gamma)
    
    # Convert the result back to an image
    result_img = Image.fromarray(result_array)
    
    # Display the result
    result_img_tk = ImageTk.PhotoImage(result_img)
    label_image.configure(image=result_img_tk)
    label_image.image = result_img_tk

# Create the main window
root = tk.Tk()
root.title("Image Mapping")

# Create the image display label
label_image = tk.Label(root)
label_image.pack()

# Create the mapping type radio buttons
mapping_var = tk.IntVar(value=1)
radio_linear = tk.Radiobutton(root, text="Linear", variable=mapping_var, value=1)
radio_non_linear = tk.Radiobutton(root, text="Non-Linear (Gamma Correction)", variable=mapping_var, value=2)
radio_linear.pack()
radio_non_linear.pack()

# Create the entry fields for linear mapping
tk.Label(root, text="a: ").pack()
entry_a = tk.Entry(root)
entry_a.pack()

tk.Label(root, text="b: ").pack()
entry_b = tk.Entry(root)
entry_b.pack()

tk.Label(root, text="c: ").pack()
entry_c = tk.Entry(root)
entry_c.pack()

tk.Label(root, text="d: ").pack()
entry_d = tk.Entry(root)
entry_d.pack()

# Create the entry field for gamma correction with a label
tk.Label(root, text="Gamma: ").pack()
entry_gamma = tk.Entry(root)
entry_gamma.pack()

# Create the apply button
button_apply = tk.Button(root, text="Apply Mapping", command=apply_mapping)
button_apply.pack()

# Start the GUI loop
root.mainloop()