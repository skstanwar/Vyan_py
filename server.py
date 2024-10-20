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
def play_station(station_url):
    st.write(f"""
        <style>
            /* Full-width audio player */
            audio {{
                width: 100%;
            }}

            /* Light blinking effect */
            .blinking-light {{
                width: 50px;
                height: 50px;
                background-color: navy;
                border-radius: 50%;
                margin: 20px auto;
                animation: blink 1s infinite;
                box-shadow: 0 0 10px rgba(0, 0, 128, 0.8);
            }}

            /* Keyframes for the blinking animation */
            @keyframes blink {{
                0% {{ box-shadow: 0 0 5px rgba(0, 0, 128, 0.2); }}
                50% {{ box-shadow: 0 0 20px rgba(0, 0, 255, 1); }}
                100% {{ box-shadow: 0 0 5px rgba(0, 0, 128, 0.2); }}
            }}
        </style>

        <!-- Blinking light container -->
        <div class="blinking-light" id="blinking_light"></div>

        <!-- Audio player -->
        <audio id="audio_player" controls autoplay>
            <source src="{station_url}" type="audio/mpeg">
        </audio>

        <script>
            var audioPlayer = document.getElementById('audio_player');
            var light = document.getElementById('blinking_light');

            // Synchronize blinking light with the audio state
            audioPlayer.onplay = function() {{
                light.style.animationPlayState = 'running';
            }};

            audioPlayer.onpause = function() {{
                light.style.animationPlayState = 'paused';
            }};
        </script>
    """, unsafe_allow_html=True)
if stations:
    station_names = [station['name'] for station in stations]
    
    # Store the selected station in session state
    if 'selected_station' not in st.session_state:
        st.session_state.selected_station = station_names[0]

    # User selects a station from the list
    selected_station = st.selectbox("Select a radio station:", station_names, index=station_names.index(st.session_state.selected_station))

    # Update the selected station in session state
    if st.session_state.selected_station != selected_station:
        st.session_state.selected_station = selected_station
        st.experimental_set_query_params()  # Rerun the app after selecting a station

    # Get the selected station's stream URL
    selected_station_index = station_names.index(st.session_state.selected_station)
    station_url = stations[selected_station_index]['url']
    
    # Automatically play the selected station
    st.write(f"Playing: {st.session_state.selected_station}")
    play_station(station_url)

else:
    st.write("No stations found. Try searching for a different station.")
