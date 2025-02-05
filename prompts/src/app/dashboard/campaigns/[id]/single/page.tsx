"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Wand2, ArrowLeft } from "lucide-react"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { useRouter } from "next/navigation"

export default function SingleGenPage() {
  const router = useRouter()
  const [isGenerating, setIsGenerating] = useState(false)

  // Mock data - esto vendrá de la API
  const campaignData = {
    mainKeyword: "marketing digital",
    relatedKeywords: ["seo", "estrategias", "2024"]
  }

  return (
    <div className="container max-w-4xl space-y-8 py-8">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => router.back()}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <h1 className="text-2xl font-bold">Generar Artículo</h1>
        </div>
        <Button 
          className="bg-purple-600 hover:bg-purple-700"
          disabled={isGenerating}
          onClick={() => setIsGenerating(true)}
        >
          <Wand2 className="mr-2 h-4 w-4" />
          {isGenerating ? "Generando..." : "Generar con AI"}
        </Button>
      </div>

      <div className="grid gap-6">
        {/* Keywords y Título */}
        <Card className="p-6">
          <h2 className="mb-4 font-semibold">Keywords y Título</h2>
          <div className="space-y-4">
            <div>
              <label className="mb-2 block text-sm">Keyword Principal</label>
              <div className="flex items-center gap-2">
                <Badge>{campaignData.mainKeyword}</Badge>
                <span className="text-sm text-muted-foreground">
                  (de la campaña)
                </span>
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm">Keywords Relacionadas</label>
              <div className="flex flex-wrap gap-2">
                {campaignData.relatedKeywords.map(keyword => (
                  <Badge key={keyword} variant="secondary">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm">Título Sugerido</label>
              <Input 
                placeholder="Ej: 10 Estrategias de Marketing Digital para 2024"
                className="max-w-2xl"
              />
            </div>
          </div>
        </Card>

        {/* Tono y Formato */}
        <Card className="p-6">
          <h2 className="mb-4 font-semibold">Tono y Formato</h2>
          <div className="grid gap-6 md:grid-cols-2">
            <div className="space-y-4">
              <div>
                <label className="mb-2 block text-sm">Tono de Escritura</label>
                <Select defaultValue="professional">
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

              <div>
                <label className="mb-2 block text-sm">Formato</label>
                <Select defaultValue="article">
                  <SelectTrigger>
                    <SelectValue placeholder="Selecciona un formato" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="article">Artículo</SelectItem>
                    <SelectItem value="guide">Guía</SelectItem>
                    <SelectItem value="tutorial">Tutorial</SelectItem>
                    <SelectItem value="review">Review</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="space-y-6">
              <div>
                <div className="mb-4 flex justify-between">
                  <label className="text-sm">Nivel de Detalle</label>
                  <span className="text-sm text-muted-foreground">70%</span>
                </div>
                <Slider defaultValue={[70]} max={100} step={1} />
              </div>

              <div>
                <div className="mb-4 flex justify-between">
                  <label className="text-sm">Longitud</label>
                  <span className="text-sm text-muted-foreground">850 palabras</span>
                </div>
                <Slider 
                  defaultValue={[850]} 
                  min={850}
                  max={1200}
                  step={50}
                />
              </div>
            </div>
          </div>
        </Card>

        {/* Referencias */}
        <Card className="p-6">
          <h2 className="mb-4 font-semibold">Referencias</h2>
          <div className="space-y-4">
            <div>
              <label className="mb-2 block text-sm">Links Internos Sugeridos</label>
              <div className="rounded-lg border p-4">
                <div className="text-sm text-muted-foreground">
                  Se agregarán automáticamente los links más relevantes del sitio
                </div>
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm">Notas Adicionales</label>
              <Textarea 
                placeholder="Agrega notas o instrucciones específicas para la generación..."
                className="min-h-[100px]"
              />
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
} 