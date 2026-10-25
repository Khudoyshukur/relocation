// Builds site/config.js at deploy time. It holds the GitHub token and the notes
// encryption key, both encrypted with a key derived from the site username and
// password. Only someone who knows the login can unlock them.
import { webcrypto as crypto } from "node:crypto";
import { writeFileSync } from "node:fs";

const { SITE_USERNAME, SITE_PASSWORD, SITE_GH_TOKEN, SITE_DATA_KEY } = process.env;
const missing = Object.entries({ SITE_USERNAME, SITE_PASSWORD, SITE_GH_TOKEN, SITE_DATA_KEY })
  .filter(([, v]) => !v).map(([k]) => k);
if (missing.length) {
  console.error(`Missing repository secrets: ${missing.join(", ")}`);
  process.exit(1);
}

const ITERATIONS = 600_000;
const b64 = bytes => Buffer.from(bytes).toString("base64");
const salt = crypto.getRandomValues(new Uint8Array(16));
const iv = crypto.getRandomValues(new Uint8Array(12));

// Must match passwordKey() in site/index.html.
const material = await crypto.subtle.importKey(
  "raw", new TextEncoder().encode(`${SITE_USERNAME.trim().toLowerCase()}\n${SITE_PASSWORD}`),
  "PBKDF2", false, ["deriveKey"]);
const key = await crypto.subtle.deriveKey(
  { name: "PBKDF2", salt, iterations: ITERATIONS, hash: "SHA-256" },
  material, { name: "AES-GCM", length: 256 }, false, ["encrypt"]);

const payload = JSON.stringify({ token: SITE_GH_TOKEN.trim(), dataKey: SITE_DATA_KEY.trim() });
const data = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, new TextEncoder().encode(payload));

const config = { iterations: ITERATIONS, salt: b64(salt), iv: b64(iv), data: b64(new Uint8Array(data)) };
writeFileSync(new URL("../site/config.js", import.meta.url), `window.SITE_CONFIG = ${JSON.stringify(config)};\n`);
console.log("site/config.js written");
