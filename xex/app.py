import streamlit as st
import sqlite3
import uuid
from PIL import Image, ImageDraw, ImageFont
import qrcode
from datetime import datetime

# Database functions
def create_database():
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    
    # Create the students table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            student_name TEXT
        )
    ''')
    
    # Create the certificates table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY,
            cert_id TEXT UNIQUE,
            student_id TEXT,
            university_name TEXT,
            date_of_issue TEXT,
            description TEXT,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def register_student(student_name):
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    
    student_id = str(uuid.uuid4())
    cursor.execute('INSERT INTO students (student_id, student_name) VALUES (?, ?)', (student_id, student_name))
    
    conn.commit()
    conn.close()
    return student_id

def issue_certificate(student_id, university_name, date_of_issue, description):
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    
    cert_id = str(uuid.uuid4())
    cursor.execute('INSERT INTO certificates (cert_id, student_id, university_name, date_of_issue, description) VALUES (?, ?, ?, ?, ?)', 
                   (cert_id, student_id, university_name, date_of_issue, description))
    
    conn.commit()
    conn.close()
    return cert_id

def validate_certificate(cert_id):
    conn = sqlite3.connect('certificates.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM certificates WHERE cert_id=?', (cert_id,))
    certificate = cursor.fetchone()
    
    conn.close()
    return certificate

# Certificate Image Generation
def generate_certificate_image(cert_id, student_name, university_name, date_of_issue, description):
    width, height = 700, 480
    image = Image.new('RGB', (width, height), 'white')
    qr_imgage_0 = Image.new('RGB', (1000, 1000), 'white')
    draw = ImageDraw.Draw(image)
    
    font_large = ImageFont.truetype("arial.ttf", 40)
    font_medium = ImageFont.truetype("arial.ttf", 30)
    font_small = ImageFont.truetype("arial.ttf", 20)
    
    draw.text((50, 50), "Congratulations!", font=font_large, fill='black')
    draw.text((50, 120), f"Name: {student_name}", font=font_medium, fill='black')
    draw.text((50, 180), f"University: {university_name}", font=font_medium, fill='black')
    draw.text((50, 240), f"Date of Issue: {date_of_issue}", font=font_medium, fill='black')
    draw.text((50, 300), f"Certificate Description: {description}", font=font_small, fill='black')
    draw.text((50, 340), f"Certificate ID: {cert_id}", font=font_small, fill='black')
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=30, border=2)
    qr.add_data(cert_id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # image.paste(qr_img, (500, 300))
    
    qr_imgage_0.paste(qr_img)
    return image, qr_imgage_0

# Streamlit UI
st.title("Certificate Issuance and Verification System")

create_database()

role = st.sidebar.radio("Choose your role", ["Student", "University", "Viewer"])

if role == "Student":
    student_name = st.text_input("Enter your name:")
    if st.button("Register"):
        student_id = register_student(student_name)
        st.success(f"Registration successful! Your Student ID is: {student_id}")

elif role == "University":
    student_id = st.text_input("Enter Student ID:")
    university_name = st.text_input("Enter University Name:")
    date_of_issue = st.date_input("Date of Issue:")
    description = st.text_input("Certificate Description:")
    if st.button("Issue Certificate"):
        cert_id = issue_certificate(student_id, university_name, date_of_issue.strftime('%Y-%m-%d'), description)
        if cert_id:
            student_name = validate_certificate(cert_id)[2]  # Fetching student_name based on the returned certificate for image generation
            certificate_img = generate_certificate_image(cert_id, student_name, university_name, date_of_issue.strftime('%Y-%m-%d'), description)
            st.image(certificate_img[0], caption="Your Certificate")
            
                
            st.image(certificate_img[1], caption="Your Certificate QR Code")           
            st.success(f"Certificate issued! Certificate ID is: {cert_id}")

elif role == "Viewer":
    cert_id = st.text_input("Enter Certificate ID:")
    if st.button("Validate"):
        certificate = validate_certificate(cert_id)
        if certificate:
            st.success(f"This is a valid certificate issued to {certificate[2]} By {certificate[3]} on {certificate[4]}. Certificate is about: {certificate[5]}")
        else:
            st.error("Invalid Certificate ID!")
