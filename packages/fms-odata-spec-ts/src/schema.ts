/**
 * Schema modification (DDL) types for the FileMaker OData API.
 *
 * @see docs/10-schema-modification.md
 */

/** FileMaker field types for table creation. */
export type FMFieldType =
  | 'NUMERIC'
  | 'DECIMAL'
  | 'INT'
  | 'DATE'
  | 'TIME'
  | 'TIMESTAMP'
  | 'VARCHAR'
  | 'CHARACTER VARYING'
  | 'BLOB'
  | 'VARBINARY'
  | 'LONGVARBINARY'
  | 'BINARY VARYING';

/** Default value expressions for fields. */
export type FMFieldDefault =
  | 'USER'
  | 'USERNAME'
  | 'CURRENT_USER'
  | 'CURRENT_DATE'
  | 'CURDATE'
  | 'CURRENT_TIME'
  | 'CURTIME'
  | 'CURRENT_TIMESTAMP'
  | 'CURTIMESTAMP'
  | string;

/** Field definition for table creation or adding fields. */
export interface FMFieldDefinition {
  /** Field name. Required. */
  name: string;
  /** Field type. Required. May include length: "VARCHAR(200)" or repetitions: "INT[4]". */
  type: string;
  /** Whether the field is a primary key. Default: false. */
  primary?: boolean;
  /** Whether the field requires unique values. Default: false. */
  unique?: boolean;
  /** Whether the field allows null values. Default: true. */
  nullable?: boolean;
  /** Whether the field is a global field. Default: false. */
  global?: boolean;
  /** Default value expression. */
  default?: FMFieldDefault;
  /** Relative path for secure external storage (BLOB fields only). */
  externalSecurePath?: string;
}

/** Parameters for creating a table. */
export interface CreateTableParams {
  /** Table name. */
  tableName: string;
  /** Field definitions. */
  fields: FMFieldDefinition[];
}

/** Parameters for adding fields to an existing table. */
export interface AddFieldsParams {
  /** Table name. */
  tableName: string;
  /** Field definitions to add. */
  fields: FMFieldDefinition[];
}

/** All supported field types. */
export const FIELD_TYPES: FMFieldType[] = [
  'NUMERIC', 'DECIMAL', 'INT', 'DATE', 'TIME', 'TIMESTAMP',
  'VARCHAR', 'CHARACTER VARYING', 'BLOB', 'VARBINARY', 'LONGVARBINARY', 'BINARY VARYING',
];

/** All supported default value expressions. */
export const FIELD_DEFAULTS: FMFieldDefault[] = [
  'USER', 'USERNAME', 'CURRENT_USER',
  'CURRENT_DATE', 'CURDATE',
  'CURRENT_TIME', 'CURTIME',
  'CURRENT_TIMESTAMP', 'CURTIMESTAMP',
];

/** Parse a field type string to extract the base type, length, and repetitions. */
export function parseFieldType(typeStr: string): {
  baseType: string;
  length?: number;
  repetitions?: number;
} {
  // Match patterns like "VARCHAR(200)", "INT[4]", "VARCHAR(200)[4]"
  const lengthMatch = typeStr.match(/\((\d+)\)/);
  const repMatch = typeStr.match(/\[(\d+)\]/);
  const baseType = typeStr.replace(/\(.*?\)/, '').replace(/\[.*?\]/, '').trim();
  return {
    baseType,
    length: lengthMatch ? parseInt(lengthMatch[1], 10) : undefined,
    repetitions: repMatch ? parseInt(repMatch[1], 10) : undefined,
  };
}
