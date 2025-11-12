from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from google.adk.agents.llm_agent import Agent

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    #Geocode: Get Latitude and Longitude
    geolocator = Nominatim(user_agent="city_time_app")
    location = geolocator.geocode(city)
    lat, lon = location.latitude, location.longitude
    #Find Timezone from Coordinates
    tf = TimezoneFinder()
    tz_string = tf.timezone_at(lng=lon, lat=lat)
    #Get Time (Same as your original function)
    timezone = pytz.timezone(tz_string)
    current_time = datetime.now(timezone)
    
    formatted_time = current_time.strftime("%I:%M %p")
    return {"status": "success", "city": city, "time": formatted_time}

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Tells the current time of a given city.",
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
