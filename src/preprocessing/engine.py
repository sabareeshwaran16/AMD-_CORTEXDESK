import re
from typing import List, Dict, Any
from datetime import datetime
from dateutil import parser as date_parser

class PreprocessingEngine:
    """Clean and structure text for AI processing"""
    
    def process(self, raw_text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Main preprocessing pipeline"""
        cleaned = self.clean_text(raw_text)
        language = self.detect_language(cleaned)
        speakers = self.segment_speakers(cleaned)
        timestamps = self.extract_timestamps(cleaned)
        deadlines = self.normalize_deadlines(cleaned)
        chunks = self.chunk_text(cleaned)
        
        return {
            "cleaned_text": cleaned,
            "language": language,
            "speakers": speakers,
            "timestamps": timestamps,
            "deadlines": deadlines,
            "chunks": chunks,
            "metadata": metadata
        }
    
    def clean_text(self, text: str) -> str:
        """Remove noise, normalize whitespace, filter unwanted content"""
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove excessive technical jargon patterns (course codes, reference numbers)
        text = re.sub(r'\b[A-Z]\d{2}[A-Z]{2,}\d+\.\d+\b', '', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        text = re.sub(r'^\d+$', '', text, flags=re.MULTILINE)
        
        # Remove excessive punctuation
        text = re.sub(r'[•●○■□▪▫–—]{2,}', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n\s*\n', '\n', text)
        text = text.strip()
        
        # Filter out lines that are too long (likely not action items)
        lines = text.split('\n')
        filtered_lines = []
        for line in lines:
            line = line.strip()
            # Keep lines that look like action items or meeting content
            if 10 <= len(line) <= 300:
                # Check if line contains action-related keywords
                if any(keyword in line.lower() for keyword in 
                      ['action', 'task', 'todo', 'needs to', 'will', 'should', 'must',
                       'decision', 'agreed', 'approved', 'meeting', 'discussed',
                       'deadline', 'by', 'before', 'schedule', 'complete', 'review']):
                    filtered_lines.append(line)
                # Or if it's a short, clear statement
                elif len(line) < 150 and not re.search(r'[\(\)\[\]\{\}]', line):
                    filtered_lines.append(line)
        
        return '\n'.join(filtered_lines) if filtered_lines else text[:1000]
    
    def detect_language(self, text: str) -> str:
        """Simple language detection"""
        return "en"  # Default to English
    
    def segment_speakers(self, text: str) -> List[Dict[str, str]]:
        """Extract speaker segments"""
        speakers = []
        pattern = r'([A-Z][a-z]+):\s*(.+?)(?=\n[A-Z][a-z]+:|$)'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for match in matches:
            speakers.append({
                "speaker": match.group(1),
                "text": match.group(2).strip()
            })
        
        return speakers
    
    def extract_timestamps(self, text: str) -> List[str]:
        """Extract time references"""
        timestamps = []
        patterns = [
            r'\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?',
            r'\d{4}-\d{2}-\d{2}',
            r'\d{2}/\d{2}/\d{4}'
        ]
        
        for pattern in patterns:
            timestamps.extend(re.findall(pattern, text))
        
        return timestamps
    
    def normalize_deadlines(self, text: str) -> List[Dict[str, Any]]:
        """Extract and normalize deadlines"""
        deadlines = []
        
        # Pattern: "by [date]", "before [date]", "until [date]"
        pattern = r'(?:by|before|until|deadline:?)\s+([A-Za-z]+\s+\d{1,2}(?:st|nd|rd|th)?(?:,?\s+\d{4})?|\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        for match in matches:
            date_str = match.group(1)
            try:
                parsed_date = date_parser.parse(date_str, fuzzy=True)
                deadlines.append({
                    "raw": date_str,
                    "normalized": parsed_date.isoformat(),
                    "context": match.group(0)
                })
            except:
                deadlines.append({
                    "raw": date_str,
                    "normalized": None,
                    "context": match.group(0)
                })
        
        return deadlines
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for RAG"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        
        return chunks
