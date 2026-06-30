"""Endpoint definitions for the FileMaker OData API.

Mirrors ``src/endpoints.ts`` from ``@fms-odata/spec-ts``.

@see docs/02-endpoints.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional

from .versions import FMVersionMajor

__all__ = [
    "HttpMethod",
    "EndpointCategory",
    "FMEndpoint",
    "FM_ENDPOINTS",
    "get_endpoint",
    "get_endpoints_for_version",
]

#: HTTP methods used by the OData API.
HttpMethod = Literal["GET", "POST", "PATCH", "PUT", "DELETE"]

#: Endpoint category.
EndpointCategory = Literal[
    "discovery",
    "metadata",
    "query",
    "crud",
    "batch",
    "scripts",
    "containers",
    "schema",
    "webhooks",
]


@dataclass(frozen=True)
class FMEndpoint:
    """Endpoint descriptor."""

    #: Endpoint identifier (e.g. ``"getRecords"``, ``"runScript"``).
    id: str
    #: HTTP method.
    method: HttpMethod
    #: URL path template relative to ``/fmi/odata/v4``. Use ``{param}`` for path params.
    path: str
    #: Human-readable description.
    description: str
    #: Minimum FileMaker Server version that supports this endpoint.
    min_version: FMVersionMajor
    #: Endpoint category.
    category: EndpointCategory
    #: Additional HTTP methods that also work for this endpoint.
    also_methods: List[HttpMethod] = field(default_factory=list)
    #: Content-Type required for the request body.
    content_type: Optional[str] = None
    #: Query options supported by this endpoint.
    query_options: List[str] = field(default_factory=list)


#: All OData API endpoints.
FM_ENDPOINTS: List[FMEndpoint] = [
    # Discovery & metadata
    FMEndpoint(id="getDatabases", method="GET", path="/",
               description="List all hosted databases", min_version="19",
               category="discovery"),
    FMEndpoint(id="getTables", method="GET", path="/{database}",
               description="List tables in a database", min_version="19",
               category="discovery"),
    FMEndpoint(id="getSystemTable", method="GET", path="/{database}/{systemTable}",
               description="Get system table values", min_version="19",
               category="discovery"),
    FMEndpoint(id="getMetadata", method="GET", path="/{database}/$metadata",
               description="Get CSDL/EDMX metadata", min_version="19",
               category="metadata"),

    # Query
    FMEndpoint(id="getRecords", method="GET", path="/{database}/{table}",
               description="Query records from a table", min_version="19",
               category="query",
               query_options=["$filter", "$select", "$orderby", "$top", "$skip",
                              "$expand", "$count", "$apply"]),
    FMEndpoint(id="getRecord", method="GET", path="/{database}/{table}({key})",
               description="Get a single record", min_version="19",
               category="query", query_options=["$select"]),
    FMEndpoint(id="getFieldValue", method="GET",
               path="/{database}/{table}({key})/{field}",
               description="Get a single field value", min_version="19",
               category="query"),
    FMEndpoint(id="getBinaryFieldValue", method="GET",
               path="/{database}/{table}({key})/{field}/$value",
               description="Get binary value of a container field", min_version="19",
               category="query"),
    FMEndpoint(id="navigateRelated", method="GET",
               path="/{database}/{table}({key})/{relatedTable}",
               description="Navigate to related table records", min_version="19",
               category="query", query_options=["$expand", "$select"]),

    # CRUD
    FMEndpoint(id="createRecord", method="POST", path="/{database}/{table}",
               description="Create a new record", min_version="19",
               category="crud", content_type="application/json",
               also_methods=["PUT"]),
    FMEndpoint(id="updateRecord", method="PATCH",
               path="/{database}/{table}({key})",
               description="Update a record", min_version="19",
               category="crud", content_type="application/json",
               also_methods=["PUT"]),
    FMEndpoint(id="deleteRecord", method="DELETE",
               path="/{database}/{table}({key})",
               description="Delete a record", min_version="19",
               category="crud"),
    FMEndpoint(id="updateRecordRef", method="POST",
               path="/{database}/{table}({key})/{relatedTable}/$ref",
               description="Add/replace a record reference", min_version="19",
               category="crud", content_type="application/json",
               also_methods=["PATCH", "PUT", "DELETE"]),

    # Batch
    FMEndpoint(id="batch", method="POST", path="/{database}/$batch",
               description="Perform batch operations", min_version="19",
               category="batch", content_type="multipart/mixed"),

    # Scripts
    FMEndpoint(id="runScript", method="POST",
               path="/{database}/Script.{scriptName}",
               description="Run a FileMaker script by name", min_version="19",
               category="scripts", content_type="application/json"),
    FMEndpoint(id="runScriptById", method="POST",
               path="/{database}/Script.FMSID:{scriptId}",
               description="Run a FileMaker script by FMSID", min_version="26",
               category="scripts", content_type="application/json"),

    # Containers
    FMEndpoint(id="updateContainerBinary", method="PATCH",
               path="/{database}/{table}({key})/{containerField}",
               description="Update a container field with binary data",
               min_version="19", category="containers"),
    FMEndpoint(id="updateContainerBase64", method="PATCH",
               path="/{database}/{table}({key})",
               description="Update container fields with base64-encoded data",
               min_version="19", category="containers",
               content_type="application/json", also_methods=["PUT"]),

    # Schema
    FMEndpoint(id="createTable", method="POST",
               path="/{database}/FileMaker_Tables",
               description="Create a new table", min_version="19",
               category="schema", content_type="application/json"),
    FMEndpoint(id="addFields", method="PATCH",
               path="/{database}/FileMaker_Tables('{tableName}')",
               description="Add fields to a table", min_version="19",
               category="schema", content_type="application/json",
               also_methods=["PUT"]),
    FMEndpoint(id="deleteTable", method="DELETE",
               path="/{database}/FileMaker_Tables('{tableName}')",
               description="Delete a table", min_version="19", category="schema"),
    FMEndpoint(id="deleteField", method="DELETE",
               path="/{database}/FileMaker_Tables('{tableName}')/{fieldName}",
               description="Delete a field from a table", min_version="19",
               category="schema"),
    FMEndpoint(id="createIndex", method="POST",
               path="/{database}/FileMaker_Indexes",
               description="Create a field index", min_version="19",
               category="schema", content_type="application/json"),
    FMEndpoint(id="deleteIndex", method="DELETE",
               path="/{database}/FileMaker_Indexes('{indexName}')",
               description="Delete an index", min_version="19", category="schema"),

    # Webhooks
    FMEndpoint(id="createWebhook", method="POST",
               path="/{database}/Webhook.Add",
               description="Create a webhook", min_version="21",
               category="webhooks", content_type="application/json"),
    FMEndpoint(id="deleteWebhook", method="POST",
               path="/{database}/Webhook.Remove",
               description="Delete a webhook", min_version="21",
               category="webhooks", content_type="application/json"),
    FMEndpoint(id="getWebhook", method="POST",
               path="/{database}/Webhook.Get",
               description="Get specified webhook data", min_version="21",
               category="webhooks", content_type="application/json"),
    FMEndpoint(id="getAllWebhooks", method="POST",
               path="/{database}/Webhook.GetAll",
               description="Get all webhooks", min_version="21",
               category="webhooks", content_type="application/json"),
    FMEndpoint(id="invokeWebhook", method="POST",
               path="/{database}/Webhook.Invoke",
               description="Manually invoke a webhook", min_version="21",
               category="webhooks", content_type="application/json"),
]

#: Ordered list of concrete (non-future) versions, oldest first.
_VERSION_ORDER = ("19", "21", "22", "26")


def get_endpoint(id: str) -> Optional[FMEndpoint]:
    """Find an endpoint by ID."""
    for e in FM_ENDPOINTS:
        if e.id == id:
            return e
    return None


def get_endpoints_for_version(version: FMVersionMajor) -> List[FMEndpoint]:
    """Get all endpoints available in a given version.

    Unknown / future versions return every endpoint.
    """
    if version not in _VERSION_ORDER:
        return list(FM_ENDPOINTS)
    idx = _VERSION_ORDER.index(version)
    return [e for e in FM_ENDPOINTS if _VERSION_ORDER.index(e.min_version) <= idx]
