import pandas as pd
import argparse

def should_call_lead(technologies_str):
    """
    Determines the priority of a lead based on a scoring system applied
    to their website's technologies, informed by the analysis of technology.txt.
    """
    if not isinstance(technologies_str, str) or technologies_str == 'N/A':
        return 'High Priority'

    score = 0
    
    # --- Parse Technologies ---
    tech_details = {}
    for tech_item in technologies_str.split(','):
        parts = tech_item.strip().split(':')
        name = parts[0].strip()
        version = parts[1].strip() if len(parts) > 1 else None
        if name:
            tech_details[name] = version
    technologies = set(tech_details.keys())

    # --- Scoring Logic ---

    # Rule 1: Ancient Technology (Highest Priority)
    ancient_tech = {'AngularJS', 'Backbone.js', 'DreamWeaver', 'MooTools', 'Prototype', 'SWFObject', 'jQuery Mobile'}
    if any(t in technologies for t in ancient_tech):
        score += 10

    # Rule 2: DIY Website Builders
    diy_builders = {'GoDaddy Website Builder', 'Mobirise', 'Weebly', 'Wix'}
    advanced_builders = {'Squarespace', 'Webflow'}
    if any(t in technologies for t in diy_builders):
        score += 8
    if any(t in technologies for t in advanced_builders):
        score += 4

    # Rule 3: WordPress Ecosystem
    if 'WordPress' in technologies:
        score += 5
        # Bonus for complexity/performance issues
        wp_plugins = {
            'WooCommerce', 'Elementor', 'wpBakery', 'Revslider', 'Gravity Forms', 
            'W3 Total Cache', 'WP Rocket', 'WordPress Super Cache', 'NitroPack'
        }
        found_plugins = technologies.intersection(wp_plugins)
        score += len(found_plugins) * 2 # Add 2 points for each complex plugin found

    # Rule 4: Other Self-Hosted/Complex CMS/E-commerce
    complex_platforms = {'Joomla', 'Drupal', 'BigCommerce', 'Magento', 'OpenCart'}
    if any(t in technologies for t in complex_platforms):
        score += 6
    # Penalize modern SaaS e-commerce
    if 'Shopify' in technologies:
        score -= 4

    # Rule 5: Outdated Libraries & Runtimes
    if 'jQuery' in technologies or 'jQuery UI' in technologies or 'jQuery Migrate' in technologies:
        score += 2 # Base score for just having jQuery
    if 'PHP' in technologies:
        # A simple proxy for older sites, as modern frameworks often hide this
        score += 2
        
    # Rule 6: Modern Frameworks (Negative Signal)
    modern_frameworks = {'React', 'Angular', 'Vue.js', 'Next.js', 'Nuxt.js', 'Gatsby', 'Svelte'}
    modern_hosting = {'Netlify', 'Vercel'}
    if any(t in technologies for t in modern_frameworks):
        score -= 5
    if any(t in technologies for t in modern_hosting):
        score -= 3

    # Rule 7: Marketing Savvy but potentially old tech
    marketing_tools = {'HubSpot', 'Klaviyo', 'MailChimp'}
    if any(t in technologies for t in marketing_tools) and not any(t in technologies for t in modern_frameworks):
        score += 3 # They are trying to market, but their site might be holding them back

    # Rule 8: Lack of Analytics
    if 'Google Tag Manager' not in technologies and 'Google Analytics' not in technologies:
        score += 3
        
    # --- Final Decision ---
    if score >= 9:
        return 'High Priority'
    elif score >= 5:
        return 'Medium Priority'
    else:
        return 'Low Priority'

def main():
    parser = argparse.ArgumentParser(description="Adds a 'Priority' column to an Excel file based on website technologies.")
    parser.add_argument(
        '--file',
        type=str,
        default='leads.xlsx',
        help='Path to the input Excel file. Defaults to "leads.xlsx".'
    )
    args = parser.parse_args()

    try:
        print(f"Reading data from '{args.file}'...")
        df = pd.read_excel(args.file)

        if 'Technologies' not in df.columns:
            print(f"Error: Column 'Technologies' not found in the Excel file. Please run analyze_websites.py first.")
            return

        print("Analyzing technologies to determine 'Priority' status...")
        df['Priority'] = df['Technologies'].apply(should_call_lead)

        df.to_excel(args.file, index=False)
        print(f"\nSuccess! The file '{args.file}' has been updated with the 'Priority' column.")

    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()