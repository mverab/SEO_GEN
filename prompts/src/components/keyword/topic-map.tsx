"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../ui/card"
import type { TopicNode } from "../../types/api"

interface TopicMapVisualizerProps {
  topics?: TopicNode[]
  isFirstLoad?: boolean
}

export function TopicMapVisualizer({ topics, isFirstLoad = true }: TopicMapVisualizerProps) {
  const defaultTopics: TopicNode[] = [
    {
      id: "1",
      label: "Tema Principal",
      children: [
        { id: "1.1", label: "Subtema 1" },
        { id: "1.2", label: "Subtema 2" },
        { id: "1.3", label: "Subtema 3" },
      ],
    },
  ]

  const displayTopics = topics || defaultTopics

  const renderTopic = (topic: TopicNode) => (
    <div key={topic.id} className="space-y-2">
      <div className="rounded-md bg-secondary p-2">
        <span className="font-medium">{topic.label}</span>
      </div>
      {topic.children && (
        <div className="ml-4 space-y-2">
          {topic.children.map((child) => (
            <div
              key={child.id}
              className="rounded-md border bg-background p-2 text-sm"
            >
              {child.label}
            </div>
          ))}
        </div>
      )}
    </div>
  )

  return (
    <Card className={isFirstLoad ? "opacity-70" : ""}>
      <CardHeader>
        <CardTitle>Mapa de Temas</CardTitle>
        <CardDescription>
          Estructura jerárquica de temas relacionados
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {displayTopics.map(renderTopic)}
      </CardContent>
    </Card>
  )
} 