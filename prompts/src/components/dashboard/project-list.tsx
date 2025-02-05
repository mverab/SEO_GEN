"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface Project {
  id: string
  name: string
  status: "active" | "completed" | "paused"
  progress: number
  articles: number
}

export function ProjectList() {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: "1",
      name: "Proyecto SEO Blog",
      status: "active",
      progress: 65,
      articles: 12
    },
    {
      id: "2",
      name: "Contenido Redes",
      status: "paused",
      progress: 30,
      articles: 5
    }
  ])

  const handleStatusChange = (id: string, status: Project["status"]) => {
    setProjects(prev => prev.map(project =>
      project.id === id ? { ...project, status } : project
    ))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Proyectos</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {projects.map(project => (
            <div key={project.id} className="flex items-center justify-between">
              <div>
                <div className="font-medium">{project.name}</div>
                <div className="text-sm text-muted-foreground">
                  {project.articles} artículos • {project.progress}% completado
                </div>
              </div>
              <Button
                variant={project.status === "active" ? "default" : "outline"}
                onClick={() => handleStatusChange(
                  project.id,
                  project.status === "active" ? "paused" : "active"
                )}
              >
                {project.status === "active" ? "Activo" : "Pausado"}
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 