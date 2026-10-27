import assert from 'node:assert/strict';
import test from 'node:test';

import { readUpload } from '../src/download.js';
import { insideUploads, thumbnailSize } from '../src/thumbs.js';

test('reads an attachment', async () => {
  assert.equal((await readUpload('example.txt')).toString().trim(), 'ticket 1042 attachment');
});

test('thumbnails stay inside uploads', async () => {
  assert.throws(() => insideUploads('../package.json'));
  assert.throws(() => insideUploads('../uploads-old/x'));
  assert.ok((await thumbnailSize('example.txt')) > 0);
});
