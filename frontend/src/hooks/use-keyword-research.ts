"use client"

import { useMutation } from "@tanstack/react-query"
import type { KeywordResearchResponse } from "@/types/api"

export function useKeywordResearch() {
  return useMutation<KeywordResearchResponse, Error, string>({
    mutationFn: async (keyword: string) => {
      const response = await fetch("/api/keyword-research", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ keyword }),
      })

      if (!response.ok) {
        throw new Error("Error al buscar keyword")
      }

      const data = await response.json()
      
      // Aseguramos que los datos sean serializables
      return {
        topic_map: data.topic_map.map((topic: any) => ({
          id: String(topic.id),
          label: String(topic.label),
          children: topic.children?.map((child: any) => ({
            id: String(child.id),
            label: String(child.label)
          }))
        })),
        seo_potential: data.seo_potential.map((metric: any) => ({
          label: String(metric.label),
          value: typeof metric.value === 'number' ? metric.value : String(metric.value),
          description: String(metric.description)
        }))
      }
    },
  })
} 