"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface EditorContent {
  title: string
  content: string
}

export function RichTextEditor() {
  const [content, setContent] = useState<EditorContent>({
    title: "",
    content: ""
  })

  const handleSave = () => {
    console.log("Guardando:", content)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Editor de Contenido</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          <input
            type="text"
            value={content.title}
            onChange={(e) => setContent(prev => ({ ...prev, title: e.target.value }))}
            placeholder="Título del artículo"
          />
          <textarea
            value={content.content}
            onChange={(e) => setContent(prev => ({ ...prev, content: e.target.value }))}
            placeholder="Contenido del artículo"
          />
          <Button onClick={handleSave}>Guardar</Button>
        </div>
      </CardContent>
    </Card>
  )
} 