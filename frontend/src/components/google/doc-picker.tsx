"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface GoogleDoc {
  id: string
  name: string
  url: string
  lastModified: string
}

export function DocPicker() {
  const [selectedDocs, setSelectedDocs] = useState<GoogleDoc[]>([])

  const handlePickDocs = () => {
    // TODO: Implementar integración real con Google Picker API
    const mockDocs: GoogleDoc[] = [
      {
        id: "1",
        name: "Documento 1",
        url: "https://docs.google.com/1",
        lastModified: new Date().toISOString()
      }
    ]
    setSelectedDocs(mockDocs)
  }

  const handleRemoveDoc = (id: string) => {
    setSelectedDocs(prev => prev.filter(doc => doc.id !== id))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Seleccionar Documentos</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={handlePickDocs}>
          Abrir Selector
        </Button>
        <div>
          {selectedDocs.map(doc => (
            <div key={doc.id}>
              <span>{doc.name}</span>
              <span>{new Date(doc.lastModified).toLocaleDateString()}</span>
              <Button onClick={() => handleRemoveDoc(doc.id)}>
                Eliminar
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 