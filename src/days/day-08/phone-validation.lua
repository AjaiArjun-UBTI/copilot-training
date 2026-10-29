-- Lua implementation of phone validation

local ACCEPTED_EXAMPLES = {"+91 98765 43210", "(555) 123-4567", "555-123-4567", "5551234567", "+1 555 123 4567"}
local REJECTED_EXAMPLES = {"", "12345", "555-CALL-NOW", "++1 555 123 4567", "555 123 45678901234", "  "}

--- Accepts an optional leading +, then 10 to 15 digits, with spaces, dashes, dots and parentheses allowed between them.
-- @param input string to validate
-- @return boolean true if valid, false otherwise
function validatePhone(input)
  -- Type check: must be a string (Lua does implicit type coercion, but we check explicitly for TypeScript parity)
  if type(input) ~= "string" then
    return false
  end
  
  local trimmed = input:match("^%s*(.-)%s*$") or input
  
  -- Check pattern: optional +, followed by digits, spaces, dashes, dots, parentheses
  -- Lua regex: %d = digit, %s = whitespace, %( and %) = literal parens
  -- Allow +, digits, spaces, dashes, dots, parentheses
  if not trimmed:match("^%+?[%d%s()%.%-]+$") then
    return false
  end
  
  -- Extract digits only
  local digits = trimmed:gsub("%D", "")
  
  local digitCount = #digits
  return digitCount >= 10 and digitCount <= 15
end

return {
  validatePhone = validatePhone,
  ACCEPTED_EXAMPLES = ACCEPTED_EXAMPLES,
  REJECTED_EXAMPLES = REJECTED_EXAMPLES,
}
