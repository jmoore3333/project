from pathlib import Path
import json
import cv2
import glob

# Define the project directory dynamically based on the script's location
project_dir = Path(__file__).parent

# Define the path to the LeagueAssets directory
league_assets_dir = project_dir / 'LeagueAssets'

def load_champion_data(champion_name):
    json_file_path = league_assets_dir / 'en_US' / 'champion' / f"{champion_name}.json"
    if not json_file_path.exists():
        print(f"The file '{json_file_path}' does not exist.")
        return None
    
    with open(json_file_path, 'r') as json_file:
        champion_info = json.load(json_file)
    
    return champion_info

def find_best_match(target_image_path, png_files):
    target_image = cv2.imread(target_image_path)
    if target_image is None:
        print(f"Failed to load image '{target_image_path}'.")
        return None, None

    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    best_match_value = -1
    best_match_file = None

    for png_file in png_files:
        template = cv2.imread(png_file, cv2.IMREAD_GRAYSCALE)
        if template is None:
            continue
        
        result = cv2.matchTemplate(target_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > best_match_value:
            best_match_value = max_val
            best_match_file = png_file
    
    return best_match_file, best_match_value

def get_champion_info(image_file_path):
    png_files = glob.glob(str(league_assets_dir / 'img' / 'champion' / '*.png'))

    best_match_file, best_match_value = find_best_match(image_file_path, png_files)

    if best_match_file is not None:
        champion_id = Path(best_match_file).stem  # Get filename without extension
        champion_info = load_champion_data(champion_id)
        
        if champion_info is not None:
            return champion_info, best_match_file
        else:
            print(f"No data found for champion '{champion_id}'.")
            return None, None
    else:
        print("No match found.")
        return None, None

# Example usage:
target_image_path = str(league_assets_dir / 'img' / 'champion' / 'Aatrox.png')
champion_info, best_match_file = get_champion_info(target_image_path)
best_match_image = cv2.imread(best_match_file)
if best_match_image is not None:
        cv2.imshow('Best Match Image', best_match_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
else:
        print(f"Failed to load best match image '{best_match_file}'.")
if champion_info is not None:
    print(f"Champion Info:")
    print(f"Name: {champion_info['data'][Path(best_match_file).stem]['name']}")
    print(f"Name: {champion_info['data'][Path(best_match_file).stem]['title']}")
    
    # Display the best match image
else:
    print("No champion information found.")
