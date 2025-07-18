# app.py
import streamlit as st
from scraper import scrape_behance_images

st.set_page_config(page_title="Behance Image Search", layout="wide")

st.title("🔍 Behance Image Scraper")

query = st.text_input("Enter a search term", value="palestine")

if st.button("Search"):
    with st.spinner("Scraping images..."):
        try:
            image_urls = scrape_behance_images(f"https://www.behance.net/search/images/{query}")
            if not image_urls:
                st.warning("No images found.")
            else:
                st.success(f"Found {len(image_urls)} images.")
                cols = st.columns(3)
                for i, url in enumerate(image_urls):
                    cols[i % 3].image(url, use_column_width="auto")
        except Exception as e:
            st.error(f"Scraping failed: {e}")
