package main

import (
	"regexp"
	"strings"
	"unicode"
)

var (
	acceptedExamples = []string{"+91 98765 43210", "(555) 123-4567", "555-123-4567", "5551234567", "+1 555 123 4567"}
	rejectedExamples = []string{"", "12345", "555-CALL-NOW", "++1 555 123 4567", "555 123 45678901234", "  "}
)

// ValidatePhone accepts an optional leading +, then 10 to 15 digits, with spaces, dashes, dots and parentheses allowed between them.
func ValidatePhone(input string) bool {
	trimmed := strings.TrimSpace(input)
	
	// Check pattern: optional +, followed by digits, spaces, dashes, dots, parentheses
	pattern := `^\+?[\d\s().\-]+$`
	matched, err := regexp.MatchString(pattern, trimmed)
	if err != nil || !matched {
		return false
	}
	
	// Extract digits only
	digits := ""
	for _, ch := range trimmed {
		if unicode.IsDigit(ch) {
			digits += string(ch)
		}
	}
	
	return len(digits) >= 10 && len(digits) <= 15
}
