import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Function to apply specified histogram equalization
def apply_specified_histogram_equalization(img1, img2):
    # Convert the images to grayscale if they're not already
    if img1.mode != 'L':
        img1 = img1.convert('L')
    if img2.mode != 'L':
        img2 = img2.convert('L')
    
    # Calculate the histograms of the images
    hist1 = img1.histogram()
    hist2 = img2.histogram()
    
    # Calculate the cumulative distribution functions (CDF)
    cdf1 = np.cumsum(hist1)
    cdf2 = np.cumsum(hist2)
    
    # Normalize the CDFs
    cdf1 = (cdf1 - cdf1.min()) * 255 / (cdf1.max() - cdf1.min())
    cdf2 = (cdf2 - cdf2.min()) * 255 / (cdf2.max() - cdf2.min())
    
    # Create a lookup table for histogram matching
    lookup_table = np.interp(cdf1, cdf2, range(256)).astype('uint8')
    
    # Apply the lookup table to the reference image
    matched_img = img1.point(lambda i: lookup_table[i])
    
    return img1, img2, matched_img

# Function to open an image file
def open_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        return Image.open(file_path)

# Function to update the image display
def update_image_display(canvas, img):
    # Resize the image to fit the canvas without preserving the aspect ratio
    img_copy = img.copy()  # Create a copy to avoid modifying the original image
    img_copy.thumbnail((canvas.winfo_width(), canvas.winfo_height()), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img_copy)
    canvas.delete("all")  # Clear the canvas
    canvas.create_image(0, 0, image=photo, anchor='nw')
    canvas.image = photo

# Main GUI application
class HistogramEqualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Specified Histogram Equalization")
        
        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the image display canvases
        self.canvas_img1 = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas_img1.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas_img2 = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas_img2.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.canvas_matched = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas_matched.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create the apply button
        self.button_hist_eq = tk.Button(self.root, text="Apply Specified Histogram Equalization", command=self.specified_histogram_equalization)
        self.button_hist_eq.pack(side=tk.TOP, pady=10)
        
        # Initialize the images
        self.img1 = None
        self.img2 = None
        self.matched_img = None
    
    def specified_histogram_equalization(self):
        # Open two image files
        img1 = open_image()
        img2 = open_image()
        if img1 and img2:
            # Apply specified histogram equalization
            img1, img2, matched_img = apply_specified_histogram_equalization(img1, img2)
            
            # Update the image displays
            update_image_display(self.canvas_img1, img1)
            update_image_display(self.canvas_img2, img2)
            update_image_display(self.canvas_matched, matched_img)

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = HistogramEqualizationApp(root)
    root.mainloop()

 