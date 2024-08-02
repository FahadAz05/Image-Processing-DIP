import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def negative(img):
    # Compute the negative of the image
    return 255 - img

def apply_negative():
    # Get the selected image
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    # Load the image
    img = Image.open(file_path)
    img_array = np.array(img)
    
    # Apply the negative
    result_array = negative(img_array)
    
    # Convert the result back to an image
    result_img = Image.fromarray(result_array)
    
    # Display the result
    result_img_tk = ImageTk.PhotoImage(result_img)
    label_image.configure(image=result_img_tk)
    label_image.image = result_img_tk

# Create the main window
root = tk.Tk()
root.title("Digital Negative")

# Create the image display label
label_image = tk.Label(root)
label_image.pack()

# Create the apply button
button_apply = tk.Button(root, text="Apply Negative", command=apply_negative)
button_apply.pack()

# Start the GUI loop
root.mainloop()