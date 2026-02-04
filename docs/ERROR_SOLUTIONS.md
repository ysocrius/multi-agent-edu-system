# Error Solutions Log

This document tracks all errors encountered during development, their root causes, solutions, and lessons learned.

---

## Error #1: ImportError - Relative Import Beyond Top-Level Package
**Date**: 2026-02-04  
**Phase**: Testing/Deployment  
**Component**: Generator Agent, Reviewer Agent

### Problem
```
ImportError: attempted relative import beyond top-level package
```
When running `python main.py` from `src/` directory, relative imports failed:
- `from ..utils.llm_client import LLMClient` (in generator.py)
- `from .schemas import GeneratorInput` (in generator.py)

### Root Cause
Python's import system treats `src/` as the top-level when running `python main.py` directly. Relative imports using `..` try to go above the top-level package, which fails.

### Solution
Changed from relative to absolute imports:
```python
# Before (FAILED)
from ..utils.llm_client import LLMClient
from .schemas import GeneratorInput

# After (WORKS)
from utils.llm_client import LLMClient
from agents.schemas import GeneratorInput
```

Files modified:
- `src/agents/generator.py`
- `src/agents/reviewer.py`

### Prevention
- Use absolute imports when running modules directly
- Or use `python -m` to run as module: `python -m src.main`
- Add `src/` to PYTHONPATH if needed

### Interview Relevance
**Q: What import issues did you encounter?**  
A: Hit "relative import beyond top-level package" error. This happens when Python's import context doesn't match the package structure. Fixed by using absolute imports (`from agents.schemas` instead of `from .schemas`) since we're running from the `src/` directory directly.
