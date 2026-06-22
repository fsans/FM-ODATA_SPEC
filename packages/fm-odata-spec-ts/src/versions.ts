/**
 * FileMaker Server version identifiers and feature flags.
 *
 * @see docs/12-version-deltas.md
 */

/** FileMaker Server version major numbers. */
export type FMVersionMajor = '19' | '21' | '22' | '26' | 'future';

/** Human-readable version names. */
export const FM_VERSION_NAMES: Record<FMVersionMajor, string> = {
  '19': 'FileMaker 19.x',
  '21': 'Claris FileMaker 2023',
  '22': 'Claris FileMaker 2024',
  '26': 'Claris FileMaker 2026',
  future: 'Future / next',
};

/** Version status. */
export type FMVersionStatus = 'baseline' | 'supported' | 'current' | 'future';

/** OData protocol version implemented by FileMaker (always 4.0). */
export const ODATA_PROTOCOL_VERSION = '4.0' as const;

/** Feature flags for a specific FileMaker Server version. */
export interface FMFeatureFlags {
  serviceDocument: boolean;
  metadata: boolean;
  databaseListing: boolean;
  tableListing: boolean;
  recordCRUD: boolean;
  recordReferences: boolean;
  crossJoin: boolean;
  batch: boolean;
  scripts: boolean;
  scriptsByFMSID: boolean;
  scriptListing: boolean;
  containerBinaryUpload: boolean;
  containerBase64Upload: boolean;
  containerDownload: boolean;
  schemaModification: boolean;
  webhooks: boolean;
  webhookQueryHeaders: boolean;
  applyAggregation: boolean;
  typeCasting: boolean;
  parameterizedFilters: boolean;
  immutableIdUrls: boolean;
  aiAnnotation: boolean;
  serverVersionAnnotation: boolean;
  enrichedFMComment: boolean;
  authBasic: boolean;
  authFMID: boolean;
  authOAuth: boolean;
}

/** Query option availability for a specific version. */
export interface FMQueryOptionFlags {
  $filter: boolean;
  $select: boolean;
  $orderby: boolean;
  $top: boolean;
  $skip: boolean;
  $expand: boolean;
  $count: boolean;
  $apply: boolean;
  $search: boolean;
  $compute: boolean;
}

/** Complete version descriptor. */
export interface FMVersionInfo {
  major: FMVersionMajor;
  name: string;
  releaseYear: number | null;
  internalVersion: string;
  status: FMVersionStatus;
  features: FMFeatureFlags;
  queryOptions: FMQueryOptionFlags;
}

/**
 * Feature flag matrix across all supported versions.
 * Import this to programmatically check feature availability.
 */
export const FM_VERSION_MATRIX: Record<FMVersionMajor, FMVersionInfo> = {
  '19': {
    major: '19',
    name: 'FileMaker 19.x',
    releaseYear: null,
    internalVersion: '19.x',
    status: 'baseline',
    features: {
      serviceDocument: true, metadata: true, databaseListing: true, tableListing: true,
      recordCRUD: true, recordReferences: true, crossJoin: true, batch: true,
      scripts: true, scriptsByFMSID: false, scriptListing: false,
      containerBinaryUpload: true, containerBase64Upload: true, containerDownload: true,
      schemaModification: true, webhooks: false, webhookQueryHeaders: false,
      applyAggregation: false, typeCasting: false, parameterizedFilters: false,
      immutableIdUrls: false, aiAnnotation: false, serverVersionAnnotation: false,
      enrichedFMComment: false, authBasic: true, authFMID: false, authOAuth: false,
    },
    queryOptions: {
      $filter: true, $select: true, $orderby: true, $top: true, $skip: true,
      $expand: true, $count: true, $apply: false, $search: false, $compute: false,
    },
  },
  '21': {
    major: '21',
    name: 'Claris FileMaker 2023',
    releaseYear: 2023,
    internalVersion: '21.x',
    status: 'supported',
    features: {
      serviceDocument: true, metadata: true, databaseListing: true, tableListing: true,
      recordCRUD: true, recordReferences: true, crossJoin: true, batch: true,
      scripts: true, scriptsByFMSID: false, scriptListing: false,
      containerBinaryUpload: true, containerBase64Upload: true, containerDownload: true,
      schemaModification: true, webhooks: true, webhookQueryHeaders: false,
      applyAggregation: false, typeCasting: true, parameterizedFilters: true,
      immutableIdUrls: false, aiAnnotation: false, serverVersionAnnotation: false,
      enrichedFMComment: false, authBasic: true, authFMID: true, authOAuth: true,
    },
    queryOptions: {
      $filter: true, $select: true, $orderby: true, $top: true, $skip: true,
      $expand: true, $count: true, $apply: false, $search: false, $compute: false,
    },
  },
  '22': {
    major: '22',
    name: 'Claris FileMaker 2024',
    releaseYear: 2024,
    internalVersion: '22.x',
    status: 'supported',
    features: {
      serviceDocument: true, metadata: true, databaseListing: true, tableListing: true,
      recordCRUD: true, recordReferences: true, crossJoin: true, batch: true,
      scripts: true, scriptsByFMSID: false, scriptListing: false,
      containerBinaryUpload: true, containerBase64Upload: true, containerDownload: true,
      schemaModification: true, webhooks: true, webhookQueryHeaders: true,
      applyAggregation: true, typeCasting: true, parameterizedFilters: true,
      immutableIdUrls: false, aiAnnotation: false, serverVersionAnnotation: false,
      enrichedFMComment: false, authBasic: true, authFMID: true, authOAuth: true,
    },
    queryOptions: {
      $filter: true, $select: true, $orderby: true, $top: true, $skip: true,
      $expand: true, $count: true, $apply: true, $search: false, $compute: false,
    },
  },
  '26': {
    major: '26',
    name: 'Claris FileMaker 2026',
    releaseYear: 2026,
    internalVersion: '26.x',
    status: 'current',
    features: {
      serviceDocument: true, metadata: true, databaseListing: true, tableListing: true,
      recordCRUD: true, recordReferences: true, crossJoin: true, batch: true,
      scripts: true, scriptsByFMSID: true, scriptListing: true,
      containerBinaryUpload: true, containerBase64Upload: true, containerDownload: true,
      schemaModification: true, webhooks: true, webhookQueryHeaders: true,
      applyAggregation: true, typeCasting: true, parameterizedFilters: true,
      immutableIdUrls: true, aiAnnotation: true, serverVersionAnnotation: true,
      enrichedFMComment: true, authBasic: true, authFMID: true, authOAuth: true,
    },
    queryOptions: {
      $filter: true, $select: true, $orderby: true, $top: true, $skip: true,
      $expand: true, $count: true, $apply: true, $search: false, $compute: false,
    },
  },
  future: {
    major: 'future',
    name: 'Future / next',
    releaseYear: null,
    internalVersion: 'unknown',
    status: 'future',
    features: {
      serviceDocument: true, metadata: true, databaseListing: true, tableListing: true,
      recordCRUD: true, recordReferences: true, crossJoin: true, batch: true,
      scripts: true, scriptsByFMSID: true, scriptListing: true,
      containerBinaryUpload: true, containerBase64Upload: true, containerDownload: true,
      schemaModification: true, webhooks: true, webhookQueryHeaders: true,
      applyAggregation: true, typeCasting: true, parameterizedFilters: true,
      immutableIdUrls: true, aiAnnotation: true, serverVersionAnnotation: true,
      enrichedFMComment: true, authBasic: true, authFMID: true, authOAuth: true,
    },
    queryOptions: {
      $filter: true, $select: true, $orderby: true, $top: true, $skip: true,
      $expand: true, $count: true, $apply: true, $search: false, $compute: false,
    },
  },
};

/** Check if a feature is available in a given version. */
export function hasFeature(version: FMVersionMajor, feature: keyof FMFeatureFlags): boolean {
  return FM_VERSION_MATRIX[version]?.features[feature] ?? false;
}

/** Check if a query option is available in a given version. */
export function hasQueryOption(version: FMVersionMajor, option: keyof FMQueryOptionFlags): boolean {
  return FM_VERSION_MATRIX[version]?.queryOptions[option] ?? false;
}

/** Get the minimum version that supports a given feature. */
export function minVersionForFeature(feature: keyof FMFeatureFlags): FMVersionMajor | null {
  const order: FMVersionMajor[] = ['19', '21', '22', '26'];
  for (const v of order) {
    if (FM_VERSION_MATRIX[v].features[feature]) return v;
  }
  return null;
}
