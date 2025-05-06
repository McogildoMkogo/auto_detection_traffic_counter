import streamlit as st
import json
from pathlib import Path

def load_settings():
    settings_file = Path("settings.json")
    if settings_file.exists():
        with open(settings_file, "r") as f:
            return json.load(f)
    return {
        "detection_confidence": 0.5,
        "min_tracking_confidence": 0.3,
        "max_disappeared": 30,
        "save_video": True,
        "save_stats": True,
        "show_debug": False
    }

def save_settings(settings):
    settings_file = Path("settings.json")
    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=4)

def show_settings():
    st.title("Settings ⚙️")
    
    # Load current settings
    settings = load_settings()
    
    # Create a form for settings
    with st.form("settings_form"):
        st.subheader("Detection Settings")
        
        # Detection confidence
        detection_confidence = st.slider(
            "Detection Confidence",
            min_value=0.1,
            max_value=1.0,
            value=settings["detection_confidence"],
            step=0.1,
            help="Minimum confidence threshold for vehicle detection"
        )
        
        # Tracking confidence
        tracking_confidence = st.slider(
            "Tracking Confidence",
            min_value=0.1,
            max_value=1.0,
            value=settings["min_tracking_confidence"],
            step=0.1,
            help="Minimum confidence threshold for vehicle tracking"
        )
        
        # Max disappeared frames
        max_disappeared = st.slider(
            "Max Disappeared Frames",
            min_value=10,
            max_value=100,
            value=settings["max_disappeared"],
            step=5,
            help="Maximum number of frames a vehicle can be missing before being removed from tracking"
        )
        
        st.subheader("Output Settings")
        
        # Save video option
        save_video = st.checkbox(
            "Save Processed Video",
            value=settings["save_video"],
            help="Save the processed video with detection overlays"
        )
        
        # Save stats option
        save_stats = st.checkbox(
            "Save Traffic Statistics",
            value=settings["save_stats"],
            help="Save traffic statistics to CSV file"
        )
        
        # Debug mode
        show_debug = st.checkbox(
            "Show Debug Information",
            value=settings["show_debug"],
            help="Display additional debug information during processing"
        )
        
        # Submit button
        submitted = st.form_submit_button("Save Settings", use_container_width=True)
        
        if submitted:
            # Update settings
            new_settings = {
                "detection_confidence": detection_confidence,
                "min_tracking_confidence": tracking_confidence,
                "max_disappeared": max_disappeared,
                "save_video": save_video,
                "save_stats": save_stats,
                "show_debug": show_debug
            }
            
            # Save settings
            save_settings(new_settings)
            st.success("Settings saved successfully!")
    
    # Display current settings
    st.subheader("Current Settings")
    st.json(settings)
    
    # Reset button
    if st.button("Reset to Default Settings", use_container_width=True):
        default_settings = {
            "detection_confidence": 0.5,
            "min_tracking_confidence": 0.3,
            "max_disappeared": 30,
            "save_video": True,
            "save_stats": True,
            "show_debug": False
        }
        save_settings(default_settings)
        st.success("Settings reset to default values!")
        st.experimental_rerun()

if __name__ == "__main__":
    show_settings() 