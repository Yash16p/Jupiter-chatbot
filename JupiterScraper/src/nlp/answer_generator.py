"""
Smart Answer Generator for Jupiter.money RAG Bot
"""

import re
from typing import List, Tuple


class SmartAnswerGenerator:
    """
    Generates intelligent, context-aware answers
    """
    
    def __init__(self):
        self.query_patterns = {
            'savings': r'\b(savings?|deposit|interest|rate|account)\b',
            'expenses': r'\b(expense|spending|budget|track|category)\b',
            'investments': r'\b(investment|fund|portfolio|stocks?|returns?)\b',
            'security': r'\b(security|safe|protect|encryption|privacy)\b',
            'fees': r'\b(fee|charge|cost|commission|rate)\b',
            'transfers': r'\b(transfer|send|receive|move|exchange)\b'
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
        
        # Add follow-up suggestions
        follow_ups = self._get_follow_up_suggestions(query_type)
        if follow_ups:
            answer += f"\n\n**You might also want to know:** {follow_ups}"
        
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
            'fees': "Jupiter maintains transparent pricing with competitive fee structures.",
            'transfers': "Jupiter enables fast, secure money transfers with real-time tracking."
        }
        
        return insights.get(query_type, "Jupiter focuses on making financial services simple and accessible.")
    
    def _get_follow_up_suggestions(self, query_type: str) -> str:
        """Get relevant follow-up question suggestions"""
        suggestions = {
            'savings': "Try asking about interest rates, withdrawal limits, or account types.",
            'expenses': "Ask about spending categories, budget alerts, or financial insights.",
            'investments': "Inquire about investment options, risk levels, or returns.",
            'security': "Ask about security measures, data protection, or account safety.",
            'fees': "Inquire about fee structures, hidden costs, or payment methods.",
            'transfers': "Ask about transfer limits, processing times, or international transfers."
        }
        
        return suggestions.get(query_type, "Ask about specific features, benefits, or how to get started.") 