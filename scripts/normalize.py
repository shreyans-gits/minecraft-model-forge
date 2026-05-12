import os
import json

class Normalize:
    def __init__(self):
        pass

    def normalize_model(self, data):
        normalized = {}
        
        if "elements" in data and isinstance(data["elements"], list):
            clean_elements = []
            for element in data["elements"]:
                clean_el = {k: v for k, v in element.items() if not k.startswith("__")}
                clean_elements.append(clean_el)
            normalized["elements"] = clean_elements

        if "textures" in data and isinstance(data["textures"], dict):
            normalized["textures"] = {key: "#0" for key in data["textures"]}

        if "display" in data:
            normalized["display"] = data["display"]

        return normalized
    
    def normalize_dataset(self, processed_dir, normalized_dir):
        os.makedirs(normalized_dir, exist_ok=True)
        stats = {"success": 0, "error": 0}

        for filename in os.listdir(processed_dir):
            input_path = os.path.join(processed_dir, filename)
            output_path = os.path.join(normalized_dir, filename)

            if not os.path.isfile(input_path):
                continue

            try:
                with open(input_path, 'r') as f:
                    data = json.load(f)
                clean_data = self.normalize_model(data)
                with open(output_path, 'w') as f:
                    json.dump(clean_data, f, indent=4)
                stats["success"] += 1

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                stats["error"] += 1
        return stats


    def print_summary(self, stats):
        """Prints results of the normalization pass."""
        print("\n" + "="*30)
        print("NORMALIZATION COMPLETE")
        print("="*30)
        print(f"Successfully normalized: {stats['success']}")
        print(f"Unexpected failures:     {stats['error']}")
        print("="*30)

if __name__ == "__main__":
    PROCESSED_DIR = "data/processed"
    NORMALIZED_DIR = "data/normalized"
    
    normalize = Normalize()
    results = normalize.normalize_dataset(PROCESSED_DIR, NORMALIZED_DIR)
    normalize.print_summary(results)