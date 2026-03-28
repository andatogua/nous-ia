class EstadoRecomendacion:
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    RECHAZADO = "RECHAZADO"
    
    @staticmethod
    def get_color(estado):
        colors = {
            EstadoRecomendacion.PENDIENTE: "#F59E0B",
            EstadoRecomendacion.APROBADO: "#10B981",
            EstadoRecomendacion.RECHAZADO: "#EF4444"
        }
        return colors.get(estado, "#6B7280")
    
    @staticmethod
    def get_label(estado):
        labels = {
            EstadoRecomendacion.PENDIENTE: "Pendiente",
            EstadoRecomendacion.APROBADO: "Aprobada",
            EstadoRecomendacion.RECHAZADO: "Rechazada"
        }
        return labels.get(estado, estado)
    
    @staticmethod
    def get_icon(estado):
        icons = {
            EstadoRecomendacion.PENDIENTE: "⏳",
            EstadoRecomendacion.APROBADO: "✅",
            EstadoRecomendacion.RECHAZADO: "❌"
        }
        return icons.get(estado, "❓")
