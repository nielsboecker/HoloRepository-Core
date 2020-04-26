/**
 * Range for Blob Service Operations.
 * @see https://docs.microsoft.com/en-us/rest/api/storageservices/specifying-the-range-header-for-blob-service-operations
 *
 * @export
 * @interface Range
 */
export interface Range {
    /**
     * StartByte, larger than or equal 0.
     *
     * @type {string}
     * @memberof Range
     */
    offset: number;
    /**
     * Optional. Count of bytes, larger than 0.
     * If not provided, will return bytes from offset to the end.
     *
     * @type {string}
     * @memberof Range
     */
    count?: number;
}
/**
 * Generate a range string. For example:
 *
 * "bytes=255-" or "bytes=0-511"
 *
 * @export
 * @param {Range} iRange
 * @returns {string}
 */
export declare function rangeToString(iRange: Range): string;
//# sourceMappingURL=Range.d.ts.map