from pathlib import Path
import json
import cv2

# Define the project directory dynamically based on the script's location
project_dir = Path(__file__).parent

# Define the path to the LeagueAssets directory
league_assets_dir = project_dir / 'LeagueAssets'

test = 'champion.json'

    # Example to read a JSON file
json_file_path = league_assets_dir / 'en_US' / test
if not json_file_path.exists():
    print(f"The file '{json_file_path}' does not exist.")
else:
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        print(data)

# Define the path to the image file inside img and champion directories
image_file_path = league_assets_dir / 'img' / 'champion' / 'Aatrox.png'
if not image_file_path.exists():
    print(f"The file '{image_file_path}' does not exist.")
else:
    # Read the image
    image = cv2.imread(str(image_file_path))
    
    if image is None:
        print(f"Failed to load image '{image_file_path}'.")
    else:
        # Display the image
        cv2.imshow('Aatrox', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
