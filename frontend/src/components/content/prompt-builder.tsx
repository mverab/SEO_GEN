"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface Prompt {
  topic: string
  tone: string
  length: number
  keywords: string[]
}

export function AIPromptBuilder() {
  const [prompt, setPrompt] = useState<Prompt>({
    topic: "",
    tone: "informativo",
    length: 500,
    keywords: []
  })

  const handleGenerate = () => {
    const promptText = `
      Escribe un artículo sobre ${prompt.topic}
      Tono: ${prompt.tone}
      Longitud: ${prompt.length} palabras
      Keywords: ${prompt.keywords.join(", ")}
    `
    console.log("Generando con prompt:", promptText)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Generador de Prompts</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          <input
            type="text"
            value={prompt.topic}
            onChange={(e) => setPrompt(prev => ({ ...prev, topic: e.target.value }))}
            placeholder="Tema principal"
          />
          <select
            value={prompt.tone}
            onChange={(e) => setPrompt(prev => ({ ...prev, tone: e.target.value }))}
          >
            <option value="informativo">Informativo</option>
            <option value="casual">Casual</option>
            <option value="formal">Formal</option>
          </select>
          <Button onClick={handleGenerate}>Generar</Button>
        </div>
      </CardContent>
    </Card>
  )
} 