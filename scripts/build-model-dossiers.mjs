import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourcePath = path.join(root, "src/data/model-dossiers.json");
const publicDir = path.join(root, "public/model-architecture");
const modelDir = path.join(publicDir, "models");
const models = JSON.parse(await fs.readFile(sourcePath, "utf8"));

const required = [
  "id", "name", "subtitle", "organization", "releaseDate", "category",
  "parameters", "accent", "summary", "diagram", "detailedFlow", "sources",
  "route", "architecture", "formulaHtml", "formulaNotes", "training",
  "inference", "deepDive", "pitfalls",
];
const ids = new Set();
for (const model of models) {
  if (ids.has(model.id)) throw new Error(`Duplicate model id: ${model.id}`);
  ids.add(model.id);
  for (const key of required) {
    if (model[key] == null || (Array.isArray(model[key]) && model[key].length === 0)) {
      throw new Error(`${model.id} is missing ${key}`);
    }
  }
}

const manifestKeys = [
  "id", "name", "subtitle", "organization", "releaseDate", "category",
  "parameters", "accent", "summary",
];
const manifest = models.map((model) => Object.fromEntries(
  manifestKeys.map((key) => [key, model[key]])
));

await fs.mkdir(modelDir, { recursive: true });
await fs.writeFile(
  path.join(publicDir, "model-manifest.js"),
  `window.MODEL_MANIFEST=${JSON.stringify(manifest)};\n`,
);
await Promise.all(models.map((model) => fs.writeFile(
  path.join(modelDir, `${model.id}.js`),
  `window.__MODEL_DETAIL_LOADED__(${JSON.stringify(model)});\n`,
)));

console.log(`Generated manifest and ${models.length} lazy-loaded model files.`);
