"""
Coding test:
backend:
# The Challenge: Service Catalog Microservice # You are tasked with building the core of a new Service Catalog API. This API must manage a list of infrastructure services for the PI&E organization. 

# ### Setup & Data Model 

# Define a Go struct named Service to hold the following fields. Ensure appropriate JSON tags are used for marshaling/unmarshaling: # ID (string) # Name (string) # Owner (string) # Status (string) # Initialize an In-Memory Store: Create a global slice or map to store the Service objects in memory. Populate it with this initial data: # Go # {ID: "S101", Name: "Managed K8s Cluster", Owner: "Infra Team", Status: "Available"}, # {ID: "S102", Name: "S3 Storage Bucket", Owner: "Data Team", Status: "Available"}, # {ID: "S103", Name: "Internal Metrics Dashboard", Owner: "Observability", Status: "Deprecated"} # 

### Implement Endpoints # Set up a basic HTTP server using Go's built-in net/http package or a simple framework (e.g., Gin/Echo). 

Implement the following two REST endpoints: 

# #### GET /api/services: # Return the entire list of services in JSON format. # Must respond with HTTP Status 200 OK. 

# #### POST /api/services: # Accept a JSON body representing a new service request (requiring only Name and Owner). 

# Assign a new, unique ID to the service (e.g., auto-incrementing counter or UUID). 

# Set the initial Status to "In Progress".

# Add the new service to the in-memory store. # Must respond with HTTP Status 201 Created. 

# ## Verification 

# Start the Go server in the terminal. # Use the curl command in the same terminal to verify both the GET and POST endpoints are working as expected. 


frontend:

# The Challenge: 

Data Consumption and Table View You are tasked with building a component to consume and display service status data for the Service Catalog frontend. 

### Data Model & Fetching Define a TypeScript interface (or type) to model the data returned from the public API: https://jsonplaceholder.typicode.com/todos. 

Hint: The key fields are id, title, and completed. Create a component (e.g., ServiceStatusTable). Fetch Data: Use a fetch or axios call within useEffect to retrieve the data from the public endpoint. 

### UI Implementation Table Rendering: Display the fetched data in a visually clear HTML table with three columns: Service ID (mapped from id) Service Name (mapped from title) Provisioning Status (mapped from completed): If completed is true, show the status as "Available". 

If completed is false, show the status as "In Progress". State Handling: Implement the following states using React hooks: Loading State: Show a simple "Loading services..." message while the data is being fetched. Error State: If the fetch fails, display a clear "Error loading data." message. 

## Verification Run the React app (e.g., npm start in the terminal). Verify the browser view shows the table with data correctly mapped and transformed.
"""

import json
# asdict converts a dataclass instance into a plain python dict recursively - perfect for JSON
from dataclasses import dataclass, asdict
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List, Any


# -----------------------------
# 1) Data Model: Service
# -----------------------------
@dataclass
class Service:
    id: str
    name: str
    owner: str
    status: str

    def toJsonDict(self):
        return asdict(self)
    

# -----------------------------
# 2) In-Memory Store (global)
# -----------------------------
# Initialize an in-memory store and pre-populate it with initial data
serviceStore: Dict[str, Service] = {
    "S101": Service(id="S101", name="Managed K8s Cluster", owner="Infra Team", status="Available"),
    "S102": Service(id="S102", name="S3 Storage Bucket", owner="Data Team", status="Available"),
    "S103": Service(id="S103", name="Internal Metrics Dashboard", owner="Observability", status="Deprecated"),  
}

nextIdNumber = 104
# Assign a new unique ID to each new service(auto-incrementing)
def generateNextId():
    global nextIdNumber
    newId = f"S{nextIdNumber}"
    nextIdNumber += 1
    return newId


# -----------------------------
# 3) HTTP Handler + Endpoints
# -----------------------------
class Handler(BaseHTTPRequestHandler):
    def sendJson(self, statusCode, payload):
        # helper to return JSON with correct HTTP status
        # json.dumps: take a python object, convert it into a JSON string
        # encode('utf-8') converts string into bytes
        bodyBytes = json.dumps(payload).encode('utf-8')
        self.send_response(statusCode)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(bodyBytes)))
        self.end_headers()
        self.wfile.write(bodyBytes)

    def readJsonBody(self) -> Dict[str, Any]:
        contentLength = int(self.headers.get('Content-Length', '0'))
        rawBytes = self.rfile.read(contentLength) if contentLength > 0 else b''
        if not rawBytes:
            return {}
        # convert json str into python obj(dict)
        return json.loads(rawBytes.decode('utf-8'))
    def do_GET(self):
        # Req: GET /api/services returns the entire list, http 200
        if self.path != '/api/services':
            self.sendJson(404, {'error': 'Not found'})
            return
        # svc.toJsonDict()
        # converts each service object into a plain python dict with JSON-friendly keys
        serviceJson = [svc.toJsonDict() for svc in serviceStore.values()]
        self.sendJson(200, serviceJson)
    
    def do_POST(self):
        # Req POST /api/services accepts Name + Owner, creates new service, http 201
        if self.path != '/api/services':
            self.sendJson(404, {'error': 'Not found'})
            return 
        
        try:
            data = self.readJsonBody()
        except Exception:
            self.sendJson(400, { 'error': 'Invalid JSON body'})
            return 
        
        # request requires only name and owner
        name = data.get("Name") or data.get("name")
        owner = data.get("Owner") or data.get("owner")

        name = (name or '').strip()
        owner = (owner or '').strip()

        if not name or not owner:
            self.sendJson(400, {'error': "Body must include non-empty 'Name' and 'Owner'"})
            return
        
        # Req: assign unique ID and set status to 'in progress'
        newId = generateNextId()
        newService = Service(
            id = newId,
            name = name.strip(),
            owner = owner.strip(),
            status="In Progress",
        )

        # Req: add to in-memory store
        serviceStore[newId] = newService

        # Req: respond HTTP 201 created with created service JSON
        self.sendJson(201, newService.toJsonDict())

def runServer(host: str = '0.0.0.0', port: int = 8000):
    httpd = HTTPServer((host, port), Handler)
    print(f"Service Catalog API running on http://{host}:{port}")
    print("Try: GET  /api/services")
    print("Try: POST /api/services  body: {\"Name\":\"Redis Cache\",\"Owner\":\"Platform Team\"}")
    
    httpd.serve_forever()

runServer()


# frontend
