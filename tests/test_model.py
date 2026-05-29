"""
Unit Tests für AI Models
"""

import unittest
import torch
from src.ai_model.model import StyleTransferModel, EffectClassifier, KeyframePredictor

class TestStyleTransferModel(unittest.TestCase):
    """Test Suite für Style Transfer Model"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.device = torch.device("cpu")
        self.model = StyleTransferModel().to(self.device)
    
    def test_model_creation(self):
        """Test Model Initialization"""
        self.assertIsNotNone(self.model)
    
    def test_forward_pass(self):
        """Test Forward Pass"""
        batch_size = 2
        input_tensor = torch.randn(batch_size, 3, 224, 224).to(self.device)
        
        output = self.model(input_tensor)
        
        self.assertEqual(output.shape, input_tensor.shape)
        self.assertTrue(torch.all((output >= 0) & (output <= 1)))

class TestEffectClassifier(unittest.TestCase):
    """Test Suite für Effect Classifier"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.device = torch.device("cpu")
        self.model = EffectClassifier(num_effects=10).to(self.device)
    
    def test_model_creation(self):
        """Test Model Initialization"""
        self.assertIsNotNone(self.model)
    
    def test_forward_pass(self):
        """Test Forward Pass"""
        batch_size = 2
        input_tensor = torch.randn(batch_size, 3, 224, 224).to(self.device)
        
        output = self.model(input_tensor)
        
        self.assertEqual(output.shape, (batch_size, 10))
        # Prüfe dass es Wahrscheinlichkeiten sind
        self.assertTrue(torch.all((output >= 0) & (output <= 1)))
        self.assertTrue(torch.allclose(output.sum(dim=1), torch.ones(batch_size)))

class TestKeyframePredictor(unittest.TestCase):
    """Test Suite für Keyframe Predictor"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.device = torch.device("cpu")
        self.model = KeyframePredictor().to(self.device)
    
    def test_model_creation(self):
        """Test Model Initialization"""
        self.assertIsNotNone(self.model)
    
    def test_forward_pass(self):
        """Test Forward Pass"""
        batch_size = 2
        seq_length = 10
        input_tensor = torch.randn(batch_size, seq_length, 128).to(self.device)
        
        keyframes, attention_weights = self.model(input_tensor)
        
        self.assertEqual(keyframes.shape, (batch_size, seq_length, 4))
        self.assertEqual(attention_weights.shape, (batch_size, seq_length, seq_length))

if __name__ == '__main__':
    unittest.main()
