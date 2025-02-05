"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface ContentFormat {
  id: string
  name: string
  structure: string[]
}

export function FormatSelector() {
  const [selectedFormat, setSelectedFormat] = useState<string>("")

  const formats: ContentFormat[] = [
    {
      id: "how-to",
      name: "Tutorial How-To",
      structure: ["Introducción", "Materiales", "Pasos", "Conclusión"]
    },
    {
      id: "listicle",
      name: "Artículo en Lista",
      structure: ["Introducción", "Puntos Principales", "Resumen"]
    },
    {
      id: "review",
      name: "Reseña",
      structure: ["Descripción", "Pros", "Contras", "Veredicto"]
    }
  ]

  const handleSelect = (formatId: string) => {
    setSelectedFormat(formatId)
    console.log("Formato seleccionado:", formatId)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Formato de Contenido</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          {formats.map(format => (
            <div key={format.id}>
              <Button
                variant={selectedFormat === format.id ? "default" : "outline"}
                onClick={() => handleSelect(format.id)}
              >
                {format.name}
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 