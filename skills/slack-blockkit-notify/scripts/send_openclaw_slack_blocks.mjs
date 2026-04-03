#!/usr/bin/env node
import fs from 'node:fs';
import process from 'node:process';
import { sendSlackMessage, parseSlackBlocksInput } from '/usr/lib/node_modules/openclaw/dist/plugin-sdk/slack.js';

const args = process.argv.slice(2);
function arg(name) {
  const idx = args.indexOf(name);
  return idx >= 0 ? args[idx + 1] : undefined;
}

const payloadPath = arg('--payload');
const accountId = arg('--account');
if (!payloadPath) {
  console.error('Usage: send_openclaw_slack_blocks.mjs --payload <file> [--account <id>]');
  process.exit(2);
}

const payload = JSON.parse(fs.readFileSync(payloadPath, 'utf8'));
const to = payload.to || payload.channel || payload.target;
if (!to) {
  console.error('Payload must include to/channel/target');
  process.exit(2);
}
const content = payload.content || payload.text || 'Block Kit test';
const blocks = parseSlackBlocksInput(payload.channelData?.slack?.blocks ?? payload.blocks);

const opts = { blocks };
if (accountId) opts.accountId = accountId;

const result = await sendSlackMessage(to, content, opts);
console.log(JSON.stringify(result, null, 2));
