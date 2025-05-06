import streamlit as st
from pathlib import Path
import sys
import os
import streamlit.components.v1 as components

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import pages
from pages.home import show_home
from pages.analytics import show_analytics
from pages.settings import show_settings
from pages.about import show_about

# Configure the Streamlit app
st.set_page_config(
    page_title="Traffic Counter",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"  # Better for mobile
)

# Custom CSS for mobile optimization
st.markdown("""
    <style>
        /* Mobile-friendly font sizes */
        @media (max-width: 768px) {
            .stButton>button {
                width: 100%;
                margin: 5px 0;
            }
            .stSelectbox {
                width: 100%;
            }
            .stFileUploader {
                width: 100%;
            }
            .stSlider {
                width: 100%;
            }
            /* Make text more readable on mobile */
            .stMarkdown {
                font-size: 16px;
            }
            /* Adjust spacing for mobile */
            .stApp {
                padding: 1rem;
            }
        }
        /* Hide Streamlit's default menu button on mobile */
        #MainMenu {
            visibility: hidden;
        }
        /* Make the sidebar more mobile-friendly */
        .css-1d391kg {
            padding-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    # Create a mobile-friendly navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Analytics", "Settings"])
    
    if page == "Home":
        show_home()
    elif page == "Analytics":
        show_analytics()
    else:
        show_settings()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Traffic Counter")
    st.sidebar.markdown("Version 1.0")
    st.sidebar.markdown("© 2024 All Rights Reserved")

if __name__ == "__main__":
    main() 