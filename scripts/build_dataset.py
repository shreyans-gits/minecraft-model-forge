import json
import os

class BuildDataset:
    def __init__(self):
        pass

    def clean_name(self, filename):
        name = os.path.splitext(filename)[0]
        prefixes = ["template_"]
        for p in prefixes:
            if name.startswith(p):
                name = name[len(p):]

        suffixes = [
            "_left", "_right", "_middle", "_single",
            "_1tick", "_2tick", "_3tick", "_4tick",
            "_stage_1", "_stage_2", "_stage_3", "_stage_4",
            "_n", "_ne", "_ns", "_nse", "_nsew", "_nw", "_s", "_se", "_sw", "_w", "_ew", "_new", "_nesw",
            "_alt", "_locked", "_blizzard", "_ultraviolet",
            "_1", "_2", "_3", "_4"
        ]

        changed  = True
        while changed:
            changed = False
            for s in suffixes:
                if name.endswith(s):
                    name = name[:-len(s)]
                    changed = True
                    break

        name = name.replace("_", " ")
        return name.strip().lower()
    
    def serialize_model(self, data):
        return json.dumps(data, separators=(',', ':'))
    
    def build_dataset(self, normalized_dir, output_path):
        stats = {"count" : 0}
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f_out:
            for filename in os.listdir(normalized_dir):
                if not filename.endswith(".json"):
                    continue

                path = os.path.join(normalized_dir,filename)
                try:
                    with open(path,"r") as f_in:
                        data = json.load(f_in)

                    name_prompt = self.clean_name(filename)
                    model_data = self.serialize_model(data)

                    f_out.write(f"[NAME]: {name_prompt}\n")
                    f_out.write(f"[MODEL]: {model_data}\n\n")
                    stats["count"] += 1
                
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        
        return stats

    def print_summary(self, stats, output_path):
        print("\n" + "—"*30)
        print("DATASET GENERATION COMPLETE")
        print("—"*30)
        print(f"Total Examples: {stats['count']}")
        print(f"Output File:    {output_path}")
        print("—"*30)

if __name__ == "__main__":
    NORMALIZED_DIR = "data/normalized"
    DATASET_FILE = "data/dataset.txt"
    
    buildDataset = BuildDataset()
    results = buildDataset.build_dataset(NORMALIZED_DIR, DATASET_FILE)
    buildDataset.print_summary(results, DATASET_FILE)