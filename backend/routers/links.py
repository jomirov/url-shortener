from fastapi import Body, Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse, JSONResponse
from ..models.link import Link
from ..database.linkRepository import LinkRepository
from ..dependencies import lifespan
import sqlite3

router = APIRouter(lifespan=lifespan)

router.frontend(path="/link", directory="dist", fallback="index.html")

@router.post('/api/link')
def add_url(link: Link = Body(), linkRepository: LinkRepository = Depends()):
    try:
        linkRepository.add_link(link.original_url, link.short_alias)
    except sqlite3.IntegrityError:
        HTTPException(status_code=400, detail="Alias already exists")


    return JSONResponse({"message": "Link has been shortened", "status_code": 201}, status_code = 201)

@router.get('/api/link')
def show_all_links(linkRepository: LinkRepository = Depends()):
    return JSONResponse(linkRepository.show_all_links())

@router.get('/r/{alias}')
def redirect_to_url(alias: str, linkRepository: LinkRepository = Depends()):
    url = linkRepository.take_url_of_alias(alias)
    if url is None:
        raise HTTPException(status_code=404, detail="URL is not found")
    
    return RedirectResponse(url)

@router.delete('/api/link/{id}')
def remove_link(id: int, linkRepository: LinkRepository = Depends()):
    linkRepository.delete_link(id)
    return JSONResponse({"message": "Link has been deleted"}, status_code = 200)