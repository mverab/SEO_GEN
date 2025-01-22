"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface UploadedResource {
  id: string
  file: File
  progress: number
  status: "uploading" | "completed" | "error"
}

export function ResourceUploader() {
  const [uploads, setUploads] = useState<UploadedResource[]>([])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files) return

    const newUploads = Array.from(files).map(file => ({
      id: Math.random().toString(36).slice(2),
      file,
      progress: 0,
      status: "uploading" as const
    }))

    setUploads(prev => [...prev, ...newUploads])
  }

  const handleUpload = (id: string) => {
    // Simular progreso
    setUploads(prev => prev.map(upload =>
      upload.id === id
        ? { ...upload, progress: 100, status: "completed" }
        : upload
    ))
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Subir Recursos</CardTitle>
      </CardHeader>
      <CardContent>
        <input
          type="file"
          multiple
          onChange={handleFileSelect}
        />
        <div>
          {uploads.map(upload => (
            <div key={upload.id}>
              <span>{upload.file.name}</span>
              <span>{upload.progress}%</span>
              <span>{upload.status}</span>
              {upload.status === "uploading" && (
                <Button onClick={() => handleUpload(upload.id)}>
                  Subir
                </Button>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
} 