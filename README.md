# Traffic Counter Application

A real-time traffic monitoring application that uses computer vision to detect and count vehicles in video streams. The application provides analytics and insights about traffic patterns.

## Features

- Real-time vehicle detection and counting
- Support for multiple vehicle types (cars, trucks, buses, motorcycles, bicycles)
- Traffic flow analysis and visualization
- Speed estimation
- Direction detection
- Mobile-friendly interface
- Export capabilities for processed videos and statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/traffic-counter.git
cd traffic-counter
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to `http://localhost:8501`

3. Upload a video file and adjust settings as needed

4. View real-time processing and analytics

## Project Structure

```
traffic-counter/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── README.md             # Project documentation
├── pages/                # Application pages
│   ├── home.py          # Home page with video upload
│   ├── analytics.py     # Analytics and visualization
│   └── settings.py      # Application settings
└── utils/               # Utility functions
    ├── traffic_counter.py  # Core traffic counting logic
    └── visualization.py   # Data visualization utilities
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YOLOv8 for object detection
- Streamlit for the web interface
- OpenCV for video processing
