"""
Data Manager for Jupiter.money RAG Bot
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from config.settings import DATA_FILE, CACHE_FILE, REFRESH_INTERVAL


class DataManager:
    """
    Manages data loading and caching
    """
    
    def __init__(self):
        self.data_file = DATA_FILE
        self.cache_file = CACHE_FILE
    
    def load_data(self) -> list:
        """Load scraped data from file"""
        if not os.path.exists(self.data_file):
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
            return chunks
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return []
    
    def should_refresh_data(self) -> bool:
        """Check if data should be refreshed"""
        if not os.path.exists(self.cache_file):
            return True
        
        try:
            with open(self.cache_file, 'r') as file:
                cache_data = json.load(file)
            
            last_update = datetime.fromisoformat(cache_data.get('last_update', '2000-01-01'))
            return datetime.now() - last_update > timedelta(seconds=REFRESH_INTERVAL)
            
        except Exception:
            return True
    
    def update_cache(self):
        """Update cache metadata"""
        try:
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            cache_data = {
                'last_update': datetime.now().isoformat(),
                'data_file': str(self.data_file)
            }
            
            with open(self.cache_file, 'w') as file:
                json.dump(cache_data, file)
                
        except Exception as e:
            print(f"Could not update cache: {e}")
    
    def get_data_info(self) -> dict:
        """Get information about the data file"""
        if not os.path.exists(self.data_file):
            return {"exists": False, "size": 0, "last_modified": None}
        
        try:
            stat = os.stat(self.data_file)
            return {
                "exists": True,
                "size": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime)
            }
        except Exception:
            return {"exists": False, "size": 0, "last_modified": None} 