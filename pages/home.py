import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from utils.traffic_counter import TrafficCounter
from utils.visualization import create_dashboard, load_traffic_data
import pandas as pd
import time
import os

def is_streamlit_cloud():
    return os.environ.get("STREAMLIT_SERVER_HEADLESS", None) == "1"

def show_home():
    st.title("Traffic Counter")
    
    # Video source selection
    if is_streamlit_cloud():
        video_source = "Upload a video file"
        st.info("Live camera is only available when running locally.")
    else:
        video_source = st.radio("Select video source:", ["Upload a video file", "Use live camera"])
    
    uploaded_file = None
    use_camera = False
    if video_source == "Upload a video file":
        uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi"])
    else:
        use_camera = True
    
    # Counting line position slider
    count_line_pos = st.slider("Counting Line Position (as % of frame height)", min_value=0, max_value=100, value=50, step=1)
    
    if uploaded_file is not None:
        # Save uploaded file
        video_path = Path("temp_video.mp4")
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Initialize traffic counter with custom count line position
        counter = TrafficCounter(str(video_path), count_line_position=count_line_pos / 100.0)
        
        # Create two columns for video and stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Live Feed")
            video_placeholder = st.empty()
            debug_placeholder = st.empty()
            
            # Process video
            frame_skip = 3  # Process every 3rd frame
            for i, (frame, debug_info) in enumerate(counter.process_video(debug=True)):
                if i % frame_skip != 0:
                    continue
                # Convert BGR to RGB and resize for smoother display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb = cv2.resize(frame_rgb, (640, 360))
                video_placeholder.image(frame_rgb, channels="RGB")
                
                # Display debug info with vehicle types
                debug_text = f"Vehicles detected in frame: {debug_info['vehicle_count']}\n"
                for vehicle_type, count in debug_info['vehicles_by_type'].items():
                    debug_text += f"{vehicle_type.replace('_', ' ').title()}: {count}\n"
                debug_placeholder.info(debug_text)
        
        with col2:
            st.subheader("Statistics")
            stats_placeholder = st.empty()
            
            # Display current statistics
            stats = counter.stats
            stats_text = f"""
            ### Total Counts
            - Overall Total: {stats.get('total_count', 0)}
            
            ### By Vehicle Type
            - Cars: {stats.get('car', 0)}
            - Motorcycles: {stats.get('motorcycle', 0)}
            - Buses: {stats.get('bus', 0)}
            - Trucks: {stats.get('truck', 0)}
            - Bicycles: {stats.get('bicycle', 0)}
            
            ### By Direction
            - Northbound: {stats.get('north_count', 0)}
            - Southbound: {stats.get('south_count', 0)}
            
            ### Speed Information
            - Average Speed: {stats.get('avg_speed', 0):.1f} km/h
            """
            stats_placeholder.markdown(stats_text)
        
        # Clean up
        counter.stop_processing()
        video_path.unlink()
    
    # --- Live Camera Option ---
    if use_camera:
        st.info("Starting live camera. Please allow access if prompted.")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Could not open webcam.")
        else:
            counter = TrafficCounter(0, count_line_position=count_line_pos / 100.0)
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Live Camera Feed")
                video_placeholder = st.empty()
                debug_placeholder = st.empty()
                frame_skip = 3
                i = 0
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        st.warning("No frame received from camera.")
                        break
                    i += 1
                    if i % frame_skip != 0:
                        continue
                    processed_frame, debug_info = counter.process_frame(frame, debug=True)
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    frame_rgb = cv2.resize(frame_rgb, (640, 360))
                    video_placeholder.image(frame_rgb, channels="RGB")
                    debug_text = f"Vehicles detected in frame: {debug_info['vehicle_count']}\n"
                    for vehicle_type, count in debug_info['vehicles_by_type'].items():
                        debug_text += f"{vehicle_type.replace('_', ' ').title()}: {count}\n"
                    debug_placeholder.info(debug_text)
                    # Add a stop button
                    if st.button("Stop Camera"):
                        break
                    time.sleep(0.03)
            with col2:
                st.subheader("Statistics")
                stats_placeholder = st.empty()
                stats = counter.stats
                stats_text = f"""
                ### Total Counts
                - Overall Total: {stats.get('total_count', 0)}
                
                ### By Vehicle Type
                - Cars: {stats.get('car', 0)}
                - Motorcycles: {stats.get('motorcycle', 0)}
                - Buses: {stats.get('bus', 0)}
                - Trucks: {stats.get('truck', 0)}
                - Bicycles: {stats.get('bicycle', 0)}
                
                ### By Direction
                - Northbound: {stats.get('north_count', 0)}
                - Southbound: {stats.get('south_count', 0)}
                
                ### Speed Information
                - Average Speed: {stats.get('avg_speed', 0):.1f} km/h
                """
                stats_placeholder.markdown(stats_text)
            cap.release()
            counter.stop_processing()
    
    # Show dashboard if data exists
    st.subheader("Traffic Analysis Dashboard")
    df = load_traffic_data()
    if df is not None and not df.empty:
        fig = create_dashboard(df)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No traffic data available yet. Upload a video to start collecting data.")

    # Only try to access vehicle type data if we have a non-empty DataFrame
    if df is not None and not df.empty:
        vehicle_types = ['car', 'motorcycle', 'bus', 'truck', 'bicycle']
        type_values = [df[col].iloc[-1] if col in df.columns else 0 for col in vehicle_types]
        type_labels = [col.title() for col in vehicle_types]

    # --- RESET BUTTON ---
    st.markdown('---')
    if st.button('Reset All Data'):
        import os
        import shutil
        # Delete traffic_stats.csv if it exists
        if os.path.exists('traffic_stats.csv'):
            os.remove('traffic_stats.csv')
        # Delete all files in traffic_stats/ directory
        if os.path.exists('traffic_stats'):
            shutil.rmtree('traffic_stats')
        # Delete temp video if it exists
        if os.path.exists('temp_video.mp4'):
            os.remove('temp_video.mp4')
        st.success('All statistics and temporary files have been reset.') 