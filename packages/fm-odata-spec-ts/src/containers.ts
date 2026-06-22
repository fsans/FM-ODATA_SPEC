/**
 * Container field types for the FileMaker OData API.
 *
 * @see docs/07-containers.md
 */

/** MIME types supported for binary container upload. */
export type ContainerBinaryMimeType =
  | 'image/png'
  | 'image/jpeg'
  | 'image/gif'
  | 'image/tiff'
  | 'application/pdf';

/** All supported binary MIME types. */
export const CONTAINER_BINARY_MIME_TYPES: ContainerBinaryMimeType[] = [
  'image/png',
  'image/jpeg',
  'image/gif',
  'image/tiff',
  'application/pdf',
];

/** Upload encoding mode. */
export type ContainerEncoding = 'binary' | 'base64';

/** Input for uploading container data. */
export interface ContainerUploadInput {
  /** Binary data (Blob, ArrayBuffer, or Uint8Array). */
  data: Blob | ArrayBuffer | Uint8Array;
  /** MIME type. Auto-detected from magic bytes if omitted for binary mode. */
  contentType?: string;
  /** Filename to store in the container. */
  filename?: string;
  /** Encoding mode. Default: 'binary'. */
  encoding?: ContainerEncoding;
}

/** Container download result. */
export interface ContainerDownload {
  data: Blob;
  contentType: string;
  filename?: string;
}

/** FileMaker-specific container annotations for base64 JSON body. */
export interface FMContainerAnnotations {
  '@com.filemaker.odata.Filename': string;
  '@com.filemaker.odata.ContentType': string;
  data: string; // base64-encoded
}

/**
 * Sniff the MIME type from file magic bytes.
 * Returns one of the supported binary types, or null if unrecognized.
 */
export function sniffContainerMime(bytes: Uint8Array): ContainerBinaryMimeType | null {
  if (bytes.length < 4) return null;
  // PNG: 89 50 4E 47
  if (bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) {
    return 'image/png';
  }
  // JPEG: FF D8 FF
  if (bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) {
    return 'image/jpeg';
  }
  // GIF: 47 49 46 38
  if (bytes[0] === 0x47 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x38) {
    return 'image/gif';
  }
  // TIFF: 49 49 2A 00 or 4D 4D 00 2A
  if (
    (bytes[0] === 0x49 && bytes[1] === 0x49 && bytes[2] === 0x2a && bytes[3] === 0x00) ||
    (bytes[0] === 0x4d && bytes[1] === 0x4d && bytes[2] === 0x00 && bytes[3] === 0x2a)
  ) {
    return 'image/tiff';
  }
  // PDF: 25 50 44 46
  if (bytes[0] === 0x25 && bytes[1] === 0x50 && bytes[2] === 0x44 && bytes[3] === 0x46) {
    return 'application/pdf';
  }
  return null;
}

/**
 * Build a Content-Disposition header value for container upload.
 * Uses unquoted form for ASCII, RFC 5987 for non-ASCII.
 */
export function buildContentDisposition(filename: string): string {
  // Check for non-ASCII characters
  if (/^[\x20-\x7E]+$/.test(filename)) {
    return `inline; filename=${filename}`;
  }
  // RFC 5987 for non-ASCII
  const encoded = encodeURIComponent(filename);
  return `inline; filename*=UTF-8''${encoded}`;
}

/**
 * Convert binary data to base64 string.
 * Works in both Node (Buffer) and browsers.
 */
export function toBase64(data: ArrayBuffer | Uint8Array): string {
  const bytes = data instanceof Uint8Array ? data : new Uint8Array(data);
  if (typeof Buffer !== 'undefined') {
    return Buffer.from(bytes).toString('base64');
  }
  // Browser fallback
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary);
}
