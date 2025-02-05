"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Wand2, X, ArrowLeft } from "lucide-react"
import { useRouter } from "next/navigation"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

export default function SingleGenPage() {
  const router = useRouter()
  const [isGenerating, setIsGenerating] = useState(false)
  const [formData, setFormData] = useState({
    title: "",
    primaryKeyword: "",
    secondaryKeywords: [] as string[],
    tone: "professional",
    wordCount: 850,
    currentKeyword: "" // Para el input de keywords
  })

  const handleAddKeyword = () => {
    if (formData.currentKeyword.trim() && formData.secondaryKeywords.length < 5) {
      setFormData({
        ...formData,
        secondaryKeywords: [...formData.secondaryKeywords, formData.currentKeyword.trim()],
        currentKeyword: ""
      })
    }
  }

  const handleRemoveKeyword = (index: number) => {
    setFormData({
      ...formData,
      secondaryKeywords: formData.secondaryKeywords.filter((_, i) => i !== index)
    })
  }

  const handleGenerate = async () => {
    setIsGenerating(true)
    // Aquí irá la conexión con el backend
    setTimeout(() => {
      setIsGenerating(false)
      // Redirigir a la vista del artículo generado
    }, 2000)
  }

  return (
    <div className="container max-w-4xl py-6">
      <div className="mb-6">
        <Button 
          variant="ghost" 
          onClick={() => router.back()}
          className="gap-2"
        >
          <ArrowLeft className="h-4 w-4" />
          Volver
        </Button>
      </div>

      <Card className="p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold mb-2">Generar Artículo</h1>
          <p className="text-sm text-muted-foreground">
            Completa los detalles para generar un artículo optimizado para SEO
          </p>
        </div>

        <div className="space-y-6">
          <div className="grid gap-4">
            <div className="space-y-2">
              <Label htmlFor="title">Título del Artículo</Label>
              <Input
                id="title"
                placeholder="Ej: 10 Estrategias Efectivas de Marketing Digital para 2024"
                value={formData.title}
                onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="primaryKeyword">Keyword Principal</Label>
              <Input
                id="primaryKeyword"
                placeholder="Ej: marketing digital estrategias"
                value={formData.primaryKeyword}
                onChange={(e) => setFormData({ ...formData, primaryKeyword: e.target.value })}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label>Keywords Secundarias (máx. 5)</Label>
            <div className="flex gap-2">
              <Input
                placeholder="Agrega keywords relacionadas"
                value={formData.currentKeyword}
                onChange={(e) => setFormData({ ...formData, currentKeyword: e.target.value })}
                onKeyPress={(e) => e.key === "Enter" && handleAddKeyword()}
              />
              <Button 
                onClick={handleAddKeyword}
                disabled={!formData.currentKeyword.trim() || formData.secondaryKeywords.length >= 5}
              >
                Agregar
              </Button>
            </div>
            <div className="flex flex-wrap gap-2 mt-2">
              {formData.secondaryKeywords.map((keyword, index) => (
                <Badge key={index} variant="secondary" className="pl-2 pr-1">
                  {keyword}
                  <button
                    onClick={() => handleRemoveKeyword(index)}
                    className="ml-1 hover:bg-muted rounded-full p-1"
                  >
                    <X className="h-3 w-3" />
                  </button>
                </Badge>
              ))}
            </div>
          </div>

          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-2">
              <Label>Tono de Escritura</Label>
              <Select 
                value={formData.tone}
                onValueChange={(value) => setFormData({ ...formData, tone: value })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona un tono" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="professional">Profesional</SelectItem>
                  <SelectItem value="casual">Casual</SelectItem>
                  <SelectItem value="technical">Técnico</SelectItem>
                  <SelectItem value="friendly">Amigable</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <Label>Número de Palabras</Label>
              <Select 
                value={formData.wordCount.toString()}
                onValueChange={(value) => setFormData({ ...formData, wordCount: parseInt(value) })}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecciona extensión" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="850">850 palabras</SelectItem>
                  <SelectItem value="1000">1000 palabras</SelectItem>
                  <SelectItem value="1200">1200 palabras</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <Button 
            className="w-full gap-2" 
            size="lg"
            onClick={handleGenerate}
            disabled={isGenerating || !formData.title || !formData.primaryKeyword}
          >
            <Wand2 className="h-4 w-4" />
            {isGenerating ? "Generando..." : "Generar Artículo"}
          </Button>
        </div>
      </Card>
    </div>
  )
} 