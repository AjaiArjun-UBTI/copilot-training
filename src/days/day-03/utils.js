// Day 3 (Dev): five small functions, each driven by the comment above it.
// Write the comment, read the suggestion, accept / reject / EDIT. Look for: null or empty
// input, off-by-one, a missing await. Log every decision on the Day 3 page.

// Return true if the given string is a valid email address using regex.
function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Return true if the string reads the same forwards and backwards, ignoring case and non-letters.
function isPalindrome(text) {
    const cleaned = text.toLowerCase().replace(/[^a-z]/g, '');
    return cleaned === cleaned.split('').reverse().join('');
}

// Split an array into chunks of the given size. The last chunk may be shorter. Size must be >= 1.
function chunk(items, size) {
    if (size < 1) throw new Error('Size must be >= 1');
    const result = [];
    for (let i = 0; i < items.length; i += size) {
        result.push(items.slice(i, i + size));
    }
    return result;
}

// Return the sum of all integers from start to end, inclusive.
function sumRange(start, end) {
    let sum = 0;
    for (let i = start; i <= end; i++) {
        sum += i;
    }
    return sum;
}

// Fetch a URL and return the parsed JSON body. Throw an Error when the response is not ok.
async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

module.exports = { isValidEmail, isPalindrome, chunk, sumRange, fetchJson };
