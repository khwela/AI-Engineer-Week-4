import re
from typing import Dict, List, Optional
from tree_sitter import Language, Parser

class CodeProcessor:
    """Utility class for code preprocessing and analysis."""
    
    def __init__(self):
        """Initialize the code processor."""
        self.language_parsers = {}
        
    def setup_parser(self, language: str) -> None:
        """
        Set up a parser for a specific programming language.
        
        Args:
            language (str): Programming language to set up parser for
        """
        # This is a placeholder - in a real implementation, we would:
        # 1. Build/load the tree-sitter grammar for the language
        # 2. Initialize the parser with the grammar
        pass
        
    def tokenize_code(self, code: str) -> List[str]:
        """
        Tokenize code into meaningful units.
        
        Args:
            code (str): Source code to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        # Simple tokenization - in practice, use a proper tokenizer
        tokens = re.findall(r'\b\w+\b|[^\w\s]', code)
        return tokens
        
    def extract_features(self, code: str, language: str) -> Dict:
        """
        Extract features from code for analysis.
        
        Args:
            code (str): Source code to analyze
            language (str): Programming language of the code
            
        Returns:
            Dict: Extracted features
        """
        features = {
            "length": len(code),
            "num_lines": len(code.splitlines()),
            "tokens": self.tokenize_code(code),
            "language": language,
        }
        
        # Add language-specific features
        if language.lower() == "python":
            features.update(self._extract_python_features(code))
        elif language.lower() in ["javascript", "typescript"]:
            features.update(self._extract_js_features(code))
            
        return features
        
    def _extract_python_features(self, code: str) -> Dict:
        """
        Extract Python-specific features.
        
        Args:
            code (str): Python source code
            
        Returns:
            Dict: Python-specific features
        """
        features = {
            "has_type_hints": bool(re.search(r'def \w+\([^)]*: \w+[^)]*\)', code)),
            "has_docstrings": '"""' in code or "'''" in code,
            "num_functions": len(re.findall(r'\bdef\b', code)),
            "num_classes": len(re.findall(r'\bclass\b', code)),
        }
        return features
        
    def _extract_js_features(self, code: str) -> Dict:
        """
        Extract JavaScript/TypeScript-specific features.
        
        Args:
            code (str): JavaScript/TypeScript source code
            
        Returns:
            Dict: JavaScript-specific features
        """
        features = {
            "has_types": bool(re.search(r':\s*\w+', code)),  # TypeScript type annotations
            "num_functions": len(re.findall(r'\bfunction\b|\b=>\b', code)),
            "num_classes": len(re.findall(r'\bclass\b', code)),
            "uses_async": bool(re.search(r'\basync\b', code)),
        }
        return features
        
    def calculate_complexity(self, code: str) -> float:
        """
        Calculate code complexity score.
        
        Args:
            code (str): Source code to analyze
            
        Returns:
            float: Complexity score (0-1)
        """
        # This is a simple complexity calculation
        # In practice, use more sophisticated metrics
        tokens = self.tokenize_code(code)
        
        # Factors that increase complexity
        complexity_factors = {
            'if': 0.1,
            'for': 0.1,
            'while': 0.1,
            'try': 0.1,
            'catch': 0.05,
            'switch': 0.1,
            'case': 0.05,
        }
        
        complexity = 0.0
        for token in tokens:
            if token in complexity_factors:
                complexity += complexity_factors[token]
                
        # Normalize to 0-1 range
        return min(1.0, complexity)
        
    def find_code_smells(self, code: str, language: str) -> List[Dict]:
        """
        Identify potential code smells.
        
        Args:
            code (str): Source code to analyze
            language (str): Programming language of the code
            
        Returns:
            List[Dict]: List of identified code smells
        """
        smells = []
        
        # Check for long lines
        for i, line in enumerate(code.splitlines(), 1):
            if len(line) > 80:
                smells.append({
                    "type": "style",
                    "message": "Line exceeds recommended length of 80 characters",
                    "line": i,
                    "severity": "low"
                })
                
        # Check for complex functions
        if self.calculate_complexity(code) > 0.7:
            smells.append({
                "type": "complexity",
                "message": "High code complexity detected",
                "line": 1,
                "severity": "medium"
            })
            
        return smells
        
    def suggest_improvements(self, code: str, language: str) -> List[Dict]:
        """
        Generate improvement suggestions.
        
        Args:
            code (str): Source code to analyze
            language (str): Programming language of the code
            
        Returns:
            List[Dict]: List of improvement suggestions
        """
        suggestions = []
        features = self.extract_features(code, language)
        
        # Suggest type hints for Python
        if language.lower() == "python" and not features["has_type_hints"]:
            suggestions.append({
                "type": "improvement",
                "message": "Consider adding type hints for better code readability",
                "line": 1,
                "example": "def function(param: str) -> str:"
            })
            
        # Suggest async/await for JavaScript
        if language.lower() in ["javascript", "typescript"] and not features["uses_async"]:
            if "fetch" in code or "promise" in code.lower():
                suggestions.append({
                    "type": "improvement",
                    "message": "Consider using async/await for better promise handling",
                    "line": 1,
                    "example": "async function getData() {\n  const response = await fetch(url);\n}"
                })
                
        return suggestions 