import streamlit as st
import json

# Load voter data
with open("voter_data.json", "r") as f:
    voter_data = json.load(f)

# Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyBqLvvo1yD-1DNKzGexTJbGoqR-OaokipU"

# --- Generate HTML with SVG-based custom renderer ---
def generate_map_html(vote_status=True):
    marker_color = "green" if vote_status else "red"
    status_str = "Voted" if vote_status else "Not Voted"

    # Filter and convert data
    filtered_data = [p for p in voter_data if p.get("voted") == vote_status]
    filtered_json = json.dumps(filtered_data)

    html = f"""
    <!DOCTYPE html>
    <html>
      <head>
        <title>Muslim Voter Map - {status_str}</title>
        <style>
          #map {{
            height: 90vh;
            width: 100%;
          }}
        </style>

        <!-- Load Google Maps + Clusterer -->
        <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}" async defer></script>
        <script src="https://unpkg.com/@googlemaps/markerclusterer/dist/index.min.js"></script>

        <script>
          const data = {filtered_json};

          window.initMap = function() {{
            const map = new google.maps.Map(document.getElementById("map"), {{
              center: {{ lat: 47.6, lng: -122.3 }},
              zoom: 9,
            }});

            const markers = data.map(person => {{
              return new google.maps.Marker({{
                position: {{
                  lat: parseFloat(person.lat),
                  lng: parseFloat(person.lng)
                }},
                icon: "http://maps.google.com/mapfiles/ms/icons/{marker_color}-dot.png",
                title: `${{person.name}} ({status_str})`
              }});
            }});

            const renderer = {{
              render({{ count, position }}) {{
                const color = count > 100 ? "orange" : "blue";
                const svg = window.btoa(`
                  <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40">
                    <circle cx="20" cy="20" r="18" fill="${{color}}" stroke="white" stroke-width="2"/>
                    <text x="20" y="25" text-anchor="middle" font-size="14" fill="white">${{count}}</text>
                  </svg>
                `);
                return new google.maps.Marker({{
                  position,
                  icon: {{
                    url: `data:image/svg+xml;base64,${{svg}}`,
                    scaledSize: new google.maps.Size(40, 40)
                  }}
                }});
              }}
            }};

            new markerClusterer.MarkerClusterer({{
              map,
              markers,
              renderer
            }});
          }};

          // Fallback manual init after everything loads (iframe-safe)
          window.onload = function() {{
            if (typeof google !== "undefined" && google.maps) {{
              window.initMap();
            }}
          }};
        </script>
      </head>
      <body>
        <div id="map"></div>
      </body>
    </html>
    """
    return html

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🗳️ Muslim Voter Map (Private View)")

tab1, tab2 = st.tabs(["✅ Voted", "❌ Not Voted"])

with tab1:
    st.components.v1.html(generate_map_html(True), height=750)

with tab2:
    st.components.v1.html(generate_map_html(False), height=750)

