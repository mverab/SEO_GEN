"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface Goal {
  id: string
  name: string
  target: number
  current: number
  unit: string
}

export function ProgressTracker() {
  const goals: Goal[] = [
    {
      id: "1",
      name: "Artículos Mensuales",
      target: 20,
      current: 12,
      unit: "artículos"
    },
    {
      id: "2",
      name: "Keywords Investigadas",
      target: 100,
      current: 65,
      unit: "keywords"
    }
  ]

  const calculateProgress = (current: number, target: number) => {
    return Math.round((current / target) * 100)
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Objetivos</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {goals.map(goal => (
            <div key={goal.id}>
              <div className="flex justify-between mb-1">
                <span className="text-sm font-medium">{goal.name}</span>
                <span className="text-sm text-muted-foreground">
                  {goal.current} / {goal.target} {goal.unit}
                </span>
              </div>
              <div className="h-2 bg-secondary rounded-full">
                <div
                  className="h-2 bg-primary rounded-full"
                  style={{ width: `${calculateProgress(goal.current, goal.target)}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 