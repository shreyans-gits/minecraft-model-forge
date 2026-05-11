import json
import os
import shutil

class Filter:
    def __init__(self):
        pass

    def _isValid(self,filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            return False, "invalid_json"
        
        if "elements" not in data:
            return False, "missing_elements_key"

        elements = data["elements"]
        if not isinstance(elements, list):
            return False, "elements_not_a_list"

        count = len(elements)
        if count < 3:
            return False, "too_simple"
        if count > 64:
            return False, "too_complex"

        return True, "passed"
        
    def filter_dataset(self, raw_dir, processed_dir):
        os.makedirs(processed_dir, exist_ok=True)
        stats = {
            "passed": 0,
            "invalid_json": 0,
            "missing_elements_key": 0,
            "elements_not_a_list": 0,
            "too_simple": 0,
            "too_complex": 0
        }

        for filename in os.listdir(raw_dir):
            raw_path = os.path.join(raw_dir, filename)
            
            if not os.path.isfile(raw_path):
                continue

            valid, reason = self._isValid(raw_path)

            if valid:
                stats["passed"] += 1
                shutil.copy(raw_path, os.path.join(processed_dir, filename))
            else:
                stats[reason] += 1

        return stats
    
    def print_summary(self, stats):
        print("FILTERING SUMMARY")
        print(f"✅ PASSED:  {stats['passed']}")
        print(f"❌ FAILED:  {sum(stats.values()) - stats['passed']}")
        print("-" * 30)
        print("Breakdown of Rejections:")
        for reason, count in stats.items():
            if reason != "passed" and count > 0:
                clean_reason = reason.replace("_", " ").capitalize()
                print(f" - {clean_reason}: {count}")
        print("-" * 30)


if __name__ == "__main__":
    RAW_DATA_DIR = "data/raw"
    PROCESSED_DATA_DIR = "data/processed"

    filter = Filter()
    results = filter.filter_dataset(RAW_DATA_DIR, PROCESSED_DATA_DIR)
    filter.print_summary(results)