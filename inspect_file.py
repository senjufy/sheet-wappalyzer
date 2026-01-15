import pandas as pd

try:
    # Read the Excel file
    df = pd.read_excel('leads.xlsx')
    
    # Print the column headers
    print("File Columns:")
    print(list(df.columns))
    
    # Print the first 5 rows to show the structure
    print("\nFile Head:")
    print(df.head())
    
    # --- New Technology Analysis Step ---
    if 'Technologies' in df.columns:
        print("\n--- Analyzing found technologies ---")
        all_technologies = set()
        tech_with_versions = {}

        # Use dropna() to avoid errors on empty cells
        for technologies_str in df['Technologies'].dropna():
            if isinstance(technologies_str, str):
                for tech_item in technologies_str.split(','):
                    parts = tech_item.strip().split(':')
                    name = parts[0].strip()
                    if name:
                        all_technologies.add(name)
                        if len(parts) > 1:
                            version = parts[1].strip()
                            if name not in tech_with_versions:
                                tech_with_versions[name] = set()
                            tech_with_versions[name].add(version)

        print(f"Found {len(all_technologies)} unique technologies in the 'Technologies' column.")
        print("Here is a summary:")
        sorted_techs = sorted(list(all_technologies))
        for tech in sorted_techs:
            if tech in tech_with_versions:
                versions_found = sorted(list(tech_with_versions[tech]))
                # To avoid long lists, show up to 3 versions and then '...'
                display_versions = versions_found[:3]
                if len(versions_found) > 3:
                    display_versions.append('...')
                print(f"- {tech} (versions found: {', '.join(display_versions)})")
            else:
                print(f"- {tech}")
    else:
        print("'Technologies' column not found. Run analyze_websites.py to generate it.")
    
except FileNotFoundError:
    print("Error: The file 'leads.xlsx' was not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")