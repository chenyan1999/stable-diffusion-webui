import os
import re
import pickle
from pathlib import Path

with open("test/files_to_check.pkl", "rb") as f:
    ground_truth = pickle.load(f)

def convert_path(file_path: str) -> str:
    return str(Path(file_path).as_posix()) if os.name == "posix" else file_path

def check_files():
    all_passed = True
    for idx, file_info in enumerate(ground_truth, start=1):
        if os.name == "posix":
            file_path = file_info["linux_path"]
        else:
            file_path = file_info["win_path"]
        
        if not os.path.exists(file_path):
            all_passed = False
            print(f"Test {idx} failed for not finding the target file.")
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        if len(lines) != file_info["num_line"]:
            all_passed = False
            print(f"Test {idx} failed for having wrong number of lines in file.")
            continue
        
        if lines[file_info["at_line"]].strip() != file_info["expected"].strip():
            all_passed = False
            print(f"Test {idx} failed for not finding the target code at line {file_info['at_line']}.")
            continue
        
        
        print(f"Test {idx} passed.")
    return all_passed

if __name__ == "__main__":
    success = check_files()
    
    if success:
        print("All tests passed")
    else:
        print("\n Exist failed tests")