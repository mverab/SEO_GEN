"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card"
import type { SEOMetric } from "../../types/api"

interface SEOMetricsDisplayProps {
  metrics?: SEOMetric[]
  isFirstLoad?: boolean
}

export function SEOMetricsDisplay({ metrics, isFirstLoad = true }: SEOMetricsDisplayProps) {
  const defaultMetrics: SEOMetric[] = [
    {
      label: "Volumen de Búsqueda",
      value: "-",
      description: "Búsquedas mensuales promedio",
    },
    {
      label: "Dificultad",
      value: "-",
      description: "Nivel de competencia",
    },
    {
      label: "Intención",
      value: "-",
      description: "Tipo de intención de búsqueda",
    },
  ]

  const displayMetrics = metrics || defaultMetrics

  return (
    <Card className={isFirstLoad ? "opacity-70" : ""}>
      <CardHeader>
        <CardTitle>Métricas SEO</CardTitle>
        <CardDescription>
          Análisis detallado de la keyword
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-4">
        {displayMetrics.map((metric, i) => (
          <div key={i} className="flex flex-col space-y-1.5">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">{metric.label}</span>
              <span className="text-2xl font-bold">{metric.value}</span>
            </div>
            <p className="text-xs text-muted-foreground">
              {metric.description}
            </p>
          </div>
        ))}
      </CardContent>
    </Card>
  )
} 