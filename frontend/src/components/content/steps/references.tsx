"use client"

import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Plus, Trash2 } from "lucide-react"
import { useState } from "react"

interface Reference {
  url: string
  notes: string
}

export function ReferencesStep() {
  const [references, setReferences] = useState<Reference[]>([])

  const handleAddReference = () => {
    setReferences([...references, { url: "", notes: "" }])
  }

  const handleRemoveReference = (index: number) => {
    setReferences(references.filter((_, i) => i !== index))
  }

  const handleUpdateReference = (
    index: number,
    field: keyof Reference,
    value: string
  ) => {
    const newReferences = [...references]
    newReferences[index] = { ...newReferences[index], [field]: value }
    setReferences(newReferences)
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Label>Referencias</Label>
        <Button
          onClick={handleAddReference}
          variant="outline"
          size="sm"
          className="gap-2"
        >
          <Plus className="h-4 w-4" />
          Agregar Referencia
        </Button>
      </div>

      <div className="space-y-4">
        {references.map((ref, index) => (
          <div key={index} className="relative space-y-2 rounded-lg border p-4">
            <Button
              variant="ghost"
              size="icon"
              className="absolute right-2 top-2"
              onClick={() => handleRemoveReference(index)}
            >
              <Trash2 className="h-4 w-4" />
            </Button>

            <div className="space-y-2">
              <Label>URL</Label>
              <Input
                value={ref.url}
                onChange={(e) =>
                  handleUpdateReference(index, "url", e.target.value)
                }
                placeholder="https://..."
              />
            </div>

            <div className="space-y-2">
              <Label>Notas</Label>
              <Textarea
                value={ref.notes}
                onChange={(e) =>
                  handleUpdateReference(index, "notes", e.target.value)
                }
                placeholder="Información relevante de esta fuente..."
                className="h-20"
              />
            </div>
          </div>
        ))}

        {references.length === 0 && (
          <div className="rounded-lg border border-dashed p-8 text-center text-muted-foreground">
            No hay referencias agregadas
          </div>
        )}
      </div>
    </div>
  )
} 