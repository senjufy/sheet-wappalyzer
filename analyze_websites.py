import pandas as pd
from Wappalyzer import Wappalyzer, WebPage
import asyncio
import aiohttp
import argparse

async def analyze_website_tech_async(session, url, semaphore):
    """
    Asynchronously analyzes a single website, using a semaphore to limit concurrency.
    """
    async with semaphore:
        if not isinstance(url, str) or not url.strip():
            return 'N/A', 'Missing or invalid URL'
            
        wappalyzer = Wappalyzer.latest()
        
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            await asyncio.sleep(0.1)
            
            async with session.get(url, timeout=20, headers=headers, allow_redirects=True) as response:
                response.raise_for_status()
                html = await response.text()
                
                webpage = WebPage(url, html, response.headers)
                technologies = wappalyzer.analyze(webpage)
                
                technologies_str = ', '.join(sorted(technologies)) if technologies else 'N/A'
                return technologies_str, 'Success'
                
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            status_message = f"Error: {type(e).__name__}"
            if hasattr(e, 'status') and e.status == 403:
                status_message = "Error: Forbidden (403)"
            elif "Timeout" in str(e):
                 status_message = "Error: Connection Timeout"
            return 'N/A', status_message
            
        except Exception as e:
            return 'N/A', f"An unexpected error occurred: {type(e).__name__}"

async def main(args):
    """Main function to run the asynchronous analysis with command-line arguments."""
    try:
        print(f"Reading data from '{args.file}'...")
        df = pd.read_excel(args.file)
        
        if args.url_column not in df.columns:
            print(f"Error: Column '{args.url_column}' not found in the Excel file.")
            print(f"Available columns are: {list(df.columns)}")
            return

        print(f"Found website column: '{args.url_column}'")
        
        urls_to_process = df[args.url_column].tolist()
        
        print(f"Starting analysis of {len(urls_to_process)} URLs with a concurrency limit of {args.concurrency}...")
        
        semaphore = asyncio.Semaphore(args.concurrency)
        async with aiohttp.ClientSession() as session:
            tasks = [analyze_website_tech_async(session, url, semaphore) for url in urls_to_process]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        print("Analysis complete.")

        final_results = []
        for res in results:
            if isinstance(res, Exception):
                final_results.append(('N/A', f'Error: {res}'))
            else:
                final_results.append(res)
        
        df['Technologies'] = [res[0] for res in final_results]
        df['Status'] = [res[1] for res in final_results]

        df.to_excel(args.file, index=False)
        
        print(f"\nSuccess! The file '{args.file}' has been updated.")

    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze website technologies from an Excel file and update it in place.")
    parser.add_argument(
        '--file', 
        type=str, 
        default='leads.xlsx',
        help='Path to the input Excel file. Defaults to "leads.xlsx".'
    )
    parser.add_argument(
        '--url_column', 
        type=str, 
        default='Website',
        help='Name of the column containing website URLs. Defaults to "Website".'
    )
    parser.add_argument(
        '--concurrency',
        type=int,
        default=25,
        help='Number of concurrent requests to make. Defaults to 25.'
    )
    
    args = parser.parse_args()
    asyncio.run(main(args))