from fpdf import FPDF
from tkinter.filedialog import askopenfilenames

# Open file dialog to select images
list_of_images = askopenfilenames(title="Select images to convert to PDF", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])

if not list_of_images:
    print("No images selected.")
    exit()

Pdf = FPDF()

# Add selected images to the PDF
for i in list_of_images:
    Pdf.add_page()
    Pdf.image(i, x=10, y=10, w=190)  # Adjust x, y, w, h as needed

Pdf.output("image_to_pdf_result.pdf", "F")
print("PDF created successfully!")