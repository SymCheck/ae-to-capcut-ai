"""
FastAPI Server für AE to CapCut AI Converter
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import json
import tempfile
from typing import Optional
import uvicorn

from src.video_processor.capcut_generator import CapCutGenerator
from src.ai_model.inference import ModelInference
from src.utils.logger import logger
from src.utils.config import DATA_DIR

app = FastAPI(
    title="AE to CapCut AI API",
    description="Convert After Effects Projects to CapCut format using AI",
    version="0.1.0"
)

# Globale Instanzen
generator = CapCutGenerator()
inference = ModelInference()

# Pydantic Models
class ConversionRequest(BaseModel):
    """Request für Conversion"""
    project_name: str
    enable_style_transfer: bool = False

class ConversionResponse(BaseModel):
    """Response nach Conversion"""
    status: str
    project_id: str
    output_path: str
    message: str

class ModelStatus(BaseModel):
    """Status der Modelle"""
    style_transfer: str
    effect_classifier: str
    keyframe_predictor: str

# Health Check
@app.get("/health")
async def health_check():
    """Health Check Endpoint"""
    return {
        "status": "healthy",
        "service": "AE to CapCut AI API",
        "version": "0.1.0"
    }

# Conversion Endpoints
@app.post("/api/v1/convert", response_model=ConversionResponse)
async def convert_project(
    file: UploadFile = File(...),
    enable_style_transfer: bool = False,
    background_tasks: BackgroundTasks = None
):
    """
    Konvertiert ein After Effects Projekt zu CapCut Format
    
    Args:
        file: AE JSON Datei
        enable_style_transfer: Wende Style Transfer an
        
    Returns:
        Conversion Response
    """
    try:
        # Validiere Datei
        if not file.filename.endswith('.json'):
            raise HTTPException(status_code=400, detail="Only JSON files supported")
        
        # Speichere Datei temporär
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = Path(tmp.name)
        
        # Konvertiere Projekt
        project_name = file.filename.replace('.json', '')
        output_path = DATA_DIR / "capcut_projects" / f"{project_name}_capcut.json"
        
        result = generator.generate_from_ae_project(tmp_path, output_path)
        
        logger.info(f"Successfully converted project: {project_name}")
        
        return ConversionResponse(
            status="success",
            project_id=project_name,
            output_path=str(output_path),
            message=f"Project {project_name} converted successfully"
        )
    
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup
        if tmp_path.exists():
            tmp_path.unlink()

@app.post("/api/v1/batch-convert")
async def batch_convert(
    input_directory: str = None
):
    """
    Batch Konvertierung von mehreren Projekten
    
    Args:
        input_directory: Input Verzeichnis
        
    Returns:
        Conversion Results
    """
    try:
        input_dir = Path(input_directory) if input_directory else DATA_DIR / "raw_ae_projects"
        output_dir = DATA_DIR / "capcut_projects"
        
        if not input_dir.exists():
            raise HTTPException(status_code=400, detail="Input directory not found")
        
        results = generator.batch_convert(input_dir, output_dir)
        
        return {
            "status": "success",
            "projects_converted": len(results),
            "output_directory": str(output_dir),
            "results": [str(r) for r in results]
        }
    
    except Exception as e:
        logger.error(f"Batch conversion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Model Management Endpoints
@app.get("/api/v1/models/status", response_model=ModelStatus)
async def get_model_status():
    """Gibt Status der Modelle zurück"""
    return ModelStatus(
        style_transfer="ready",
        effect_classifier="ready",
        keyframe_predictor="ready"
    )

@app.get("/api/v1/models/list")
async def list_models():
    """Listen verfügbare Modelle auf"""
    model_dir = DATA_DIR / "models"
    
    if not model_dir.exists():
        return {"models": []}
    
    models = list(model_dir.glob("*.pth"))
    
    return {
        "models": [m.name for m in models],
        "count": len(models)
    }

@app.post("/api/v1/models/reload")
async def reload_models():
    """Reloaded alle Modelle"""
    try:
        global inference
        inference = ModelInference()
        
        logger.info("Models reloaded successfully")
        
        return {
            "status": "success",
            "message": "Models reloaded"
        }
    
    except Exception as e:
        logger.error(f"Model reload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Project Management
@app.get("/api/v1/projects")
async def list_projects():
    """Liste alle CapCut Projekte"""
    capcut_dir = DATA_DIR / "capcut_projects"
    
    if not capcut_dir.exists():
        return {"projects": []}
    
    projects = list(capcut_dir.glob("*.json"))
    
    return {
        "projects": [p.name for p in projects],
        "count": len(projects)
    }

@app.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str):
    """Lade ein spezifisches Projekt"""
    try:
        project_path = DATA_DIR / "capcut_projects" / f"{project_id}.json"
        
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        with open(project_path, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        
        return project_data
    
    except Exception as e:
        logger.error(f"Error loading project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/projects/{project_id}/download")
async def download_project(project_id: str):
    """Downloade ein Projekt"""
    try:
        project_path = DATA_DIR / "capcut_projects" / f"{project_id}.json"
        
        if not project_path.exists():
            raise HTTPException(status_code=404, detail="Project not found")
        
        return FileResponse(
            project_path,
            media_type="application/json",
            filename=f"{project_id}.json"
        )
    
    except Exception as e:
        logger.error(f"Error downloading project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Stats & Analytics
@app.get("/api/v1/stats")
async def get_stats():
    """Gibt System-Statistiken"""
    ae_dir = DATA_DIR / "raw_ae_projects"
    capcut_dir = DATA_DIR / "capcut_projects"
    
    ae_count = len(list(ae_dir.glob("*.json"))) if ae_dir.exists() else 0
    capcut_count = len(list(capcut_dir.glob("*.json"))) if capcut_dir.exists() else 0
    
    return {
        "ae_projects": ae_count,
        "capcut_projects": capcut_count,
        "models_loaded": True,
        "status": "operational"
    }

# Error Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP Exception Handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

def run_server(host: str = "0.0.0.0", port: int = 8000, debug: bool = True):
    """Starte den Server"""
    uvicorn.run(app, host=host, port=port, reload=debug)

if __name__ == "__main__":
    run_server(debug=True)
