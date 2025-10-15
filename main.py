import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

app = FastAPI()

# returns the list of all papers from db
@app.get("/papers")
def read_all_papers():
    try:
        return supabase.table("papers").select("*").execute().data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e.message}")   

# returns the paper that matches the given id
@app.get("/papers/{id}")
def read_paper(id):
    try:
        result = supabase.table("papers").select("*").eq("id", id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed: {e.message}")
    
    papers = result.data
        
    if not papers:    
        raise HTTPException(status_code=404, detail=f"Paper with id {id} not found")

    return papers[0]

