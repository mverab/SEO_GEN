"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface ExportConfig {
  title: string
  content: string
  format: "doc" | "pdf"
  folder?: string
}

export function ExportToDocs() {
  const [isExporting, setIsExporting] = useState(false)
  const [config, setConfig] = useState<ExportConfig>({
    title: "",
    content: "",
    format: "doc"
  })

  const handleExport = async () => {
    try {
      setIsExporting(true)
      // TODO: Implementar exportación real a Google Docs
      await new Promise(resolve => setTimeout(resolve, 1000))
      console.log("Exportando:", config)
    } catch (error) {
      console.error("Error al exportar:", error)
    } finally {
      setIsExporting(false)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Exportar a Google Docs</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          <input
            type="text"
            value={config.title}
            onChange={(e) => setConfig(prev => ({ ...prev, title: e.target.value }))}
            placeholder="Título del documento"
          />
          <select
            value={config.format}
            onChange={(e) => setConfig(prev => ({ 
              ...prev, 
              format: e.target.value as ExportConfig["format"] 
            }))}
          >
            <option value="doc">Documento</option>
            <option value="pdf">PDF</option>
          </select>
          <Button 
            onClick={handleExport}
            disabled={isExporting || !config.title}
          >
            {isExporting ? "Exportando..." : "Exportar"}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
} 