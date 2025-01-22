"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface ExportOption {
  id: string
  name: string
  format: string
}

export function ExportOptions() {
  const [selectedOption, setSelectedOption] = useState<string>("")

  const options: ExportOption[] = [
    { id: "markdown", name: "Markdown", format: ".md" },
    { id: "html", name: "HTML", format: ".html" },
    { id: "gdoc", name: "Google Docs", format: "gdoc" },
    { id: "word", name: "Word", format: ".docx" }
  ]

  const handleExport = (optionId: string) => {
    setSelectedOption(optionId)
    console.log("Exportando en formato:", optionId)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Exportar Contenido</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          {options.map(option => (
            <Button
              key={option.id}
              variant={selectedOption === option.id ? "default" : "outline"}
              onClick={() => handleExport(option.id)}
            >
              {option.name}
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 