import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const root = new URL("../src/content/", import.meta.url);
const categories = new Set(["dexterous-hand", "dual-arm", "humanoid"]);
const ids = new Set();
let checked = 0;

async function walk(directory) {
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) await walk(path);
    if (!entry.isFile() || !/\.mdx?$/.test(entry.name)) continue;
    const text = await readFile(path, "utf8");
    const frontmatter = text.match(/^---\n([\s\S]*?)\n---/);
    if (!frontmatter) throw new Error(`${path}: missing frontmatter`);
    const category = frontmatter[1].match(/^category:\s*(.+)$/m)?.[1]?.trim();
    if (!categories.has(category)) throw new Error(`${path}: invalid category`);
    const id = path.replace(String(root.pathname), "");
    if (ids.has(id)) throw new Error(`${path}: duplicate id`);
    ids.add(id);
    checked += 1;
  }
}

await walk(root);
console.log(`Validated ${checked} content file(s).`);
