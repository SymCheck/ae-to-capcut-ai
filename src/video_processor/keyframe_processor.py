"""
Keyframe Processing Module
"""

from typing import List, Dict, Any, Tuple
import numpy as np
from src.utils.logger import logger

class KeyframeProcessor:
    """Verarbeitet und optimiert Keyframe-Animationen"""
    
    def __init__(self):
        self.logger = logger
    
    def interpolate_keyframes(
        self,
        keyframes: List[Dict[str, Any]],
        target_fps: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Interpoliert Keyframes für sanfte Animation
        
        Args:
            keyframes: Liste von Keyframes
            target_fps: Ziel-FPS für Interpolation
            
        Returns:
            Interpolierte Keyframes
        """
        if len(keyframes) < 2:
            return keyframes
        
        interpolated = []
        
        for i in range(len(keyframes) - 1):
            current = keyframes[i]
            next_kf = keyframes[i + 1]
            
            interpolated.append(current)
            
            # Berechne Intermediate Frames
            current_time = current.get("time", 0)
            next_time = next_kf.get("time", 1)
            current_value = current.get("value", 0)
            next_value = next_kf.get("value", 0)
            
            frame_count = int((next_time - current_time) * target_fps)
            
            for frame in range(1, frame_count):
                t = frame / frame_count
                
                # Easing basierend auf ease_in/ease_out
                ease_in = current.get("ease_in", 0)
                ease_out = current.get("ease_out", 0)
                
                # Linear interpolation mit easing
                eased_t = self._apply_easing(t, ease_in, ease_out)
                
                interpolated_value = current_value + (next_value - current_value) * eased_t
                interpolated_time = current_time + (next_time - current_time) * t
                
                interpolated.append({
                    "time": interpolated_time,
                    "value": interpolated_value,
                    "interpolated": True,
                })
        
        # Füge letztes Keyframe hinzu
        interpolated.append(keyframes[-1])
        
        self.logger.info(f"Interpolated {len(keyframes)} keyframes to {len(interpolated)} frames")
        return interpolated
    
    def _apply_easing(self, t: float, ease_in: float, ease_out: float) -> float:
        """
        Wendet Easing-Kurven an
        
        Args:
            t: Normalisierte Zeit (0-1)
            ease_in: Ease-In Stärke
            ease_out: Ease-Out Stärke
            
        Returns:
            Eased Zeit
        """
        if ease_in > 0:
            t = t * t * ease_in + t * (1 - ease_in)
        
        if ease_out > 0:
            t = (1 - ((1 - t) ** 2)) * ease_out + t * (1 - ease_out)
        
        return t
    
    def smooth_animation_curve(self, values: List[float]) -> List[float]:
        """
        Glättet eine Animations-Kurve
        
        Args:
            values: Liste von Werten
            
        Returns:
            Geglättete Werte
        """
        if len(values) < 3:
            return values
        
        smoothed = [values[0]]
        
        for i in range(1, len(values) - 1):
            # Simple 3-point moving average
            avg = (values[i - 1] + values[i] + values[i + 1]) / 3
            smoothed.append(avg)
        
        smoothed.append(values[-1])
        return smoothed
    
    def optimize_keyframes(
        self,
        keyframes: List[Dict[str, Any]],
        tolerance: float = 0.01
    ) -> List[Dict[str, Any]]:
        """
        Optimiert Keyframes durch Entfernung redundanter Punkte
        
        Args:
            keyframes: Original Keyframes
            tolerance: Toleranz für Punkt-Entfernung
            
        Returns:
            Optimierte Keyframes
        """
        if len(keyframes) <= 2:
            return keyframes
        
        optimized = [keyframes[0]]
        
        for i in range(1, len(keyframes) - 1):
            prev_kf = optimized[-1]
            curr_kf = keyframes[i]
            next_kf = keyframes[i + 1]
            
            # Berechne Abweichung
            prev_val = prev_kf.get("value", 0)
            curr_val = curr_kf.get("value", 0)
            next_val = next_kf.get("value", 0)
            
            # Linearer Wert zwischen prev und next
            t = (curr_kf.get("time", 0) - prev_kf.get("time", 0)) / \
                (next_kf.get("time", 0) - prev_kf.get("time", 0)) if \
                next_kf.get("time", 0) != prev_kf.get("time", 0) else 0.5
            
            linear_value = prev_val + (next_val - prev_val) * t
            
            # Prüfe ob Abweichung größer als Toleranz
            deviation = abs(curr_val - linear_value)
            
            if deviation > tolerance:
                optimized.append(curr_kf)
        
        optimized.append(keyframes[-1])
        
        self.logger.info(f"Optimized keyframes: {len(keyframes)} → {len(optimized)}")
        return optimized
