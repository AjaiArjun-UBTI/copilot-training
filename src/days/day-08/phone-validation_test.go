package main

import "testing"

func TestValidatePhone(t *testing.T) {
	tests := []struct {
		name  string
		input string
		want  bool
	}{
		// Accepted cases
		{"+91 98765 43210", "+91 98765 43210", true},
		{"(555) 123-4567", "(555) 123-4567", true},
		{"555-123-4567", "555-123-4567", true},
		{"5551234567", "5551234567", true},
		{"+1 555 123 4567", "+1 555 123 4567", true},
		
		// Rejected cases
		{"empty string", "", false},
		{"12345", "12345", false},
		{"555-CALL-NOW", "555-CALL-NOW", false},
		{"++1 555 123 4567", "++1 555 123 4567", false},
		{"555 123 45678901234", "555 123 45678901234", false},
		{"whitespace only", "  ", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := ValidatePhone(tt.input); got != tt.want {
				t.Errorf("ValidatePhone(%q) = %v, want %v", tt.input, got, tt.want)
			}
		})
	}
}
