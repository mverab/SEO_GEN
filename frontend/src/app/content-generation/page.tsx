"use client"

import { RichTextEditor } from "@/components/content/rich-text-editor"
import { AIPromptBuilder } from "@/components/content/prompt-builder"
import { FormatSelector } from "@/components/content/format-selector"
import { ExportOptions } from "@/components/content/export-options"

export default function ContentGenerationPage() {
  return (
    <div className="container space-y-8">
      <h1>Generación de Contenido</h1>
      <div className="grid gap-8">
        <AIPromptBuilder />
        <FormatSelector />
        <RichTextEditor />
        <ExportOptions />
      </div>
    </div>
  )
} 