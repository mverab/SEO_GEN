"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Wand2, ArrowLeft, ArrowRight } from "lucide-react"
import { KeywordsList } from "@/components/keywords/keywords-list"

const startSteps = [
  {
    title: "¡Bienvenido a SEO Generator!",
    description: "Vamos a ayudarte a rankear tu SEO sin esfuerzo. Comencemos con una keyword principal."
  },
  {
    title: "Ingresa tu Keyword",
    description: "Escribe la keyword principal para tu contenido. Nuestro sistema generará sugerencias relacionadas."
  },
  {
    title: "Mejora con AI",
    description: "Usa nuestro botón de AI para generar keywords relacionadas y optimizar tu estrategia SEO."
  }
]

interface StartPopoverProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function StartPopover({ open, onOpenChange }: StartPopoverProps) {
  const [mainKeyword, setMainKeyword] = useState("")
  const [suggestedKeywords, setSuggestedKeywords] = useState<string[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)

  const handleGenerateKeywords = async () => {
    if (!mainKeyword.trim()) return
    
    setIsGenerating(true)
    try {
      const mockKeywords = [
        "marketing digital estrategias",
        "marketing online empresas",
        "estrategias seo 2024",
        "posicionamiento web",
        "seo para principiantes"
      ]
      setSuggestedKeywords(mockKeywords)
      onOpenChange(false)
    } catch (error) {
      console.error("Error generando keywords:", error)
    } finally {
      setIsGenerating(false)
    }
  }

  const handleNext = () => {
    if (currentStep < startSteps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrev = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-lg px-4">
        <Card className="p-6 text-center">
          <h1 className="mb-6 text-3xl font-bold">
            Let&apos;s rank your SEO effortless
          </h1>
          
          <div className="mx-auto max-w-md space-y-4">
            <div className="flex gap-2">
              <Input
                value={mainKeyword}
                onChange={(e) => setMainKeyword(e.target.value)}
                placeholder="Ingresa tu keyword principal..."
                className="text-center"
              />
            </div>
            
            <Button 
              onClick={handleGenerateKeywords}
              disabled={!mainKeyword.trim() || isGenerating}
              className="gap-2"
            >
              <Wand2 className="h-4 w-4" />
              {isGenerating ? "Generando..." : "Improve with AI"}
            </Button>
          </div>

          <div className="mt-6 space-y-3">
            <div className="space-y-1">
              <p className="text-[13px] font-medium">{startSteps[currentStep].title}</p>
              <p className="text-xs text-muted-foreground">
                {startSteps[currentStep].description}
              </p>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">
                {currentStep + 1}/{startSteps.length}
              </span>
              <div className="flex gap-0.5">
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6"
                  onClick={handlePrev}
                  disabled={currentStep === 0}
                >
                  <ArrowLeft className="h-4 w-4" />
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  className="h-6 w-6"
                  onClick={handleNext}
                  disabled={currentStep === startSteps.length - 1}
                >
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
} 