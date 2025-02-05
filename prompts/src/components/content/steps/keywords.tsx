"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { X } from "lucide-react"
import { useState } from "react"

export function KeywordsStep() {
  const [keywords, setKeywords] = useState<string[]>([])
  const [inputValue, setInputValue] = useState("")

  const handleAddKeyword = (e: React.FormEvent) => {
    e.preventDefault()
    if (inputValue.trim()) {
      setKeywords([...keywords, inputValue.trim()])
      setInputValue("")
    }
  }

  const handleRemoveKeyword = (index: number) => {
    setKeywords(keywords.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <Label>Keywords</Label>
        <form onSubmit={handleAddKeyword} className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Agrega keywords principales..."
          />
          <Button type="submit">Agregar</Button>
        </form>
      </div>

      <div className="flex flex-wrap gap-2">
        {keywords.map((keyword, index) => (
          <Badge key={index} variant="secondary" className="pl-2 pr-1">
            {keyword}
            <button
              onClick={() => handleRemoveKeyword(index)}
              className="ml-1 rounded-full p-1 hover:bg-muted"
            >
              <X className="h-3 w-3" />
            </button>
          </Badge>
        ))}
      </div>

      <div className="space-y-2">
        <Label>Tono de Voz</Label>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <Label className="text-xs">Formalidad</Label>
            <input
              type="range"
              min="0"
              max="100"
              className="w-full"
              defaultValue="50"
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Casual</span>
              <span>Formal</span>
            </div>
          </div>
          <div>
            <Label className="text-xs">Tecnicidad</Label>
            <input
              type="range"
              min="0"
              max="100"
              className="w-full"
              defaultValue="50"
            />
            <div className="flex justify-between text-xs text-muted-foreground">
              <span>Simple</span>
              <span>Técnico</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 