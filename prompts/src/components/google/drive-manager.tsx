"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Button } from "../ui/button"

interface DriveFile {
  id: string
  name: string
  type: string
  size: number
  lastModified: string
}

export function DriveManager() {
  const [files, setFiles] = useState<DriveFile[]>([])
  const [currentPath, setCurrentPath] = useState<string[]>([])

  const handleFetchFiles = async () => {
    // TODO: Implementar integración real con Google Drive API
    const mockFiles: DriveFile[] = [
      {
        id: "1",
        name: "Documento.doc",
        type: "document",
        size: 1024,
        lastModified: new Date().toISOString()
      }
    ]
    setFiles(mockFiles)
  }

  const handleNavigate = (path: string) => {
    setCurrentPath(prev => [...prev, path])
    handleFetchFiles()
  }

  const handleBack = () => {
    setCurrentPath(prev => prev.slice(0, -1))
    handleFetchFiles()
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Google Drive</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          <Button 
            onClick={handleBack}
            disabled={currentPath.length === 0}
          >
            Atrás
          </Button>
          <div>
            Ruta: /{currentPath.join("/")}
          </div>
          <div>
            {files.map(file => (
              <div key={file.id}>
                <span>{file.name}</span>
                <span>{file.type}</span>
                <span>{Math.round(file.size / 1024)} KB</span>
                <span>{new Date(file.lastModified).toLocaleDateString()}</span>
                {file.type === "folder" && (
                  <Button onClick={() => handleNavigate(file.name)}>
                    Abrir
                  </Button>
                )}
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
} 