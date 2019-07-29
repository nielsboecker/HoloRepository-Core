package openapi

import "strings"

// ParseQueryIDs - parse queries for ids sent via HTTP
func ParseQueryIDs(query string) []string {
	ids := strings.Split(query, ",")
	if len(ids) > 1 && ids[len(ids)-1] == "" {
		ids = ids[:len(ids)-1]
	}
	return ids
}
