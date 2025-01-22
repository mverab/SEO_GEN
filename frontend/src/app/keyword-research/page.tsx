"use client"

import { KeywordSearchBar } from "../../components/keyword/search-bar"
import { TopicMapVisualizer } from "../../components/keyword/topic-map"
import { SEOMetricsDisplay } from "../../components/keyword/metrics"
import { KeywordSuggestions } from "../../components/keyword/suggestions"
import type { KeywordResearchResponse } from "../../types/api"
import { useState } from "react"

export default function KeywordResearchPage() {
  const [data, setData] = useState<KeywordResearchResponse | null>(null)
  const [isFirstLoad, setIsFirstLoad] = useState(true)

  const handleSuccess = (newData: KeywordResearchResponse) => {
    setData(newData)
    setIsFirstLoad(false)
  }

  const handleSuggestionSelect = (keyword: string) => {
    // TODO: Implementar lógica para buscar la keyword sugerida
    console.log("Keyword seleccionada:", keyword)
  }

  return (
    <div className="container space-y-8">
      <div className="flex flex-col space-y-4">
        <h1 className="text-3xl font-bold">Investigación de Keywords</h1>
        <p className="text-muted-foreground">
          Analiza keywords y descubre oportunidades SEO para tu contenido
        </p>
      </div>
      
      <KeywordSearchBar onSuccess={handleSuccess} />
      
      <div className="grid gap-6 md:grid-cols-2">
        <SEOMetricsDisplay metrics={data?.seo_potential} isFirstLoad={isFirstLoad} />
        <TopicMapVisualizer topics={data?.topic_map} isFirstLoad={isFirstLoad} />
      </div>

      <KeywordSuggestions 
        suggestions={data?.suggestions} 
        onSelect={handleSuggestionSelect}
        isFirstLoad={isFirstLoad}
      />
    </div>
  )
} 