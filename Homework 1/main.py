import requests
import csv

# Replace with your Google Maps API key
api_key = 'AIzaSyCVUjwJ6nufe64Z8yDUNcYI13sCgBHTdAo'

# Define the API endpoint for the Google Places API
api_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Define the parameters for the request
params = {
    'location': '41.745328, 21.262274',  # Latitude and longitude for Macedonia
    'radius': 50000,  # Radius in meters (adjust as needed)
    'keyword': 'winery',  # Keyword to search for wineries
    'key': api_key
}

# Make the API request
response = requests.get(api_url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'results' in data:
        wineries = data['results']
        with open(f'wineries_0.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['ID', 'Name', 'Address', 'Phone Number', 'International Phone Number', 'Opening hours', 'Website', 'Business status', 'Rating', 'Total Reviewers', 'Google maps URL', 'Latitude', 'Longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for winery in wineries:

                name = winery.get('name', 'N/A')
                business_status = winery.get('business_status', 'N/A')
                place_id = winery.get('place_id', 'N/A')
                address = winery.get('vicinity', 'N/A')
                rating = winery.get('rating', 'N/A')
                total_user_ratings = winery.get('user_ratings_total', 'N/A')
                latitude = winery['geometry']['location']['lat']
                longitude = winery['geometry']['location']['lng']
                
                

                get_place_details = f"https://maps.googleapis.com/maps/api/place/details/json?placeid={place_id}&key={api_key}"
                response_place_details = requests.get(get_place_details)

                weekday_working_hours = list()
                number = 'N/A'
                international_number = 'N/A'
                winery_maps_url = 'N/A'
                website = 'N/A'
                if response_place_details.status_code == 200:
                    response_details = response_place_details.json()
                    if 'result' in response_details:
                        details = response_details['result']
                        if 'current_opening_hours' in details:
                            weekday_working_hours = list(details['current_opening_hours']['weekday_text'])
                        number = details.get('formatted_phone_number', 'N/A')
                        website = details.get('website', 'N/A')
                        winery_maps_url = details['url']
                        
                        international_number= details.get('international_phone_number', 'N/A')
                writer.writerow({
                        'ID': place_id,
                        'Name': name,
                        'Address': address,
                        'Rating': rating,
                        'Phone Number': number,
                        'International Phone Number': international_number,
                        'Opening hours':  weekday_working_hours,
                        'Website': website,
                        'Google maps URL' : winery_maps_url,
                        'Business status': business_status,
                        'Total Reviewers': total_user_ratings,
                        'Latitude': latitude,
                        'Longitude': longitude
                    })
                    
            

else:   
    print(f'Error: Unable to retrieve data. Status code: {response.status_code}')
