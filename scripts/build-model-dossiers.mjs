import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { createHash } from "node:crypto";

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
  "controller",
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
  for (const key of ["name", "status", "platform", "interface", "execution", "adaptation", "checkedAt"]) {
    if (typeof model.controller[key] !== "string" || !model.controller[key].trim()) {
      throw new Error(`${model.id} is missing controller.${key}`);
    }
  }
  if (!model.controller.sources?.length) throw new Error(`${model.id} has no controller sources`);
  for (const group of model.figureGroups ?? []) {
    if (!group.title || !group.images?.length) throw new Error(`${model.id} has an empty figure group`);
    for (const figure of group.images) {
      if (!/^\.\/assets\/[a-zA-Z0-9/_-]+\.webp$/.test(figure.src)) throw new Error(`${model.id} has an invalid figure path`);
      const stat = await fs.stat(path.join(publicDir, figure.src));
      if (stat.size !== figure.bytes || !figure.alt || figure.width <= 0 || figure.height <= 0) {
        throw new Error(`${model.id} has stale or incomplete figure metadata: ${figure.src}`);
      }
    }
  }
}

const manifestKeys = [
  "id", "name", "subtitle", "organization", "releaseDate", "category",
  "parameters", "accent", "summary",
];
const manifest = models.map((model) => ({
  ...Object.fromEntries(manifestKeys.map((key) => [key, model[key]])),
  controllerName: model.controller.name,
  detailVersion: createHash("sha256").update(JSON.stringify(model)).digest("hex").slice(0, 12),
}));

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
