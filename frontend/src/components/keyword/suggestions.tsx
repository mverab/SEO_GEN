"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card"
import { Button } from "../ui/button"
import { Plus } from "lucide-react"

interface KeywordSuggestion {
  keyword: string
  relevance: number
  competition: "Alta" | "Media" | "Baja"
}

interface KeywordSuggestionsProps {
  suggestions?: KeywordSuggestion[]
  onSelect?: (keyword: string) => void
  isFirstLoad?: boolean
}

export function KeywordSuggestions({ 
  suggestions, 
  onSelect,
  isFirstLoad = true 
}: KeywordSuggestionsProps) {
  const defaultSuggestions: KeywordSuggestion[] = [
    { keyword: "Sugerencia 1", relevance: 85, competition: "Baja" },
    { keyword: "Sugerencia 2", relevance: 75, competition: "Media" },
    { keyword: "Sugerencia 3", relevance: 65, competition: "Alta" },
  ]

  const displaySuggestions = suggestions || defaultSuggestions

  return (
    <Card className={isFirstLoad ? "opacity-70" : ""}>
      <CardHeader>
        <CardTitle>Keywords Relacionadas</CardTitle>
        <CardDescription>
          Sugerencias basadas en tu búsqueda
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {displaySuggestions.map((suggestion, index) => (
            <div
              key={index}
              className="flex items-center justify-between rounded-lg border p-4"
            >
              <div className="space-y-1">
                <p className="font-medium">{suggestion.keyword}</p>
                <div className="flex gap-2 text-sm text-muted-foreground">
                  <span>Relevancia: {suggestion.relevance}%</span>
                  <span>•</span>
                  <span>Competencia: {suggestion.competition}</span>
                </div>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onSelect?.(suggestion.keyword)}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 