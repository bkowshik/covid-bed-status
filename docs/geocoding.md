# Geocoding


## Hospital locations

- Ref: https://docs.google.com/spreadsheets/d/132M1nGBzTap5aCfFLzCdiXl1DTZkPyuQzZPrNe1iyJU/

Copied over the hospital details from the BBMP website into the above Google sheet. Then, using Google Geocoding API, we request `(latitude, longitude)` passing in both the name and address of the hospital. Since, the address of the Government hospitals was not on the list, I used Google Maps to get their addresses.


### Workflow


```bash
# Explort Google Maps API key.
export GOOGLE_MAPS_API_KEY='YOUR_API_KEY'

# Run script to download geo-locations of all the hospitals, one after another.
# NOTE: The raw hospitals dataset is located one directory above.
python geocode_hospitals.py
```


### Issues

- There are `323` hospitals listed but there are some that appear twice on the list. The unique number of hospitals is __`318`__. One example of a hospital that appears twice is _Radhakrishna Multispeciality Hospital Ivf Center._
- There are some hospitals who's address returned did not return any results. For these, we have manually used Google Maps and updated the address in `data/hospitals_raw.csv'. Ex:

```bash
# Previous address.
No3 Millers Tank Bund Road Cunningham Road Opp To Fortune Hotel Vasanth Nagar Bangalore 560052

# Manually updated address from Google Maps.
5/13 5/13 Miller Tank Bund Rd Kaverappa Layout Vasanth Nagar Bengaluru Karnataka 560051
```


### Example

For `Rangadore hospital` with the address `1st Cross Rd Shankarapura Basavanagudi Bengaluru Karnataka 560004` the Google Maps API looks like below:

- https://maps.googleapis.com/maps/api/geocode/json?address=Rangadore+hospital+1st+Cross+Rd+Shankarapura+Basavanagudi+Bengaluru+Karnataka+560004&key=YOUR_API_KEY

The response from Google Geocoding API looks like below:

```json
{
    "results": [
        {
            "address_components": [
                {
                    "long_name": "1st Cross Road",
                    "short_name": "1st Cross Rd",
                    "types": [
                        "route"
                    ]
                },
                {
                    "long_name": "Shankarapuram",
                    "short_name": "Shankarapuram",
                    "types": [
                        "political",
                        "sublocality",
                        "sublocality_level_2"
                    ]
                },
                {
                    "long_name": "Basavanagudi",
                    "short_name": "Basavanagudi",
                    "types": [
                        "political",
                        "sublocality",
                        "sublocality_level_1"
                    ]
                },
                {
                    "long_name": "Bengaluru",
                    "short_name": "Bengaluru",
                    "types": [
                        "locality",
                        "political"
                    ]
                },
                {
                    "long_name": "Bangalore Urban",
                    "short_name": "Bangalore Urban",
                    "types": [
                        "administrative_area_level_2",
                        "political"
                    ]
                },
                {
                    "long_name": "Karnataka",
                    "short_name": "KA",
                    "types": [
                        "administrative_area_level_1",
                        "political"
                    ]
                },
                {
                    "long_name": "India",
                    "short_name": "IN",
                    "types": [
                        "country",
                        "political"
                    ]
                },
                {
                    "long_name": "560004",
                    "short_name": "560004",
                    "types": [
                        "postal_code"
                    ]
                }
            ],
            "formatted_address": "1st Cross Rd, Shankarapuram, Basavanagudi, Bengaluru, Karnataka 560004, India",
            "geometry": {
                "location": {
                    "lat": 12.95345,
                    "lng": 77.5712082
                },
                "location_type": "GEOMETRIC_CENTER",
                "viewport": {
                    "northeast": {
                        "lat": 12.9547989802915,
                        "lng": 77.5725571802915
                    },
                    "southwest": {
                        "lat": 12.9521010197085,
                        "lng": 77.56985921970849
                    }
                }
            },
            "place_id": "ChIJAQAAwJIVrjsR4Xn1wQxeQ5I",
            "plus_code": {
                "compound_code": "XH3C+9F Basavanagudi, Bengaluru, Karnataka, India",
                "global_code": "7J4VXH3C+9F"
            },
            "types": [
                "establishment",
                "health",
                "hospital",
                "point_of_interest"
            ]
        }
    ],
    "status": "OK"
}
```
