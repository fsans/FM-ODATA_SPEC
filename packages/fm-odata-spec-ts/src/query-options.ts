/**
 * Query option types for the FileMaker OData API.
 *
 * @see docs/03-query-options.md
 */

/** Supported system query options. */
export type QueryOption =
  | '$filter'
  | '$select'
  | '$orderby'
  | '$top'
  | '$skip'
  | '$expand'
  | '$count'
  | '$apply'
  | '$search'
  | '$compute';

/** Query options not supported by FileMaker. */
export type UnsupportedQueryOption = '$search' | '$compute';

/** Supported $filter comparison operators. */
export type FilterComparisonOp = 'eq' | 'ne' | 'gt' | 'ge' | 'lt' | 'le';

/** Supported $filter logical operators. */
export type FilterLogicalOp = 'and' | 'or' | 'not';

/** Supported $filter string functions. */
export type FilterStringFunction =
  | 'startswith'
  | 'endswith'
  | 'contains'
  | 'length'
  | 'tolower'
  | 'toupper'
  | 'trim'
  | 'substring'
  | 'indexof'
  | 'concat';

/** Supported $filter date/time functions. */
export type FilterDateTimeFunction =
  | 'year'
  | 'month'
  | 'day'
  | 'hour'
  | 'minute'
  | 'second'
  | 'date'
  | 'time';

/** Supported $filter numeric functions. */
export type FilterNumericFunction = 'round' | 'floor' | 'ceiling';

/** All supported $filter built-in functions. */
export type FilterFunction =
  | FilterStringFunction
  | FilterDateTimeFunction
  | FilterNumericFunction;

/** Explicitly unsupported $filter functions. */
export type UnsupportedFilterFunction =
  | 'fractionalseconds'
  | 'isof'
  | 'geo.distance'
  | 'geo.length'
  | 'geo.intersects'
  | 'any'
  | 'all';

/** Sort direction for $orderby. */
export type SortDirection = 'asc' | 'desc';

/** $orderby clause. */
export interface OrderByClause {
  field: string;
  direction?: SortDirection;
}

/** $apply aggregate function. */
export type AggregateFunction = 'sum' | 'min' | 'max' | 'average' | 'countdistinct';

/** $apply aggregate expression. */
export interface AggregateExpression {
  field: string;
  function: AggregateFunction;
  alias: string;
  /** Optional offset added to the field value before aggregation. */
  add?: number;
}

/** $apply groupby expression. */
export interface GroupByExpression {
  fields: string[];
  aggregate?: AggregateExpression[];
}

/** $apply transformation (either aggregate-only or groupby with optional aggregate). */
export type ApplyTransformation =
  | { type: 'aggregate'; expressions: AggregateExpression[] }
  | { type: 'groupby'; expression: GroupByExpression };

/** Query parameters for a record query. */
export interface QueryParams {
  $filter?: string;
  $select?: string[];
  $orderby?: OrderByClause[];
  $top?: number;
  $skip?: number;
  $expand?: string | string[];
  $count?: boolean;
  $apply?: string;
}

/** Standard OData response envelope for a collection. */
export interface ODataCollection<T> {
  '@odata.context': string;
  '@odata.count'?: number;
  value: T[];
  '@odata.nextLink'?: string;
}

/** Standard OData response envelope for a single entity. */
export type ODataEntity<T> = {
  '@odata.context': string;
  '@odata.etag'?: string;
} & T;

/** Query result (simplified). */
export interface QueryResult<T> {
  value: T[];
  count?: number;
  nextLink?: string;
}

/**
 * Escape single quotes in OData string literals.
 * OData requires 'O''Brien' (doubled quotes) for names containing apostrophes.
 */
export function escapeStringLiteral(s: string): string {
  return s.replace(/'/g, "''");
}

/**
 * Format a primitive value as an OData literal for use in $filter.
 * Strings are single-quoted with escaped internal quotes.
 * Numbers, booleans are raw. Dates are ISO-8601.
 */
export function formatLiteral(value: string | number | boolean | Date): string {
  if (typeof value === 'string') {
    return `'${escapeStringLiteral(value)}'`;
  }
  if (typeof value === 'number') {
    return String(value);
  }
  if (typeof value === 'boolean') {
    return value ? 'true' : 'false';
  }
  if (value instanceof Date) {
    return value.toISOString().replace(/\.\d{3}Z$/, 'Z');
  }
  return String(value);
}
