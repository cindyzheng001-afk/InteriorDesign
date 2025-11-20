import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
from google import genai
from google.genai import types
import io
import json

# --- 1. SETUP & CONFIGURATION ---
load_dotenv()
st.set_page_config(page_title="AI Interior Decorator", page_icon="✨", layout="wide")

# Get API Key securely
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize the Google AI Client
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing AI Client: {e}")

# --- 2. AI FUNCTIONS (The "Data Mining" Logic) ---

def generate_room_image(original_image, style, user_notes):
    """
    Uses Imagen 3 (via Gemini SDK) to generate a new room design.
    """
    if not client: return None
    
    # Construct the prompt
    prompt = (
        f"A photorealistic interior design photo of a {style} room. "
        f"{user_notes}. "
        f"High quality, 8k resolution, architectural photography."
    )
    
    try:
        # Generate the image
        response = client.models.generate_image(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(number_of_images=1)
        )
        return response.generated_images[0].image
    except Exception as e:
        st.error(f"Image Generation Failed: {e}")
        return None

def extract_product_data(image):
    """
    Uses Gemini Vision to 'mine' the generated image for specific products.
    Returns a structured JSON list.
    """
    if not client: return []
    
    prompt = """
    Analyze this interior design image. Identify 5 distinct furniture or decor items visible.
    Return the result as a JSON list.
    Each item must have:
    - "name": The name of the item (e.g., "Velvet Sofa")
    - "color": The specific color/material
    - "query": A precise Google Shopping search query
    
    Return ONLY raw JSON. No markdown formatting.
    """

    try:
        # Analyze image
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[image, prompt]
        )
        
        # Clean the text to ensure it is valid JSON
        json_text = response.text.strip()
        if json_text.startswith("```"):
            json_text = json_text.strip("```json").strip("```")
            
        return json.loads(json_text)
    except Exception as e:
        st.warning(f"Could not extract products: {e}")
        return []

# --- 3. USER INTERFACE (The Web App) ---

st.title("✨ AI Interior Decorator")
st.markdown("### Final Project: End-to-End Design Miner")
st.write("Upload a room photo, select a style, and let the AI generate a new look + shopping links.")

# Sidebar for inputs
with st.sidebar:
    st.header("Project Controls")
    
    # Input 1: Image
    uploaded_file = st.file_uploader("1. Upload Room Photo", type=['jpg', 'png', 'jpeg'])
    
    # Input 2: Style
    style = st.selectbox("2. Select Style", 
        ["Modern Minimalist", "Bohemian Chic", "Industrial Loft", 
         "Mid-Century Modern", "Scandinavian", "Cyberpunk", "Luxury Art Deco"])
    
    # Input 3: Custom Prompt
    notes = st.text_area("3. Custom Requests", "e.g., Make the sofa dark blue, add a large rug.")
    
    # Check for API Key
    if not api_key:
        st.warning("⚠️ API Key missing. Please check your settings.")
    
    # Run Button
    run_btn = st.button("🎨 Generate Design", type="primary")

# Main Display Layout
col1, col2 = st.columns(2)

# Logic to run when button is clicked
if uploaded_file:
    # Load and show original
    original_img = Image.open(uploaded_file)
    with col1:
        st.subheader("Original Room")
        st.image(original_img, use_container_width=True)

    if run_btn and api_key:
        with st.spinner("🤖 AI is processing... (Generating new room design)"):
            # Step 1: Generate
            new_room_img = generate_room_image(original_img, style, notes)
            
        if new_room_img:
            with col2:
                st.subheader(f"✨ Result: {style}")
                st.image(new_room_img, use_container_width=True)
            
            # Step 2: Data Mine
            st.divider()
            st.subheader("🛍️ Product Analysis (Data Mining)")
            st.write("The AI is now analyzing the *newly generated* image to identify purchasable items.")
            
            with st.spinner("🔍 Mining product data..."):
                items = extract_product_data(new_room_img)
                
                if items:
                    # Display items in a nice grid
                    grid = st.columns(3)
                    for i, item in enumerate(items):
                        with grid[i % 3]:
                            st.info(f"**{item['name']}**")
                            st.caption(f"Color: {item['color']}")
                            # Link button
                            q = item['query'].replace(" ", "+")
                            st.markdown(f"[🛒 Find on Google](https://www.google.com/search?q={q}&tbm=shop)")