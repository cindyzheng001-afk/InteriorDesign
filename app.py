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

# --- 2. AI FUNCTIONS ---

def generate_room_image(style, user_notes, original_image=None):
    """
    Generates a room design. 
    """
    if not client: return None
    
    # Base prompt
    prompt = f"A photorealistic interior design photo of a {style} room. {user_notes}. High quality, 8k resolution, architectural photography."
    
    try:
        # Attempt 1: Standard Generation (Imagen 3)
        response = client.models.generate_image(
            model='imagen-3.0-generate-001',
            prompt=prompt,
            config=types.GenerateImageConfig(number_of_images=1)
        )
        return response.generated_images[0].image

    except AttributeError:
        # Attempt 2: Fallback for different SDK versions
        try:
            # Some versions use plural 'generate_images'
            response = client.models.generate_images(
                model='imagen-3.0-generate-001',
                prompt=prompt,
                config=types.GenerateImageConfig(number_of_images=1)
            )
            return response.generated_images[0].image
        except Exception as e2:
            st.error(f"Generation Error (Check Library Version): {e2}")
            return None
            
    except Exception as e:
        st.error(f"Image Generation Failed: {e}")
        return None

def extract_product_data(image):
    """
    Uses Gemini Vision to 'mine' the generated image for specific products.
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

# --- 3. USER INTERFACE ---

st.title("✨ AI Interior Decorator")
st.markdown("### Final Project: End-to-End Design Miner")

# Sidebar for inputs
with st.sidebar:
    st.header("Project Controls")
    
    # Mode Selection
    mode = st.radio("1. Choose Mode", ["Redesign Existing Room", "Design from Scratch"])
    
    uploaded_file = None
    # Logic: Only show uploader if "Redesign" is selected
    if mode == "Redesign Existing Room":
        uploaded_file = st.file_uploader("2. Upload Room Photo", type=['jpg', 'png', 'jpeg'])
    else:
        st.info("✨ Creative Mode: Describe your dream room below.")

    # Style Selection
    style = st.selectbox("3. Select Style", 
        ["Modern Minimalist", "Bohemian Chic", "Industrial Loft", 
         "Mid-Century Modern", "Scandinavian", "Cyberpunk", "Luxury Art Deco"])
    
    # Custom Prompt
    notes = st.text_area("4. Custom Requests", "e.g., Make the sofa dark blue, add a large rug.")
    
    # Check for API Key
    if not api_key:
        st.warning("⚠️ API Key missing. Please check your settings.")
    
    # Run Button
    run_btn = st.button("🎨 Generate Design", type="primary")

# Main Display Layout
col1, col2 = st.columns(2)

# -- LOGIC HANDLER --

# Case 1: Redesign Mode
if mode == "Redesign Existing Room":
    if uploaded_file:
        original_img = Image.open(uploaded_file)
        with col1:
            st.subheader("Original Room")
            st.image(original_img, use_container_width=True)
    else:
        with col1:
            st.info("👈 Please upload an image to start.")

# Case 2: Scratch Mode
elif mode == "Design from Scratch":
    with col1:
        st.subheader("Your Concept")
        st.markdown(f"**Style:** {style}")
        st.markdown(f"**Notes:** {notes}")
        st.caption("(Generating from blank canvas...)")

# -- GENERATION TRIGGER --
if run_btn and api_key:
    # Validation
    if mode == "Redesign Existing Room" and not uploaded_file:
        st.error("Please upload an image first!")
        st.stop()

    with st.spinner("🤖 AI is processing..."):
        # Step 1: Generate
        new_room_img = generate_room_image(style, notes, None)
        
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
