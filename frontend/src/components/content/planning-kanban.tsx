"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface KanbanItem {
  id: string
  title: string
  status: "todo" | "in-progress" | "review" | "done"
}

export function PlanningKanban() {
  const [items, setItems] = useState<KanbanItem[]>([])

  const columns = {
    todo: items.filter(item => item.status === "todo"),
    "in-progress": items.filter(item => item.status === "in-progress"),
    review: items.filter(item => item.status === "review"),
    done: items.filter(item => item.status === "done")
  }

  const moveItem = (itemId: string, newStatus: KanbanItem["status"]) => {
    setItems(prev => prev.map(item =>
      item.id === itemId ? { ...item, status: newStatus } : item
    ))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Tablero de Planificación</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-4 gap-4">
          {Object.entries(columns).map(([status, items]) => (
            <div key={status}>
              <h3 className="capitalize">{status}</h3>
              {items.map(item => (
                <div key={item.id}>
                  {item.title}
                </div>
              ))}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 