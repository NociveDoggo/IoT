import requests


BLYNK_AUTH_TOKEN = "5biBY2fS84cyCHbeU_lgTTEe4EFz-DAY"
ID = "V0"  # String format for virtual pin
SERVER_ADDRESS = "blynk.cloud"

# Properly formatted URL as a string with f-string formatting
# URL = f"https://blynk.cloud/external/api/get?token={BLYNK_AUTH_TOKEN}&dataStreamId={ID}"
URL = f"https://{SERVER_ADDRESS}/external/api/get?token={BLYNK_AUTH_TOKEN}&{ID}"


response = requests.get(URL)
print(response.text)
