"use client"

import { useState } from "react"
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Search } from "lucide-react"
import { useKeywordResearch } from "../../hooks/use-keyword-research"
import type { KeywordResearchResponse } from "../../types/api"

interface KeywordSearchBarProps {
  onSuccess?: (data: KeywordResearchResponse) => void
}

export function KeywordSearchBar({ onSuccess }: KeywordSearchBarProps) {
  const [keyword, setKeyword] = useState("")
  const { mutate, isPending: isLoading } = useKeywordResearch()

  const handleSearch = () => {
    if (!keyword.trim()) return
    
    mutate(keyword, {
      onSuccess: (data) => {
        onSuccess?.(data)
        setKeyword("")
      },
      onError: (error) => {
        console.error("Error:", error)
      },
    })
  }

  return (
    <div className="flex w-full max-w-sm items-center space-x-2">
      <Input
        type="text"
        placeholder="Ingresa una keyword..."
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSearch()
        }}
        disabled={isLoading}
        className="flex-1"
      />
      <Button 
        onClick={handleSearch}
        disabled={isLoading || !keyword.trim()}
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            Buscando...
          </span>
        ) : (
          <>
            <Search className="mr-2 h-4 w-4" />
            Buscar
          </>
        )}
      </Button>
    </div>
  )
} 