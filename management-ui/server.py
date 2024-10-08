'''
License: 5G-MAG Public License (v1.0)
Author: Vuk Stojkovic, David Waring
Copyright: (C) Fraunhofer FOKUS, British Broadcasting Corporation
For full license terms please see the LICENSE file distributed with this
program. If this file is missing then the license can be retrieved from
https://drive.google.com/file/d/1cinCiA778IErENZ3JN52VFW-1ffHpx7Z/view
'''

import os
import json
import requests
import asyncio
import httpx
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI, Query, Depends, HTTPException, Response, Request
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from utils import lib_to_sys_path

load_dotenv()
lib_to_sys_path()

from rt_m1_client.types import ResourceId, ApplicationId, ConsumptionReportingConfiguration, PolicyTemplate, MetricsReportingConfiguration
from rt_m1_client.configuration import Configuration
from rt_m1_client.session import M1Session
from rt_m1_client.data_store import JSONFileDataStore
from rt_m1_client.exceptions import M1Error

config = Configuration()

OPTIONS_ENDPOINT = os.getenv("OPTIONS_ENDPOINT", "http://" + config.get('m1_address', 'localhost') + ":" + config.get('m1_port',7777) + "/3gpp-m1/v2/provisioning-sessions/")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://0.0.0.0:8000,http://127.0.0.1:8000,http://localhost:8000").split(',')

app = FastAPI()
_m1_session = None


# Auxiliary function to pass proper configuration as dependency injection parameter
def get_config():
    return Configuration()


async def get_session(config: Configuration) -> M1Session:
    global _m1_session
    if _m1_session is None:
        data_store_dir = config.get('data_store')
        if data_store_dir is not None:
            data_store = await JSONFileDataStore(config.get('data_store'))
        else:
            data_store = None
        _m1_session = await M1Session((config.get('m1_address', 'localhost'),
                                       config.get('m1_port',7777)),
                                       data_store,
                                       config.get('certificate_signing_class'))
    return _m1_session

# Error handling
@app.exception_handler(M1Error)
async def m1_error_handler(request: Request, exc: M1Error):
    if exc.args[2] is not None:
        return JSONResponse(status_code=exc.args[1], content=exc.args[2])
    return PlainTextResponse(status_code=exc.args[1], content=exc.args[0])

# UI page rendering
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
@app.get("/")
def landing_page():
    return FileResponse("templates/index.html")


"""
Endpoint: Create Provisioning Session
HTTP Method: POST
Path: /create_session
Description: This endpoint will create a empty provisioning session.
"""
@app.post("/create_session")
async def new_provisioning_session(app_id: Optional[str] = None, asp_id: Optional[str] = None):
    session = await get_session(config)
    app_id = app_id or config.get('external_app_id')
    asp_id = asp_id or config.get('asp_id')

    provisioning_session_id: Optional[ResourceId] = await session.createDownlinkPullProvisioningSession(
        ApplicationId(app_id),
        ApplicationId(asp_id) if asp_id else None)
    
    if provisioning_session_id is None:
        raise HTTPException(status_code=400, detail="Failed to create a new provisioning session")
        
    return {"provisioning_session_id": provisioning_session_id}

"""
Endpoint: Fetch all provisioning sessions
HTTP Method: GET
Path: /fetch_all_sessions
Description: This endpoint will a list of all provisioning sessions.
"""
@app.get("/fetch_all_sessions")
async def get_all_sessions():
    session = await get_session(config)
    session_ids = await session.provisioningSessionIds() 
    return {"session_ids": list(session_ids)}

"""
Endpoint: Remove all provisioning sessions
HTTP Method: DELETE
Path: /remove_all_sessions
Description: This endpoint will remove all provisioning sessions from the memory.
"""
@app.delete("/remove_all_sessions")
async def remove_all_sessions():    
    session = await get_session(config)
    session_ids = await session.provisioningSessionIds()

    for session_id in session_ids:
        result = await session.provisioningSessionDestroy(session_id)
        if result is None:
            raise HTTPException(status_code=404, detail=f"Provisioning Session {session_id} not found")
        if not result:
            raise HTTPException(status_code=500, detail=f"Failed to remove session {session_id}")
    return {"message": "All provisioning sessions were destroyed"}


"""
Endpoint: Delete Provisioning Session
HTTP Method: DELETE
Path: /delete_session/{provisioning_session_id}
Description: This endpoint will delete a particular provisioning session with all its resources.
"""
@app.delete("/delete_session/{provisioning_session_id}")
async def cmd_delete_session(provisioning_session_id: str, config: Configuration = Depends(get_config)):
    session = await get_session(config)
    result = await session.provisioningSessionDestroy(provisioning_session_id)
    
    if result is None:
        raise HTTPException(status_code=404, detail=f"Provisioning Session {provisioning_session_id} not found")
    
    if not result:
        raise HTTPException(status_code=500, detail=f"Failed to destroy Provisioning Session {provisioning_session_id}")
    
    return JSONResponse(content={"message": f"Provisioning Session {provisioning_session_id} and all its resources were destroyed"}, status_code=200)

"""
Endpoint: Create Content Hosting Configuration from JSON data example
HTTP Method: POST
Path: /set_stream/{provisioning_session_id}
Description: This endpoint will add Content hosting configuration to particular provisioning session, taking JSON example data.
"""
@app.post("/set_stream/{provisioning_session_id}")
async def set_stream(provisioning_session_id: str, config: Configuration = Depends(get_config)):
    session = await get_session(config)
    json_path = "examples/ContentHostingConfiguration_Llama-Drama_pull-ingest.json"
    with open(json_path, 'r') as f:
        chc = json.load(f)
    
    old_chc = await session.contentHostingConfigurationGet(provisioning_session_id)
    
    if old_chc is None:
        result = await session.contentHostingConfigurationCreate(provisioning_session_id, chc)
    else:
        for dc in chc['distributionConfigurations']:
            for strip_field in ['canonicalDomainName', 'baseURL']:
                if strip_field in dc:
                    del dc[strip_field]
        result = await session.contentHostingConfigurationUpdate(provisioning_session_id, chc)

    if not result:
            return JSONResponse(content={"message": f"Failed to set hosting for provisioning session {provisioning_session_id}"}, status_code=400)
        
    return JSONResponse(content={"message": f"Hosting set for provisioning session {provisioning_session_id}"}, status_code=200)

"""
Endpoint: Retrieve all provisioning sessions details
HTTP Method: GET
Path: /details
Description: This endpoint will return all details for all active provisioning sessions
"""
async def get_session_details(session, ps_id):
    details = {"Certificates": {}}
    certs = await session.certificateIds(ps_id)

    for cert_id in certs:
        try:
            cert = await session.certificateGet(ps_id, cert_id)
            details["Certificates"][cert_id] = cert if cert else "Certificate not yet uploaded"
        except Exception as err:
            details["Certificates"][cert_id] = f"Certificate not available: {str(err)}"

    chc = await session.contentHostingConfigurationGet(ps_id)
    details["ContentHostingConfiguration"] = chc if chc else "Not defined"

    crc = await session.consumptionReportingConfigurationGet(ps_id)
    details["ConsumptionReportingConfiguration"] = crc if crc else "Not defined"

    pt_ids = await session.policyTemplateIds(ps_id)
    details["PolicyTemplates"] = {}
    for pt_id in pt_ids:
        pt = await session.policyTemplateGet(ps_id, pt_id)
        details["PolicyTemplates"][pt_id] = pt if pt else "PolicyTemplate not found"

    mrc_ids = await session.metricsReportingConfigurationIds(ps_id)
    details["MetricsReportingConfigurations"] = {}
    for mrc_id in mrc_ids:
        mrc = await session.metricsReportingConfigurationGet(ps_id, mrc_id)
        details["MetricsReportingConfigurations"][mrc_id] = mrc if mrc else "MetricsReportingConfiguration not found"

    return ps_id, details

@app.get("/details")
async def get_provisioning_session_details():
    session = await get_session(config)
    provisioning_session_ids = await session.provisioningSessionIds()

    tasks = [get_session_details(session, ps_id) for ps_id in provisioning_session_ids]
    details = await asyncio.gather(*tasks)

    return JSONResponse(content={"Details": dict(details)})

"""
Endpoint: Set certificate for provisioning session
HTTP Method: POST
Path: /certificate/{provisioning_session_id}
Description: This endpoint will set a certificate for a particular provisioning session.
"""
@app.post("/certificate/{provisioning_session_id}")
async def new_certificate(provisioning_session_id: str, csr: bool = Query(False), extra_domain_names: str = Query(None)):
    config = Configuration()
    session = await get_session(config)
    cert_id = None
    try:
        if csr:
            result = await session.certificateNewSigningRequest(provisioning_session_id, extra_domain_names=extra_domain_names)
            if result is None:
                raise HTTPException(status_code=400, detail='Failed to reserve certificate')
            cert_id, csr_data = result
            return {"certificate_id": cert_id, "csr": csr_data}
        else:
            cert_id = await session.createNewCertificate(provisioning_session_id, extra_domain_names=extra_domain_names)
            if cert_id is None:
                raise HTTPException(status_code=400, detail='Failed to create certificate')
        return {"certificate_id": cert_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/list_certificate_ids/{provisioning_session_id}")
async def list_certificate_ids(provisioning_session_id: str):
    config = Configuration()
    session = await get_session(config)
    try:
        cert_ids = await session.certificateIds(provisioning_session_id)
        if cert_ids is None:
            raise HTTPException(status_code=404, detail="No certificates found for the provided provisioning session ID")
        return {"certificate_ids": cert_ids}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
Endpoint: Show certificate for provisioning session
HTTP Method: GET
Path: /show_certificate/{provisioning_session_id}/{certificate_id}
Description: This endpoint will show a certificate for a particular provisioning session.
"""
@app.get("/show_certificate/{provisioning_session_id}/{certificate_id}")
async def show_certificate(provisioning_session_id: str, certificate_id: str):
    session = await get_session(config)
    cert = await session.certificateGet(provisioning_session_id, certificate_id)
    if cert is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert

"""
Endpoint: Show protocol for provisioning session
HTTP Method: GET
Path: /show_protocol/{provisioning_session_id}
Description: This endpoint will show the protocol for a particular provisioning session.
"""
@app.get("/show_protocol/{provisioning_session_id}")
async def show_protocol(provisioning_session_id: str):

    session = await get_session(config)
    protocols = await session.provisioningSessionProtocols(provisioning_session_id)
    
    if protocols is None:
        raise HTTPException(status_code=404, detail=f"Failed to fetch the content protocols for provisioning session {provisioning_session_id}")
        
    protocol_data = {"provisioning_session": provisioning_session_id}

    if 'downlinkIngestProtocols' in protocols:
        protocol_data['Downlink'] = [proto["termIdentifier"] for proto in protocols['downlinkIngestProtocols']]
    else:
        protocol_data['Downlink'] = "No downlink capability"

    if 'uplinkEgestProtocols' in protocols:
        protocol_data['Uplink'] = [proto["termIdentifier"] for proto in protocols['uplinkEgestProtocols']]
    else:
        protocol_data['Uplink'] = "No uplink capability"

    if 'geoFencingLocatorTypes' in protocols:
        protocol_data['Geo-fencing'] = protocols['geoFencingLocatorTypes']
    else:
        protocol_data['Geo-fencing'] = "No geo-fencing capability"

    return protocol_data

"""
Endpoint: Set consumption reporting for provisioning session
HTTP Method: POST
Path: /set_consumption/{provisioning_session_id}
Description: This endpoint will set consumption reporting for a particular provisioning session.
"""
@app.post("/set_consumption/{provisioning_session_id}")
async def set_consumption(provisioning_session_id: str, crc: ConsumptionReportingConfiguration):
    session = await get_session(config)
    result = await session.setOrUpdateConsumptionReporting(provisioning_session_id, crc)
    if result:
        return {"message": "Consumption reporting parameters set"}
    raise HTTPException(status_code=400, detail="Failed to set consumption reporting parameters")

"""
Endpoint: Show consumption reporting for provisioning session
HTTP Method: GET
Path: /show_consumption/{provisioning_session_id}
Description: This endpoint will retrieve consumption reporting data for a particular provisioning session.
"""
@app.get("/show_consumption/{provisioning_session_id}")
async def show_consumption(provisioning_session_id: str):
    session = await get_session(config)
    crc = await session.consumptionReportingConfigurationGet(provisioning_session_id)
    if crc is None:
        return {"message": "No consumption reporting configured"}
    return {"Consumption Reporting": crc}

"""
Endpoint: Delete consumption reporting for provisioning session
HTTP Method: DELETE
Path: /del_consumption/{provisioning_session_id}
Description: This endpoint will remove consumption reporting for a particular provisioning session.
"""
@app.delete("/del_consumption/{provisioning_session_id}")
async def del_consumption(provisioning_session_id: str):
    session = await get_session(config)
    result = await session.consumptionReportingConfigurationDelete(provisioning_session_id)
    if result:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=400, detail="No consumption reporting to remove")

"""
Endpoint: Create dynamic policy for provisioning session
HTTP Method: POST
Path: /create_policy_template/{provisioning_session_id}
Description: This endpoint will create a dynamic policy for a particular provisioning session.
"""
@app.post("/create_policy_template/{provisioning_session_id}")
async def create_policy_template(provisioning_session_id: str, request: Request):

    session = await get_session(config)
    request_body = await request.body()

    try:
        policy_template = PolicyTemplate.fromJSON(request_body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing policy template data: {str(e)}")

    policy_template_id = await session.policyTemplateCreate(provisioning_session_id, policy_template)

    if policy_template_id is not None:
        return {"policy_template_id": policy_template_id}
    else:
        raise HTTPException(status_code=400, detail="Addition of PolicyTemplate to provisioning session failed!")
    
"""
Endpoint: Retrieve list policy template IDs for provisioning session
HTTP Method: GET
Path: /list_policy_template_ids/{provisioning_session_id}
Description: This endpoint will retrieve a list of policy template IDs for a particular provisioning session.
"""
@app.get("/list_policy_template_ids/{provisioning_session_id}")
async def list_policy_template_ids(provisioning_session_id: str):
    provisionig_session_url = f"{OPTIONS_ENDPOINT}/{provisioning_session_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(provisionig_session_url)
            response.raise_for_status() 
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error when listing policy template IDs: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Connection error to M1 interface")

    all_data = response.json()
    policy_template_ids = all_data.get("policyTemplateIds")
    if not policy_template_ids:
        raise HTTPException(status_code=404, detail="No PolicyTemplate found")

    return policy_template_ids    

    
"""
Endpoint: Retrieve dynamic policy for provisioning session
HTTP Method: GET
Path: /show_policy_template/{provisioning_session_id}/{policy_template_id}
Description: This endpoint will retrieve a dynamic policy for a particular provisioning session.
"""
@app.get("/show_policy_template/{provisioning_session_id}/{policy_template_id}")
async def show_policy_template(provisioning_session_id: str, policy_template_id: str):
    
    session = await get_session(config)    
    policy_template: Optional[PolicyTemplate] = await session.policyTemplateGet(provisioning_session_id, policy_template_id)
    if policy_template is None:
        raise HTTPException(status_code=404, detail="PolicyTemplate not found")
    
    return policy_template


"""
Endpoint: Delete dynamic policy for provisioning session
HTTP Method: DELETE
Path: /delete_policy_template/{provisioning_session_id}/{policy_template_id}
Description: This endpoint will remove a dynamic policy for a particular provisioning session.
"""
@app.delete("/delete_policy_template/{provisioning_session_id}/{policy_template_id}")
async def delete_policy_template(provisioning_session_id: str, policy_template_id: str):

    session = await get_session(config)
    deletion: bool = await session.policyTemplateDelete(provisioning_session_id, policy_template_id)
    
    if deletion:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="PolicyTemplate not found or could not be deleted")
    
"""
Endpoint: Create metrics reporting for provisioning session
HTTP Method: POST
Path: /create_metrics/{provisioning_session_id}
Description: This endpoint will create metrics reporting for a particular provisioning session.
"""
@app.post("/create_metrics/{provisioning_session_id}")
async def create_metrics(provisioning_session_id: str, request: Request):
    
    session = await get_session(config)
    request_body = await request.body()
    
    try:
        metrics_reporting_configuration = MetricsReportingConfiguration.fromJSON(request_body)

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing metrics reporting data: {str(e)}")
    
    metrics_reporting_configuration_id = await session.metricsReportingConfigurationCreate(provisioning_session_id, metrics_reporting_configuration)

    if metrics_reporting_configuration_id is not None:
        return {"metrics_reporting_configuration_id": metrics_reporting_configuration_id}
    else:
        raise HTTPException(status_code=400, detail="Addition of MetricsReportingConfiguration to provisioning session failed!")
    
"""
Endpoint: Retrieve metrics reporting for provisioning session
HTTP Method: GET
Path: /show_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}
Description: This endpoint will retrieve metrics reporting data for a particular provisioning session.
"""
@app.get("/show_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}")
async def show_metrics(provisioning_session_id: str, metrics_reporting_configuration_id: str):
    
    session = await get_session(config)
    metrics_reporting_configuration: Optional[MetricsReportingConfiguration] = await session.metricsReportingConfigurationGet(provisioning_session_id, metrics_reporting_configuration_id)
    if metrics_reporting_configuration is None:
        raise HTTPException(status_code=404, detail="MetricsReportingConfiguration not found")
    
    return metrics_reporting_configuration
  
"""
Endpoint: Update metrics reporting for provisioning session
HTTP Method: PUT
Path: /update_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}
Description: This endpoint will update metrics reporting for a particular provisioning session.
"""
@app.put("/update_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}")
async def update_metrics(provisioning_session_id: str, metrics_reporting_configuration_id: str, request: Request):
    
    session = await get_session(config)
    request_body = await request.body()
    
    try:
        metrics_reporting_configuration = MetricsReportingConfiguration.fromJSON(request_body)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing metrics reporting data: {str(e)}")
    
    result = await session.metricsReportingConfigurationUpdate(provisioning_session_id, metrics_reporting_configuration_id, metrics_reporting_configuration)
    
    if result is not None:
        return Response(status_code=200)
    else:
        raise HTTPException(status_code=404, detail="MetricsReportingConfiguration not found or could not be updated")
    
"""
Endpoint: Delete metrics reporting for provisioning session
HTTP Method: DELETE
Path: /delete_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}
Description: This endpoint will remove metrics reporting for a particular provisioning session.
"""
@app.delete("/delete_metrics/{provisioning_session_id}/{metrics_reporting_configuration_id}")
async def delete_metrics(provisioning_session_id: str, metrics_reporting_configuration_id: str):
    
    session = await get_session(config)
    deletion: bool = await session.metricsReportingConfigurationDelete(provisioning_session_id, metrics_reporting_configuration_id)
    
    if deletion:
        return Response(status_code=204)
    else:
        raise HTTPException(status_code=404, detail="MetricsReportingConfiguration not found or could not be deleted")
    
"""
Endpoint: Retrieve list metrics reporting IDs for provisioning session
HTTP Method: GET
Path: /list_metrics_ids/{provisioning_session_id}
Description: This endpoint will retrieve a list of metrics reporting IDs for a particular provisioning session.
"""
@app.get("/list_metrics_ids/{provisioning_session_id}")
async def list_metrics_ids(provisioning_session_id: str):
    provisionig_session_url = f"{OPTIONS_ENDPOINT}/{provisioning_session_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(provisionig_session_url)
            response.raise_for_status() 
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Error when listing metrics IDs: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail="Connection error to M1 interface")

    all_data = response.json()
    metrics_ids = all_data.get("metricsReportingConfigurationIds")
    if not metrics_ids:
        raise HTTPException(status_code=404, detail="No MetricsReportingConfiguration found")

    return metrics_ids

"""
Endpoint: Connection checker
HTTP Method: GET
Path: /connection_checker
Description: This endpoint will check the connection to the M1 interface sending an OPTIONS request.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/connection_checker")
async def connection_checker():
    try:
        response = requests.options(OPTIONS_ENDPOINT)
        if response.status_code == 204:
            return {"status": "STABLE"}
        else:
            return {"status": "UNSTABLE"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/policy_template_checker/{provisioning_session_id}")
async def policy_template_checker(provisioning_session_id: str):
    policy_templates_url = f"{OPTIONS_ENDPOINT}/{provisioning_session_id}/policy-templates"
    try:
        response = requests.options(policy_templates_url)
        if response.status_code == 204 and 'POST' in response.headers['allow']:
            return {"enabled": True}
        return {"enabled": False}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
