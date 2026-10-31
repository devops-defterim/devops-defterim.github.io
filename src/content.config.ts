import { defineCollection, z } from 'astro:content';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: docsLoader(),
		schema: docsSchema({
			extend: z.object({
				module: z.string().optional(),
				lessons: z.array(z.union([z.number().int().min(0), z.literal('talimat')])).optional(),
				order: z.number().optional(),
			}),
		}),
	}),
};
