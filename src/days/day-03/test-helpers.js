// Day 3 (QA): five assertion helpers, each driven by the comment above it.
// After accepting, check the helper really FAILS when it should (mutate the expected value).
const assert = require("node:assert/strict");

// Assert that response.status equals 201 and response.body.id is a non-empty string.
function assertCreated(response) {
    assert.equal(response.status, 201);
    assert.ok(response.body.id && typeof response.body.id === 'string');
}

// Assert that the user object has the given role in its roles array.
function assertUserHasRole(user, role) {
    assert.ok(Array.isArray(user.roles), 'User roles should be an array');
    assert.ok(user.roles.includes(role), `User should have role: ${role}`);
}

// Assert that response.body has every key listed in schema.required, each of the declared type.
function assertResponseSchemaValid(response, schema) {
    const body = response.body;
    for (const key of schema.required) {
        assert.ok(body.hasOwnProperty(key), `Missing required key: ${key}`);
        assert.equal(typeof body[key], schema.properties[key].type, `Invalid type for key: ${key}`);
    }
}

// Assert that the value is a valid ISO-8601 date string.
function assertIsoDate(value) {
    assert.ok(typeof value === 'string', 'Value should be a string');
    assert.ok(!isNaN(Date.parse(value)), 'Value should be a valid ISO-8601 date string');
}

// Assert that the array is sorted ascending by the given key.
function assertSortedBy(items, key) {
    for (let i = 1; i < items.length; i++) {
        assert.ok(items[i - 1][key] <= items[i][key], `Array is not sorted by key: ${key}`);
    }
}

module.exports = { assert, assertCreated, assertUserHasRole, assertResponseSchemaValid, assertIsoDate, assertSortedBy };
