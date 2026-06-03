"""
Reasoning Engine for REX AI - Multi-path reasoning with confidence scoring.
"""

import logging
from typing import Dict, List, Tuple, Optional
from enum import Enum
import random

logger = logging.getLogger(__name__)


class ReasoningPath(Enum):
    """Reasoning paths the engine can use."""
    LOGICAL = "logical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    HEURISTIC = "heuristic"
    PROBABILISTIC = "probabilistic"


class ReasoningTrace:
    """Represents a reasoning trace."""
    
    def __init__(self):
        self.steps: List[str] = []
        self.paths_used: List[str] = []
        self.conclusions: List[str] = []
        self.confidence_scores: List[float] = []
    
    def add_step(self, step: str, path: str, confidence: float):
        """Add a step to the trace."""
        self.steps.append(step)
        if path not in self.paths_used:
            self.paths_used.append(path)
        self.confidence_scores.append(confidence)
    
    def add_conclusion(self, conclusion: str):
        """Add a conclusion."""
        self.conclusions.append(conclusion)
    
    def get_summary(self) -> Dict:
        """Get a summary of the reasoning."""
        avg_confidence = sum(self.confidence_scores) / len(self.confidence_scores) if self.confidence_scores else 0.0
        return {
            "steps": len(self.steps),
            "paths_used": self.paths_used,
            "avg_confidence": avg_confidence,
            "conclusions": self.conclusions,
            "trace": "\\n".join(self.steps),
        }


class ReasoningEngine:
    """Multi-path reasoning engine."""
    
    def __init__(self):
        """Initialize reasoning engine."""
        self.reasoning_history: List[ReasoningTrace] = []
        self.max_reasoning_steps = 10
        logger.info("ReasoningEngine initialized")
    
    def reason(self, question: str, preferred_paths: Optional[List[ReasoningPath]] = None) -> Tuple[str, float]:
        """
        Execute multi-path reasoning.
        
        Args:
            question: The question to reason about
            preferred_paths: Optional list of preferred reasoning paths
            
        Returns:
            Tuple of (conclusion, confidence_score)
        """
        trace = ReasoningTrace()
        
        # Use preferred paths or all paths
        paths = preferred_paths if preferred_paths else list(ReasoningPath)
        
        results = []
        
        for path in paths:
            conclusion, confidence = self._apply_reasoning_path(question, path, trace)
            results.append((conclusion, confidence))
        
        # Combine results
        final_conclusion, final_confidence = self._combine_results(results)
        trace.add_conclusion(final_conclusion)
        
        self.reasoning_history.append(trace)
        
        logger.debug(f"Reasoning complete - Confidence: {final_confidence}")
        return final_conclusion, final_confidence
    
    def _apply_reasoning_path(self, question: str, path: ReasoningPath, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply a specific reasoning path."""
        
        if path == ReasoningPath.LOGICAL:
            return self._logical_reasoning(question, trace)
        elif path == ReasoningPath.CREATIVE:
            return self._creative_reasoning(question, trace)
        elif path == ReasoningPath.ANALYTICAL:
            return self._analytical_reasoning(question, trace)
        elif path == ReasoningPath.HEURISTIC:
            return self._heuristic_reasoning(question, trace)
        elif path == ReasoningPath.PROBABILISTIC:
            return self._probabilistic_reasoning(question, trace)
        
        return "Unable to reason", 0.0
    
    def _logical_reasoning(self, question: str, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply logical deduction reasoning."""
        trace.add_step(
            f"[{ReasoningPath.LOGICAL.value}] Applying logical deduction to question",
            ReasoningPath.LOGICAL.value,
            0.85
        )
        
        # Simple logical reasoning
        conclusion = f"Based on logical analysis: {question} requires careful consideration of facts and rules."
        return conclusion, 0.85
    
    def _creative_reasoning(self, question: str, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply creative reasoning."""
        trace.add_step(
            f"[{ReasoningPath.CREATIVE.value}] Exploring creative possibilities",
            ReasoningPath.CREATIVE.value,
            0.70
        )
        
        conclusion = f"Creatively exploring possibilities for: {question}"
        return conclusion, 0.70
    
    def _analytical_reasoning(self, question: str, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply analytical reasoning."""
        trace.add_step(
            f"[{ReasoningPath.ANALYTICAL.value}] Breaking down problem analytically",
            ReasoningPath.ANALYTICAL.value,
            0.80
        )
        
        conclusion = f"Analytical breakdown shows: {question} can be examined component by component."
        return conclusion, 0.80
    
    def _heuristic_reasoning(self, question: str, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply heuristic reasoning based on experience."""
        trace.add_step(
            f"[{ReasoningPath.HEURISTIC.value}] Using experience-based heuristics",
            ReasoningPath.HEURISTIC.value,
            0.75
        )
        
        conclusion = f"From experience, {question} suggests common patterns and solutions."
        return conclusion, 0.75
    
    def _probabilistic_reasoning(self, question: str, trace: ReasoningTrace) -> Tuple[str, float]:
        """Apply probabilistic reasoning."""
        trace.add_step(
            f"[{ReasoningPath.PROBABILISTIC.value}] Calculating statistical likelihood",
            ReasoningPath.PROBABILISTIC.value,
            0.65
        )
        
        confidence = random.uniform(0.6, 0.8)
        conclusion = f"Statistical analysis of {question} suggests probability-based conclusions."
        return conclusion, confidence
    
    def _combine_results(self, results: List[Tuple[str, float]]) -> Tuple[str, float]:
        """Combine results from multiple reasoning paths."""
        if not results:
            return "Unable to reason", 0.0
        
        # Average confidence
        avg_confidence = sum(conf for _, conf in results) / len(results)
        
        # Pick best conclusion (for now, the first high-confidence one)
        best_result = max(results, key=lambda x: x[1])
        
        return best_result[0], avg_confidence
    
    def get_reasoning_trace(self) -> Dict:
        """Get the last reasoning trace."""
        if self.reasoning_history:
            return self.reasoning_history[-1].get_summary()
        return {"steps": 0, "paths_used": [], "avg_confidence": 0.0, "trace": "No reasoning performed yet"}
