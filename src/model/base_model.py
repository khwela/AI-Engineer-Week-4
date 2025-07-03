from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class CodeAnalysisModel(ABC):
    """Base class for code analysis models."""
    
    @abstractmethod
    def analyze_code(self, code: str, language: str) -> Dict[str, List[Dict]]:
        """
        Analyze code and return suggestions.
        
        Args:
            code (str): The source code to analyze
            language (str): Programming language of the code
            
        Returns:
            Dict[str, List[Dict]]: Dictionary containing:
                - issues: List of identified issues
                - suggestions: List of improvement suggestions
                - metrics: Code quality metrics
        """
        pass
    
    @abstractmethod
    def train(self, training_data: List[Dict], **kwargs) -> None:
        """
        Train the model on new data.
        
        Args:
            training_data (List[Dict]): List of training examples
            **kwargs: Additional training parameters
        """
        pass
    
    @abstractmethod
    def evaluate(self, test_data: List[Dict]) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            test_data (List[Dict]): Test dataset
            
        Returns:
            Dict[str, float]: Dictionary of evaluation metrics
        """
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        """
        Save model to disk.
        
        Args:
            path (str): Path to save the model
        """
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        """
        Load model from disk.
        
        Args:
            path (str): Path to load the model from
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, str]:
        """
        Get model information.
        
        Returns:
            Dict[str, str]: Dictionary containing model metadata
        """
        pass 