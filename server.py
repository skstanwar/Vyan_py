import streamlit as st
import requests
st.set_page_config(page_title="Vyan", page_icon="🎙️", layout="wide")
# Function to search radio stations from Radio-Browser API
def search_stations(query):
    url = f"https://de1.api.radio-browser.info/json/stations/search?name={query}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Function to play the selected station
def play_station(station_url):
    st.write(f"""
        <audio id="audio_player" controls autoplay>
            <source src="{station_url}" type="audio/mpeg">
        </audio>
        <script>
            var audioPlayer = document.getElementById('audio_player');
            function playAudio() {{
                audioPlayer.play();
            }}
            function pauseAudio() {{
                audioPlayer.pause();
            }}
        </script>
    """, unsafe_allow_html=True)

# Streamlit app layout
st.title("Radio Station Player")
st.write("""
    <style>
        .disk-animation {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            background: conic-gradient(from 0deg, #ff6b6b, #556270);
            animation: rotate 3s linear infinite;
            margin: 0 auto; /* Center the disk */
        }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>

    <div class="disk-animation"></div>
    """, unsafe_allow_html=True)
# Search box to find radio stations
query = st.text_input("Search for a radio station:", "")

# Fetch and display search results
stations = search_stations(query) if query else []

if stations:
    # Track the currently selected station's index
    station_names = [station['name'] for station in stations]
    
    # Initialize session state to track the index of the selected station
    if "station_index" not in st.session_state:
        st.session_state.station_index = 0
    
    selected_station = station_names[st.session_state.station_index]
    
    # Display selected station
    st.write(f"Playing: {selected_station}")
    
    # Get the selected station's stream URL
    station_url = stations[st.session_state.station_index]['url']
    
    # Play/pause/next/previous buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("Previous"):
            if st.session_state.station_index > 0:
                st.session_state.station_index -= 1
            else:
                st.session_state.station_index = len(stations) - 1
    
    with col2:
        if st.button("Play"):
            play_station(station_url)
    
    with col3:
        if st.button("Pause"):
            st.write('<script>pauseAudio()</script>', unsafe_allow_html=True)  # Add proper pause functionality later
    
    with col4:
        if st.button("Next"):
            if st.session_state.station_index < len(stations) - 1:
                st.session_state.station_index += 1
            else:
                st.session_state.station_index = 0
    # Add animation for song visualization
    

else:
    st.write("No stations found. Try searching for a different station.")
