'use client'

import { Button } from '@/components/ui/button'
import { Download } from 'lucide-react'

interface ExportData {
  title: string
  keyword: string
  secondary_keywords?: string
  plannedDate?: Date
  status: string
}

export function CSVExporter({ data }: { data: ExportData[] }) {
  const handleExport = () => {
    // Convertir datos a formato CSV
    const headers = ['title', 'keyword', 'secondary_keywords', 'plannedDate', 'status']
    const csvContent = [
      headers.join(','),
      ...data.map(row => 
        headers.map(header => 
          row[header as keyof ExportData] || ''
        ).join(',')
      )
    ].join('\n')

    // Crear y descargar archivo
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)
    
    link.setAttribute('href', url)
    link.setAttribute('download', `content_plan_${new Date().toISOString()}.csv`)
    link.style.visibility = 'hidden'
    
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <Button 
      onClick={handleExport}
      className="flex items-center gap-2"
    >
      <Download className="h-4 w-4" />
      Exportar a CSV
    </Button>
  )
} 