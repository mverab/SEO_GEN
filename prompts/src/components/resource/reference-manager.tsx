"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface Reference {
  id: string
  title: string
  url: string
  type: "article" | "study" | "statistic"
  notes: string
}

export function ReferenceManager() {
  const [references, setReferences] = useState<Reference[]>([])

  const handleAdd = () => {
    const newReference: Reference = {
      id: Math.random().toString(36).slice(2),
      title: "",
      url: "",
      type: "article",
      notes: ""
    }
    setReferences(prev => [...prev, newReference])
  }

  const handleUpdate = (id: string, data: Partial<Reference>) => {
    setReferences(prev => prev.map(ref =>
      ref.id === id ? { ...ref, ...data } : ref
    ))
  }

  const handleDelete = (id: string) => {
    setReferences(prev => prev.filter(ref => ref.id !== id))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Gestor de Referencias</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={handleAdd}>Agregar Referencia</Button>
        <div>
          {references.map(ref => (
            <div key={ref.id}>
              <input
                type="text"
                value={ref.title}
                onChange={(e) => handleUpdate(ref.id, { title: e.target.value })}
                placeholder="Título"
              />
              <input
                type="url"
                value={ref.url}
                onChange={(e) => handleUpdate(ref.id, { url: e.target.value })}
                placeholder="URL"
              />
              <select
                value={ref.type}
                onChange={(e) => handleUpdate(ref.id, { type: e.target.value as Reference["type"] })}
              >
                <option value="article">Artículo</option>
                <option value="study">Estudio</option>
                <option value="statistic">Estadística</option>
              </select>
              <Button onClick={() => handleDelete(ref.id)}>Eliminar</Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 