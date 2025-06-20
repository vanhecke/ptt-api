"""
PTT API Web Service

A FastAPI web service that wraps around the PTT (parsett) library for parsing torrent titles.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging

# Import PTT library
try:
    from PTT import parse_title
except ImportError:
    # Fallback import if the module structure is different
    try:
        from parsett import parse_title
    except ImportError:
        raise ImportError("Could not import parse_title from PTT or parsett")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="PTT API",
    description="A web service that wraps around the PTT (parsett) library for parsing torrent titles",
    version="1.0.0",
    docs_url="/",
    redoc_url="/redoc"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class ParseResponse(BaseModel):
    """Response model for parse endpoint"""
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    original_title: str

class HealthResponse(BaseModel):
    """Response model for health endpoint"""
    status: str
    service: str
    version: str

class BatchParseRequest(BaseModel):
    """Request model for batch parse endpoint"""
    titles: List[str]
    translate_languages: bool = False

class BatchParseResponse(BaseModel):
    """Response model for batch parse endpoint"""
    success: bool
    results: List[ParseResponse]
    total_processed: int

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        service="PTT API",
        version="1.0.0"
    )

@app.get("/parse", response_model=ParseResponse)
async def parse_torrent_title(
    title: str = Query(..., description="The torrent title to parse", min_length=1),
    translate_languages: bool = Query(False, description="Whether to translate language codes to full names")
):
    """
    Parse a torrent title and return structured data.
    
    Args:
        title: The torrent title to parse
        translate_languages: Whether to translate language codes to full names (default: False)
    
    Returns:
        ParseResponse: Structured data extracted from the torrent title
    """
    try:
        logger.info(f"Parsing title: {title}")
        
        # Parse the title using PTT
        result = parse_title(title, translate_languages=translate_languages)
        
        logger.info(f"Parse result: {result}")
        
        return ParseResponse(
            success=True,
            data=result,
            original_title=title
        )
        
    except Exception as e:
        logger.error(f"Error parsing title '{title}': {str(e)}")
        return ParseResponse(
            success=False,
            error=str(e),
            original_title=title
        )

@app.get("/parse-simple")
async def parse_torrent_title_simple(
    title: str = Query(..., description="The torrent title to parse", min_length=1),
    translate_languages: bool = Query(False, description="Whether to translate language codes to full names")
):
    """
    Parse a torrent title and return the raw result (simplified endpoint).
    
    Args:
        title: The torrent title to parse
        translate_languages: Whether to translate language codes to full names (default: False)
    
    Returns:
        Dict: Raw structured data extracted from the torrent title
    """
    try:
        logger.info(f"Parsing title (simple): {title}")
        
        # Parse the title using PTT
        result = parse_title(title, translate_languages=translate_languages)
        
        logger.info(f"Parse result (simple): {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error parsing title '{title}': {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/examples")
async def get_examples():
    """
    Get example torrent titles and their parsed results.
    """
    examples = [
        "The.Simpsons.S01E01.1080p.BluRay.x265.HEVC.10bit.AAC.5.1.Tigole",
        "www.Tamilblasters.party - The Wheel of Time (2021) Season 01 EP(01-08) [720p HQ HDRip - [Tam + Tel + Hin] - DDP5.1 - x264 - 2.7GB - ESubs]",
        "The.Walking.Dead.S06E07.SUBFRENCH.HDTV.x264-AMB3R.mkv",
        "Avengers.Endgame.2019.2160p.UHD.BluRay.x265.HDR.Atmos-TERMINAL",
        "Game.of.Thrones.S08E06.The.Iron.Throne.1080p.AMZN.WEB-DL.DDP5.1.H.264-GoT"
    ]
    
    results = []
    for example in examples:
        try:
            parsed = parse_title(example)
            results.append({
                "title": example,
                "parsed": parsed
            })
        except Exception as e:
            results.append({
                "title": example,
                "error": str(e)
            })
    
    return {"examples": results}

@app.post("/parse-batch", response_model=BatchParseResponse)
async def parse_batch_titles(request: BatchParseRequest):
    """
    Parse multiple torrent titles in batch.
    
    Args:
        request: BatchParseRequest containing list of titles and options
    
    Returns:
        BatchParseResponse: Results for all parsed titles
    """
    try:
        logger.info(f"Batch parsing {len(request.titles)} titles")
        
        results = []
        for title in request.titles:
            try:
                parsed = parse_title(title, translate_languages=request.translate_languages)
                results.append(ParseResponse(
                    success=True,
                    data=parsed,
                    original_title=title
                ))
            except Exception as e:
                logger.error(f"Error parsing title '{title}': {str(e)}")
                results.append(ParseResponse(
                    success=False,
                    error=str(e),
                    original_title=title
                ))
        
        return BatchParseResponse(
            success=True,
            results=results,
            total_processed=len(request.titles)
        )
        
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=12000)