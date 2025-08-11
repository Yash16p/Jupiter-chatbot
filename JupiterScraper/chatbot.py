"""
Jupiter.money RAG Chatbot - Simple Single File Version
Just run: streamlit run chatbot.py
"""

import os
import streamlit as st
import numpy as np
import re
from typing import List, Tuple
from collections import Counter
from datetime import datetime
import json

# Constants
DATA_FILE = os.path.join("JupiterScraper", "JupiterScraper", "data", "scraped_texts.txt")
TOP_K = 5

# Enhanced TF-IDF Vectorizer
class TFIDFVectorizer:
    def __init__(self):
        self.vocabulary = {}
        self.idf = {}
        
    def fit(self, documents: List[str]):
        """Build vocabulary and calculate IDF scores"""
        # Build vocabulary with financial synonyms
        doc_freq = Counter()
        for doc in documents:
            words = self._tokenize(doc)
            # Add synonyms for key financial terms
            expanded_words = self._expand_with_synonyms(words)
            doc_freq.update(set(expanded_words))
        
        # Create vocabulary and IDF
        total_docs = len(documents)
        for word, freq in doc_freq.items():
            self.vocabulary[word] = len(self.vocabulary)
            self.idf[word] = np.log(total_docs / freq)
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization"""
        words = re.findall(r'\b\w+\b', text.lower())
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        return [word for word in words if len(word) > 2 and word not in stop_words]
    
    def _expand_with_synonyms(self, words: List[str]) -> List[str]:
        """Expand words with financial synonyms"""
        synonyms = {
            'account': ['account', 'banking', 'wallet'],
            'savings': ['savings', 'deposit', 'money', 'funds'],
            'expense': ['expense', 'spending', 'cost', 'payment'],
            'investment': ['investment', 'invest', 'fund', 'portfolio'],
            'security': ['security', 'safe', 'secure', 'protection'],
            'fee': ['fee', 'charge', 'cost', 'rate'],
            'transfer': ['transfer', 'send', 'receive', 'move']
        }
        
        expanded = words.copy()
        for word in words:
            for category, syns in synonyms.items():
                if word in syns:
                    expanded.extend(syns)
        return expanded
    
    def transform_single(self, text: str) -> np.ndarray:
        """Transform single text to TF-IDF vector"""
        if not self.vocabulary:
            return np.array([])
        
        words = self._tokenize(text)
        word_freq = Counter(words)
        
        vector = np.zeros(len(self.vocabulary))
        for word, freq in word_freq.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                tf = freq / len(words)
                vector[idx] = tf * self.idf[word]
        
        return vector

# Smart Answer Generator
class AnswerGenerator:
    def __init__(self):
        self.query_patterns = {
            'savings': r'\b(savings?|deposit|interest|rate|account)\b',
            'expenses': r'\b(expense|spending|budget|track|category)\b',
            'investments': r'\b(investment|fund|portfolio|stocks?|returns?)\b',
            'security': r'\b(security|safe|protect|encryption|privacy)\b',
            'fees': r'\b(fee|charge|cost|commission|rate)\b'
        }
    
    def generate_answer(self, query: str, context_chunks: List[str], scores: List[float]) -> str:
        """Generate intelligent answers from context"""
        
        if not context_chunks:
            return "I couldn't find specific information on that yet. Try asking about Jupiter's savings accounts, expense tracking, or security features."
        
        # Detect query type
        query_type = self._detect_query_type(query)
        
        # Filter chunks by relevance
        relevant_chunks = []
        for chunk, score in zip(context_chunks, scores):
            if score > 0.15:  # Threshold for relevance
                relevant_chunks.append((chunk, score))
        
        if not relevant_chunks:
            return "The information I found doesn't seem directly relevant. Try rephrasing your question."
        
        # Sort by relevance
        relevant_chunks.sort(key=lambda x: x[1], reverse=True)
        
        # Generate structured answer
        answer = "**Here's what I found about your question:**\n\n"
        
        # Add the most relevant information first
        top_chunks = relevant_chunks[:3]  # Top 3 most relevant
        
        for i, (chunk, score) in enumerate(top_chunks, 1):
            # Clean and format the chunk
            clean_chunk = self._clean_text_chunk(chunk)
            answer += f"{i}. {clean_chunk}\n"
        
        # Add contextual insights
        insights = self._get_contextual_insights(query_type)
        if insights:
            answer += f"\n**Quick insights:** {insights}"
        
        # Add source attribution
        answer += "\n\n*This information comes from Jupiter's official website.*"
        
        return answer
    
    def _detect_query_type(self, query: str) -> str:
        """Detect the type of financial query"""
        query_lower = query.lower()
        
        for query_type, pattern in self.query_patterns.items():
            if re.search(pattern, query_lower):
                return query_type
        
        return "general"
    
    def _clean_text_chunk(self, chunk: str) -> str:
        """Clean and format text chunks"""
        chunk = re.sub(r'\s+', ' ', chunk.strip())
        
        if len(chunk) > 250:
            sentences = re.split(r'[.!?]', chunk[:250])
            if len(sentences) > 1:
                chunk = '. '.join(sentences[:-1]) + '.'
            else:
                chunk = chunk[:250].rsplit(' ', 1)[0] + '...'
        
        return chunk
    
    def _get_contextual_insights(self, query_type: str) -> str:
        """Get contextual insights based on query type"""
        insights = {
            'savings': "Jupiter offers competitive interest rates and automated savings features.",
            'expenses': "Jupiter provides detailed spending analytics and budget tracking tools.",
            'investments': "Jupiter offers user-friendly investment options with professional guidance.",
            'security': "Jupiter uses bank-grade security with multiple layers of protection.",
            'fees': "Jupiter maintains transparent pricing with competitive fee structures."
        }
        
        return insights.get(query_type, "Jupiter focuses on making financial services simple and accessible.")

# Main Chatbot Class
class JupiterChatbot:
    def __init__(self):
        self.vectorizer = TFIDFVectorizer()
        self.answer_generator = AnswerGenerator()
        self.is_trained = False
    
    def load_data(self) -> List[str]:
        """Load scraped data from file"""
        if not os.path.exists(DATA_FILE):
            return []
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as file:
                content = file.read()
            
            chunks = [chunk.strip() for chunk in content.split('\n\n') if chunk.strip()]
            
            if chunks:
                st.success(f"✅ Loaded {len(chunks)} information sections")
            
            return chunks
            
        except Exception as e:
            st.error(f"❌ Error loading data: {e}")
            return []
    
    def train(self, chunks: List[str]):
        """Train the vectorizer on the data"""
        if chunks:
            self.vectorizer.fit(chunks)
            self.is_trained = True
    
    def answer_question(self, query: str, chunks: List[str]) -> Tuple[str, List[str], List[float]]:
        """Answer questions using similarity search"""
        
        if not chunks or not self.is_trained:
            return "No data available. Please scrape first.", [], []
        
        try:
            # Generate query embedding
            query_vector = self.vectorizer.transform_single(query)
            
            if len(query_vector) == 0:
                return "Error processing query. Please try again.", [], []
            
            # Calculate similarities
            similarities = []
            for i, chunk in enumerate(chunks):
                chunk_vector = self.vectorizer.transform_single(chunk)
                if len(chunk_vector) > 0:
                    # Cosine similarity
                    cos_sim = self._cosine_similarity(query_vector, chunk_vector)
                    similarities.append((i, cos_sim, chunk))
            
            if not similarities:
                return "No relevant information found.", [], []
            
            # Sort by similarity and get top results
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_results = similarities[:TOP_K]
            
            relevant_chunks = [result[2] for result in top_results]
            scores = [result[1] for result in top_results]
            
            return "Search completed successfully.", relevant_chunks, scores
            
        except Exception as e:
            st.warning(f"Search failed: {e}")
            return "Search failed. Please try again.", [], []
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="Jupiter Assistant",
        page_icon="",
        layout="wide"
    )
    
    st.title("Jupiter Assistant")
    st.caption("Your intelligent guide to Jupiter's financial services")
    
    # Initialize chatbot
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = JupiterChatbot()
    
    chatbot = st.session_state.chatbot
    
    # Sidebar
    with st.sidebar:
        st.header("Welcome")
        st.write("Ask about Jupiter's accounts, payments, security, investments, and more.")
        
        # Data status
        data_exists = os.path.exists(DATA_FILE)
        if data_exists:
            st.success("✅ Data file found")
        else:
            st.info("📥 No data file found. Please run the scraper first.")
    
    # Load and train data
    chunks = chatbot.load_data()
    if chunks and not chatbot.is_trained:
        with st.spinner("Training chatbot..."):
            chatbot.train(chunks)
    
    # Main interaction
    question = st.text_input(
        "What would you like to know about Jupiter?",
        placeholder="e.g., What are the benefits of a Jupiter Savings Account?"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ask = st.button("Ask Jupiter Assistant", type="primary")
    
    # Quick suggestions
    st.write("**Popular questions:**")
    cols = st.columns(3)
    suggestions = [
        "How does Jupiter help me track expenses?",
        "What fees should I know about?",
        "Is my money secure with Jupiter?",
        "What investment options do you offer?",
        "How do I open a savings account?",
        "What are the transfer limits?"
    ]
    
    for i, suggestion in enumerate(suggestions):
        col_idx = i % 3
        if cols[col_idx].button(suggestion, key=f"sugg_{i}"):
            question = suggestion
            st.session_state["__auto_submit__"] = True
    
    # Handle question submission
    submitted = ask or st.session_state.pop("__auto_submit__", False)
    if submitted and question:
        with st.spinner("🔍 Searching Jupiter's knowledge base..."):
            # Get answer
            status, relevant_chunks, scores = chatbot.answer_question(question, chunks)
            
            if relevant_chunks and scores:
                # Generate answer
                answer = chatbot.answer_generator.generate_answer(question, relevant_chunks, scores)
                
                # Display answer
                st.markdown("---")
                st.markdown(answer)
                
                # Optional: Show source details
                with st.expander("📚 See more details"):
                    for i, chunk in enumerate(relevant_chunks[:2], 1):
                        preview = chunk.strip()
                        if len(preview) > 400:
                            preview = preview[:400].rsplit(' ', 1)[0] + '...'
                        st.write(f"**Source {i}:**")
                        st.write(preview)
                        if i < min(2, len(relevant_chunks)):
                            st.write("---")
            else:
                st.info("I couldn't find specific information on that yet. Try asking about Jupiter's savings accounts, expense tracking, or security features.")
    
    # Footer
    st.markdown("---")
    st.caption("Jupiter Assistant • Powered by AI • Information from official sources")

if __name__ == "__main__":
    main() 