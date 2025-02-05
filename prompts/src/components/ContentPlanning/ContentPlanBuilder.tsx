'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { toast } from '@/components/ui/use-toast'
import { Label } from '@/components/ui/label'
import { Copy } from 'lucide-react'
import { Textarea } from '@/components/ui/textarea'

interface ContentPlanFormData {
  keywords: string
}

interface ContentPlanBuilderProps {
  onPlanGenerated: (plan: any[]) => void
}

export function ContentPlanBuilder({ onPlanGenerated }: ContentPlanBuilderProps) {
  const [isLoading, setIsLoading] = useState(false)
  const [rawContent, setRawContent] = useState<string>('')
  const [formData, setFormData] = useState<ContentPlanFormData>({
    keywords: ''
  })

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(rawContent)
      toast({
        title: "Copiado al portapapeles",
        description: "El plan ha sido copiado exitosamente"
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo copiar al portapapeles",
        variant: "destructive"
      })
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8001/api/content-plan/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          keywords: formData.keywords.split('\n').map(k => k.trim()).filter(k => k)
        })
      })

      if (!response.ok) throw new Error('Error generando plan')
      
      const data = await response.json()
      onPlanGenerated(data.plan || [])
      setRawContent(data.raw_content || '')
      
      toast({
        title: "Plan generado exitosamente",
        description: "Tu plan de contenido está listo para revisión"
      })

    } catch (error) {
      toast({
        title: "Error",
        description: "No se pudo generar el plan",
        variant: "destructive"
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <Card className="p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label>Lista de Keywords (una por línea)</Label>
            <Textarea
              required
              value={formData.keywords}
              onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({...formData, keywords: e.target.value})}
              placeholder="Ingresa tus keywords, una por línea"
              rows={10}
            />
          </div>

          <Button type="submit" disabled={isLoading}>
            {isLoading ? 'Generando...' : 'Generar Plan'}
          </Button>
        </form>
      </Card>

      {rawContent && (
        <Card className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Plan de Contenido</h3>
            <div className="space-x-2">
              <Button variant="outline" size="sm" onClick={handleCopy}>
                <Copy className="h-4 w-4 mr-2" />
                Copiar
              </Button>
              <Button variant="outline" size="sm" onClick={() => onPlanGenerated([])}>
                Exportar CSV
              </Button>
            </div>
          </div>
          <pre className="bg-muted p-4 rounded-lg overflow-auto whitespace-pre-wrap">
            {rawContent}
          </pre>
        </Card>
      )}
    </div>
  )
} 