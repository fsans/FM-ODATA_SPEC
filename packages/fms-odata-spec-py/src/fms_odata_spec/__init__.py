"""fms-odata-spec - Python types and spec definitions for the FileMaker Server OData API.

This package mirrors the TypeScript package ``@fms-odata/spec-ts`` (see
https://github.com/fsans/fms-odata-spec). It is types + pure helpers only;
there is no HTTP client and no validation framework. All models are stdlib
:dataclasses:`dataclasses <dataclasses>`.
"""

from __future__ import annotations

# Versions and feature flags
from .versions import (
    FM_VERSION_MATRIX,
    FM_VERSION_NAMES,
    ODATA_PROTOCOL_VERSION,
    FMFeatureFlags,
    FMQueryOptionFlags,
    FMVersionInfo,
    FMVersionMajor,
    FMVersionStatus,
    has_feature,
    has_query_option,
    min_version_for_feature,
)

# Authentication
from .auth import (
    FMAuthConfig,
    FMAuthHeaders,
    FMAuthScheme,
    FMAuthToken,
    FMAuthTokenProvider,
    FMBasicAuthConfig,
    FMIDAuthConfig,
    basic_auth,
    fmid_auth,
    normalize_auth_token,
)

# Endpoints
from .endpoints import (
    FM_ENDPOINTS,
    FMEndpoint,
    EndpointCategory,
    HttpMethod,
    get_endpoint,
    get_endpoints_for_version,
)

# Query options
from .query_options import (
    AggregateExpression,
    AggregateFunction,
    ApplyTransformation,
    FilterComparisonOp,
    FilterDateTimeFunction,
    FilterFunction,
    FilterLogicalOp,
    FilterNumericFunction,
    FilterStringFunction,
    GroupByExpression,
    ODataCollection,
    ODataEntity,
    OrderByClause,
    QueryOption,
    QueryParams,
    QueryResult,
    SortDirection,
    UnsupportedFilterFunction,
    UnsupportedQueryOption,
    escape_string_literal,
    format_literal,
)

# Metadata
from .metadata import (
    SYSTEM_FIELDS,
    SYSTEM_TABLES,
    EdmAction,
    EdmEntitySet,
    EdmEntityType,
    EdmEnumType,
    EdmProperty,
    FMAnnotations,
    FMBooleanAnnotations,
    FMValueAnnotations,
    FMServerVersion,
    ImmutableIdType,
    ODataMetadata,
    extract_major_version,
    extract_major_version_from_metadata,
    parse_server_version,
    parse_version_string,
)

# Scripts
from .scripts import (
    SCRIPT_ERROR_CODES,
    ScriptDescriptor,
    ScriptIdentifier,
    ScriptOptions,
    ScriptResult,
    ScriptResultEnvelope,
    ScriptScope,
    parse_script_response,
    script_path_segment,
    script_request_body,
)

# Containers
from .containers import (
    CONTAINER_BINARY_MIME_TYPES,
    ContainerBinaryMimeType,
    ContainerDownload,
    ContainerEncoding,
    ContainerUploadInput,
    FMContainerAnnotations,
    build_content_disposition,
    sniff_container_mime,
    to_base64,
)

# Batch
from .batch import (
    BatchHandle,
    BatchOpResult,
    BatchOpType,
    BatchOperation,
    BatchRequest,
    BatchResult,
    Changeset,
    generate_boundary,
)

# Webhooks
from .webhooks import (
    WebhookCreateParams,
    WebhookData,
    WebhookOperation,
    webhook_path,
)

# Schema modification (DDL)
from .schema import (
    FIELD_DEFAULTS,
    FIELD_TYPES,
    AddFieldsParams,
    CreateTableParams,
    FMFieldDefault,
    FMFieldDefinition,
    FMFieldType,
    parse_field_type,
)

# Errors
from .errors import (
    FMAuthError,
    FMNotFoundError,
    FMODataError,
    FMScriptError,
    FMValidationError,
    ODataErrorBody,
    is_fm_odata_error,
    is_fm_script_error,
)

__version__ = "0.1.0"

__all__ = [
    "__version__",
    # versions
    "FM_VERSION_MATRIX",
    "FM_VERSION_NAMES",
    "ODATA_PROTOCOL_VERSION",
    "FMFeatureFlags",
    "FMQueryOptionFlags",
    "FMVersionInfo",
    "FMVersionMajor",
    "FMVersionStatus",
    "has_feature",
    "has_query_option",
    "min_version_for_feature",
    # auth
    "FMAuthConfig",
    "FMAuthHeaders",
    "FMAuthScheme",
    "FMAuthToken",
    "FMAuthTokenProvider",
    "FMBasicAuthConfig",
    "FMIDAuthConfig",
    "basic_auth",
    "fmid_auth",
    "normalize_auth_token",
    # endpoints
    "FM_ENDPOINTS",
    "FMEndpoint",
    "EndpointCategory",
    "HttpMethod",
    "get_endpoint",
    "get_endpoints_for_version",
    # query options
    "AggregateExpression",
    "AggregateFunction",
    "ApplyTransformation",
    "FilterComparisonOp",
    "FilterDateTimeFunction",
    "FilterFunction",
    "FilterLogicalOp",
    "FilterNumericFunction",
    "FilterStringFunction",
    "GroupByExpression",
    "ODataCollection",
    "ODataEntity",
    "OrderByClause",
    "QueryOption",
    "QueryParams",
    "QueryResult",
    "SortDirection",
    "UnsupportedFilterFunction",
    "UnsupportedQueryOption",
    "escape_string_literal",
    "format_literal",
    # metadata
    "SYSTEM_FIELDS",
    "SYSTEM_TABLES",
    "EdmAction",
    "EdmEntitySet",
    "EdmEntityType",
    "EdmEnumType",
    "EdmProperty",
    "FMAnnotations",
    "FMBooleanAnnotations",
    "FMValueAnnotations",
    "FMServerVersion",
    "ImmutableIdType",
    "ODataMetadata",
    "extract_major_version",
    "extract_major_version_from_metadata",
    "parse_server_version",
    "parse_version_string",
    # scripts
    "SCRIPT_ERROR_CODES",
    "ScriptDescriptor",
    "ScriptIdentifier",
    "ScriptOptions",
    "ScriptResult",
    "ScriptResultEnvelope",
    "ScriptScope",
    "parse_script_response",
    "script_path_segment",
    "script_request_body",
    # containers
    "CONTAINER_BINARY_MIME_TYPES",
    "ContainerBinaryMimeType",
    "ContainerDownload",
    "ContainerEncoding",
    "ContainerUploadInput",
    "FMContainerAnnotations",
    "build_content_disposition",
    "sniff_container_mime",
    "to_base64",
    # batch
    "BatchHandle",
    "BatchOpResult",
    "BatchOpType",
    "BatchOperation",
    "BatchRequest",
    "BatchResult",
    "Changeset",
    "generate_boundary",
    # webhooks
    "WebhookCreateParams",
    "WebhookData",
    "WebhookOperation",
    "webhook_path",
    # schema
    "FIELD_DEFAULTS",
    "FIELD_TYPES",
    "AddFieldsParams",
    "CreateTableParams",
    "FMFieldDefault",
    "FMFieldDefinition",
    "FMFieldType",
    "parse_field_type",
    # errors
    "FMAuthError",
    "FMNotFoundError",
    "FMODataError",
    "FMScriptError",
    "FMValidationError",
    "ODataErrorBody",
    "is_fm_odata_error",
    "is_fm_script_error",
]
