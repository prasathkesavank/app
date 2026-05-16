# app.py

import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="K7 Builders",
    page_icon="🏠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #0e1117;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    background-color: #d4af37;
    color: black;
    font-size: 18px;
    font-weight: bold;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background-color: #1c1f26;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

.metric-box {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.title("🏠 K7 Builders")
st.subheader("Building Homes, Workplaces, Gardening & Landscaping")

st.image(
    "https://images.unsplash.com/photo-1504307651254-35680f356dfd",
    use_container_width=True
)

# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-box">
        <h2>250+</h2>
        <p>Projects Completed</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box">
        <h2>500+</h2>
        <p>Happy Clients</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box">
        <h2>15+</h2>
        <p>Years Experience</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- SERVICES ----------------

st.header("🛠 Services")

services = [
    "🏡 Home Construction",
    "🏢 Office Construction",
    "🌳 Landscaping",
    "🪴 Gardening",
    "🎨 Interior Design",
    "🔨 Renovation"
]

cols = st.columns(3)

for i, service in enumerate(services):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card">
            <h3>{service}</h3>
            <p>Professional quality service with modern design and planning.</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ---------------- COST ESTIMATOR ----------------

st.header("💰 AI Construction Cost Estimator")

col1, col2 = st.columns(2)

with col1:

    building_type = st.selectbox(
        "Select Building Type",
        ["House", "Villa", "Apartment", "Office"]
    )

    area = st.number_input(
        "Enter Area (sq.ft)",
        min_value=500,
        max_value=20000,
        value=1200
    )

    floors = st.slider(
        "Number of Floors",
        1,
        10,
        1
    )

with col2:

    quality = st.selectbox(
        "Material Quality",
        ["Basic", "Premium", "Luxury"]
    )

    interior = st.selectbox(
        "Interior Style",
        ["Modern", "Classic", "Minimal", "Luxury"]
    )

    landscaping = st.multiselect(
        "Landscaping Features",
        ["Lawn", "Swimming Pool", "Water Fountain", "Garden Lights"]
    )

# ---------------- COST LOGIC ----------------

if st.button("Calculate Estimate"):

    if quality == "Basic":
        rate = 2400

    elif quality == "Premium":
        rate = 2700

    else:
        rate = 3500

    construction_cost = area * floors * rate

    landscape_cost = 0

    if "Lawn" in landscaping:
        landscape_cost += 50000

    if "Swimming Pool" in landscaping:
        landscape_cost += 300000

    if "Water Fountain" in landscaping:
        landscape_cost += 80000

    if "Garden Lights" in landscaping:
        landscape_cost += 30000

    total_cost = construction_cost + landscape_cost

    duration = floors * 4

    st.success("✅ Estimation Completed")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Construction Cost",
            f"₹ {construction_cost:,.0f}"
        )

    with col2:
        st.metric(
            "Landscaping Cost",
            f"₹ {landscape_cost:,.0f}"
        )

    with col3:
        st.metric(
            "Total Cost",
            f"₹ {total_cost:,.0f}"
        )

    st.info(f"⏳ Estimated Completion Time: {duration} Months")

st.divider()

# ---------------- CONTACT FORM ----------------

st.header("📞 Contact K7 Builders")

with st.form("contact_form"):

    name = st.text_input("Your Name")

    phone = st.text_input("Phone Number")

    location = st.text_input("Project Location")

    requirement = st.text_area(
        "Describe Your Requirement"
    )

    submit = st.form_submit_button("Submit")

    if submit:

        # ---------------- SAVE DATA ----------------

        data = {
            "Name": [name],
            "Phone": [phone],
            "Location": [location],
            "Requirement": [requirement],
            "Time": [datetime.now()]
        }

        df = pd.DataFrame(data)

        try:
            old = pd.read_csv("leads.csv")
            new = pd.concat([old, df], ignore_index=True)
            new.to_csv("leads.csv", index=False)

        except:
            df.to_csv("leads.csv", index=False)

        # ---------------- EMAIL SETTINGS ----------------

        sender_email = "Prasathkesavan93_bec26@mepcoeng.ac.in"

        sender_password = "9944204999"

        receiver_email = "c1nithinsanthoshk23@gmail.com"

        subject = "New Customer Request - K7 Builders"

        body = f"""
New customer enquiry received.

Name: {name}

Phone: {phone}

Location: {location}

Requirement:
{requirement}

Submitted At:
{datetime.now()}
"""

        # ---------------- SEND EMAIL ----------------

        try:

            msg = MIMEMultipart()

            msg["From"] = sender_email

            msg["To"] = receiver_email

            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                sender_email,
                sender_password
            )

            server.sendmail(
                sender_email,
                receiver_email,
                msg.as_string()
            )

            server.quit()

            st.success(
                "✅ Request Submitted Successfully!"
            )

        except Exception as e:

            st.error(f"Email Error: {e}")

st.divider()

# ---------------- GALLERY ----------------

st.header("🏗 Project Gallery")

gallery = st.columns(3)

images = [
    "https://images.unsplash.com/photo-1505691938895-1758d7feb511",
    "https://images.unsplash.com/photo-1494526585095-c41746248156",
    "https://images.unsplash.com/photo-1448630360428-65456885c650"
]

for i in range(3):

    with gallery[i]:

        st.image(
            images[i],
            use_container_width=True
        )

st.divider()

# ---------------- FOOTER ----------------

st.markdown("""
<center>

### K7 Builders

Building Your Dreams 🏠

📍 Madurai, Tamil Nadu

📞 +91 9042460030, 9944204999

📧 c1nithinsanthoshk23@gmail.com

</center>
""", unsafe_allow_html=True)
