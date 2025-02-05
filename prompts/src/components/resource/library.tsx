"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface Resource {
  id: string
  title: string
  type: "image" | "document" | "link"
  url: string
  tags: string[]
}

export function ResourceLibrary() {
  const [resources, setResources] = useState<Resource[]>([])
  const [filter, setFilter] = useState("")

  const filteredResources = resources.filter(resource =>
    resource.title.toLowerCase().includes(filter.toLowerCase()) ||
    resource.tags.some(tag => tag.toLowerCase().includes(filter.toLowerCase()))
  )

  const handleDelete = (id: string) => {
    setResources(prev => prev.filter(resource => resource.id !== id))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Biblioteca de Recursos</CardTitle>
      </CardHeader>
      <CardContent>
        <input
          type="text"
          placeholder="Buscar recursos..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        <div>
          {filteredResources.map(resource => (
            <div key={resource.id}>
              <span>{resource.title}</span>
              <span>{resource.type}</span>
              <button onClick={() => handleDelete(resource.id)}>Eliminar</button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 