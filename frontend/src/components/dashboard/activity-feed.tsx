"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

interface Activity {
  id: string
  type: "article" | "keyword" | "export"
  action: string
  target: string
  timestamp: string
}

export function ActivityFeed() {
  const activities: Activity[] = [
    {
      id: "1",
      type: "article",
      action: "creó",
      target: "Guía SEO 2024",
      timestamp: new Date().toISOString()
    },
    {
      id: "2",
      type: "keyword",
      action: "investigó",
      target: "marketing digital",
      timestamp: new Date().toISOString()
    }
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Actividad Reciente</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map(activity => (
            <div key={activity.id} className="flex items-center gap-2">
              <div className="text-sm text-muted-foreground">
                {new Date(activity.timestamp).toLocaleTimeString()}
              </div>
              <div>
                <span className="font-medium">{activity.type}</span>
                {" "}{activity.action}{" "}
                <span className="font-medium">{activity.target}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 