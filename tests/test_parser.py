"""
Unit Tests für AE Parser
"""

import unittest
import json
from pathlib import Path
import tempfile
from src.video_processor.ae_parser import AEProjectParser

class TestAEProjectParser(unittest.TestCase):
    """Test Suite für After Effects Parser"""
    
    def setUp(self):
        """Setup Test Fixtures"""
        self.parser = AEProjectParser()
        
        # Erstelle Test-Projekt JSON
        self.test_project = {
            "project": {
                "name": "Test Project",
                "fps": 30,
                "duration": 120,
                "width": 1920,
                "height": 1080,
            },
            "compositions": [
                {
                    "name": "Main Comp",
                    "layers": [
                        {
                            "name": "Video Layer",
                            "type": "video",
                            "effects": [
                                {
                                    "name": "Color Correction",
                                    "type": "color_correction",
                                    "parameters": {"brightness": 0.5}
                                }
                            ],
                            "keyframes": [
                                {
                                    "property": "position",
                                    "time": 0,
                                    "value": [0, 0],
                                    "ease_in": 0.1,
                                    "ease_out": 0.1,
                                }
                            ]
                        },
                        {
                            "name": "Text Layer",
                            "type": "text",
                            "content": "Test Text",
                            "font": "Arial",
                            "font_size": 24,
                        }
                    ]
                }
            ]
        }
    
    def test_parse_project(self):
        """Test Project Parsing"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.test_project, f)
            tmp_path = Path(f.name)
        
        try:
            result = self.parser.parse_project(tmp_path)
            self.assertEqual(result["project"]["name"], "Test Project")
        finally:
            tmp_path.unlink()
    
    def test_extract_effects(self):
        """Test Effects Extraction"""
        effects = self.parser.extract_effects(self.test_project)
        self.assertEqual(len(effects), 1)
        self.assertEqual(effects[0]["effect_name"], "Color Correction")
    
    def test_extract_keyframes(self):
        """Test Keyframe Extraction"""
        keyframes = self.parser.extract_keyframes(self.test_project)
        self.assertEqual(len(keyframes), 1)
        self.assertEqual(keyframes[0]["property"], "position")
    
    def test_extract_text_layers(self):
        """Test Text Layer Extraction"""
        text_layers = self.parser.extract_text_layers(self.test_project)
        self.assertEqual(len(text_layers), 1)
        self.assertEqual(text_layers[0]["content"], "Test Text")
    
    def test_get_project_metadata(self):
        """Test Metadata Extraction"""
        metadata = self.parser.get_project_metadata(self.test_project)
        self.assertEqual(metadata["name"], "Test Project")
        self.assertEqual(metadata["fps"], 30)
        self.assertEqual(metadata["duration"], 120)

if __name__ == '__main__':
    unittest.main()
