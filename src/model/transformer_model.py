import os
from typing import Dict, List, Optional
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from .base_model import CodeAnalysisModel

class TransformerCodeAnalyzer(CodeAnalysisModel):
    """Transformer-based code analysis model."""
    
    def __init__(self, model_name: str = "microsoft/codebert-base", device: str = None):
        """
        Initialize the transformer model.
        
        Args:
            model_name (str): Name of the pre-trained model
            device (str): Device to run the model on ('cuda' or 'cpu')
        """
        self.model_name = model_name
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)
        
    def preprocess_code(self, code: str) -> str:
        """
        Preprocess code before analysis.
        
        Args:
            code (str): Raw source code
            
        Returns:
            str: Preprocessed code
        """
        # Remove unnecessary whitespace
        code = code.strip()
        # Add special tokens for code
        return f"<code>{code}</code>"
        
    def analyze_code(self, code: str, language: str) -> Dict[str, List[Dict]]:
        """
        Analyze code and return suggestions.
        
        Args:
            code (str): The source code to analyze
            language (str): Programming language of the code
            
        Returns:
            Dict[str, List[Dict]]: Analysis results
        """
        processed_code = self.preprocess_code(code)
        inputs = self.tokenizer(processed_code, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits.softmax(dim=-1)
        
        # Example analysis results (to be replaced with actual model predictions)
        return {
            "issues": [
                {
                    "type": "style",
                    "message": "Consider using more descriptive variable names",
                    "line": 1,
                    "severity": "low"
                }
            ],
            "suggestions": [
                {
                    "type": "improvement",
                    "message": "Add type hints for better code readability",
                    "line": 1,
                    "example": "def function(param: str) -> str:"
                }
            ],
            "metrics": [
                {
                    "name": "complexity",
                    "value": 0.75,
                    "description": "Code complexity score (0-1)"
                }
            ]
        }
        
    def train(self, training_data: List[Dict], **kwargs) -> None:
        """
        Train the model on new data.
        
        Args:
            training_data (List[Dict]): List of training examples
            **kwargs: Additional training parameters
        """
        epochs = kwargs.get('epochs', 3)
        batch_size = kwargs.get('batch_size', 16)
        learning_rate = kwargs.get('learning_rate', 2e-5)
        
        optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
        
        self.model.train()
        for epoch in range(epochs):
            for i in range(0, len(training_data), batch_size):
                batch = training_data[i:i + batch_size]
                
                # Process batch data
                codes = [item['code'] for item in batch]
                labels = [item['label'] for item in batch]
                
                inputs = self.tokenizer(codes, padding=True, truncation=True, 
                                     return_tensors="pt", max_length=512)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                labels = torch.tensor(labels).to(self.device)
                
                outputs = self.model(**inputs, labels=labels)
                loss = outputs.loss
                
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                
    def evaluate(self, test_data: List[Dict]) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            test_data (List[Dict]): Test dataset
            
        Returns:
            Dict[str, float]: Evaluation metrics
        """
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        
        with torch.no_grad():
            for item in test_data:
                inputs = self.tokenizer(item['code'], return_tensors="pt", truncation=True)
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
                labels = torch.tensor([item['label']]).to(self.device)
                
                outputs = self.model(**inputs, labels=labels)
                total_loss += outputs.loss.item()
                
                predictions = outputs.logits.argmax(dim=-1)
                correct += (predictions == labels).sum().item()
                total += labels.size(0)
        
        return {
            "loss": total_loss / len(test_data),
            "accuracy": correct / total
        }
        
    def save(self, path: str) -> None:
        """
        Save model to disk.
        
        Args:
            path (str): Path to save the model
        """
        os.makedirs(path, exist_ok=True)
        self.model.save_pretrained(path)
        self.tokenizer.save_pretrained(path)
        
    def load(self, path: str) -> None:
        """
        Load model from disk.
        
        Args:
            path (str): Path to load the model from
        """
        self.model = AutoModelForSequenceClassification.from_pretrained(path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        self.model.to(self.device)
        
    def get_model_info(self) -> Dict[str, str]:
        """
        Get model information.
        
        Returns:
            Dict[str, str]: Model metadata
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "model_type": "transformer",
            "framework": "pytorch",
            "num_parameters": str(sum(p.numel() for p in self.model.parameters())),
            "version": "1.0.0"
        } 