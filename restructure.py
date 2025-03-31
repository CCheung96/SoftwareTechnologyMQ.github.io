import os
import shutil
import yaml

# File paths (adjust these to match your actual directory structure)
ROOT_DIR = "/home/crystal/SoftwareTechnologyMQ.github.io"  # Root folder of your Jekyll site
OUTPUT_DIR = "/home/crystal/SoftwareTechnologyMQ.github.io/_posts"  # Posts directory where lessons will go
TOC_PATH = "/home/crystal/SoftwareTechnologyMQ.github.io/_data/toc.yml"  # Path to the TOC YAML file

# Normalize file names by lowercasing and removing spaces
def normalize(filename):
    return filename.lower().replace(" ", "_")

# Read the TOC (Table of Contents) file
with open(TOC_PATH, "r", encoding="utf-8") as file:
    toc_data = yaml.safe_load(file)

# Loop through each unit in the TOC
for unit in toc_data['nav']:
    unit_code = unit['title']  # Get the unit code (COMP1000, COMP1010, etc.)
    subnav = unit.get('subnav', [])  # Get the lessons for this unit

    # Create a directory for the unit (if it doesn't exist)
    unit_folder = os.path.join(OUTPUT_DIR, unit_code.lower())
    os.makedirs(unit_folder, exist_ok=True)

    # Loop through each lesson in the unit's subnav
    for lesson in subnav:
        lesson_title = lesson.get('title')  # The lesson's title (for example "Transition to Processing")
        lesson_url = lesson.get('url')  # The URL of the lesson (e.g., "/transition_to_processing")

        # We expect that lesson URL corresponds to a markdown file
        # Search for the lesson markdown file in the root directory
        source_file = None
        for filename in os.listdir(ROOT_DIR):
            # Match the file URL (normalize and check the `.md` files)
            if filename.endswith(".md") and normalize(filename) == normalize(lesson_url.replace("/", "") + ".md"):
                source_file = filename
                break

        if source_file:
            # Move the markdown file to the appropriate unit folder
            source_path = os.path.join(ROOT_DIR, source_file)
            dest_path = os.path.join(unit_folder, normalize(lesson_title) + ".md")
            shutil.move(source_path, dest_path)
            print(f"Moved {source_file} to {dest_path}")
        else:
            print(f"Warning: Lesson file for '{lesson_title}' not found.")

