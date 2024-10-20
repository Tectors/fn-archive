#!/usr/bin/python3

# Global functions used
from requests import get
import os.path
import base64
import time

def parse_build_version(BuildVersion) -> str:
    platform = BuildVersion.split('-')[-1]
    type = BuildVersion.split('-')[0]
    version = BuildVersion.split('-')[1]
    netcl  = BuildVersion.split('-')[3]

    return {
        "platform": platform,
        "type": type,
        "version": version,
        "netcl": netcl,
    }

def add_pak_content(pak):
    listing = []

    # Read the full SVG template
    with open('./.github/source/dependents/templates/definition.svg', 'r') as template_file:
        full_template = template_file.read()

    try:
        # Fetch cosmetics data from the API
        url = f'https://fortnite-api.com/v2/cosmetics/br/search/all?dynamicPakId={pak}'
        cosmetics_data = get(url).json().get('data', [])

        for file in reversed(cosmetics_data):
            svg_path = f'./.github/source/dependents/referred/{file["id"]}.svg'

            # Skip if the SVG already exists
            if os.path.exists(svg_path):
                listing.append(file['id'])
                continue
            
            print(f'Added new SVG with the id: {file["id"]}')
            time.sleep(2) # Rate limiting

            # Fetch the icon image
            response = get(file['images']['icon'])

            if response.status_code != 200:
                print(f"Failed to download image for ID {file['id']}: {response.status_code}")
                continue

            print(f'Response on #{pak} pak (#{file["id"]})')

            # Encode the image in base64
            encoded_image = base64.b64encode(response.content).decode('ascii')
            content = full_template.replace('{0}', f'data:image/png;base64,{encoded_image}')

            # Write the SVG file
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(content)
                listing.append(file['id'])

    except Exception as e:
        print(f'Error on {pak}: {e}')
        return listing

    return listing

def save_image(content, name):
    image_path = f'./.github/source/dependents/monthly-rotaton/{name}'
    with open(image_path, "wb") as f:
        f.write(content)
    
    return name