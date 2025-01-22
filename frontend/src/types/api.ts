export interface KeywordResearchResponse {
  topic_map: TopicNode[]
  seo_potential: SEOMetric[]
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