"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface Article {
  id: string
  title: string
  status: "draft" | "scheduled" | "published"
  scheduledDate?: string
}

export function ArticleScheduler() {
  const [articles, setArticles] = useState<Article[]>([])

  const handleSchedule = (articleId: string, date: string) => {
    setArticles(prev => prev.map(article => 
      article.id === articleId 
        ? { ...article, status: "scheduled", scheduledDate: date }
        : article
    ))
  }

  const handleStatusChange = (articleId: string, status: Article["status"]) => {
    setArticles(prev => prev.map(article => 
      article.id === articleId 
        ? { ...article, status }
        : article
    ))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Calendario de Publicación</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          {articles.map(article => (
            <div key={article.id}>
              <span>{article.title}</span>
              <span>{article.status}</span>
              <span>{article.scheduledDate}</span>
              <Button onClick={() => handleStatusChange(article.id, "published")}>
                Publicar
              </Button>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 