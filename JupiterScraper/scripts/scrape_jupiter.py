#!/usr/bin/env python3
"""
Simple Jupiter.money Scraper
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import requests
from bs4 import BeautifulSoup
import time
from config.settings import BASE_URL, USER_AGENT, MAX_PAGES, REQUEST_DELAY


def scrape_jupiter():
    """Scrape Jupiter.money website"""
    print("🚀 Starting Jupiter.money scraper...")
    
    # Create data directory
    data_dir = Path("JupiterScraper/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    data_file = data_dir / "scraped_texts.txt"
    
    # URLs to scrape
    urls = [
        BASE_URL,
        f"{BASE_URL}/about-us",
        f"{BASE_URL}/services",
        f"{BASE_URL}/features",
        f"{BASE_URL}/pricing"
    ]
    
    all_texts = []
    
    for i, url in enumerate(urls):
        print(f"📄 Scraping {i+1}/{len(urls)}: {url}")
        
        try:
            headers = {"User-Agent": USER_AGENT}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove unwanted elements
            for unwanted in soup(["script", "style", "nav", "footer", "header"]):
                unwanted.extract()
            
            # Extract text content
            text = soup.get_text(separator=" ", strip=True)
            
            if text and len(text) > 100:
                all_texts.append(text)
                print(f"✅ Extracted {len(text)} characters")
            else:
                print(f"⚠️  Insufficient content from {url}")
            
            # Delay between requests
            time.sleep(REQUEST_DELAY)
            
        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
    
    # Save scraped data
    if all_texts:
        with open(data_file, "w", encoding="utf-8") as file:
            file.write("\n\n".join(all_texts))
        
        print(f"\n🎉 Scraping completed!")
        print(f"📁 Data saved to: {data_file}")
        print(f"📊 Total chunks: {len(all_texts)}")
        print(f"💾 File size: {data_file.stat().st_size / 1024:.1f} KB")
    else:
        print("❌ No data was scraped")


if __name__ == "__main__":
    scrape_jupiter() 