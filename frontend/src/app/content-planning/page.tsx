"use client"

import { ContentPlanBuilder } from "@/components/content/plan-builder"
import { ArticleScheduler } from "@/components/content/article-scheduler"
import { CSVExporter } from "@/components/content/csv-exporter"
import { PlanningKanban } from "@/components/content/planning-kanban"
import { useState } from "react"

export default function ContentPlanningPage() {
  const [plans, setPlans] = useState([])

  return (
    <div className="container space-y-8">
      <h1>Planificación de Contenido</h1>
      <div className="grid gap-8">
        <ContentPlanBuilder />
        <ArticleScheduler />
        <CSVExporter data={plans} />
        <PlanningKanban />
      </div>
    </div>
  )
} 