import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

const dossier = defineCollection({
  loader: glob({ pattern: "**/*.{md,mdx}", base: "./src/content" }),
  schema: z.object({
    title: z.string(),
    category: z.enum(["datasets", "model-architecture", "evaluation", "macro-thinking"]),
    kind: z.enum(["model", "dataset", "benchmark", "evaluation", "theory", "guidance", "roadmap"]),
    author: z.enum(["xiaoyazhai", "youchengcai"]).optional(),
    organization: z.string().optional(),
    releaseDate: z.coerce.date().optional(),
    summary: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    references: z.array(z.object({ title: z.string(), url: z.string().url() })).default([]),
  }),
});

export const collections = { dossier };
