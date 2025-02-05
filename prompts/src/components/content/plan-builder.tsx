"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"
import { Input } from "../ui/input"

interface ContentPlan {
  title: string
  keywords: string[]
  outline: string[]
}

export function ContentPlanBuilder() {
  const [plan, setPlan] = useState<ContentPlan>({
    title: "",
    keywords: [],
    outline: []
  })

  const handleAddKeyword = (keyword: string) => {
    setPlan(prev => ({
      ...prev,
      keywords: [...prev.keywords, keyword]
    }))
  }

  const handleAddOutlineItem = (item: string) => {
    setPlan(prev => ({
      ...prev,
      outline: [...prev.outline, item]
    }))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Plan de Contenido</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            placeholder="Título del contenido"
            value={plan.title}
            onChange={(e) => setPlan(prev => ({ ...prev, title: e.target.value }))}
          />
          <div>
            <h4>Keywords</h4>
            {plan.keywords.map((kw, i) => (
              <div key={i}>{kw}</div>
            ))}
          </div>
          <div>
            <h4>Esquema</h4>
            {plan.outline.map((item, i) => (
              <div key={i}>{item}</div>
            ))}
          </div>
          <Button onClick={() => console.log(plan)}>Guardar Plan</Button>
        </div>
      </CardContent>
    </Card>
  )
} 