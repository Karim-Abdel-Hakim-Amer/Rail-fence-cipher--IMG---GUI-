import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk

from cipher import rail_fence_encrypt, rail_fence_decrypt
from img_util import load_image, save_image

img = None  # Global variable to store the currently loaded image


def show_image(img, label):
    """
    Convert an OpenCV image to a Tkinter-compatible image
    and display it in the given label.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # OpenCV loads BGR; convert to RGB
    pil_img = Image.fromarray(img_rgb)              # Convert to PIL Image
    pil_img = pil_img.resize((300, 300))           # Resize for display
    tk_img = ImageTk.PhotoImage(pil_img)           # Convert to Tkinter format
    label.config(image=tk_img)                      # Update label with image
    label.image = tk_img                            # Keep reference to prevent GC


def upload_image():
    """Open a file dialog to select an image and show it in the original label."""
    global img
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.png *.jpg *.bmp")]
    )
    if path:
        img = load_image(path)       
        show_image(img, original_label)


def get_rails():
    """
    Read the number of rails from the entry box.
    Returns the rails as an int if valid, else None.
    """
    try:
        rails = int(rails_entry.get())
        if rails < 2:
            raise ValueError
        return rails
    except ValueError:
        messagebox.showerror("Error", "Rails must be an integer ≥ 2")
        return None


def encrypt_image():
    """Encrypt the currently loaded image using Rail Fence cipher."""
    global img
    if img is None:
        messagebox.showerror("Error", "Upload an image first")
        return

    rails = get_rails()
    if rails is None:
        return

    flat = img.flatten().tolist()                   # Flatten image to 1D list
    encrypted = rail_fence_encrypt(flat, rails)     # Encrypt
    encrypted_img = np.array(encrypted, dtype=np.uint8).reshape(img.shape)  # Reshape back

    show_image(encrypted_img, result_label)        # Show encrypted image

    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        save_image(save_path, encrypted_img)       # Save encrypted image


def decrypt_image():
    """Decrypt the currently loaded image using Rail Fence cipher."""
    global img
    if img is None:
        messagebox.showerror("Error", "Upload an image first")
        return

    rails = get_rails()
    if rails is None:
        return

    flat = img.flatten().tolist()                   # Flatten image to 1D list
    decrypted = rail_fence_decrypt(flat, rails)     # Decrypt
    decrypted_img = np.array(decrypted, dtype=np.uint8).reshape(img.shape)  # Reshape back

    show_image(decrypted_img, result_label)        # Show decrypted image

    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        save_image(save_path, decrypted_img)       # Save decrypted image


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Rail Fence Image Cipher")

# Frame for buttons and input
controls = tk.Frame(root)
controls.pack(pady=10)

# Frame for image previews
preview = tk.Frame(root)
preview.pack()

# Upload button
tk.Button(controls, text="Upload Image", command=upload_image).grid(row=0, column=0, padx=5)

# Rails input
tk.Label(controls, text="Rails:").grid(row=0, column=1)
rails_entry = tk.Entry(controls, width=5)
rails_entry.grid(row=0, column=2)
rails_entry.insert(0, "5")  # Default rails = 5

# Encrypt / Decrypt buttons
tk.Button(controls, text="Encrypt", command=encrypt_image).grid(row=0, column=3, padx=5)
tk.Button(controls, text="Decrypt", command=decrypt_image).grid(row=0, column=4, padx=5)

# Labels to show images side by side
original_label = tk.Label(preview, text="Original Image")
original_label.pack(side="left", padx=10)

result_label = tk.Label(preview, text="Result Image")
result_label.pack(side="right", padx=10)

root.mainloop()
