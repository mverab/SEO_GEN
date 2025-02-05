"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Check, RefreshCw, X } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useRouter } from "next/navigation"

interface KeywordsListProps {
  mainKeyword: string
  keywords: string[]
  onRegenerate: () => void
  onReset: () => void
}

export function KeywordsList({
  mainKeyword,
  keywords,
  onRegenerate,
  onReset
}: KeywordsListProps) {
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([])
  const [showCampaignDialog, setShowCampaignDialog] = useState(false)
  const [campaignName, setCampaignName] = useState("")
  const router = useRouter()

  const handleToggleKeyword = (keyword: string) => {
    setSelectedKeywords(prev =>
      prev.includes(keyword)
        ? prev.filter(k => k !== keyword)
        : [...prev, keyword]
    )
  }

  const handleCreateCampaign = () => {
    // Aquí conectaremos con la API para crear la campaña
    console.log("Crear campaña:", {
      name: campaignName,
      mainKeyword,
      keywords: selectedKeywords
    })
    setShowCampaignDialog(false)
    // Redirigir a la página de campañas
    router.push("/dashboard/campaigns")
  }

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold">Keywords Sugeridas</h2>
            <p className="text-sm text-muted-foreground">
              Selecciona las keywords que deseas incluir en tu campaña
            </p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={onReset}>
              <X className="mr-2 h-4 w-4" />
              Cancelar
            </Button>
            <Button variant="outline" size="sm" onClick={onRegenerate}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Regenerar
            </Button>
          </div>
        </div>

        <div className="mb-6">
          <div className="mb-4 flex items-center gap-2">
            <Badge variant="default" className="text-base">
              {mainKeyword}
            </Badge>
            <span className="text-sm text-muted-foreground">Keyword Principal</span>
          </div>
          
          <div className="space-y-2">
            {keywords.map((keyword) => (
              <div
                key={keyword}
                className="flex items-center justify-between rounded-lg border p-3 transition-colors hover:bg-accent"
              >
                <div className="flex items-center gap-2">
                  <span>{keyword}</span>
                  <Badge variant="secondary" className="text-xs">
                    Relacionada
                  </Badge>
                </div>
                <Button
                  variant={selectedKeywords.includes(keyword) ? "default" : "outline"}
                  size="sm"
                  onClick={() => handleToggleKeyword(keyword)}
                >
                  <Check className="h-4 w-4" />
                </Button>
              </div>
            ))}
          </div>
        </div>

        <Button
          className="w-full"
          disabled={selectedKeywords.length === 0}
          onClick={() => setShowCampaignDialog(true)}
        >
          Crear Campaña ({selectedKeywords.length} keywords)
        </Button>
      </Card>

      <Dialog open={showCampaignDialog} onOpenChange={setShowCampaignDialog}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Crear Nueva Campaña</DialogTitle>
            <DialogDescription>
              Nombra tu campaña para comenzar a generar contenido con las keywords seleccionadas.
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Input
                value={campaignName}
                onChange={(e) => setCampaignName(e.target.value)}
                placeholder="Nombre de la campaña..."
              />
            </div>
            
            <div className="space-y-2">
              <h4 className="text-sm font-medium">Keywords Seleccionadas:</h4>
              <div className="flex flex-wrap gap-2">
                <Badge variant="default">{mainKeyword}</Badge>
                {selectedKeywords.map((keyword) => (
                  <Badge key={keyword} variant="secondary">
                    {keyword}
                  </Badge>
                ))}
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCampaignDialog(false)}>
              Cancelar
            </Button>
            <Button 
              onClick={handleCreateCampaign}
              disabled={!campaignName.trim()}
            >
              Crear Campaña
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
} 