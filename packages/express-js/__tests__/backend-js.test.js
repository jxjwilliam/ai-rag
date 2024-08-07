'use strict';

const backendJs = require('..');
const assert = require('assert').strict;

assert.strictEqual(backendJs(), 'Hello from backendJs');
console.info('backendJs tests passed');
