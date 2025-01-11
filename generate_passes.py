import json
import os
import zipfile
from jinja2 import Template
from passbook.modsource passbook-env/bin/activateels import Pass, Barcode

# Define member data
members = [
    {"serial_number": "001", "name": "John Doe", "nsid": "nsid123", "membership_number": "12345"},
    {"serial_number": "002", "name": "Jane Smith", "nsid": "nsid456", "membership_number": "67890"},
]

# Create pass template
template_path = "pass_template.json"
with open(template_path, "r") as file:
    template_content = file.read()
template = Template(template_content)

# Output directory for passes
output_dir = "passes"
os.makedirs(output_dir, exist_ok=True)

# Generate .pkpass files
for member in members:
    # Render pass.json
    pass_json_content = template.render(member)
    pass_json_path = f"{output_dir}/pass_{member['serial_number']}.json"
    with open(pass_json_path, "w") as pass_file:
        pass_file.write(pass_json_content)

    # Create manifest and signature (using a placeholder for simplicity)
    manifest = {"pass.json": pass_json_content}
    manifest_path = f"{output_dir}/manifest_{member['serial_number']}.json"
    with open(manifest_path, "w") as manifest_file:
        json.dump(manifest, manifest_file)

    # Create .pkpass (zipped file)
    pkpass_path = f"{output_dir}/pass_{member['serial_number']}.pkpass"
    with zipfile.ZipFile(pkpass_path, "w") as pkpass:
        pkpass.write(pass_json_path, "pass.json")
        pkpass.write(manifest_path, "manifest.json")
        for img in ["icon.png", "logo.png"]:
            pkpass.write(f"images/{img}", img)

    print(f"Generated pass: {pkpass_path}")

print("All passes generated!")