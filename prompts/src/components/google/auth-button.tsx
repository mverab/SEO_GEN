"use client"

import { useState } from "react"
import { Button } from "../ui/button"

interface GoogleUser {
  id: string
  email: string
  name: string
  accessToken: string
}

export function GoogleAuthButton() {
  const [user, setUser] = useState<GoogleUser | null>(null)

  const handleAuth = async () => {
    try {
      // TODO: Implementar autenticación real con Google
      const mockUser = {
        id: "123",
        email: "usuario@gmail.com",
        name: "Usuario Test",
        accessToken: "mock-token"
      }
      setUser(mockUser)
    } catch (error) {
      console.error("Error de autenticación:", error)
    }
  }

  const handleLogout = () => {
    setUser(null)
  }

  return (
    <div>
      {user ? (
        <div>
          <span>{user.name}</span>
          <Button onClick={handleLogout}>Cerrar Sesión</Button>
        </div>
      ) : (
        <Button onClick={handleAuth}>
          Conectar con Google
        </Button>
      )}
    </div>
  )
} 