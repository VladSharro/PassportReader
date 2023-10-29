import cv2
import pytesseract
import re
import tkinter as tk
from tkinter import filedialog

# Path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function to extract the name and surname in English from a passport image using Tesseract OCR
def extract_name_and_surname(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use thresholding to improve OCR accuracy
    _, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Perform OCR using Tesseract
    extracted_text = pytesseract.image_to_string(thresh_img, config='--psm 6')

    # Split the extracted text into lines
    lines = extracted_text.split('\n')

    name = ""
    surname = ""

    for line in lines:
        pattern = r'<([A-Z]+)<<([A-Z]+)<'
        matches = re.search(pattern, line)
        if matches:
            name = matches.group(1)
            surname = matches.group(2)
            break

    return name, surname

# Function to handle the "Open" button click event
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        name, surname = extract_name_and_surname(file_path)
        result_label.config(text=f'Name: {name}\nSurname: {surname}')

# Create the main application window
app = tk.Tk()
app.title("Passport OCR")

# Create a button for opening files
open_button = tk.Button(app, text="Open File", command=open_file)
open_button.pack()

# Create a label to display the result
result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
