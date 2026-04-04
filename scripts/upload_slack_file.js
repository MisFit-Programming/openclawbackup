#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { WebClient } = require('/usr/lib/node_modules/openclaw/node_modules/@slack/web-api');

function getArg(name) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : undefined;
}

const channel = getArg('--channel');
const filePath = getArg('--file');
const title = getArg('--title') || path.basename(filePath || 'report.html');
const initialComment = getArg('--comment') || '';
if (!channel || !filePath) {
  console.error('Usage: upload_slack_file.js --channel <id> --file <path> [--title <title>] [--comment <text>]');
  process.exit(2);
}
const config = JSON.parse(fs.readFileSync('/root/.openclaw/openclaw.json', 'utf8'));
const token = config?.channels?.slack?.botToken;
if (!token) {
  console.error('Missing Slack bot token in config');
  process.exit(3);
}
(async () => {
  const client = new WebClient(token);
  const result = await client.files.uploadV2({
    channel_id: channel,
    file: fs.createReadStream(filePath),
    filename: path.basename(filePath),
    title,
    initial_comment: initialComment || undefined,
  });
  console.log(JSON.stringify({ ok: true, file_id: result.files?.[0]?.id || null, channel }, null, 2));
})().catch((err) => {
  console.error(err?.data ? JSON.stringify(err.data) : (err?.message || String(err)));
  process.exit(1);
});
