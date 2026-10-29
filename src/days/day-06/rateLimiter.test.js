// Day 6 (QA): these tests have assertions but no descriptions. Ask Copilot for a
// Given-When-Then description above each test, then check each one against the assertions.
const { test } = require("node:test");
const assert = require("node:assert/strict");
const { createRateLimiter } = require("./rateLimiter");

// Given: rate limiter with max=2 requests per window
// When: same key is checked 3 times within the same window
// Then: 1st check .allowed=true, 2nd check .allowed=true, 3rd check .allowed=false
test("test 1", () => {
  const check = createRateLimiter({ max: 2, windowMs: 1000, now: () => 0 });
  assert.equal(check("a").allowed, true);
  assert.equal(check("a").allowed, true);
  assert.equal(check("a").allowed, false);
});

// Given: rate limiter with max=1 request per window
// When: two different keys are checked once each
// Then: both checks pass (separate key = separate limit)
test("test 2", () => {
  const check = createRateLimiter({ max: 1, windowMs: 1000, now: () => 0 });
  check("a");
  assert.equal(check("b").allowed, true);
});

// Given: rate limiter with max=1 request per 1000ms window
// When: time advances by 1000ms (window expires) and same key is checked again
// Then: the second check passes (window reset)
test("test 3", () => {
  let t = 0;
  const check = createRateLimiter({ max: 1, windowMs: 1000, now: () => t });
  check("a");
  t = 1000;
  assert.equal(check("a").allowed, true);
});

// ⚠️  MISMATCH: Test name suggests error handling, but asserts that createRateLimiter throws.
// Module docstring says "Never throws"—this test contradicts the documented behavior.
// Given: no options provided (undefined)
// When: createRateLimiter is called without arguments
// Then: function throws an error
test("test 4", () => {
  assert.throws(() => createRateLimiter());
});

// Given: rate limiter with max=3 requests per window
// When: same key is checked once
// Then: remaining count is 2 (max - count)
test("test 5", () => {
  const check = createRateLimiter({ max: 3, windowMs: 1000, now: () => 0 });
  assert.equal(check("a").remaining, 2);
});
