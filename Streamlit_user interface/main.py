#this is the main file that will be used to run the FastAPI server
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union
import json
import import_ipynb
from bson import ObjectId
import datahandlers_v5 as  OutputManager

# Utility function to handle ObjectId serialization
def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [objectid_to_str(item) for item in obj]
    else:
        return obj

# Define FastAPI app
app = FastAPI()

# Define an instance of OutputManager
output_manager = OutputManager.OutputManager()

# Define the Pydantic model to validate the incoming request data
class QueryRequest(BaseModel):
    query: dict  # Contains "what", "time", and other query parameters
    point: Union[List[float], None] = None  # Latitude, Longitude for location (Point)
    area: Union[str, float, None] = None  # Area for search (either "polygon" or a numeric radius value)

@app.post("/unified_search")
async def unified_search(request: QueryRequest):
    try:
        # Extract data from the incoming request
        query = request.query
        point = request.point
        area = request.area  # This can either be "polygon" or a numeric radius value

        # If no click_point or area is provided, return all results based on the query alone
        if point is None or area is None:
            # Perform a search without location-based filtering (i.e., no radius or polygon)
            om = output_manager
            om.perform_search(query=query)  # Just perform a search with the query
            results = om.data
        else:
            # If a point and area are provided, perform the search with location-based filtering
            if len(point) != 2:
                raise HTTPException(status_code=400, detail="Point must contain exactly two values: latitude and longitude.")

            # Create an instance of OutputManager to handle the query
            om = output_manager

            # Check if the user wants to perform a polygon-based search
            if area == "polygon":
                # Perform search using polygon (this assumes the OutputManager has polygon_data method)
                om.perform_search(query=query, point=point, area="polygon")
                results = om.data
            else:
                # Assume the area is a numeric radius value if it's not "polygon"
                try:
                    if isinstance(area, float) or isinstance(area, int):
                        radius = float(area)  # If it's numeric, we can use it directly
                    else:
                        raise ValueError("Invalid area format")
                    
                    om.perform_search(query=query, point=point, area=radius)
                    results = om.data
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid area. Please provide a numeric radius or 'polygon'.")

        # Convert ObjectId to string for each result if present
        results = objectid_to_str(results)

        # Return the unified results (without limiting the number of results)
        return {
            "query": query,
            "num_results": len(results),
            "results": results
        }

    except HTTPException as e:
        # Handle known HTTP exceptions
        raise e
    except Exception as e:
        # Log the error for debugging purposes and raise an HTTP error
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Endpoint to test with a simple GET method if needed
@app.get("/")
def read_root():
    return {"message": "Welcome to the Unified Search API"}