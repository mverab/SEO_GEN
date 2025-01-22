"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface NicheCategory {
  id: string
  name: string
  topics: string[]
}

export function NicheOrganizer() {
  const [categories, setCategories] = useState<NicheCategory[]>([])

  const handleAddCategory = () => {
    const newCategory: NicheCategory = {
      id: Math.random().toString(36).slice(2),
      name: "",
      topics: []
    }
    setCategories(prev => [...prev, newCategory])
  }

  const handleAddTopic = (categoryId: string, topic: string) => {
    setCategories(prev => prev.map(cat =>
      cat.id === categoryId
        ? { ...cat, topics: [...cat.topics, topic] }
        : cat
    ))
  }

  const handleUpdateCategory = (id: string, name: string) => {
    setCategories(prev => prev.map(cat =>
      cat.id === id ? { ...cat, name } : cat
    ))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Organizador de Nichos</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={handleAddCategory}>Nueva Categoría</Button>
        <div>
          {categories.map(category => (
            <div key={category.id}>
              <input
                type="text"
                value={category.name}
                onChange={(e) => handleUpdateCategory(category.id, e.target.value)}
                placeholder="Nombre de categoría"
              />
              <div>
                {category.topics.map((topic, index) => (
                  <div key={index}>{topic}</div>
                ))}
                <input
                  type="text"
                  placeholder="Nuevo tema"
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      const input = e.target as HTMLInputElement
                      handleAddTopic(category.id, input.value)
                      input.value = ""
                    }
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 