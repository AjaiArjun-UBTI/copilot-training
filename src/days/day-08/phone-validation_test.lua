-- Test harness for phone-validation.lua
-- Run with: lua phone-validation_test.lua

local validator = require("phone-validation")
local validatePhone = validator.validatePhone

local function test(name, input, expected)
  local result = validatePhone(input)
  local status = result == expected and "✓ PASS" or "✗ FAIL"
  print(string.format("%s: %s (input=%q, expected=%s, got=%s)", status, name, input, expected, result))
  return result == expected
end

local passed = 0
local total = 0

-- Test accepted cases
print("\n--- Accepted Cases ---")
total = total + 1; if test("Indian phone with +91", "+91 98765 43210", true) then passed = passed + 1 end
total = total + 1; if test("US phone with parentheses", "(555) 123-4567", true) then passed = passed + 1 end
total = total + 1; if test("US phone with dashes", "555-123-4567", true) then passed = passed + 1 end
total = total + 1; if test("US phone no formatting", "5551234567", true) then passed = passed + 1 end
total = total + 1; if test("International with +1", "+1 555 123 4567", true) then passed = passed + 1 end

-- Test rejected cases
print("\n--- Rejected Cases ---")
total = total + 1; if test("Empty string", "", false) then passed = passed + 1 end
total = total + 1; if test("Too few digits", "12345", false) then passed = passed + 1 end
total = total + 1; if test("Contains letters", "555-CALL-NOW", false) then passed = passed + 1 end
total = total + 1; if test("Double plus sign", "++1 555 123 4567", false) then passed = passed + 1 end
total = total + 1; if test("Too many digits", "555 123 45678901234", false) then passed = passed + 1 end
total = total + 1; if test("Whitespace only", "  ", false) then passed = passed + 1 end

-- Edge case: type coercion (Lua will accept non-strings due to implicit coercion, but we check type)
print("\n--- Type Handling ---")
total = total + 1
local result = validatePhone(12345)
print(string.format("%s: Number input (expected false, got %s)", result == false and "✓ PASS" or "✗ FAIL", result))
if result == false then passed = passed + 1 end

print(string.format("\n%d/%d tests passed", passed, total))
if passed == total then
  print("All tests passed! ✓")
else
  print(string.format("Some tests failed: %d failures", total - passed))
end
