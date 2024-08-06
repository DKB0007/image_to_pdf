import base64
import streamlit as st
import img2pdf
from tempfile import NamedTemporaryFile

# Function to generate a PDF from ordered images
def generate_ordered_pdf(image_order):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_bytes = img2pdf.convert(image_order)
        tmp.write(pdf_bytes)
        return tmp.name

# Custom CSS to add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data_url = f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{data_url}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Add background image
    add_bg_from_local("pexels-catiamatos-1072179.jpg")

    # Add a logo and enhance the title
    logo = "logo.jpg"  # Provide the path to your logo image
    st.image(logo, width=150)
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Image to PDF Converter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555;'>Upload your images and specify the page order to create a customized PDF.</p>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader("Upload images", type=["jpg", "jpeg", "png", "bmp", "gif"], accept_multiple_files=True)

    if uploaded_files:
        st.subheader("Specify the page order for each image:")
        
        image_order = []
        for i, uploaded_file in enumerate(uploaded_files):
            with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(uploaded_file.read())
                tmp.seek(0)
                image_path = tmp.name
                
                cols = st.columns([1, 2])
                cols[0].image(image_path, caption=f"Image {i + 1}", use_column_width=True)
                page_number = cols[1].number_input(f"Page number for Image {i + 1}", min_value=1, value=i + 1)
                image_order.append((page_number, image_path))
        
        image_order.sort()

        if st.button("Convert to PDF"):
            ordered_images = [img for _, img in image_order]
            pdf_path = generate_ordered_pdf(ordered_images)
            
            st.success("PDF generated successfully!")
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="output.pdf")

if __name__ == "__main__":
    main()
