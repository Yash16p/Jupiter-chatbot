# Jupiter.money RAG Q&A Bot

An intelligent, AI-powered question-answering system for Jupiter.money's financial services, built with advanced text analysis and web scraping capabilities.

## 🚀 Features

- **Advanced RAG System**: Retrieval-Augmented Generation using enhanced TF-IDF and semantic similarity
- **Smart Q&A**: Context-aware answers with follow-up suggestions
- **Financial Domain Knowledge**: Understands banking and finance terminology
- **Customer-Focused UI**: Clean, professional interface without technical jargon
- **Easy to Use**: Single command to run the entire system

## 📁 Project Structure

```
JupiterScraper/
├── README.md                           # This file
├── chatbot.py                          # Main chatbot application (run this!)
├── requirements_enhanced.txt            # Enhanced bot dependencies
├── config/                             # Configuration files
│   ├── __init__.py
│   └── settings.py                     # Global settings and constants
├── src/                                # Source code modules
│   ├── __init__.py                     # Package initialization
│   ├── nlp/                            # Natural language processing
│   │   ├── __init__.py
│   │   ├── vectorizer.py               # Enhanced TF-IDF vectorizer
│   │   ├── similarity.py               # Multi-algorithm similarity search
│   │   └── answer_generator.py         # Smart answer generation
│   └── data/                           # Data management
│       ├── __init__.py
│       └── manager.py                  # Data loading and caching
├── scripts/                            # Utility scripts
│   ├── setup.py                        # Environment setup
│   └── scrape_jupiter.py               # Jupiter website scraper
└── data/                               # Scraped data storage (created automatically)
    └── scraped_texts.txt               # Main data file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Chrome browser (for dynamic scraping)
- Windows 10/11 (tested on Windows)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd JupiterScraper
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_enhanced.txt
   ```

## 🚀 Quick Start

### 1. Scrape Jupiter Data (First Time)
```bash
python scripts/scrape_jupiter.py
```

### 2. Run the Chatbot
```bash
python -m streamlit run chatbot.py
```

**That's it!** The chatbot will open in your browser.

## 📖 Usage

### Web Interface
1. Open your browser to the URL shown (usually `http://localhost:8501`)
2. Ask questions about Jupiter's services
3. Get intelligent, context-aware answers

### Sample Questions
- "What are Jupiter's savings account features?"
- "How does Jupiter help with expense tracking?"
- "What investment options does Jupiter offer?"
- "How secure is Jupiter's platform?"
- "What are Jupiter's fees and charges?"

## 🔧 Configuration

### Settings (`config/settings.py`)
- `BASE_URL`: Jupiter.money website URL
- `REFRESH_INTERVAL`: Data refresh frequency (6 hours)
- `CHUNK_SIZE`: Text chunk size for processing
- `TOP_K`: Number of results to retrieve

### Environment Variables
```bash
JUPITER_SCRAPER_DEBUG=true          # Enable debug mode
JUPITER_SCRAPER_MAX_PAGES=100       # Maximum pages to scrape
JUPITER_SCRAPER_TIMEOUT=30          # Scraping timeout in seconds
```

## 🧪 Testing

### Test Bot Components
```bash
python test_enhanced.py
```

## 📊 Performance

### Scraping Performance
- **Static pages**: ~2-3 seconds per page
- **Total time**: ~1-2 minutes for basic scraping

### Search Performance
- **Query processing**: <100ms
- **Similarity search**: <500ms for 1000 chunks
- **Answer generation**: <200ms

### Memory Usage
- **Base memory**: ~50MB
- **With data loaded**: ~100-200MB
- **Peak during search**: ~300MB

## 🔍 How It Works

### 1. Data Collection
- **Web Scraping**: BeautifulSoup for HTML content
- **Content Processing**: Text extraction, cleaning, and chunking

### 2. Text Analysis
- **Enhanced TF-IDF**: Vocabulary building with financial synonyms
- **Multi-algorithm Search**: TF-IDF + Cosine + Word Overlap
- **Context Understanding**: Query type detection and categorization

### 3. Answer Generation
- **Smart Context**: Relevance-based information selection
- **Structured Output**: Organized, readable responses
- **Follow-up Suggestions**: Intelligent question recommendations

## 🚨 Troubleshooting

### Common Issues

1. **Chrome WebDriver Issues**
   ```bash
   # Reinstall webdriver-manager
   pip uninstall webdriver-manager
   pip install webdriver-manager
   ```

2. **Memory Issues**
   - Reduce `CHUNK_SIZE` in settings
   - Limit maximum pages in scraping

3. **Scraping Blocked**
   - Add delays between requests
   - Rotate user agents

### Debug Mode
```bash
set JUPITER_SCRAPER_DEBUG=true
python scripts/scrape_jupiter.py
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Commit: `git commit -m 'Add feature'`
5. Push: `git push origin feature-name`
6. Create Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Add docstrings for functions
- Include tests for new features

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Jupiter.money for providing the financial services information
- Streamlit for the web application framework
- BeautifulSoup for web scraping capabilities
- The open-source community for various NLP and ML libraries

---

## 🎯 **Quick Commands Summary**

```bash
# Setup environment
python scripts/setup.py

# Scrape data (first time)
python scripts/scrape_jupiter.py

# Run chatbot
python -m streamlit run chatbot.py
```

**Built with ❤️ for intelligent financial assistance** 