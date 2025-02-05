export interface KeywordResearchResponse {
  topic_map: TopicNode[]
  seo_potential: SEOMetric[]
  suggestions: KeywordSuggestion[]
}

export interface TopicNode {
  id: string
  label: string
  children?: TopicNode[]
}

export interface SEOMetric {
  label: string
  value: string | number
  description: string
}

export interface KeywordSuggestion {
  keyword: string
  relevance: number
  competition: "Alta" | "Media" | "Baja"
} 