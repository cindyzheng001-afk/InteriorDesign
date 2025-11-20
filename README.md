\# 🛋️ AI Interior Decorator \& Product Miner



\*\*Final Project: Data Mining\*\*

\*Powered by Gemini 3.0 \& Streamlit\*



\## 📖 Project Overview

This application is an end-to-end Data Mining tool that utilizes Generative AI to revolutionize interior design. It performs two key mining operations:

1\.  \*\*Generative Mining:\*\* It takes unstructured input (a room photo) and user intent (style prompts) to generate structured visual output.

2\.  \*\*Extraction Mining:\*\* It uses Multimodal Computer Vision to scan the generated image, identify specific furniture entities, and extract attribute data (Name, Color, Search Query) to create a "Shop the Look" experience.



\## 🚀 Features

\*   \*\*Style Transfer:\*\* Instantly redesign any room into styles like Modern, Bohemian, or Cyberpunk.

\*   \*\*Automated Object Detection:\*\* Identifies furniture within the newly generated image.

\*   \*\*Structured Data Extraction:\*\* Converts visual pixels into a JSON list of purchasable items.

\*   \*\*Direct Shopping Integration:\*\* Generates Google Shopping links for identified items.



\## 🛠️ Tech Stack

\*   \*\*Frontend:\*\* Streamlit (Python)

\*   \*\*AI Engine:\*\* Google Gemini 3 (via `google-genai` SDK)

\*   \*\*Image Processing:\*\* Pillow (PIL)

\*   \*\*Environment Management:\*\* Python Dotenv



\## 💻 How to Run Locally



1\.  \*\*Clone the repository:\*\*

&nbsp;   ```bash

&nbsp;   git clone https://github.com/YOUR\_USERNAME/ai-interior-decorator.git

&nbsp;   cd ai-interior-decorator

&nbsp;   ```



2\.  \*\*Install dependencies:\*\*

&nbsp;   ```bash

&nbsp;   pip install -r requirements.txt

&nbsp;   ```



3\.  \*\*Set up API Key:\*\*

&nbsp;   Create a file named `.env` in the main folder and add your Google Gemini API key:

&nbsp;   ```text

&nbsp;   GEMINI\_API\_KEY=your\_api\_key\_here

&nbsp;   ```



4\.  \*\*Run the App:\*\*

&nbsp;   ```bash

&nbsp;   streamlit run app.py

&nbsp;   ```



\## 🌐 Live Demo

\[Insert your Streamlit Share URL here]


## 📄 License
Copyright © 2025 [Your Name]. All Rights Reserved.
This software is for educational and demonstration purposes. Unauthorized copying, modification, distribution, or commercial use of this code is strictly prohibited.

