"""
Unit Tests für Effects Mapper
"""

import unittest
from src.video_processor.effects_mapper import EffectsMapper, TextAnimationMapper, TransitionMapper

class TestEffectsMapper(unittest.TestCase):
    """Test Suite für Effects Mapper"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.mapper = EffectsMapper()
    
    def test_map_color_correction_effect(self):
        """Test Color Correction Mapping"""
        ae_effect = {
            "layer_name": "Video",
            "effect_name": "Color Correction",
            "type": "color_correction",
            "parameters": {
                "brightness": 0.8,
                "contrast": 0.6,
            },
            "enabled": True,
        }
        
        mapped = self.mapper.map_effect(ae_effect)
        self.assertIsNotNone(mapped)
        self.assertEqual(mapped["type"], "color_adjustment")
        self.assertEqual(mapped["layer_name"], "Video")
    
    def test_map_blur_effect(self):
        """Test Blur Effect Mapping"""
        ae_effect = {
            "layer_name": "Video",
            "effect_name": "Gaussian Blur",
            "type": "gaussian_blur",
            "parameters": {
                "radius": 5.0,
            },
            "enabled": True,
        }
        
        mapped = self.mapper.map_effect(ae_effect)
        self.assertIsNotNone(mapped)
        self.assertEqual(mapped["type"], "blur")
    
    def test_map_unknown_effect(self):
        """Test Unknown Effect Handling"""
        ae_effect = {
            "layer_name": "Video",
            "effect_name": "Unknown Effect",
            "type": "unknown",
            "parameters": {},
            "enabled": True,
        }
        
        mapped = self.mapper.map_effect(ae_effect)
        self.assertIsNone(mapped)
    
    def test_normalize_value(self):
        """Test Value Normalization"""
        result1 = self.mapper._normalize_value(2.0, "brightness")
        self.assertEqual(result1, 1.0)
        
        result2 = self.mapper._normalize_value(-1.0, "brightness")
        self.assertEqual(result2, 0.0)
        
        result3 = self.mapper._normalize_value(0.5, "brightness")
        self.assertEqual(result3, 0.5)

class TestTextAnimationMapper(unittest.TestCase):
    """Test Suite für Text Animation Mapper"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.mapper = TextAnimationMapper()
    
    def test_map_fade_animation(self):
        """Test Fade Animation Mapping"""
        ae_animation = {
            "type": "fade",
            "duration": 0.5,
            "delay": 0.1,
            "intensity": 1.0,
        }
        
        mapped = self.mapper.map_text_animation(ae_animation)
        self.assertEqual(mapped["type"], "fade")
        self.assertEqual(mapped["duration"], 0.5)
    
    def test_map_slide_animation(self):
        """Test Slide Animation Mapping"""
        ae_animation = {
            "type": "slide",
            "duration": 0.5,
        }
        
        mapped = self.mapper.map_text_animation(ae_animation)
        self.assertEqual(mapped["type"], "slide")

class TestTransitionMapper(unittest.TestCase):
    """Test Suite für Transition Mapper"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.mapper = TransitionMapper()
    
    def test_map_dissolve_transition(self):
        """Test Dissolve Transition Mapping"""
        ae_transition = {
            "name": "dissolve",
            "duration": 0.5,
            "intensity": 1.0,
        }
        
        mapped = self.mapper.map_transition(ae_transition)
        self.assertEqual(mapped["type"], "fade")
    
    def test_map_wipe_transition(self):
        """Test Wipe Transition Mapping"""
        ae_transition = {
            "name": "wipe",
            "duration": 0.5,
        }
        
        mapped = self.mapper.map_transition(ae_transition)
        self.assertEqual(mapped["type"], "slide")

if __name__ == '__main__':
    unittest.main()
