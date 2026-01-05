from django.test import TestCase
from docentes.models import Asignacion, Profesor, Aula, Horario, Dia
from planes.models import Plan


class AsignacionStrTestCase(TestCase):
    """Test cases for Asignacion.__str__() method"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a plan
        self.plan = Plan.objects.create(
            nombre="Matemática + Comunicación",
            nivel="primaria",
            activo=True
        )
        
        # Create professors
        self.prof1 = Profesor.objects.create(
            nombres="Alfredo",
            apellidos="Vásquez Sotero",
            activo=True
        )
        self.prof2 = Profesor.objects.create(
            nombres="Diana",
            apellidos="Castillo",
            activo=True
        )
        
        # Create aula
        self.aula = Aula.objects.create(
            nombre="Salón Grande",
            capacidad=30
        )
        
        # Create dias
        self.dia_mar = Dia.objects.create(codigo="mar")
        self.dia_jue = Dia.objects.create(codigo="jue")
        
        # Create horario
        self.horario = Horario.objects.create(
            hora_inicio="09:00:00",
            hora_fin="12:00:00"
        )
        self.horario.dias.add(self.dia_mar, self.dia_jue)
    
    def test_asignacion_str_without_grado(self):
        """Test __str__ when grado is not set"""
        asignacion = Asignacion.objects.create(
            plan=self.plan,
            aula=self.aula,
            horario=self.horario,
            cupo_maximo=30,
            precio=100.00
        )
        asignacion.profesores.add(self.prof1, self.prof2)
        
        result = str(asignacion)
        
        # Should contain professors, plan name, horario and aula
        self.assertIn("Vásquez Sotero, Alfredo", result)
        self.assertIn("Castillo, Diana", result)
        self.assertIn("Matemática + Comunicación", result)
        self.assertIn("Salón Grande", result)
        # Should NOT contain grado text when grado is None
        self.assertNotIn("Prim", result)
        self.assertNotIn("Sec", result)
    
    def test_asignacion_str_with_grado(self):
        """Test __str__ when grado is set"""
        asignacion = Asignacion.objects.create(
            plan=self.plan,
            aula=self.aula,
            horario=self.horario,
            grado="4° Prim",
            cupo_maximo=30,
            precio=100.00
        )
        asignacion.profesores.add(self.prof1, self.prof2)
        
        result = str(asignacion)
        
        # Should contain professors, plan name, grado, horario and aula
        self.assertIn("Vásquez Sotero, Alfredo", result)
        self.assertIn("Castillo, Diana", result)
        self.assertIn("Matemática + Comunicación", result)
        self.assertIn("4° Prim", result)
        self.assertIn("Salón Grande", result)
    
    def test_asignacion_str_format_with_grado(self):
        """Test exact format of __str__ with grado"""
        asignacion = Asignacion.objects.create(
            plan=self.plan,
            aula=self.aula,
            horario=self.horario,
            grado="4° Prim",
            cupo_maximo=30,
            precio=100.00
        )
        asignacion.profesores.add(self.prof1, self.prof2)
        
        result = str(asignacion)
        
        # Verify the grado appears after plan name with " - " separator
        self.assertIn("Matemática + Comunicación - 4° Prim", result)
