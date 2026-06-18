import os

# Your actual ID and the placeholder you want to use
OLD_ID = "your_username"
NEW_ID = "your_username"

# We only target text-based files to avoid corrupting PDFs or zip files
TARGET_EXTENSIONS = ('.py', '.txt', '.md')

def anonymize_files():
    files_updated = 0
    
    # Walk through the current directory
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(TARGET_EXTENSIONS):
                filepath = os.path.join(root, file)
                
                try:
                    # Read the file
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if the ID exists in the file
                    if OLD_ID in content:
                        new_content = content.replace(OLD_ID, NEW_ID)
                        
                        # Write the changes back
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        print(f"✅ Updated: {filepath}")
                        files_updated += 1
                        
                except Exception as e:
                    print(f"⚠️ Skipping {filepath} (Error: {e})")

    print(f"\n🎉 Done! Replaced '{OLD_ID}' with '{NEW_ID}' in {files_updated} files.")

if __name__ == "__main__":
    print("Starting anonymization...")
    anonymize_files()