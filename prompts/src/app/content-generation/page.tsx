"use client"

import { RichTextEditor } from "@/components/content/rich-text-editor"
import { AIPromptBuilder } from "@/components/content/prompt-builder"
import { FormatSelector } from "@/components/content/format-selector"
import { ExportOptions } from "@/components/content/export-options"
import { AIMetrics } from "@/components/content/AIMetrics"
import { useState } from "react"

export default function ContentGenerationPage() {
  const [aiMetrics, setAiMetrics] = useState({
    score: 0,
    wasImproved: false,
    features: {}
  })

  const handleContentGenerated = (content: any) => {
    if (content.metadata) {
      setAiMetrics({
        score: content.metadata.ai_score || 0,
        wasImproved: content.metadata.was_improved || false,
        features: content.metadata.features || {}
      })
    }
  }

  return (
    <div className="container space-y-8">
      <h1>Generación de Contenido</h1>
      <div className="grid gap-8 grid-cols-1 md:grid-cols-[2fr_1fr]">
        <div className="space-y-8">
          <AIPromptBuilder onGenerate={handleContentGenerated} />
          <FormatSelector />
          <RichTextEditor />
          <ExportOptions />
        </div>
        <div>
          <AIMetrics {...aiMetrics} />
        </div>
      </div>
    </div>
  )
} 