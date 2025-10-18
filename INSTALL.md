# Installation Instructions

## Fix Gemini SDK Routing Issue

If you're getting errors like:
```
404 models/gemini-pro is not found for API version v1beta
```

This means the wrong client is being used. Follow these steps:

### 1. Clean up conflicting packages

```powershell
pip uninstall google-generativeai google-ai-generativelanguage -y
pip uninstall google-cloud-aiplatform -y
```

### 2. Reinstall fresh

```powershell
pip install --upgrade google-generativeai
pip install python-dotenv
```

### 3. Verify installation

```powershell
python -c "import google.generativeai as genai; print(genai.__version__)"
```

Should show version 0.8.x or higher.

### 4. Install other dependencies

```powershell
pip install -r requirements.txt
```

## Why This Happens

- **Wrong**: `google-ai-generativelanguage_v1beta` (gRPC client for Vertex AI)
- **Correct**: `google.generativeai` (REST client for Gemini API)

The gRPC client requires service accounts and project IDs (Vertex AI).
The REST client works with API keys (Gemini API).

## Test It Works

```powershell
python test_gemini.py
```

Should see:
```
✓ Gemini Initialized: True
✅ Extraction successful!
```

## If Still Having Issues

Check which client is being imported:

```powershell
python -c "import google.generativeai as genai; print(genai.GenerativeModel.__module__)"
```

Should output:
```
google.generativeai.generative_models
```

NOT:
```
google.ai.generativelanguage_v1beta...
```
