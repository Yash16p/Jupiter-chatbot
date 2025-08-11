#!/usr/bin/env python3
"""
Simple test script for Jupiter.money RAG Bot components
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        from src.nlp.vectorizer import EnhancedTFIDFVectorizer
        print("✅ EnhancedTFIDFVectorizer imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EnhancedTFIDFVectorizer: {e}")
        return False
    
    try:
        from src.nlp.similarity import EnhancedSimilaritySearch
        print("✅ EnhancedSimilaritySearch imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import EnhancedSimilaritySearch: {e}")
        return False
    
    try:
        from src.nlp.answer_generator import SmartAnswerGenerator
        print("✅ SmartAnswerGenerator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import SmartAnswerGenerator: {e}")
        return False
    
    try:
        from src.data.manager import DataManager
        print("✅ DataManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DataManager: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality of components"""
    print("\n🔧 Testing basic functionality...")
    
    try:
        from src.nlp.vectorizer import EnhancedTFIDFVectorizer
        
        # Test vectorizer
        vectorizer = EnhancedTFIDFVectorizer()
        test_docs = [
            "Jupiter offers savings accounts with competitive interest rates",
            "Track your expenses and budget with Jupiter's smart tools",
            "Invest in mutual funds and stocks through Jupiter's platform"
        ]
        
        vectorizer.fit(test_docs)
        print("✅ Vectorizer fit successful")
        
        # Test similarity search
        from src.nlp.similarity import EnhancedSimilaritySearch
        similarity = EnhancedSimilaritySearch()
        similarity.fit(test_docs)
        print("✅ Similarity search initialized")
        
        # Test answer generator
        from src.nlp.answer_generator import SmartAnswerGenerator
        generator = SmartAnswerGenerator()
        print("✅ Answer generator initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_data_loading():
    """Test data loading functionality"""
    print("\n📁 Testing data loading...")
    
    try:
        from src.data.manager import DataManager
        
        manager = DataManager()
        data_info = manager.get_data_info()
        
        if data_info["exists"]:
            print(f"✅ Data file found: {data_info['size']} bytes")
            print(f"   Last modified: {data_info['last_modified']}")
        else:
            print("⚠️  Data file not found - run scraper first")
        
        return True
        
    except Exception as e:
        print(f"❌ Data loading test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Jupiter.money RAG Bot Components\n")
    
    # Test imports
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed. Check dependencies.")
        return
    
    # Test basic functionality
    func_ok = test_basic_functionality()
    if not func_ok:
        print("\n❌ Basic functionality tests failed.")
        return
    
    # Test data loading
    data_ok = test_data_loading()
    
    print("\n" + "="*50)
    if imports_ok and func_ok:
        print("🎉 All tests passed! The bot is ready to run.")
        print("\n📖 Next steps:")
        print("1. Run: python -m streamlit run chatbot.py")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    print("="*50)

if __name__ == "__main__":
    main() 