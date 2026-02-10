import json
import yaml
import argparse
import os
import sys

# -------------------------------
# COMMON VALIDATION FUNCTION
# -------------------------------
def validate_config(config, schema, source_name):
    print(f"\n🧪 Validating configuration from {source_name}...")

    errors = []

    # 1️⃣ Required keys check
    for key, expected_type in schema.items():
        if key not in config:
            errors.append(f"❌ Missing required key: {key}")
        else:
            value = str(config[key])

            # 2️⃣ Type validation
            if expected_type == "integer":
                if not value.isdigit():
                    errors.append(f"❌ {key} should be INTEGER, but got '{value}'")
            elif expected_type == "boolean":
                if value.lower() not in ["true", "false"]:
                    errors.append(f"❌ {key} should be BOOLEAN (true/false), but got '{value}'")
            elif expected_type == "string":
                if value == "":
                    errors.append(f"❌ {key} should be STRING, but got empty value")

    # Print results
    if errors:
        print("\n".join(errors))
    else:
        print("✅ All keys present with correct types!")

    return len(errors)


# -------------------------------
# LOAD SCHEMA
# -------------------------------
def load_schema(schema_file):
    ext = os.path.splitext(schema_file)[1].lower()
    try:
        with open(schema_file, "r") as f:
            if ext == ".json":
                return json.load(f)
            elif ext in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            else:
                print("❌ Unsupported schema format!")
                sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Schema file '{schema_file}' not found!")
        sys.exit(1)


# -------------------------------
# LOAD CONFIG FILE
# -------------------------------
def load_config(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    config = {}

    try:
        with open(file_path, "r") as f:
            if ext == ".env":
                for line in f:
                    line = line.strip()
                    if line == "" or line.startswith("#"):
                        continue
                    if "=" not in line:
                        print(f"⚠️ Invalid line in .env: {line}")
                        continue
                    key, value = line.split("=", 1)
                    config[key] = value
            elif ext == ".json":
                config = json.load(f)
            elif ext in [".yaml", ".yml"]:
                config = yaml.safe_load(f)
            else:
                print("❌ Unsupported config format!")
                sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Config file '{file_path}' not found!")
        sys.exit(1)

    return config


# -------------------------------
# CLI ARGUMENTS
# -------------------------------
parser = argparse.ArgumentParser(description="Config File Error Finder")
parser.add_argument("config_file", help=".env/.json/.yaml config file path")
parser.add_argument("schema_file", help="Schema file path (.json/.yaml)")
args = parser.parse_args()

# -------------------------------
# RUN VALIDATION
# -------------------------------
schema = load_schema(args.schema_file)
config = load_config(args.config_file)
errors_count = validate_config(config, schema, args.config_file)

print(f"\nSummary: Total Errors = {errors_count}")

if errors_count > 0:
    sys.exit(1)  # Exit with error code if invalid
else:
    sys.exit(0)  # Success

