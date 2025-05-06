import streamlit as st
import cv2
from pathlib import Path
import tempfile
import os
from utils.traffic_counter import TrafficCounter
import time

def show_home():
    st.title("Traffic Counter 🚗")
    
    # Create two columns for mobile-friendly layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Video")
        video_file = st.file_uploader("Choose a video file", type=['mp4', 'avi', 'mov'])
        
        if video_file is not None:
            # Save the uploaded file temporarily
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            video_path = tfile.name
            
            # Get video properties
            cap = cv2.VideoCapture(video_path)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            cap.release()
            
            # Mobile-friendly count line position slider
            st.subheader("Count Line Position")
            count_line_pos = st.slider(
                "Adjust the counting line position",
                min_value=0,
                max_value=100,
                value=50,
                help="Drag to adjust where the counting line appears in the video"
            )
            
            # Process button
            if st.button("Start Processing", use_container_width=True):
                with st.spinner("Processing video..."):
                    try:
                        counter = TrafficCounter(str(video_path), count_line_position=count_line_pos / 100.0)
                        counter.process_video()
                        
                        # Display results in a mobile-friendly way
                        st.success("Processing complete!")
                        
                        # Show results in expandable sections
                        with st.expander("View Results", expanded=True):
                            st.write(f"Total vehicles counted: {counter.total_count}")
                            st.write(f"Processing time: {counter.processing_time:.2f} seconds")
                            
                            # Display the output video
                            if os.path.exists(counter.output_path):
                                st.video(counter.output_path)
                            
                            # Download button for the processed video
                            with open(counter.output_path, 'rb') as f:
                                st.download_button(
                                    label="Download Processed Video",
                                    data=f,
                                    file_name="processed_video.mp4",
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
    
    with col2:
        st.subheader("Instructions")
        st.markdown("""
        1. Upload a video file (MP4, AVI, or MOV)
        2. Adjust the counting line position
        3. Click 'Start Processing'
        4. Wait for the results
        5. Download the processed video
        """)
        
        # Add some helpful tips
        st.info("💡 Tips:")
        st.markdown("""
        - For best results, use videos with clear visibility
        - The counting line should be placed where vehicles cross
        - Processing time depends on video length and quality
        """)

if __name__ == "__main__":
    show_home() 