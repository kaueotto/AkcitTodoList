"""Schemas (modelos de validação) Pydantic para a API."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    """Schema base com campos comuns."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Título da tarefa"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Descrição detalhada da tarefa"
    )


class TaskCreate(TaskBase):
    """Schema para criação de tarefa."""

    class Config:
        """Configuração do schema."""

        schema_extra = {
            "example": {
                "title": "Aprender Python",
                "description": "Estudar conceitos avançados"
            }
        }


class TaskUpdate(BaseModel):
    """Schema para atualização de tarefa."""

    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Novo título da tarefa"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Nova descrição da tarefa"
    )
    status: Optional[str] = Field(
        None,
        description="Novo status: 'pending' ou 'completed'"
    )

    class Config:
        """Configuração do schema."""

        schema_extra = {
            "example": {
                "title": "Novo Título",
                "status": "completed"
            }
        }


class TaskResponse(TaskBase):
    """Schema para resposta de tarefa (read)."""

    id: int = Field(..., description="ID único da tarefa")
    status: str = Field(
        default="pending",
        description="Status da tarefa: 'pending' ou 'completed'"
    )
    created_at: datetime = Field(
        ...,
        description="Data/hora de criação"
    )
    updated_at: datetime = Field(
        ...,
        description="Data/hora da última atualização"
    )

    class Config:
        """Configuração do schema."""

        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Aprender Python",
                "description": "Estudar conceitos avançados",
                "status": "pending",
                "created_at": "2026-04-21T13:56:24.101005",
                "updated_at": "2026-04-21T13:56:24.101005"
            }
        }


class TaskStats(BaseModel):
    """Schema para estatísticas de tarefas."""

    total: int = Field(
        ...,
        description="Total de tarefas"
    )
    pending: int = Field(
        ...,
        description="Quantidade de tarefas pendentes"
    )
    completed: int = Field(
        ...,
        description="Quantidade de tarefas concluídas"
    )

    class Config:
        """Configuração do schema."""

        schema_extra = {
            "example": {
                "total": 5,
                "pending": 3,
                "completed": 2
            }
        }


class ErrorResponse(BaseModel):
    """Schema para resposta de erro."""

    error: str = Field(
        ...,
        description="Mensagem de erro"
    )

    class Config:
        """Configuração do schema."""

        schema_extra = {
            "example": {
                "error": "Tarefa não encontrada"
            }
        }
