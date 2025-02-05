"use client"

import { Button } from "../ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface ExportData {
  title: string
  keywords: string[]
  outline: string[]
  scheduledDate?: string
}

export function CSVExporter({ data }: { data: ExportData[] }) {
  const handleExport = () => {
    const headers = ["Título", "Keywords", "Esquema", "Fecha Programada"]
    const rows = data.map(item => [
      item.title,
      item.keywords.join(", "),
      item.outline.join(", "),
      item.scheduledDate || ""
    ])

    const csvContent = [
      headers.join(","),
      ...rows.map(row => row.join(","))
    ].join("\n")

    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = "plan-contenido.csv"
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Exportar Plan</CardTitle>
      </CardHeader>
      <CardContent>
        <Button onClick={handleExport}>
          Exportar a CSV
        </Button>
      </CardContent>
    </Card>
  )
} 