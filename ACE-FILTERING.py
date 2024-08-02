import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np

# Function to apply ACE1 filtering
def apply_ace1_filtering(img, window_size, k1, k2):
    # Convert the image to grayscale if it's not already
    if img.mode != 'L':
        img = img.convert('L')
    
    # Initialize the output image with the same size and mode as the input image
    output_img = Image.new(img.mode, img.size)
    
    # Calculate the offset for the window
    offset = window_size // 2
    
    # Iterate over the image pixels
    for y in range(offset, img.height - offset):
        for x in range(offset, img.width - offset):
            # Extract the window from the image
            window_pixels = [img.getpixel((x + dx - offset, y + dy - offset)) for dy in range(window_size) for dx in range(window_size)]
            
            # Calculate the mean and standard deviation of the window
            mean = sum(window_pixels) / len(window_pixels)
            std_dev = np.std(window_pixels)
            
            # Apply the ACE1 formula
            new_pixel_value = mean + k1 * std_dev + k2 * (img.getpixel((x, y)) - mean)
            
            # Clip the pixel value to the valid range (0-255)
            new_pixel_value = max(0, min(new_pixel_value, 255))
            
            # Set the new pixel value in the output image
            output_img.putpixel((x, y), int(new_pixel_value))
    
    return output_img

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
    canvas.create_image(0, 0, image=photo, anchor='nw')
    canvas.image = photo

# Main GUI application
class ACE1FilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ACE1 Filtering")
        
        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the image display canvas
        self.canvas_img = tk.Canvas(self.main_frame, width=400, height=400)
        self.canvas_img.pack(padx=10, pady=10)
        
    
        # Create the apply button
        self.button_ace1 = tk.Button(self.root, text="Apply ACE1 Filtering", command=self.ace1_filtering)
        self.button_ace1.pack(side=tk.TOP, pady=10)
        
        # Initialize the image
        self.img = None
    
    def ace1_filtering(self):
        # Open an image file
        img = open_image()
        if img:
            # Get the window size and k1, k2 values from the user
            while True:
                try:
                    window_size = int(input("Enter the window size for ACE1 filtering (must be an odd number): "))
                    if window_size % 2 == 0:
                        print("Window size must be an odd number. Please try again.")
                        continue
                    k1 = float(input("Enter the k1 value for ACE1 filtering: "))
                    k2 = float(input("Enter the k2 value for ACE1 filtering: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter an integer for the window size and floating-point numbers for k1 and k2.")
            
            # Apply ACE1 filtering
            filtered_img = apply_ace1_filtering(img, window_size, k1, k2)
            
            # Update the image display
            update_image_display(self.canvas_img, filtered_img)

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = ACE1FilterApp(root)
    root.mainloop()